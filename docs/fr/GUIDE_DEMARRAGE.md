# Reverse Engineering — Dragon Quest Monsters: Joker (Nintendo DS)

Guide pas à pas pour passer d'une ROM commerciale `.nds` à du **code source
reconstruit et lisible**. Écrit pour être suivi sans connaissance préalable
du reverse engineering.

> **[Doc] Documentation principale : [README-COMPLET.md](README-COMPLET.md)**
> Ce document-ci est le guide de démarrage. Le README complet couvre
> **tout** en 16 sections : chaque outil, chaque commande, chaque erreur
> commise et sa correction, les formats décodés (`.d16`, `.sdat`, `.strm`),
> le piège du mode Thumb, le tiroir GNOME, et l'aide-mémoire finale.
>
> **[Doc] Ressources : [EXTRACTION-RESSOURCES.md](EXTRACTION-RESSOURCES.md)**
> Images `.d16` → PNG, sons `.sdat`/`.strm` → WAV, et pourquoi le jeu ne
> peut pas tourner sur une machine ARM ordinaire.

---

## 0. Ce qu'on cherche et ce qu'on va réellement obtenir

**Objectif :** récupérer le code de la ROM.

**Ce que « récupérer le code » veut dire concrètement.** Il faut lever une
ambiguïté tout de suite, parce qu'elle détermine tout le reste :

| Ce qu'on ne peut pas avoir | Pourquoi |
|---|---|
| Les `.c` originaux de Square Enix | Ils n'ont jamais été dans la ROM. Le jeu a été compilé : le compilateur a jeté le source, les noms de variables, les commentaires. |
| Les vrais noms de fonctions | Idem. `FUN_02012345` est un nom *généré* par l'outil, pas le nom d'origine. |

| Ce qu'on peut avoir | Comment |
|---|---|
| Tout le code assembleur ARM, exact | `objdump`, Ghidra |
| Du C reconstruit proche de l'original | Décompilateur Ghidra |
| Tous les assets (modèles 3D, textures, sons, textes) | `ndstool` |
| Les adresses, la structure mémoire, les tables de données | Analyse de l'en-tête + Ghidra |

Donc « récupérer le code entièrement » = **on obtient 100 % du code**, sous
forme de pseudo-C décompilé + assembleur. C'est exploitable, recompilable
par morceaux, patchable. Ce n'est pas le source d'origine, et c'est
impossible — ce n'est pas une limite de nos outils, c'est une limite de
l'information : elle a été détruite à la compilation.

---

## 1. Comprendre la cible : la Nintendo DS

Avant de toucher à un octet, il faut savoir à quoi on a affaire. La DS n'est
pas une console simple : c'est une machine à **deux processeurs**.

```
┌─────────────────────────────────────────────────────┐
│                  Nintendo DS                        │
│                                                     │
│   ┌──────────────┐            ┌──────────────┐      │
│   │    ARM9      │            │    ARM7      │      │
│   │  ARM946E-S   │            │  ARM7TDMI    │      │
│   │   67 MHz     │            │   33 MHz     │      │
│   │              │            │              │      │
│   │  LE JEU :    │            │  LA BASSESSE │      │
│   │  moteur 3D   │            │  audio, WiFi │      │
│   │  gameplay    │            │  touches, RTC│      │
│   │  IA, menus   │            │  alimentation│      │
│   └──────┬───────┘            └──────┬───────┘      │
│          │                           │              │
│          └─────────┬─────────────────┘              │
│                    │                                │
│            ┌───────▼────────┐                       │
│            │  4 Mo de RAM   │  (partagée)           │
│            └────────────────┘                       │
└─────────────────────────────────────────────────────┘
```

Conséquences pratiques pour nous :

- **Deux binaires à analyser**, pas un. `arm9.bin` (le jeu) et `arm7.bin`
  (le support). On passe 90 % du temps sur l'ARM9.
- **Jeu d'instructions ARM** (32 bits) et **Thumb** (16 bits) coexistent.
  Une fonction peut basculer de l'un à l'autre — c'est la principale source
  d'erreurs de désassemblage.
- **Adresses de chargement fixes et connues.** C'est une chance énorme : sur
  PC, l'ASLR rend l'analyse pénible. Ici, l'ARM9 est *toujours* à
  `0x02000000`. Tous les pointeurs dans le code sont des adresses absolues
  valides → on peut suivre les appels de fonction directement.

### L'en-tête de la ROM : la carte d'identité

Les 512 premiers octets d'un `.nds` sont un en-tête standardisé qui dit tout.
C'est **toujours la première chose à lire**.

| Offset | Champ | Valeur ici | Sens |
|---|---|---|---|
| `0x00` | Titre | `DQM:JOKER` | Nom interne |
| `0x0C` | Game code | `AJRP` | `NTR-AJRP-EUR` = version européenne |
| `0x10` | Maker | `GD` | Square Enix |
| `0x14` | Capacité | `0x0A` | 1024 Mbit = 128 Mo |
| `0x20` | ARM9 ROM offset | `0x4000` | Où le code ARM9 commence dans le fichier |
| `0x24` | ARM9 entry | `0x02000800` | **Point d'entrée** du jeu |
| `0x28` | ARM9 RAM addr | `0x02000000` | Adresse de chargement |
| `0x2C` | ARM9 size | `0x78A18` | Taille du code |
| `0x30` | ARM7 ROM offset | `0x1E5E00` | |
| `0x34` | ARM7 entry | `0x02380000` | |
| `0x40` | FNT offset | `0x20C800` | Table des noms de fichiers |
| `0x48` | FAT offset | `0x218A00` | Table des positions de fichiers |
| `0x50` | ARM9 ovl table | `0x7CC00` | Table des overlays |

**FNT + FAT** forment le « système de fichiers » interne : c'est grâce à eux
qu'on peut extraire les 3845 fichiers avec leurs vrais noms.

### Les overlays : le code paginé

La DS n'a que 4 Mo de RAM. Un jeu de 128 Mo ne peut donc pas charger tout son
code d'un coup. Solution : le code est découpé en **overlays** — des blocs de
code chargés à la demande depuis la carte, comme des pages mémoire.

Ici, la table `y9.bin` en déclare 3, et ils sont révélateurs :

| Overlay | Taille | Adresse de chargement |
|---|---|---|
| 0 | 378 912 o | `0x02184B40` |
| 1 | 618 112 o | `0x02184B40` |
| 2 | 480 736 o | `0x02184B40` |

**Même adresse pour les trois** → ils s'excluent mutuellement. Ce sont les
gros blocs du jeu (probablement : combat, village, menus) qui s'échangent
dans le même espace mémoire.

---

## 2. Étape 1 — Reconnaissance

**Ne jamais attaquer un binaire sans l'avoir d'abord observé.**

```bash
cd ~/Documents/ReverseEngeneering

# Voir ce qu'il y a dans l'archive
7z l "2109 - Dragon Quest Monsters - Joker (E)(EXiMiUS).7z"

# Extraire
7z x "2109 - Dragon Quest Monsters - Joker (E)(EXiMiUS).7z"
```

**Technologie :** `7z` (LZMA). Sans intérêt pour le RE lui-même, mais notez
que la ROM fait **exactement 134 217 728 octets** = 128 Mo pile. Une ROM DS
est toujours une puissance de 2 : c'est un premier signe qu'elle est saine.

```bash
# Lire l'en-tête
ndstool -i "2109 - Dragon Quest Monsters - Joker (E)(EXiMiUS).nds"
```

**Technologie : `ndstool`.** L'outil de référence pour les ROM DS (devkitPro).
Il connaît le format NDS par cœur : il lit l'en-tête, la table FAT/FNT, les
overlays, les CRC. C'est lui qui fait le gros du travail d'extraction.

Résultat — les CRC sont `OK`, le footer ARM9 est trouvé, la bannière dit
`DRAGON QUEST MONSTERS / Joker / SQUARE ENIX`. ROM **valide et non altérée**.

> **Vérifier les CRC n'est pas optionnel.** Si la ROM est corrompue, tout le
> travail d'analyse qui suit sera bâti sur du sable.

---

## 3. Étape 2 — Découpage en composants

```bash
mkdir -p work/extracted && cd work/extracted

ndstool -x "../../2109 - Dragon Quest Monsters - Joker (E)(EXiMiUS).nds" \
    -9 arm9.bin -7 arm7.bin \
    -y9 y9.bin  -y7 y7.bin \
    -d data -y overlay \
    -t banner.bin -v
```

Ou, plus simplement, avec le script fourni :

```bash
tools/nds-inspect.sh "2109 - Dragon Quest Monsters - Joker (E)(EXiMiUS).nds"
```

Ce qu'on obtient :

| Élément | Taille | Rôle |
|---|---|---|
| `arm9.bin` | 494 116 o | **Le jeu** |
| `arm7.bin` | 158 116 o | Audio/WiFi/touches |
| `overlay/` | 3 fichiers, 1,5 Mo | Code paginé |
| `data/` | 3845 fichiers, 117 Mo | Assets + données |
| `y9.bin` | 96 o | Table des overlays |
| `banner.bin` | 2112 o | Bannière du menu DS |

### Ce que révèle l'inventaire de `data/`

Cette liste est une **mine d'information sur l'architecture du jeu**. Les
extensions ne sont pas choisies au hasard, ce sont les bibliothèques de
Nintendo :

| Extension | Nombre | Technologie |
|---|---|---|
| `.nsbca` | 1261 | **Nitendo DS Animation** — animations squelettiques |
| `.nsbmd` | 411 | **Nitro System Binary Model** — modèles 3D |
| `.nsbma` | 25 | Matériaux |
| `.nsbta` | — | Textures d'animation |
| `.sdat` / `.sadl` | 1 | **Sound Data** — musiques et sons |
| `.d16` | 40 | Images 16 bits |
| `.SCR/.PAL/.CHR` | 60/60/60 | Tiles de fonds 2D (format GBA-like) |
| `.map` / `.evt` | 90/80 | Cartes et scripts d'événements |
| `mes_*.bin[DFSIE]` | ~250 | **Textes traduits** |

Deux observations décisives :

1. **Le suffixes `D/F/I/S/E`** sur les fichiers de messages (`mes_bank.binD`,
   `...binF`…) signifient **Deutsch, Français, Italiano, Spanish, English**.
   C'est ce qui permet à une seule ROM européenne de contenir 5 langues.
   → Une traduction fan-made modifie ces fichiers, pas le code.

2. **Le moteur est le Nitro SDK de Nintendo**, pas un moteur maison.
   C'est une excellente nouvelle : le SDK est documenté publiquement
   ([GBATEK](https://problemkaputt.de/gbatek.htm), [ndecomp](https://github.com/DSMistery/ndecomp)),
   donc on peut **reconnaître** les fonctions du SDK dans le code et les
   écarter pour se concentrer sur la logique propre à Square Enix.

Les chaînes trouvées dans l'ARM9 le confirment :

```
[SDK+NINTENDO:BACKUP]
[SDK+NINTENDO:WiFi2.0.30000.0703091639]
[SDK+UBIQUITOUS:SSL]
[SDK+NINTENDO:DWC2.1.30000.070519.0938_DWC_2_1]
```

`DWC` = **Nintendo Wi-Fi Connection**. Le jeu utilise les fonctions réseau
officielles de Nintendo — l'équivalent de nos bibliothèques système.

---

## 4. Étape 3 — Vérifier que le code est exploitable

**Piège classique :** beaucoup de ROMs DS ont leur ARM9 **compressé**
(LZ77, RLE, ou BLZ/Huffman) et commencent par une signature comme `0xFF 'BLZ'`.
Ghidra sur un flux compressé ne produit que du bruit.

Vérification faite ici : `arm9.bin` commence par `FF DE FF E7`… qui
*ressemble* à une signature, mais décodé en ARM c'est `0xE7FFDEFF` =
`mvn r15, #0xff0`. C'est un motif de remplissage standard, pas de la
compression. **L'ARM9 est en clair.**

On le confirme en désassemblant au point d'entrée (`0x02000800` → offset
`0x800` dans le fichier) :

```bash
arm-none-eabi-objdump -D -b binary -m armv5te -EL \
    --start-address=0x800 --stop-address=0x840 arm9.bin
```

```asm
mov  ip, #0x4000000    ; adresse de base des registres I/O de la DS
str  ip, [ip, #520]    ; écrit dans REG_IME (interrupt master enable)
ldrh r0, [ip, #6]      ; lit REG_IE / IF
cmp  r0, #0
bne  ...
bl   0xa78             ; appel de fonction
mov  r0, #19           ; mode CPU "IRQ"
msr  CPSR_c, r0        ; bascule en mode IRQ
```

C'est du **vrai code de démarrage** cohérent : on initialise les
interruptions, on change de mode processeur, on met en place les piles. La
preuve que le binaire est analysable.

**Technologie : `objdump` de binutils ARM.** Un désassembleur « bête » : il
lit les octets et les traduit en instructions, sans rien comprendre. Utile
pour vérifier rapidement, insuffisant pour analyser (il ne trouve pas les
fonctions, ne suit pas les appels).

---

## 5. Étape 4 — La décompilation : le cœur du travail

C'est ici qu'on passe de « suite d'octets » à « code compréhensible ».

### Pourquoi Ghidra

| Outil | Force | Faiblesse |
|---|---|---|
| `objdump` | Simple, rapide, exact | Aucune analyse. 500 000 lignes illisibles. |
| `radare2` | Puissant, scriptable, léger | Courbe d'apprentissage rude |
| **Ghidra** | **Décompilateur vers C**, analyse automatique, gratuit | Gourmand, interface lourde |

**Le décompilateur est la vraie révolution.** Un désassembleur montre :

```asm
ldr r0, [r4, #4]
cmp r0, #0
beq 0x2010abc
add r0, r0, #1
str r0, [r4, #4]
```

Un décompilateur montre :

```c
if (*(int *)(param_1 + 4) != 0) {
    *(int *)(param_1 + 4) += 1;
}
```

C'est la même chose, mais on lit la seconde version directement. Ghidra y
arrive en construisant un **graphe de flux de contrôle** (CFG), puis en
remontant à une représentation intermédiaire (P-code), puis en la
« remontant » vers du C (technique dite *decompilation*).

### Les adresses de chargement : le point critique

**C'est l'erreur n°1 des débutants.** Il faut dire à Ghidra *où* ce binaire
sera chargé en mémoire, sinon tous les pointeurs sont faux.

| Module | Adresse | Langage Ghidra |
|---|---|---|
| `arm9.bin` | `0x02000000` | `ARM:LE:32:v5t` |
| `arm7.bin` | `0x02380000` | `ARM:LE:32:v4t` |
| `overlay_*.bin` | `0x02184B40` | `ARM:LE:32:v5t` |

- **`LE`** : little-endian (la DS l'est).
- **`v5`** : ARMv5TE (ARM946E-S de l'ARM9) — supporte les instructions DSP.
- **`v4`** : ARMv4T (ARM7TDMI) — **pas** de v5 ! Mettre v5 produirait des
  instructions inexistantes sur cette puce.
- **`t`** : **critique** — voir ci-dessous.

Sans `-loader-baseAddr 0x02000000`, Ghidra croit que le code est à l'adresse
0. Un appel à `bl 0x2010abc` pointerait alors dans le vide, et **aucune
fonction ne serait reliée à une autre**. Résultat : 1952 fonctions isolées
au lieu d'un programme structuré.

### Le piège du Thumb — la leçon la plus importante

Chaque processeur de la DS sait exécuter **deux jeux d'instructions** :

| | ARM | Thumb |
|---|---|---|
| Taille | 32 bits | **16 bits** |
| Avantage | Puissant, registres illimités | Code ~30 % plus compact |

Le processeur bascule de l'un à l'autre **à l'exécution**. Ce qui décide,
c'est le **bit 0 de l'adresse cible d'un saut** :

```
bit 0 = 0   →   la cible est du code ARM
bit 0 = 1   →   la cible est du code Thumb
```

On l'a observé concrètement dans l'ARM7 :

```asm
0238061c:  ldr  ip, [pc]       ; charge l'adresse qui suit
02380620:  bx   ip             ; saute en changeant de jeu d'instructions
02380624:  .word 0x038035a1    ; adresse IMPAIRE → cible en Thumb !
```

`0x038035a1` a son bit 0 à 1 → la destination est du **Thumb**, pas de l'ARM.

**Le problème :** dans Ghidra, les langages *sans* `t` (`ARM:LE:32:v5`) ne
désassemblent **que** l'ARM. Toute zone Thumb y apparaît comme des
instructions invalides, et Ghidra écrit :

```c
/* WARNING: Control flow encountered bad instruction data */
void FUN_0238061c(void) {
    /* WARNING: Bad instruction - Truncating control flow here */
    halt_baddata();
}
```

Ce n'est **pas** une erreur : c'est du code réel que l'outil n'a pas su lire.
Et c'est un piège vicieux, parce qu'on obtient un fichier parfaitement
plausible, juste **silencieusement incomplet**.

**La correction** — demander explicitement la variante `t` :

```bash
-processor "ARM:LE:32:v4t"     # ARMv4T + Thumb
```

**Mesure sur cette ROM :**

| Module | Langage | Fonctions | `halt_baddata` |
|---|---|---|---|
| ARM7 | `v4` | 358 | **558** |
| ARM7 | `v4t` | **399** | **0** |
| ARM9 | `v5` | 1952 | 10 |
| ARM9 | `v5t` | **1979** | **0** |
| overlay 2 | `v5` | 2275 | — |
| overlay 2 | `v5t` | **2439** | **0** |

**41 fonctions de l'ARM7 et 27 de l'ARM9 étaient invisibles**, soit ~68
fonctions perdues, plus 568 zones de code illisibles. Un seul caractère dans
un nom de langage.

> **Leçon générale :** en reverse engineering, l'échec silencieux est bien
> plus dangereux que l'erreur franche. Toujours compter les avertissements
> `bad instruction` dans le résultat — un décompte non nul signifie qu'il
> manque du code. `tools/nds-decompile.sh` utilise `v4t`/`v5t` par défaut.

### La commande

```bash
/opt/ghidra/support/analyzeHeadless <projet> <nom> \
    -import arm9.bin \
    -processor "ARM:LE:32:v5" \
    -loader BinaryLoader \
    -loader-baseAddr 0x02000000 \
    -scriptPath tools/ghidra_scripts \
    -postScript ExportDecompiled.java arm9
```

Ou en une commande, tout le jeu :

```bash
tools/nds-decompile.sh "2109 - Dragon Quest Monsters - Joker (E)(EXiMiUS).nds"
```

**`analyzeHeadless`** est Ghidra sans interface graphique. Indispensable
pour traiter 500 000 lignes de code : cliquer sur 1952 fonctions à la main
serait absurde.

### Le script d'export

`tools/ghidra_scripts/ExportDecompiled.java` parcourt toutes les fonctions
que Ghidra a identifiées et écrit le C décompilé. Le cœur :

```java
DecompInterface dec = new DecompInterface();
dec.openProgram(currentProgram);

FunctionIterator funcs =
    currentProgram.getFunctionManager().getFunctions(true);

while (funcs.hasNext()) {
    Function f = funcs.next();
    DecompileResults res = dec.decompileFunction(f, 60, monitor);
    if (res.decompileCompleted()) {
        w.println(res.getDecompiledFunction().getC());
    }
}
```

---

## 6. Résultats obtenus

| Module | Rôle | Fonctions | Échecs | Fichier |
|---|---|---|---|---|
| ARM9 | Le jeu | 1979 | 0 | `work/decompiled/arm9.c` |
| ARM7 | Audio/WiFi | 399 | 0 | `work/decompiled/arm7.c` |
| Overlay 0 | Code paginé | 1204 | 0 | `work/decompiled/overlay_0000.c` |
| Overlay 1 | Code paginé | 1119 | 0 | `work/decompiled/overlay_0001.c` |
| Overlay 2 | Code paginé | 2439 | 0 | `work/decompiled/overlay_0002.c` |
| **Total** | | **7140** | **0** | **279 930 lignes de C** |

**Zéro échec, zéro `halt_baddata`.** L'intégralité du code exécutable de la
ROM est décompilée.

### Exemple : la première fonction, déjà identifiable

```c
undefined4 FUN_02000950(int param_1)
{
  if (param_1 != 0) {
    puVar5 = (undefined1 *)(param_1 + *(int *)(param_1 + -4));
    puVar7 = (ushort *)(param_1 - (*(uint *)(param_1 + -8) >> 0x18));
    uVar4  = param_1 - (*(uint *)(param_1 + -8) & 0xffffff);
    ...
    while ((int)uVar4 < (int)puVar7) {
      puVar7 = (ushort *)((int)puVar7 + -1);
      bVar9 = *(byte *)puVar7;
      iVar10 = 8;
      while (0 < iVar10) {
        if ((bVar9 & 0x80) == 0) { ... }
```

**On peut déjà dire ce que c'est.** Le motif `param_1 - (*(uint*)(param_1-8) & 0xffffff)`
et `>> 0x18` est la signature exacte des en-têtes de compression **BIOS de la
GBA/DS** :

- `+0` : `0x24` (`0x20` = 8 bits, `0x24` = 16 bits, `0x28` = 32 bits)
- `+1..3` : taille décompressée
- `-8` : longueur compressée
- `-4` : offset du symbf

C'est `SWI_Unpack` / `LZ77UnComp`, la fonction de décompression fournie par
le BIOS de la console. **La toute première fonction du jeu est un
décompresseur BIOS** — typique : le SDK en place un au démarrage.

C'est exactement ce à quoi ressemble le travail de RE : *lire du code
machine et y reconnaître des motifs connus*.

---

## 7. Ce qu'il reste à faire (et comment)

Le code est récupéré, mais il est **anonyme**. Le transformer en quelque
chose d'exploitable est le travail d'analyse :

1. **Nommer les fonctions du SDK.** Les adresses `0x02000000`–`0x02080000`
   contiennent le Nitro SDK. Le reconnaître permet de renommer des centaines
   de fonctions d'un coup.
2. **Suivre les appels depuis le point d'entrée** (`0x02000800`) pour
   reconstruire la boucle principale du jeu.
3. **Exploiter les chaînes de caractères.** Elles servent de points d'ancrage :
   une chaîne `"SAVE"` à côté d'une fonction indique une fonction de sauvegarde.
4. **Croiser avec les tables de `data/`.** `ItemTbl.bin`, `SkillTbl.bin`,
   `ExperienceTbl.bin` sont des tables de données comment le code les lit — 
   retrouver la fonction qui les ouvre donne accès à la structure du jeu.

### Où continuer

| Piste | Outil |
|---|---|
| Explorer visuellement l'ARM9 | Ghidra (`ghidraRun`) |
| Traiter les 3845 fichiers `data/` | [Tinke](https://github.com/pleonex/tinke), [ndspy](https://github.com/RubenTheCoder/ndspy) |
| Exécuter et tracer le jeu | `desmume-cli` |
| Modèles 3D / animations | [apicula](https://github.com/pleonex/apicula) |
| Documentation matériel | [GBATEK](https://problemkaputt.de/gbatek.htm) |

---

## 8. Cadre légal — à lire

Ce travail relève de la **préservation, de l'étude et de l'interopérabilité**,
trois activités explicitement protégées par le droit européen
(directive 2009/24/CE, art. 5 et 6) et français (CPI art. L.122-6-1).

Ce qui est légal :
- Analyser une ROM qu'on possède, pour comprendre comment elle marche.
- Étudier les formats, produire de la documentation.
- Modifier sa propre copie à des fins personnelles.

Ce qui ne l'est pas :
- **Distribuer la ROM** ou le code décompilé (c'est une œuvre protégée).
- **Publier les assets** (musiques, modèles, textes) de Square Enix.
- Vendre quoi que ce soit issu de ce travail.

Règle simple : **on peut tout analyser, on ne peut rien redistribuer.**
Ce dossier est un espace d'étude personnel — gardez-le ainsi.

---

## 8 bis. Extraire les ressources (images, sons)

Voir le guide dédié : **[EXTRACTION-RESSOURCES.md](EXTRACTION-RESSOURCES.md)**

En résumé, la ROM ne contient ni `.png` ni `.mp3` — la console ne sait pas
les lire. Les ressources sont dans les formats natifs du matériel, et il
faut rétro-ingénierer chacun :

| Ressource | Format DS | Outil | Résultat |
|---|---|---|---|
| Images | `.d16` (BGR555) | `tools/d16topng.py` | 40 PNG 256×192 |
| Audio jouable | `.strm` dans `.sdat` | `tools/strmtowav.py` | 199 WAV, 6,5 min |
| Partitions | `.sseq` | `vgmstream` | à synthétiser |
| Modèles 3D | `.nsbmd` | `apicula` | maillages |

```bash
python3 tools/d16topng.py --all work/extracted/data out/png
python3 tools/sdatextract.py work/extracted/data/sound_data.sdat out/sound
python3 tools/strmtowav.py --all out/sound/STRM out/wav
```

---

## 9. Aide-mémoire

```bash
# Voir l'en-tête d'une ROM
ndstool -i jeu.nds

# Tout extraire
tools/nds-inspect.sh jeu.nds

# Tout décompiler vers du C
tools/nds-decompile.sh jeu.nds

# Désassembler un module à la main
arm-none-eabi-objdump -D -b binary -m armv5te -EL arm9.bin > arm9.asm

# Ghidra graphique
ghidraRun

# Lancer le jeu
desmume-cli jeu.nds

# radare2 sur l'ARM9
r2 -a arm -b 32 -m 0x02000000 arm9.bin
```

### Correspondance des offsets ARM9

```
adresse RAM  →  offset fichier
0x02000000   →  0x000000
0x02000800   →  0x000800   (point d'entrée)
0x0207            (fin du code)
```
