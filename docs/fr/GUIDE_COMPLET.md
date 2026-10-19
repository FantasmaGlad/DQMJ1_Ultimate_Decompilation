## Reverse Engineering — Dragon Quest Monsters: Joker (Nintendo DS)

> **Documentation complète et pédagogique de A à Z.**
> Ce document raconte *tout* ce qui a été fait, dans l'ordre, avec le
> raisonnement derrière chaque décision, les erreurs commises et comment
> elles ont été corrigées. Objectif : que vous puissiez refaire la même
> chose seul sur n'importe quelle ROM, et comprendre chaque outil.

---

## Table des matières

| § | Sujet |
|---|---|
| [0](#0-ce-quon-cherche-et-ce-quon-obtient-vraiment) | Ce qu'on cherche et ce qu'on obtient vraiment |
| [1](#1-comprendre-la-machine-avant-de-la-toucher) | Comprendre la machine avant de la toucher |
| [2](#2-lenvironnement-de-travail) | L'environnement de travail |
| [3](#3-étape-1--reconnaissance) | Étape 1 — Reconnaissance |
| [4](#4-étape-2--découpage-en-composants) | Étape 2 — Découpage en composants |
| [5](#5-étape-3--comprendre-le-système-de-fichiers) | Étape 3 — Le système de fichiers |
| [6](#6-étape-4--vérifier-que-le-code-est-exploitable) | Étape 4 — Vérifier que le code est exploitable |
| [7](#7-étape-5--la-décompilation) | Étape 5 — La décompilation |
| [8](#8-le-piège-du-thumb--la-leçon-centrale) | **Le piège du Thumb — la leçon centrale** |
| [9](#9-résultats-obtenus) | Résultats obtenus |
| [10](#10-extraire-les-ressources-images-sons) | Extraire les ressources (images, sons) |
| [11](#11-peut-on-exécuter-le-jeu-sur-une-machine-arm-) | Peut-on exécuter le jeu sur ARM ? |
| [12](#12-le-tiroir-gnome--reverse-engineering-) | Le tiroir GNOME |
| [13](#13-tous-les-outils-du-dossier) | Tous les outils du dossier |
| [14](#14-les-erreurs-commises-et-ce-quelles-enseignent) | **Les erreurs commises et ce qu'elles enseignent** |
| [15](#15-la-bibliothèque-modelblender) | **La bibliothèque ModelBlender (411 modèles prêts à l'emploi)** |
| [16](#16-cadre-légal) | Cadre légal |
| [17](#17-aide-mémoire) | Aide-mémoire |

---

## 0. Ce qu'on cherche, et ce qu'on obtient vraiment

**Objectif initial :** récupérer le code entièrement d'une ROM de DS.

Il faut lever une ambiguïté **tout de suite**, car elle détermine tout le
reste du travail et évite une déception :

| Ce qu'on ne peut PAS avoir | Pourquoi c'est impossible |
|---|---|
| Les fichiers `.c` originaux de Square Enix | Ils n'ont **jamais été dans la ROM**. Le compilateur les a détruits à la compilation. |
| Les vrais noms de fonctions | Idem. `FUN_02012345` est un nom *généré par l'outil*, pas un nom d'origine. |
| Les commentaires, la structure des dossiers source | Jamais stockés dans le binaire. |

| Ce qu'on obtient réellement | Comment |
|---|---|
| **100 % du code assembleur ARM**, exact | `objdump`, Ghidra |
| Du **C reconstruit**, proche de l'original | Décompilateur Ghidra |
| Tous les assets (images, sons, modèles 3D, textes) | `ndstool` + outils maison |
| Les adresses mémoire et la structure du programme | Lecture de l'en-tête + analyse |

> **Le point clé à comprendre :** ce n'est pas une limite de nos outils,
> c'est une limite de l'information. Elle a été détruite à la compilation,
> définitivement. « Récupérer le code entièrement » signifie donc :
> **on obtient 100 % du code sous forme de pseudo-C décompilé +
> assembleur.** C'est exploitable, recompilable par morceaux, patchable.
> Ce n'est pas le source d'origine, et ça ne le sera jamais.

**Résultat final de cette session : 7 140 fonctions décompilées,
279 930 lignes de C, 0 échec.**

---

## 1. Comprendre la machine avant de la toucher

Avant de toucher un octet, il faut savoir à quoi on a affaire. C'est
l'étape que les débutants sautent, et c'est celle qui fait perdre le plus
de temps ensuite.

### 1.1 La Nintendo DS est une machine à deux processeurs

```
┌──────────────────────────────────────────────────────────┐
│                    Nintendo DS                           │
│                                                          │
│   ┌────────────────┐          ┌────────────────┐         │
│   │     ARM9       │          │     ARM7       │         │
│   │  ARM946E-S     │          │   ARM7TDMI     │         │
│   │    67 MHz      │          │    33 MHz      │         │
│   │  ARMv5TE       │          │   ARMv4T       │         │
│   │                │          │                │         │
│   │  LE JEU :      │          │  LE SUPPORT :  │         │
│   │  · moteur 3D   │          │  · audio       │         │
│   │  · gameplay    │          │  · Wi-Fi       │         │
│   │  · IA, menus   │          │  · tactile     │         │
│   │  · sauvegarde  │          │  · horloge     │         │
│   │                │          │  · alimentation│         │
│   └───────┬────────┘          └───────┬────────┘         │
│           │                           │                  │
│           └──────────┬────────────────┘                  │
│                      │                                   │
│            ┌─────────▼─────────┐                         │
│            │  4 Mo de RAM      │  partagée               │
│            └───────────────────┘                         │
└──────────────────────────────────────────────────────────┘
```

**Conséquences pratiques pour nous :**

1. **Il y a deux binaires à analyser**, pas un. `arm9.bin` (le jeu) et
   `arm7.bin` (le support). On passe ~90 % du temps sur l'ARM9.
2. **Deux jeux d'instructions coexistent** : ARM (32 bits) et Thumb
   (16 bits). Une même fonction peut basculer de l'un à l'autre. C'est la
   principale source d'erreurs de désassemblage — voir §8.
3. **Les adresses de chargement sont fixes et connues.** C'est une chance
   énorme : sur PC, l'ASLR rend l'analyse pénible. Ici l'ARM9 est
   *toujours* à `0x02000000`. Tous les pointeurs dans le code sont des
   adresses absolues valides → on peut suivre les appels de fonction
   directement, sans indirection.

### 1.2 L'en-tête de la ROM : la carte d'identité

Les **512 premiers octets** d'un `.nds` sont un en-tête standardisé qui dit
tout. C'est **toujours la première chose à lire.**

| Offset | Taille | Champ | Valeur ici | Signification |
|---|---|---|---|---|
| `0x00` | 12 | Titre | `DQM:JOKER` | Nom interne du jeu |
| `0x0C` | 4 | Game code | `AJRP` | `NTR-AJRP-EUR` = version européenne |
| `0x10` | 2 | Maker code | `GD` | Square Enix |
| `0x12` | 1 | Unit code | `0x00` | DS (pas DSi) |
| `0x13` | 1 | Encryption | `0x00` | Non chiffrée |
| `0x14` | 4 | Capacité | `0x0A` | 1024 Mbit = **128 Mo** |
| `0x1E` | 1 | Version ROM | `0` | |
| `0x20` | 4 | **ARM9 ROM offset** | `0x4000` | Où le code ARM9 commence dans le fichier |
| `0x24` | 4 | **ARM9 entry point** | `0x02000800` | **Point d'entrée du jeu** |
| `0x28` | 4 | ARM9 RAM address | `0x02000000` | Adresse de chargement |
| `0x2C` | 4 | ARM9 size | `0x78A18` | Taille du code |
| `0x30` | 4 | ARM7 ROM offset | `0x1E5E00` | |
| `0x34` | 4 | ARM7 entry point | `0x02380000` | |
| `0x38` | 4 | ARM7 RAM address | `0x02380000` | |
| `0x3C` | 4 | ARM7 size | `0x269A4` | |
| `0x40` | 4 | **FNT offset** | `0x20C800` | Table des noms de fichiers |
| `0x44` | 4 | FNT size | `0xC184` | |
| `0x48` | 4 | **FAT offset** | `0x218A00` | Table des positions de fichiers |
| `0x4C` | 4 | FAT size | `0x7840` | |
| `0x50` | 4 | ARM9 overlay table | `0x7CC00` | Table des overlays |
| `0x68` | 4 | Banner offset | `0x220400` | |

**FNT + FAT** forment le « système de fichiers » interne : c'est grâce à
eux qu'on extrait les 3 845 fichiers avec leurs vrais noms (§5).

> **Le réflexe à acquérir :** l'en-tête n'est pas décoratif. Chaque
> adresse qu'on donnera plus tard à Ghidra vient d'ici. Mal lire l'en-tête
> = toute l'analyse est fausse.

### 1.3 La contrainte mémoire, et pourquoi le code est découpé

La DS n'a que **4 Mo de RAM**. Un jeu de 128 Mo ne peut donc pas charger
tout son code d'un coup. La solution de Nintendo : découper le code en
**overlays** — des blocs chargés à la demande depuis la cartouche, comme
des pages mémoire.

Pour cette ROM, la table `y9.bin` déclare **3 overlays**, et leurs
adresses de chargement sont révélatrices :

| Overlay | Taille | Code | BSS | Adresse de chargement |
|---|---|---|---|---|
| 0 | 378 912 o | `0x5C820` | 198 016 o | `0x02184B40` |
| 1 | 618 112 o | `0x96E80` | 21 472 o | `0x02184B40` |
| 2 | 480 736 o | `0x755E0` | 132 320 o | `0x02184B40` |

**Les trois ont la MÊME adresse** → ils s'excluent mutuellement. Un seul
est résident à la fois. Ce sont les gros blocs du jeu (probablement
combat / village / menus) qui s'échangent dans le même espace mémoire.

Chaque entrée de la table `y9.bin` fait **32 octets** :
```
u32 overlay_id          identifiant
u32 ram_address         adresse de chargement
u32 ram_size            taille du code
u32 bss_size            taille de la zone non initialisée
u32 static_init_start   adresse du bloc d'initialisation statique
u32 static_init_end
u32 file_id             index dans la FAT
u32 flags               compression, etc.
```

---

## 2. L'environnement de travail

### 2.1 Le matériel et le système

```
Machine   : pavilionratonlaveurmalefiquedefanta
OS        : Ubuntu 26.04.1 LTS (Resolute Raccoon)
Noyau     : Linux 7.0.0-31-generic
CPU       : 16 cœurs
RAM       : 14 Go
Disque    : 135 Go libres
Bureau    : GNOME Shell 50.1
```

### 2.2 La ROM de départ

```
Archive  : 2109 - Dragon Quest Monsters - Joker (E)(EXiMiUS).7z  (30 Mo)
Contenu  : 5 fichiers
  · 2109 - Dragon Quest Monsters - Joker (E)(EXiMiUS).nds  128 Mo
  · 2109 - Cover.png
  · 2109 - Icon.png
  · 2109 - InGame.png
  · 2109 - EXiMiUS.nfo
```

**Première observation, importante :** la ROM fait **exactement
134 217 728 octets** = 128 Mo pile. Une ROM DS fait toujours une puissance
de 2. C'est un premier signe qu'elle est saine (non tronquée, non
sur-dumpée). On le vérifiera proprement avec les CRC au §3.

### 2.3 Les outils installés

| Outil | Version | Rôle | Installation |
|---|---|---|---|
| **ndstool** | 2.3.1 | Découpe des ROM DS | déjà présent (`/usr/local/bin`) |
| **Ghidra** | 12.1.3 | Décompilateur (le cœur) | téléchargé → `/opt/ghidra` |
| **Java** | OpenJDK 21 | Requis par Ghidra | déjà présent |
| **binutils-arm-none-eabi** | 2.45 | `objdump` ARM, désassemblage | déjà présent |
| **gcc-arm-none-eabi** | 14.2 | Chaîne de compilation ARM | `apt` |
| **radare2** | 6.0.7 | Framework RE en console | déjà présent |
| **DeSmuME** | 0.9.13 | Émulateur DS (débogage) | `apt` |
| **capstone** | 5.0.7 | Désassembleur Python | `apt` |
| **Pillow** | 12.1.1 | Traitement d'images | déjà présent |
| **ndspy** | 4.2.0 | Bibliothèque Python Nitro | `pip` |
| **ffmpeg** | 8.0.1 | Conversion audio | déjà présent |
| **ghex** | — | Éditeur hexadécimal | déjà présent |

#### Pourquoi Ghidra, et pas seulement objdump ?

C'est une question centrale. Comparons :

| Outil | Force | Faiblesse |
|---|---|---|
| `objdump` | Simple, rapide, exact | **Aucune analyse.** Il ne trouve pas les fonctions, ne suit pas les appels. 500 000 lignes illisibles. |
| `radare2` | Puissant, scriptable, léger | Courbe d'apprentissage rude, décompilateur moins bon |
| **Ghidra** | **Décompilateur vers C**, analyse automatique, gratuit | Gourmand en RAM, interface lourde |

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
remontant à une représentation intermédiaire appelée **P-code**, puis en la
« remontant » vers du C — technique dite *decompilation*.

> **Analogie :** le désassembleur traduit mot à mot ; le décompilateur
> reformule la phrase. Les deux sont justes, mais un seul se lit.

---

## 3. Étape 1 — Reconnaissance

**Règle d'or : ne jamais attaquer un binaire sans l'avoir d'abord observé.**

```bash
cd ~/Documents/ReverseEngeneering

# 1. Voir ce qu'il y a dans l'archive
7z l "2109 - Dragon Quest Monsters - Joker (E)(EXiMiUS).7z"

# 2. Extraire
7z x "2109 - Dragon Quest Monsters - Joker (E)(EXiMiUS).7z"

# 3. Lire l'en-tête
ndstool -i "2109 - Dragon Quest Monsters - Joker (E)(EXiMiUS).nds"
```

**Sortie obtenue (extraits) :**

```
Game title                DQM:JOKER
Game code                 AJRP (NTR-AJRP-EUR)
Maker code                GD (Square-Enix)
Device capacity           0x0A (1024 Mbit)
ARM9 ROM offset           0x4000
ARM9 entry address        0x2000800
ARM9 RAM address          0x2000000
ARM9 code size            0x78A18
Logo CRC                  OK
Header CRC                OK
Banner CRC                OK
English banner text       DRAGON QUEST MONSTERS / Joker / SQUARE ENIX
ARM9 footer found.
```

**Analyse de ce résultat :**

- **CRC tous `OK`** → la ROM est intacte, non corrompue, non modifiée.
- **`AJRP`, `NTR-AJRP-EUR`** → version européenne, 5 langues (voir §5.4).
- **`GD`** → Square Enix.
- **ARM9 à `0x02000000`**, ARM7 à `0x02380000` → on connaît les adresses de
  chargement dont Ghidra aura besoin.

> **Vérifier les CRC n'est pas optionnel.** Si la ROM est corrompue, tout
> le travail d'analyse qui suit sera bâti sur du sable, et on ne s'en
> apercevra qu'après des heures. C'est 5 secondes contre des jours.

> **Note technique :** `ndstool` affiche les adresses avec un zéro de
> moins (`0x2000800`). C'est `0x02000800` — l'outil omet les zéros de tête.
> Toujours recompter les chiffres.

---

## 4. Étape 2 — Découpage en composants

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

### 4.1 Signification de chaque option de ndstool

| Option | Cible | Ce que c'est |
|---|---|---|
| `-9` | `arm9.bin` | **Le jeu** — CPU principal |
| `-7` | `arm7.bin` | Le support — audio, Wi-Fi, tactile |
| `-y9` | `y9.bin` | Table des overlays ARM9 |
| `-y7` | `y7.bin` | Table des overlays ARM7 (vide ici) |
| `-d` | `data/` | Tous les fichiers du NitroFS |
| `-y` | `overlay/` | Les overlays eux-mêmes |
| `-t` | `banner.bin` | Bannière du menu de la console |
| `-v` | — | Verbeux (affiche les détails) |

### 4.2 Résultat du découpage

| Élément | Taille | Rôle |
|---|---|---|
| `arm9.bin` | 494 116 o | **Le jeu** |
| `arm7.bin` | 158 116 o | Audio / WiFi / tactile |
| `overlay/` | 3 fichiers, 1,5 Mo | Code paginé |
| `data/` | **3 845 fichiers, 117 Mo** | Assets + données |
| `y9.bin` | 96 o | Table des overlays |
| `banner.bin` | 2 112 o | Bannière |

---

## 5. Étape 3 — Comprendre le système de fichiers

### 5.1 NitroFS : le système de fichiers de la DS

La DS n'a pas de FAT32 ni d'ext4. Nintendo a conçu **NitroFS**, décrit par
deux tables pointées par l'en-tête :

```
FNT (File Name Table)   un ARBRE de répertoires
                        chaque entrée de dossier = 8 octets
                        { offset_du_nom, premier_id_fichier, id_parent }

FAT (File Allocation Table)   un TABLEAU PLAT
                        chaque entrée = 8 octets
                        { offset_début, offset_fin }
```

**L'astuce de NitroFS :** les fichiers n'ont pas d'identifiant stocké. Les
ID sont **attribués séquentiellement** dans l'ordre du parcours de l'arbre,
en partant du `premier_id_fichier` du dossier racine.

Pour retrouver un nom, il faut donc **parcourir l'arbre** et compter.
C'est exactement ce que fait `tools/nds_fs.py`.

### 5.2 L'inventaire des 3 845 fichiers — une mine d'information

Cette liste révèle **l'architecture complète du jeu**. Les extensions ne
sont pas choisies au hasard : ce sont les bibliothèques de Nintendo.

| Extension | Nombre | Technologie réelle |
|---|---|---|
| `.nsbca` | 1 261 | **Nintendo DS Bone Animation** — animations squelettiques |
| `.nsbmd` | 411 | **Nitro System Binary Model** — modèles 3D |
| `.bin` | 322 | Tables de données (voir §5.3) |
| `.pal` | 226 | Palettes de sprites |
| `.dma` | 226 | Données de sprites |
| `.efc` | 216 | Effets (particules) |
| `.pos` | 115 | Positions (cinématiques) |
| `.map` | 90 | Cartes |
| `.evt` | 80 | **Scripts d'événements** |
| `.evD/.evF/.evI/.evS` | 80 × 4 | **Dialogues traduits** (voir §5.4) |
| `.enct` | 66 | Encounter tables (rencontres) |
| `.SCR/.PAL/.CHR` | 60 × 3 | Tuiles de fonds 2D (format hérité de la GBA) |
| `.d16` | 40 | Images 16 bits (voir §10.1) |
| `.nsbma` | 25 | Animations de matériaux |
| `mes_*.bin[DFSIE]` | ~250 | **Textes traduits** |
| `.sdat` | 1 | **Archive sonore complète** (voir §10.2) |

### 5.3 Les tables de données : le cœur du gameplay

Certains noms de fichiers sont extraordinairement parlants — ils
**documentent le jeu sans qu'on ait à l'analyser** :

```
ItemTbl.bin              table des objets
SkillTbl.bin             table des compétences
ExperienceTbl.bin        courbe d'expérience
AbilityTbl.bin           capacités
BtlChrTbl.bin            personnages de combat
BtlEnmyPrm.bin           paramètres des ennemis
EnmyPtnTbl.bin           patterns d'IA ennemie
AI_PatternTbl.bin        (31 440 o) patterns d'IA
DamageTbl.bin            calcul des dégâts
ModelTbl.bin             modèles
MotionTbl.bin            mouvements
ChgMnstrTbl.bin          tables de fusion de monstres
SkillPointTbl.bin        points de compétence
```

> **Leçon :** ces noms ont survécu parce qu'ils servaient au développeur.
> Ils sont **de l'or pour le rétro-ingénieur** : ils disent où chercher.
> Retrouver la fonction qui ouvre `ItemTbl.bin` donne accès à toute la
> structure du système d'objets.

### 5.4 Les 5 langues dans une seule ROM

Les suffixes sur les fichiers de messages sont **D, F, I, S, E** :

```
mes_bank.binD    mes_bank.binF    mes_bank.binI    mes_bank.binS    mes_bank.binE
mes_bbs.binD     mes_bbs.binF     ...
mes_itemname.binD  mes_itemname.binF  ...
```

**D**eutsch, **F**rançais, **I**taliano, **S**panish, **E**nglish.

C'est ainsi qu'une ROM européenne contient 5 langues : **les traductions
sont des données, pas du code**. Il y a 50 fichiers `mes_*` × 5 langues.

> **Conséquence pratique majeure :** une traduction fan-made modifie ces
> fichiers et **jamais le code**. Pas besoin de désassembler quoi que ce
> soit pour traduire un jeu DS. C'est une information qui vaut de l'or, et
> elle vient juste de la lecture des noms de fichiers.

### 5.5 Les chaînes de caractères dans le code

```bash
strings -n 6 arm9.bin | head -40
```

Résultat marquant :

```
[SDK+NINTENDO:BACKUP]
[SDK+UBIQUITOUS:CPS]
[SDK+NINTENDO:WiFi2.0.30000.0703091639]
[SDK+UBIQUITOUS:SSL]
[SDK+NINTENDO:DWC2.1.30000.070519.0938_DWC_2_1]
```

**Analyse :**

- **`SDK+NINTENDO`** → le jeu utilise le **Nitro SDK** officiel, pas un
  moteur maison. Excellente nouvelle : ce SDK est documenté publiquement
  ([GBATEK](https://problemkaputt.de/gbatek.htm)), donc on peut
  **reconnaître** les fonctions du SDK dans le code et les écarter pour se
  concentrer sur la logique propre à Square Enix.
- **`WiFi2.0`** → la pile Wi-Fi de la DS.
- **`DWC2.1`** → **Nintendo Wi-Fi Connection**. Le jeu utilise les
  fonctions réseau officielles de Nintendo — l'équivalent de nos
  bibliothèques système.
- **`BACKUP`** → le module de sauvegarde.

---

## 6. Étape 4 — Vérifier que le code est exploitable

**Piège classique et vicieux :** beaucoup de ROMs DS ont leur ARM9
**compressé** (LZ77, RLE, ou BLZ/Huffman) et commencent par une signature
comme `0xFF 'BLZ'`. Si on lance Ghidra sur un flux compressé, on obtient
**du bruit pur** — et on peut perdre des heures à se demander pourquoi.

### 6.1 Le faux positif qu'il faut savoir reconnaître

```bash
xxd -l 16 arm9.bin
# ffde ffe7 ffde ffe7 ffde ffe7 ffde 7342
```

Les trois premiers octets `FF DE FF E7` ressemblent à une signature de
compression. **Mais décodé en ARM, c'est :**

```asm
mvn r15, #0xff0        ; 0xE7FFDEFF
```

C'est un **motif de remplissage standard** (une instruction qui ne fait
rien d'utile), pas de la compression.

**Comment trancher définitivement :** désassembler au point d'entrée
(`0x02000800` → offset `0x800` dans le fichier) et voir si on obtient du
code cohérent.

```bash
arm-none-eabi-objdump -D -b binary -m armv5te -EL \
    --start-address=0x800 --stop-address=0x840 arm9.bin
```

```asm
800:  mov   ip, #0x4000000     ; adresse de base des registres I/O de la DS
804:  str   ip, [ip, #520]     ; écrit dans REG_IME (interrupt master enable)
808:  ldrh  r0, [ip, #6]       ; lit REG_IE / REG_IF
80c:  cmp   r0, #0
810:  bne   0x808              ; boucle d'attente
814:  bl    0xa78              ; appel de fonction
818:  mov   r0, #19            ; mode CPU « IRQ »
81c:  msr   CPSR_c, r0         ; bascule en mode IRQ
820:  ldr   r0, [pc, #240]
824:  add   r0, r0, #16320
828:  mov   sp, r0             ; met en place la pile
```

**C'est du vrai code de démarrage, parfaitement cohérent :** on initialise
les interruptions, on attend, on change de mode processeur, on installe les
piles. **Conclusion : l'ARM9 est en clair, il est analysable.** [OK]

### 6.2 Le même contrôle sur l'ARM7

```bash
arm-none-eabi-objdump -D -b binary -m armv4t -EL --start-address=0 --stop-address=0x40 arm7.bin
```

```asm
0:  mov  ip, #0x4000000     ; mêmes registres I/O
4:  str  ip, [ip, #520]
8:  ldr  r1, [pc, #188]
c:  mov  r0, #0x3800000     ; 0x03800000 (WRAM ARM7)
10: cmp  r0, r1
14: movpl r1, r0
...
2c: mov  r0, #19            ; mode IRQ
30: msr  CPSR_c, r0
34: ldr  sp, [pc, #152]     ; pile
```

Également du code de démarrage valide. [OK]

> **À retenir :** avant de décompiler, **toujours** désassembler les
> 64 premiers octets au point d'entrée. Si on ne reconnaît pas un
> prologue de démarrage cohérent, c'est probablement compressé — et il
> faut décompresser d'abord.

---

## 7. Étape 5 — La décompilation

C'est le cœur du travail. On passe de « suite d'octets » à « code
compréhensible ».

### 7.1 La structure réelle d'un ARM9 : les 3 sections

Point subtil découvert grâce à `tools/extract_code.py` (basé sur la
bibliothèque `ndspy`). Un ARM9 DS n'est **pas un bloc unique** : le
NitroSDK le découpe en plusieurs **sections**, décrites par une
**« copy table »** située à l'offset `codeSettingsOffs` (ici `0x00000B68`).

```
┌─────────────────────────────────────────────────────────┐
│  arm9.bin — 3 sections                                   │
│                                                          │
│  [0] SECTION PRINCIPALE        base 0x02000000           │
│      taille 492 576 o    ← c'est le jeu                  │
│      (« implicite » : déjà à sa place en mémoire)        │
│                                                          │
│  [1] section annexe 1          base 0x01FF8000           │
│      taille 1 408 o      ← recopiée au boot              │
│                                                          │
│  [2] section annexe 2          base 0x027E0000           │
│      taille 96 o         ← recopiée au boot (bss 32 o)   │
└─────────────────────────────────────────────────────────┘
```

**Pourquoi c'est important :** les sections annexes sont recopiées à
**d'autres adresses** au démarrage. Si on les analyse à la mauvaise
adresse, tous leurs pointeurs internes sont faux.

C'est aussi ce qui explique la différence de taille entre les deux
extractions :
- `ndstool` donne 494 116 octets (tout le bloc depuis `0x4000`)
- `ndspy` donne 492 576 octets (la section principale seule)
- Écart = 1 540 octets = les sections annexes + l'en-tête

**Les deux sont corrects**, ils répondent à des questions différentes.

### 7.2 Les adresses de chargement : le point critique

**C'est l'erreur n°1 des débutants.** Il faut dire à Ghidra *où* ce
binaire sera chargé en mémoire, sinon tous les pointeurs sont faux.

| Module | Adresse de base | Langage Ghidra |
|---|---|---|
| `arm9.bin` | `0x02000000` | `ARM:LE:32:v5t` |
| `arm7.bin` | `0x02380000` | `ARM:LE:32:v4t` |
| section ARM9 annexe | `0x01FF8000` / `0x027E0000` | `ARM:LE:32:v5t` |
| section ARM7 annexe | `0x037F8000` / `0x027E0000` | `ARM:LE:32:v4t` |
| `overlay_0/1/2` | `0x02184B40` | `ARM:LE:32:v5t` |

**Décomposition d'un nom de langage Ghidra :**

```
ARM : LE : 32 : v5t
 │     │    │    └── v5t = ARMv5TE + Thumb  ← LE « t » EST CRITIQUE
 │     │    └─────── 32 bits
 │     └──────────── little-endian (la DS l'est)
 └────────────────── processeur ARM
```

- **`LE`** : little-endian.
- **`v5`** : ARMv5TE (ARM946E-S de l'ARM9) — supporte les instructions DSP.
- **`v4`** : ARMv4T (ARM7TDMI) — **pas** de v5 ! Mettre v5 produirait des
  instructions inexistantes sur cette puce.
- **`t`** : **critique** — voir §8.

**Sans `-loader-baseAddr 0x02000000`**, Ghidra croit que le code est à
l'adresse 0. Un appel à `bl 0x2010abc` pointerait alors dans le vide, et
**aucune fonction ne serait reliée à une autre**. Résultat : ~2000
fonctions isolées au lieu d'un programme structuré.

### 7.3 Le piège de la Secure Area

Les **2 premiers Ko** (`0x800` octets) de l'ARM9 sont la **Secure Area** :
une zone chiffrée par Nintendo pour des raisons de protection.

```
arm9.bin (tel qu'extrait)        arm9.bin (après neutralisation)
─────────────────────────        ──────────────────────────────
0x0000  ffde ffe7 ffde ffe7      0x0000  00 00 00 00 00 00 00 00
        (données chiffrées)              (zéros)
...
0x0800  01c3 a0e3 08c2 8ce5      0x0800  01c3 a0e3 08c2 8ce5
        ↑ POINT D'ENTRÉE RÉEL            ↑ inchangé
```

**Ce qu'il faut savoir :** une fois déchiffrée, la Secure Area ne contient
que `encryObj` et des zéros. **Elle n'a aucun intérêt fonctionnel.**

`tools/extract_code.py` la remplace par des zéros pour ne pas polluer
l'analyse. Le point d'entrée réel est `0x02000800`, **juste après**.

### 7.4 La commande de décompilation

```bash
/opt/ghidra/support/analyzeHeadless <projet> <nom> \
    -import arm9.bin \
    -processor "ARM:LE:32:v5t" \
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
pour traiter 280 000 lignes de code : cliquer sur 7 140 fonctions à la
main serait absurde.

### 7.5 Le script d'export expliqué

`tools/ghidra_scripts/ExportDecompiled.java` parcourt toutes les fonctions
que Ghidra a identifiées et écrit le C décompilé. Le cœur :

```java
DecompInterface dec = new DecompInterface();
dec.openProgram(currentProgram);            // branche le décompilateur

FunctionIterator funcs =
    currentProgram.getFunctionManager().getFunctions(true);  // true = ordre d'adresse

while (funcs.hasNext()) {
    Function f = funcs.next();
    DecompileResults res = dec.decompileFunction(f, 60, monitor);  // 60 s max
    if (res.decompileCompleted()) {
        w.println(res.getDecompiledFunction().getC());   // le C !
    }
}
```

**Trois détails importants :**

1. **`getFunctions(true)`** : le `true` trie par adresse croissante. Sans
   ça, l'ordre est arbitraire et le fichier illisible.
2. **Le timeout de 60 s** : certaines fonctions énormes font boucler le
   décompilateur. Le timeout évite de bloquer sur une seule.
3. **`decompileCompleted()`** : il faut tester le retour. Un décompilateur
   peut échouer sur une fonction (« pcode error ») sans lever d'exception.

### 7.6 Pourquoi Ghidra doit-on lancer module par module ?

Chaque module (ARM9, ARM7, chaque overlay) est un **binaire distinct** avec
sa propre adresse de base. Ghidra analyse un programme à la fois. D'où 5
lancements successifs.

C'est aussi **méthodologiquement correct** : un overlay est un module
autonome, chargé à la demande. Les analyser séparément est le bon modèle
mental.

---

## 8. Le piège du Thumb — la leçon centrale

**C'est la découverte la plus importante de toute cette session, et elle
mérite sa propre section.**

### 8.1 Le problème : deux jeux d'instructions

Chaque processeur de la DS sait exécuter **deux jeux d'instructions** :

| | ARM | Thumb |
|---|---|---|
| Taille d'instruction | 32 bits | **16 bits** |
| Avantages | Puissant, 16 registres accessibles, instructions conditionnelles | Code **~30 % plus compact** |
| Inconvénients | Code volumineux | Moins de registres, moins d'instructions |

Le processeur bascule de l'un à l'autre **à l'exécution**. Ce qui décide,
c'est le **bit 0 de l'adresse cible d'un saut** :

```
bit 0 = 0   →   la cible est du code ARM   (adresse paire)
bit 0 = 1   →   la cible est du code Thumb (adresse impaire)
```

C'est astucieux : l'adresse d'une instruction ARM est toujours multiple de
4, celle d'une instruction Thumb multiple de 2. Les deux bits de poids
faible sont donc **libres**, et Nintendo les utilise comme indicateur de
mode.

### 8.2 L'observation qui a tout déclenché

En décompilant l'ARM7, le résultat contenait **558 avertissements** :

```c
/* WARNING: Control flow encountered bad instruction data */
void FUN_0238061c(void)
{
    /* WARNING: Bad instruction - Truncating control flow here */
    halt_baddata();
}
```

En désassemblant cette zone, on découvre le motif :

```asm
0238061c:  ldr  ip, [pc]        ; charge l'adresse qui suit dans ip
02380620:  bx   ip              ; saute en changeant de jeu d'instructions
02380624:  .word 0x038035a1     ; ← l'adresse cible
```

**`0x038035a1` : regardez le dernier chiffre — `1`, donc le bit 0 est à 1.**
→ La destination est du **Thumb**, pas de l'ARM.

Ce motif `ldr ip,[pc]` / `bx ip` s'appelle un **veneer** (ou *trampoline*) :
un petit bout de code qui sert uniquement à changer de mode en sautant.

**Vérification faite :**
```python
0x038035a1 & 1  = 1        → Thumb
0x038035a1 & ~1 = 0x38035a0 → adresse réelle du code Thumb
```

### 8.3 Pourquoi c'est un piège vicieux

Dans Ghidra, les langages **sans `t`** (`ARM:LE:32:v5`) ne désassemblent
**que** l'ARM. Toute zone Thumb y apparaît comme des instructions
invalides.

Le vrai danger n'est pas l'erreur — c'est le **silence** :

> Ghidra produit un fichier **parfaitement plausible**, qui compile, qui a
> l'air complet. Il ne manque juste… 41 fonctions. Sans aucun message
> d'erreur global. **Un échec silencieux est bien plus dangereux qu'une
> erreur franche.**

### 8.4 La correction

Un seul caractère dans le nom du langage :

```bash
# [ ] AVANT — ARM seulement
-processor "ARM:LE:32:v5"
-processor "ARM:LE:32:v4"

# [x] APRÈS — ARM + Thumb
-processor "ARM:LE:32:v5t"
-processor "ARM:LE:32:v4t"
```

Le `t` final signifie *« ce processeur possède aussi le jeu Thumb, et
Ghidra doit en tenir compte »*.

### 8.5 Les mesures, avant / après

| Module | Langage | Fonctions | `halt_baddata` |
|---|---|---|---|
| ARM7 | `v4` | 358 | **558** |
| ARM7 | `v4t` | **399** | **0** |
| ARM9 | `v5` | 1952 | 10 |
| ARM9 | `v5t` | **1979** | **0** |
| overlay 2 | `v5` | 2275 | — |
| overlay 2 | `v5t` | **2439** | **0** |

**Bilan : 41 fonctions de l'ARM7 et 27 de l'ARM9 étaient invisibles**, soit
**68 fonctions perdues**, plus 568 zones de code illisibles. À cause d'un
seul caractère.

### 8.6 La leçon transférable

> **En reverse engineering, comptez toujours les avertissements.**
> Un `grep -c halt_baddata` non nul dans le résultat signifie qu'il manque
> du code. Ne jamais se fier au fait que « ça a l'air de marcher ».

C'est une règle générale : **valider par une mesure objective**, pas par
impression. Elle s'appliquera à toutes les étapes suivantes (validation des
images, validation de l'audio).

---

## 9. Résultats obtenus

### 9.1 Le code

| Module | Rôle | Fonctions | Échecs | Fichier |
|---|---|---|---|---|
| ARM9 | Le jeu | **1 979** | 0 | `work/decompiled/arm9.c` |
| ARM7 | Audio/WiFi | **399** | 0 | `work/decompiled/arm7.c` |
| Overlay 0 | Code paginé | **1 204** | 0 | `work/decompiled/overlay_0000.c` |
| Overlay 1 | Code paginé | **1 119** | 0 | `work/decompiled/overlay_0001.c` |
| Overlay 2 | Code paginé | **2 439** | 0 | `work/decompiled/overlay_0002.c` |
| **TOTAL** | | **7 140** | **0** | **279 930 lignes de C** |

**Zéro échec, zéro `halt_baddata`.** L'intégralité du code exécutable de la
ROM est décompilée.

### 9.2 Exemple : la toute première fonction, déjà identifiable

```c
undefined4 FUN_02000950(int param_1)
{
  if (param_1 != 0) {
    puVar5 = (undefined1 *)(param_1 + *(int *)(param_1 + -4));
    puVar7 = (ushort *)(param_1 - (*(uint *)(param_1 + -8) >> 0x18));
    uVar4  = param_1 - (*(uint *)(param_1 + -8) & 0xffffff);
    puVar6 = puVar5;
    while ((int)uVar4 < (int)puVar7) {
      puVar7 = (ushort *)((int)puVar7 + -1);
      bVar9 = *(byte *)puVar7;
      iVar10 = 8;
      while (0 < iVar10) {
        if ((bVar9 & 0x80) == 0) {
          puVar7 = (ushort *)((int)puVar7 + -1);
          puVar6 = puVar6 + -1;
          ...
```

**On peut déjà dire ce que c'est.** Le motif :

```c
param_1 - (*(uint *)(param_1 - 8) & 0xffffff)     // début des données
*(uint *)(param_1 - 8) >> 0x18                    // type de compression
```

est la signature exacte des en-têtes de compression **BIOS de la GBA/DS** :

```
+0        : type   (0x20 = LZ77 8 bits, 0x24 = LZ77 16 bits, 0x28 = RLE)
+1 .. +3  : taille décompressée
-8        : longueur compressée
-4        : offset du symbole de compression
```

C'est `SWI_Unpack` / `LZ77UnComp` — la fonction de décompression fournie par
le BIOS de la console **en ROM**, que le SDK appelle au démarrage.

> **C'est exactement à quoi ressemble le travail de RE :** lire du code
> machine et y **reconnaître des motifs connus**. La première fonction du
> jeu est un décompresseur, ce qui est parfaitement logique — le jeu doit
> décompresser ses assets.

### 9.3 La désassemblage brut, en complément

Pour référence, les désassemblages complets sont dans `work/analysis/` :

| Fichier | Taille | Lignes |
|---|---|---|
| `arm9.asm` | 4,6 Mo | 121 568 |
| `arm7.asm` | 1,5 Mo | 39 508 |
| `overlay_0000.asm` | 3,5 Mo | 93 886 |
| `overlay_0001.asm` | 5,9 Mo | 153 949 |
| `overlay_0002.asm` | 4,7 Mo | 119 687 |

### 9.4 Remonter d'une chaîne au code qui l'utilise

Outil avancé et très instructif : `tools/xref_string.py`.

**Le problème :** sur ARM, une instruction ne peut pas contenir une adresse
32 bits en immédiat (l'encodage ne le permet pas). Le compilateur pose donc
l'adresse dans un **« pool littéral »** — une table de mots 32 bits glissée
au milieu du code — puis émet un `ldr rX, [pc, #imm]` qui la charge
relativement au PC.

La chaîne de références est donc :

```
   code  ──ldr [pc,#imm]──►  entrée du pool littéral  ──valeur──►  la chaîne
```

**Exemple réel d'utilisation :**

```bash
python3 tools/xref_string.py work/code/arm9.bin 0x02000000 "/sound_data.sdat"
```

**Résultat :**

```
--- 1. Occurrences de la chaîne ---
    offset 0x0777FC  ->  adresse 0x020777FC

--- 2. Entrées de pool littéral pointant sur ces occurrences ---
    slot 0x020420B0 (offset 0x0420B0) contient 0x020777FC

--- 3. Instructions qui chargent ces slots ---
    0x02041FD8  [arm]  ldr r1, [pc, #0xD0]  -> pool 0x020420B0 -> "/sound_data.sdat"
```

**On a trouvé, en trois étapes, l'instruction exacte qui charge le chemin
du fichier sonore.** Il ne reste plus qu'à décompiler `FUN_02041FD8` pour
voir comment le jeu ouvre son archive audio.

> **C'est la technique fondamentale du RE :** les chaînes servent de
> **points d'ancrage**. Une chaîne `"SAVE"` près d'une fonction → c'est la
> sauvegarde. Une chaîne `"item"` → le système d'objets. On part de ce
> qu'on connaît pour aller vers ce qu'on ne connaît pas.

---

## 10. Extraire les ressources (images, sons)

### 10.1 Pourquoi il n'y a ni `.png` ni `.mp3` dans la ROM

**C'est le point de départ, et il faut le comprendre avant de chercher des
outils.**

Un `.png` est un format **de fichier** : en-tête, table de couleurs, blocs
`IDAT` compressés en zlib. Un `.mp3` idem, avec ses trames MPEG. Ces
formats ont été conçus pour **le stockage et l'échange entre ordinateurs**.

La Nintendo DS ne lit **aucun** de ces deux formats :

| Ce que la DS a | Pourquoi |
|---|---|
| Pas de décodeur PNG | Elle a un décodeur de tuiles 2D et un moteur 3D qui lit des textures en **BGR555 brut**. Décoder du zlib en temps réel coûterait trop cher en CPU et en RAM. |
| Pas de décodeur MP3 | Son matériel audio lit du PCM et de l'ADPCM directement. Chaque échantillon doit être jouable instantanément. |
| Pas de GPU au sens PC | Son « GPU » est un ensemble de **registres mémoire mappés** (`0x04000000`+) qu'on pilote en écrivant des valeurs. |

**Conséquence :** le jeu stocke ses ressources dans les **formats natifs du
matériel**. Les `.nsbmd`, `.d16`, `.sdat` ne sont pas des « archives à
décompresser » comme un `.zip` : ce sont des **structures mémoire
sérialisées**, prêtes à être copiées en VRAM ou dans le mélangeur audio.

Il n'existe donc **pas de recette unique**. Chaque format demande une
rétro-ingénierie de son agencement.

### 10.2 La méthode générale (valable pour tout format inconnu)

C'est **la démarche à retenir**, celle appliquée à chaque format :

```
  1. TAILLE      Le fichier fait 98312 octets. Pour une image annoncée
                 256×192, on attend 256 × 192 × 2 = 98304 octets.
                 Écart : 8 octets.  ->  il y a un en-tête de 8 octets.

  2. SIGNATURE   Les 4 premiers octets sont 44 31 36 00 = "D16\0".
                 ->  le format s'appelle D16. C'est la preuve qu'on
                     regarde le bon endroit (un vrai en-tête, pas du bruit).

  3. DIMENSIONS  Les 4 octets suivants, lus en little-endian :
                 0x0100 = 256 et 0x00C0 = 192.
                 ->  exactement les dimensions attendues. En-tête confirmé.

  4. CONTENU     Le pixel 0 vaut 0xFBDE. En BGR555 -> R=30, G=30, B=30
                 = gris clair. Cohérent avec le coin d'une image.
                 ->  l'interprétation des pixels est la bonne.

  5. VALIDATION  On convertit et on MESURE : écart moyen entre pixels
                 voisins = 45 / 765. Du bruit aléatoire donnerait ~400.
                 ->  l'image est cohérente. Conversion correcte.
```

**L'étape 5 est la plus importante et la plus souvent oubliée.** On ne
suppose pas qu'on a réussi : **on le vérifie par une mesure objective.**

### 10.3 Les images : `.d16` → PNG

**Format découvert :**

```
Offset  Taille  Contenu
0x00    4       signature "D16\0"  (44 31 36 00)
0x04    2       largeur en pixels  (little-endian)
0x06    2       hauteur en pixels  (little-endian)
0x08    ...     pixels bruts
```

**Le BGR555** est le format natif de la DS et de la GBA. 16 bits par pixel :

```
   15  14 13 12 11 10  9  8  7  6  5  4  3  2  1  0
  +---+-------------+----------+------------------+
  | X |    BLEU     |   VERT   |      ROUGE       |
  +---+-------------+----------+------------------+
   ignoré   5 bits     5 bits       5 bits
```

Chaque composante va de **0 à 31** au lieu de 0 à 255. **Le piège de la
conversion :** ce n'est pas `× 8` (qui plafonnerait à 248) mais la
**répétition des bits de poids fort** :

```python
r8 = (r5 << 3) | (r5 >> 2)    # 0 -> 0,  31 -> 255  (toute la plage couverte)
```

*Explication :* `r5 = 31` (binaire `11111`). `31 << 3 = 248` (`11111000`).
`31 >> 2 = 7` (`111`). `248 | 7 = 255`. [OK]

**Outil :** `tools/d16topng.py`

```bash
python3 tools/d16topng.py --all work/extracted/data out/png
# -> 40/40 convertis, 256×192 chacun
```

**Validation objective obtenue :**

| Fichier | Couleurs distinctes | Écart voisins |
|---|---|---|
| `dm_pic_00.png` | 8 045 | 45 / 765 |
| `dm_pic_07.png` | 2 485 | — |
| `dm_pic_04.png` | 521 (69 % noir) | — |

L'écart de 45/765 entre pixels voisins prouve une **image structurée** (du
bruit donnerait 380–500). Les images sont correctes. [OK]

**Pour les autres formats d'image :**

| Format | Nature | Traitement |
|---|---|---|
| `.SCR` / `.PAL` / `.CHR` | Tuiles 8×8 indexées + palette + disposition | Format hérité de la GBA. Il faut les 3 fichiers pour reconstruire une image. |
| `.dma` / `.pal` | Sprites DS | Paires données + palette |
| `.nsbmd` | **Modèles 3D**, pas des images | Les textures sont à part. Outil : [apicula](https://github.com/pleonex/apicula) (Rust) |

### 10.4 Le son : `.sdat` → WAV

#### Le piège conceptuel : un SDAT n'est pas un dossier de MP3

Le `.sdat` (Sound Data Archive) est l'archive sonore standard du Nitro SDK.
Elle contient **cinq types d'objets**, et ils ne sont **pas**
interchangeables :

| Type | Nature | Équivalent PC |
|---|---|---|
| **SSEQ** | Une **partition**. « Joue le do pendant 200 ms avec l'instrument 5. » | Un fichier **MIDI** |
| **SBNK** | Une **banque** : associe chaque instrument à un échantillon | Un *soundfont* |
| **SWAR** | Des **échantillons** audio bruts (PCM/ADPCM) | Des WAV courts |
| **STRM** | De l'audio **déjà encodé** | Un WAV/MP3 complet |
| **SARC** | Un conteneur imbriqué | Un sous-dossier |

> **Le point crucial :** une musique de jeu DS est presque toujours une
> **SSEQ**. Et une SSEQ **ne contient pas de son**. Elle décrit *quoi*
> jouer et a besoin de la SBNK + du SWAR pour produire de l'audio.

**Autrement dit :** extraire une SSEQ d'un SDAT vous donne un fichier qui,
ouvert dans un lecteur audio, ne produit **rien**. Ce n'est pas un bug,
c'est sa nature. Pour l'entendre il faut **simuler la console** — un
séquenceur qui lit la partition et synthétise les échantillons. C'est
exactement ce que fait le matériel de la DS en temps réel.

#### Ce qu'on a extrait de cette ROM

**Outil :** `tools/sdatextract.py`

```bash
python3 tools/sdatextract.py work/extracted/data/sound_data.sdat out/sound
```

Résultat — l'archive fait **19 Mo** et contient :

| Type | Fichiers | Taille | Nature |
|---|---|---|---|
| SSEQ | 133 | 744 K | Partitions (ne sonnent pas seules) |
| SBNK | 31 | 128 K | Banques d'instruments |
| SWAR | 31 | 5,2 M | Échantillons audio |
| STRM | 199 | 14 M | **Audio directement jouable** |

#### Les difficultés rencontrées (et comment elles ont été résolues)

Ce SDAT **n'est pas au format standard**, ce qui a demandé plusieurs
itérations :

**Piège 1 — l'en-tête a deux variantes d'agencement.**

```
Variante classique :  trois offsets SÉPARÉS
    0x10 = offset INFO    0x14 = offset FAT    0x18 = offset FILE

Variante de ce jeu :  des PAIRES (offset, taille)
    0x10 = SYMB    0x18 = INFO    0x20 = FAT    0x28 = FILE
```

**Comment trancher :** vérifier quelle interprétation place une signature
connue à l'offset lu. Ici on trouve `SYMB` → variante B.

**Piège 2 — le bloc `SYMB` n'existe pas dans le format standard.**
Ce jeu ajoute un bloc de **symboles** (noms des sons) que le SDAT normal
n'a pas. Sa présence décale tout.

**Piège 3 — les entrées de la FAT font 16 octets, pas 8.**
Vérification : `394 entrées × 16 + 12 d'en-tête = 6316 octets`, soit
**exactement** la taille du bloc (`0x18AC`). Avec 8 octets on trouverait
788 entrées, ce qui est **faux**.

**Détail amusant et instructif :** la lecture initiale donnait
« 1 145 849 439 entrées FAT » — un nombre absurde. C'est le signe classique
d'une erreur de parsing : on lisait du **texte ASCII** (`SE_DEM_058`,
`SE_SYS_013`…) comme s'il s'agissait d'entiers. 

> **Réflexe à acquérir :** quand un décompte est absurde (milliards
> d'entrées, taille négative), **c'est toujours** une erreur de parsing.
> Ne jamais continuer en espérant que ça s'arrange.

**La solution finale :** plutôt que de deviner l'encodage des tables de
sous-blocs (qui est propriétaire), on prend la **FAT comme source de
vérité** et on sélectionne les fichiers par leur **signature interne**
(`SSEQ`, `SBNK`, `SWAR`, `STRM`). C'est plus robuste : **on s'appuie sur
les données elles-mêmes, pas sur une hypothèse.**

#### Décoder le STRM : le format

Trois codecs possibles selon l'octet à l'offset `0x18` :

| Codec | Nom | Traitement |
|---|---|---|
| 0 | PCM8 | Octets signés, à multiplier par 256 |
| 1 | PCM16 | Mots de 16 bits signés |
| 2 | **ADPCM** | Compression 4 bits/échantillon |

**Structure du header STRM (décodée par recoupement) :**

```
0x00  4   "STRM"
0x04  2   BOM (FFFE = little-endian)
0x06  2   version
0x08  4   taille du fichier
0x18  1   codec          (0=PCM8, 1=PCM16, 2=ADPCM)
0x19  1   bouclage       (loop)
0x1C  2   fréquence d'échantillonnage
0x20  4   loopStart
0x24  4   numSamples
0x28  4   numBlocks
0x2C  4   blockSize
0x50  4   "DATA"
0x54  4   taille des données
```

**L'ADPCM expliqué** (IMA-ADPCM adaptatif) : on ne stocke pas la valeur de
l'échantillon, mais **la différence** avec le précédent, sur 4 bits. Un
« index de pas » s'ajuste à chaque échantillon : quand le signal varie
vite, le pas augmente ; quand il est stable, le pas diminue. C'est ce qui
rend la compression efficace sur de l'audio.

**Format de bloc DS :** 4 octets d'en-tête (prédicteur initial + index)
puis 32 octets de nibbles = 64 échantillons. Le bloc fait donc 36 octets
pour 64 échantillons → **facteur de compression 3,5×**.

```python
for nibble in (octet & 0x0F, octet >> 4):     # 2 échantillons par octet
    pas  = TABLE_PAS[index]
    diff = (pas >> 3)
    if nibble & 1: diff += pas >> 2
    if nibble & 2: diff += pas >> 1
    if nibble & 4: diff += pas
    if nibble & 8: diff = -diff
    predicteur += diff                        # on ACCUMULE (différentiel)
    index += TABLE_INDEX[nibble]              # le pas s'adapte
```

**Outil :** `tools/strmtowav.py`

```bash
python3 tools/strmtowav.py --all out/sound/STRM out/wav
# -> 199/199 convertis, 196 avec audio réel, 6,5 minutes au total
```

**Validation objective :** la piste la plus longue fait **17,93 s**, RMS
**6409**, dynamique de −32 256 à +32 000. C'est de la vraie musique, pas du
silence ni du bruit. [OK]

**Distribution des codecs observée :** la majorité en PCM8 (`codec=0`) à
32 728 Hz ou 22 767 Hz — des fréquences typiques de la DS (elles dérivent
de l'horloge de 33,5 MHz par divisions entières).

#### Le bloc SYMB : une découverte en or

Ce SDAT contient un bloc **`SYMB`** (absent du format standard) qui donne
**562 noms symboliques** :

```
SE_BTL_001    son de combat n°1
SE_SYS_013    son système
SE_FLD_010    son de terrain
SE_DEM_021    son de cinématique
SE_SKL_054    son de compétence
BGM_001       musique de fond
```

Combiné au fichier `sound_data.sadl` (517 `#define` supplémentaires, un
fichier texte de 12 Ko expliquant que `WAVE_BGM_001 = 0`), on obtient
**plus de 1 000 noms** qui documentent l'audio du jeu **sans avoir à
l'écouter**.

> **Leçon :** dans une ROM, les **blocs de symboles** et les fichiers
> `.sadl` sont de l'or. Ils ont survécu à la compilation parce qu'ils
> servaient au développeur — et ils donnent les noms que le compilateur a
> détruits partout ailleurs.

#### Pour entendre les SSEQ (les vraies musiques)

Il faut **simuler la console**. L'outil de référence est **vgmstream** :

```bash
# Convertir une partition en WAV (il résout les références SBNK/SWAR)
vgmstream-cli -o musique.wav out/sound/SSEQ/0000_xxx.sseq

# Ou lire le .sdat entier et tout extraire
vgmstream-cli -o out/vgm/?s.wav work/extracted/data/sound_data.sdat
```

> **Note :** `vgmstream` n'est pas dans les dépôts Ubuntu et n'est pas
> installable via `pip`. Il faut le compiler depuis
> [GitHub](https://github.com/vgmstream/vgmstream). C'est le seul chaînon
> manquant de cette session — et il ne concerne que les 133 partitions,
> pas les 199 pistes déjà jouables.

### 10.5 Le malentendu SWAR : « pourquoi mes fichiers ne s'ouvrent pas »

**C'est la question la plus fréquente, et elle mérite une section à part**
car elle révèle une confusion de fond sur ce qu'est un fichier audio.

#### Le problème

On extrait d'un SDAT quatre types de fichiers. On essaie de les ouvrir dans
un lecteur audio. Résultat :

| Fichier | S'ouvre ? | Pourquoi |
|---|---|---|
| `.strm` (converti en WAV) | [OK] **Oui** | C'est de l'audio déjà encodé |
| `.swar` | [KO] **Non** | **Ce n'est pas un fichier audio** |
| `.sseq` | [KO] **Non** | C'est une partition, pas du son |
| `.sbnk` | [KO] **Non** | C'est une table d'instruments |

**Et ce n'est pas un bug, ni un échec de conversion.** Ces trois fichiers
ne sont simplement **pas de l'audio**. Les ouvrir dans un lecteur audio
revient à essayer d'écouter un `.zip` : le conteneur n'est pas le contenu.

#### L'analogie qui clarifie tout

```
   Un .swar est un  DOSSIER D'ÉCHANTILLONS
   ────────────────────────────────────────
   Comme un dossier contenant 12 fichiers WAV.
   Le dossier lui-même ne « sonne » pas : il CONTIENT des choses qui sonnent.

   Un .sseq est une  PARTITION (comme un MIDI)
   ────────────────────────────────────────────
   Elle dit « joue le do pendant 200 ms avec l'instrument 5 ».
   Elle ne contient aucun son : il faut un instrument pour la jouer.

   Un .strm est un  FICHIER AUDIO
   ──────────────────────────────
   Il contient le son lui-même. C'est le seul des quatre
   qui soit directement jouable.
```

#### La hiérarchie complète

```
  .sdat  (l'archive sonore)
    │
    ├── SSEQ  ──── la PARTITION ──────────────┐
    │              « quoi jouer »             │
    │                                          │
    ├── SBNK  ──── la BANQUE D'INSTRUMENTS ───┤  ces trois-là
    │              « instrument 5 = ? »       │  fonctionnent
    │                                          │  ENSEMBLE
    ├── SWAR  ──── les ÉCHANTILLONS ──────────┘
    │              « le son brut de l'instrument »
    │
    └── STRM  ──── l'AUDIO ENCODÉ  ← jouable seul
```

**Une musique de jeu DS est presque toujours une SSEQ.** Elle a besoin de
la SBNK (pour savoir quel instrument) et du SWAR (pour avoir le son de cet
instrument). Les trois forment une chaîne : aucun ne suffit seul.

C'est exactement comme un fichier MIDI sur PC : votre lecteur MIDI a
besoin d'un *soundfont* pour produire du son. Le MIDI seul est silencieux.

#### La solution : extraire les échantillons du SWAR

Puisque le `.swar` est un conteneur, il faut en **extraire** les
échantillons. C'est le rôle de `tools/swartowav.py` :

```bash
python3 tools/swartowav.py --all out/sound/SWAR out/wav_swar
# -> 404 échantillons extraits de 29 banques
```

**Résultat obtenu :**

| Mesure | Valeur |
|---|---|
| Banques SWAR traitées | 31 (dont 2 vides, ce qui est normal) |
| Échantillons extraits | **404** |
| Format | ADPCM 44 100 Hz (et 32 000 / 35 006 / 45 864 Hz) |
| Durée cumulée | 312 secondes (~5 min) |
| Saturation résiduelle | **0 %** sur 392/404 fichiers |

**Le total audio jouable passe donc de 199 à 603 fichiers WAV.**

#### Structure interne d'un SWAR (décodée)

```
  0x00  4   "SWAR"
  0x04  2   BOM (FFFE = little-endian)
  0x06  2   version (0x0100)
  0x08  4   taille du fichier
  0x0C  2   taille du bloc DATA
  0x0E  2   nombre de blocs
  0x10  4   "DATA"
  0x14  4   taille des données
  0x18  ... remplissage de zéros
  0x38  4   NOMBRE D'ÉCHANTILLONS        ← ici, pas à 0x0C !
  0x3C  N×4 TABLE D'OFFSETS ABSOLUS      ← chaque offset pointe
                                            directement sur son échantillon
```

#### Structure d'un échantillon (dans un SWAR)

Point subtil qui a causé une erreur : **à l'intérieur d'un SWAR, les
échantillons n'ont pas d'en-tête de fichier `SWAV`.** L'en-tête de
l'échantillon commence directement à l'offset 0 :

```
  0x00  1   codec (0 = PCM8, 1 = PCM16, 2 = ADPCM)
  0x01  1   bouclage
  0x02  2   fréquence d'échantillonnage
  0x04  2   time
  0x06  2   loopOffset
  0x08  4   longueur de boucle
  0x0C  ... données audio
```

> Un `.swav` stocké comme **fichier autonome** possède en plus un en-tête
> Nitro de `0x24` octets **avant** ces champs. C'est la source de confusion
> classique : la même structure se lit à deux offsets différents selon le
> contexte. Un `.swar` = en-tête à `0x00`. Un `.swav` = en-tête à `0x24`.

#### L'erreur d'ADPCM, et comment elle a été corrigée

**Symptôme :** les échantillons extraits étaient *presque* bons. Le début
sonnait correctement (~130 échantillons), puis **49,7 % du signal était
saturé** à ±32 767. Un son qui dégénère en bruit blanc.

**Diagnostic :** j'avais implémenté l'ADPCM « par blocs », en supposant
que chaque bloc de 36 octets recommençait par un en-tête
`(prédicteur, index)`. C'est le modèle du WAV IMA et du MS-ADPCM.

**La vérification qui a tout montré :** en lisant l'index de pas au début
de chaque bloc supposé, on obtenait `index = 235` — **impossible**, la
valeur maximale étant 88. La structure supposée n'existait pas.

**La vraie nature de l'ADPCM DS :** c'est un **flux continu**, sans aucun
en-tête répété. Le prédicteur et l'index de pas sont initialisés **une
seule fois**, depuis les 4 premiers octets de l'échantillon, puis évoluent
en continu jusqu'à la fin.

*Vérification faite auprès de la source de référence :* la bibliothèque
`vgmstream` nomme ce codec **`coding_IMA_mono`** et le documente
explicitement comme *« no header (external setup) »* — sans en-tête
interne. Elle lit d'ailleurs l'index de pas en `s16` (16 bits), et non en
`u8`.

**Après correction :**

| Mesure | Avant | Après |
|---|---|---|
| Saturation | **49,7 %** | **0,00 %** |
| RMS | 26 924 (écrêté) | 16 480 (naturel) |
| Discontinuités > 20 000 | — | **0 / 38 535** |
| Écart moyen entre échantillons | — | 410 (signal lisse) |

**La leçon :** un résultat *presque* correct est plus trompeur qu'un
résultat franchement faux. Le signal saturé ressemblait à « un son fort ».
Seule une **mesure** (49,7 % de saturation, et un index de pas à 235
impossible) a permis de trancher.

#### Résumé : quel outil pour quel type

| Type | Fichier | Nature | Comment l'entendre |
|---|---|---|---|
| **STRM** | `.strm` | Audio encodé | `strmtowav.py` → **WAV direct** |
| **SWAR** | `.swar` | Banque d'échantillons | `swartowav.py` → **WAV par échantillon** |
| **SSEQ** | `.sseq` | Partition (MIDI) | `vgmstream-cli` (simule la console) |
| **SBNK** | `.sbnk` | Instruments | Ne s'écoute pas seul |

### 10.6 Les modèles 3D : `.nsbmd` → Blender

**Question posée :** « où trouver les scènes 3D, et peut-on les ouvrir
depuis Blender ? »

#### Où sont les modèles 3D

**Réponse : 411 fichiers `.nsbmd` dans `data/`.** Leur nommage révèle
l'organisation du jeu :

| Préfixe | Nombre | Signification |
|---|---|---|
| **`m`** | **211** | **Monstres** (`m000` → `m248`, séquentiel) |
| `o` | 88 | Objets et décors |
| `bf` | 50 | Modèles de combat (*battle field*) |
| `bd` | 29 | Modèles de bâtiment |
| `n` | 16 | PNJ / personnages |
| `bh`, `bh` | 3 | Divers |

La preuve que les `m` sont les monstres : leur numérotation est
**séquentielle et continue** (`m000`, `m001`… `m248`) et correspond
exactement à la table `ModelTbl.bin` présente dans `data/`. C'est le
cœur d'un jeu de collection de monstres.

#### Que contient un `.nsbmd`

**Découverte importante : le modèle est AUTONOME.** En analysant le
fichier, on trouve :

```
  0x0000  "BMD0"   en-tête du fichier Nitro
  0x0018  "MDL0"   la GÉOMÉTRIE (sommets, faces, matériaux, squelette)
  0x4FD4  "TEX0"   les TEXTURES (incluses dans le même fichier !)
```

**409 des 411 modèles contiennent leur bloc `TEX0`.** Les textures sont
donc **incluses**, pas dans des fichiers séparés (il y a d'ailleurs
`0` fichier `.nsbtx` dans cette ROM).

> **Pourquoi c'est une excellente nouvelle :** si les textures avaient été
> séparées, il aurait fallu les associer manuellement à chaque modèle.
> Ici, tout est emballé ensemble. La conversion est directe.

#### Le chaînon manquant : apicula

Blender **ne sait pas lire** le `.nsbmd`. Ce format est propriétaire à
Nintendo. Il faut un convertisseur intermédiaire.

**L'outil de référence : [apicula](https://github.com/scurest/apicula)**
(licence MIT, écrit en Rust). Il lit les formats Nitro et écrit du
**glTF** — un format 3D standard, ouvert, que Blender importe nativement.

```
   .nsbmd  ──[ apicula ]──►  .gltf + .bin + .png  ──[ Blender ]──►  éditable
   (Nintendo)                 (standard ouvert)
```

**Installation (compilation depuis les sources) :**

```bash
git clone --depth 1 https://github.com/scurest/apicula.git
cd apicula
cargo build --release
cp target/release/apicula ~/.local/bin/
```

> **Note :** `apicula` n'est **pas** sur `crates.io` ni dans les dépôts
> Ubuntu, et pas sur `pip`. Il faut le compiler. Cela prend ~45 secondes
> avec Rust, et aucune dépendance système n'est requise.

#### La conversion

```bash
# Un modèle seul
apicula convert data/m148.nsbmd -o out/models/m148 --format gltf

# Un modèle AVEC ses animations squelettiques
apicula convert dossier_avec_modele_et_nsbca/ -o sortie --all-animations --format gltf
```

**Deux pièges d'apicula, tous deux rencontrés :**

1. **Le dossier de sortie ne doit pas préexister.** Sinon :
   `output directory already exists, choose a different one or pass
   --overwrite`. Curieux, mais c'est ainsi : il faut le laisser créer le
   dossier.
2. **Les animations doivent être regroupées avec le modèle** dans un même
   dossier d'entrée. Passer `m060.nsbmd` seul donne `0 animations` ;
   passer un dossier contenant `m060.nsbmd` + `m060_*.nsbca` donne
   `6 animations`.

#### Résultat obtenu

| Élément | Quantité |
|---|---|
| Modèles convertis en glTF | **411** |
| Modèles avec animations squelettiques | **226** |
| Fichiers glTF valides | **640 / 640** |
| Textures PNG extraites | **1 270** |
| Taille totale | 50 Mo |

#### Ce que vous obtenez dans Blender

Vérifié par import réel dans Blender 5.0.1 :

```
  m148        652 sommets   450 faces   7 matériaux   2 textures
  m248        465 sommets   351 faces   1 matériau    1 texture
  o_mirror001 686 sommets   440 faces   4 matériaux   1 texture
  n004        842 sommets   572 faces   4 matériaux   2 textures
  m060        6 animations, 1 armature, 2 maillages
  cool       33 animations, 1 armature, 2 maillages
```

**Les modèles arrivent complets** : géométrie, matériaux, textures
appliquées, et — pour les modèles animés — le **squelette** et les
**animations** utilisables dans la timeline de Blender.

#### Le workflow complet, pas à pas

```bash
# 1. Convertir tous les modèles (statique)
cd ~/Documents/ReverseEngeneering
for f in $(find work/extracted/data -iname '*.nsbmd'); do
    n=$(basename "$f" .nsbmd)
    apicula convert "$f" -o "out/models/$n" --format gltf
done
# -> 411 modèles

# 2. Convertir les modèles animés (regrouper modèle + animations)
for m in $(ls work/extracted/data/*.nsbmd | sed 's|.*/||;s/\.nsbmd$//'); do
    rm -rf /tmp/grp && mkdir -p /tmp/grp
    cp "work/extracted/data/$m.nsbmd" /tmp/grp/
    cp work/extracted/data/${m}_*.nsbca /tmp/grp/ 2>/dev/null
    [ -n "$(ls /tmp/grp/*.nsbca 2>/dev/null)" ] || continue
    apicula convert /tmp/grp -o "out/models_anim/$m" --all-animations --format gltf
done
# -> 226 modèles animés
```

**Ou en un clic** depuis le tiroir GNOME : **« Convertir les modèles 3D »**
(`re-models`), puis ouvrir Blender et faire
`Fichier → Importer → glTF 2.0`.

#### Ouvrir dans Blender

**Méthode recommandée — le script `re-blender` (fait tout automatiquement) :**

```bash
re-blender m148         # ouvre le monstre 148, textures et animation prêtes
re-blender cool         # le modèle à 33 animations
re-blender --liste      # voir tous les modèles disponibles
```

Il applique les textures, supprime la sphère parasite, cadre la vue sur le
modèle et **active la première animation** (lecture avec `ESPACE`).

**Méthode manuelle :**

```
  1. Lancer Blender
  2. Fichier → Importer → glTF 2.0 (.glb/.gltf)
  3. Naviguer vers  out/models_anim/m148/m148.gltf
  4. Passer le viewport en « Material Preview » (ou « Rendered »)
  5. Pour l'animation : éditeur « Dope Sheet » → choisir une action,
     puis l'assigner à l'armature
  6. Vue → Aligner la vue → Vue caméra, puis rendre (F12)
```

> **Astuce :** un modèle isolé (sans décor) paraît minuscule à l'ouverture.
> Appuyez sur `.` (point) du pavé numérique après l'avoir sélectionné :
> Blender cadre la vue sur l'objet.

#### « J'ai la carcasse 3D mais pas la texture ni l'animation »

**C'est le problème le plus courant, et il a trois causes distinctes.**

**Cause 1 — les textures sont des fichiers SÉPARÉS.**

Un `.gltf` n'est **pas** un fichier autonome. C'est un **plan** qui décrit
où trouver le reste :

```
   m148.gltf   le plan      « le maillage est dans le .bin,
                             la texture 1 est dans m148_1.png »
   m148.bin    la géométrie
   m148_1.png  la texture 1
   m148_2.png  la texture 2
```

*(À l'inverse, un `.glb` est un fichier unique qui embarque tout. C'est
d'ailleurs pour cela que `.glb` est préférable pour transporter un
modèle.)*

**Si les PNG sont absents**, Blender ne signale **pas** d'erreur : il crée
des images vides de taille `0×0` et affiche un maillage **gris uni**. Le
symptôme est exactement « j'ai la forme, mais pas la couleur ».

**Comment le vérifier :**

```bash
ls ~/Documents/ReverseEngeneering/out/models_anim/m148/
# doit montrer : m148.gltf  m148.bin  m148_1.png  m148_2.png
```

Ou dans Blender : `Fenêtre → Images` — une texture à `0×0` est vide.

**Cause 2 — la sphère par défaut de Blender masque le modèle.**

Si vous utilisez un Blender qui démarre avec la scène par défaut, elle
contient un cube ou une icosphere de **2 mètres**. Le modèle du monstre
mesure 16 à 22 mètres : la sphère se retrouve **au centre du monstre** et
brouille complètement la lecture.

**Comment le repérer :** l'objet s'appelle `Icosphere`, fait **42 sommets
et 80 faces**, et n'a **aucun matériau**. C'est la sphère de Blender, pas
un élément du modèle.

**Cause 3 — l'animation n'est pas assignée.**

Les animations **sont** importées (vérifiable dans l'éditeur *Dope Sheet*),
mais elles restent des *actions* non liées à l'armature. Tant qu'aucune
action n'est assignée, appuyer sur Lecture ne montre **rien** — le modèle
reste figé.

**La solution : le script `re-blender`**

```bash
re-blender m148
```

Il corrige les trois causes d'un coup :

| Action | Ce qu'il fait |
|---|---|
| **Textures** | Recharge chaque PNG depuis le disque, **le copie à côté du modèle** et l'**embarque** (`pack`) — le modèle devient autonome |
| **Nettoyage** | Supprime l'`Icosphere` parasite |
| **Viewport** | Force le mode d'affichage `TEXTURE` |
| **Animation** | Assigne la première action à l'armature et règle la plage de frames |
| **Cadrage** | Place une caméra et un éclairage adaptés à la taille du modèle |

**Sortie typique :**

```
=== Textures ===
  rechargee : m148_1.png <- m148_1.png
  rechargee : m148_2.png <- m148_2.png
  m148_1.png            128x128  OK
  m148_2.png             64x64   OK

=== Materiaux : 7 (0 sans texture valide) ===
=== Animations : 6 ===
  Animation active : m148_00 (0 a 9)
  Appuyez sur ESPACE pour la lire.

=== Modele charge ===
  610 sommets, 370 faces
```

La ligne **`0 sans texture valide`** est le contrôle à surveiller : si ce
nombre n'est pas zéro, une texture manque.

> **Vérification objective utilisée :** l'animation est-elle réelle ?
> On mesure la position d'un os non-racine à plusieurs frames.
> Pour `m148` : `y = 1.4932 → 1.4184 → 1.3780 → 1.4693`. Les os
> **bougent** — l'animation est fonctionnelle, pas juste présente.

#### Les animations : `.nsbca`

Les **1 261 fichiers `.nsbca`** (Nintendo DS Bone Animation) sont les
animations squelettiques. Elles sont nommées par convention :

```
  m060.nsbmd      le modèle du monstre n°60
  m060_00.nsbca   son animation n°00   (idle)
  m060_01.nsbca   son animation n°01   (attaque)
  m060_02.nsbca   ... etc
```

**261 modèles distincts ont des animations.** Le monstre `cool` en a 33,
ce qui suggère un personnage important (probablement un boss ou un
monstre emblématique).

**Autres formats 3D présents :**

| Format | Nombre | Nature |
|---|---|---|
| `.nsbca` | 1 261 | **Animations squelettiques** |
| `.nsbma` | 25 | Animations de matériaux (couleurs, transparence) |
| `.nsbta` | 5 | Animations de textures (UV) |

#### Et les « scènes » ?

Il n'y a pas de fichier « scène 3D » au sens de Blender — c'est-à-dire un
`.blend` avec des objets positionnés et éclairés. **La scène est
construite par le code au moment de l'exécution** :

```
  Les .map (90 fichiers)  →  la disposition des tuiles du terrain
  Les .evt (80 fichiers)  →  les scripts qui placent objets et PNJ
  Le code ARM9            →  l'assemblage en temps réel
```

**Conséquence :** pour reconstituer une scène complète, il faut soit
l'assembler à la main dans Blender (en plaçant les modèles selon les
`.map`), soit observer l'émulateur pour voir la composition voulue par le
jeu. Le modèle individuel est disponible ; la scène, elle, est un
**résultat du code**, pas une donnée.

### 10.7 Bilan des ressources extraites

| Ressource | Quantité | Validation |
|---|---|---|
| Code | 7 140 fonctions, 279 930 lignes | 0 `halt_baddata` |
| Images 2D | 40 PNG en 256×192 | écart voisins 45/765 |
| Audio jouable | **603 WAV** (199 STRM + 404 échantillons SWAR) | 0 % saturation |
| Modèles 3D | **640 glTF** (411 statiques + 229 animés) | 640/640 valides |
| Textures 3D | 1 270 PNG | importées avec les modèles |
| Partitions | 133 SSEQ + 31 SBNK | via vgmstream |
| Noms de sons | 562 symboles + 517 `#define` | lus depuis la ROM |

---

## 11. Peut-on exécuter le jeu sur une machine ARM ?

**Question posée :** « comment lancer le jeu compilé sur une machine type
ARM capable de la lire pour voir le code en action ? »

### 11.1 La réponse courte

**Ce n'est pas possible sur une machine ARM ordinaire, et ce n'est pas une
question de puissance.** C'est une question de **matériel spécifique**.

L'ARM9 du jeu n'est pas « du code ARM » au sens d'un programme Linux.
C'est un **micrologiciel qui pilote du matériel**. Il accède directement à
des registres mémoire qui **n'existent que dans la Nintendo DS**.

**Preuve mesurée dans votre ROM** — j'ai analysé les constantes chargées
par le code et trouvé **12 bancs de registres matériels** :

```
0x04000000   moteur 2D (fonds, sprites, palettes, scroll)
0x04100000   moteur 3D (géométrie, matrices, projection)
0x04200000   (registre DS)
0x04300000   (registre DS)
0x04400000   DMA (transferts mémoire automatiques)
0x04700000   (registre DS)
0x04800000   son (canaux, mélangeur, volume)
0x04A00000   (registre DS)
0x04C00000   (registre DS)
0x05000000   palette VRAM
```

Sur un Raspberry Pi, **écrire à `0x04000000` provoque un défaut de
segmentation** : cette plage est réservée au noyau. Le code n'a aucun moyen
de savoir où il tourne — il n'y a pas de couche d'abstraction.

Et ce n'est pas tout : le jeu est **deux processeurs synchronisés**.
L'ARM9 et l'ARM7 communiquent par des registres partagés et des
interruptions croisées (l'ARM7 gère l'audio et le Wi-Fi *pour* l'ARM9). Un
seul cœur ARM ne peut pas reproduire ça.

> **Le principe général à retenir :**
> « Exécuter du code ARM » n'a de sens que si **l'environnement attendu par
> ce code existe**. Un binaire de console n'est pas un programme autonome —
> c'est **la moitié d'un système**.

### 11.2 Ce qu'on peut faire, par ordre de réalisme

#### Option 1 — L'émulateur (recommandé)

C'est **la vraie réponse** à « voir le code en action ». Un émulateur
reproduit le matériel DS en logiciel : il intercepte chaque accès à
`0x04000000` et fait ce que la console ferait.

```bash
desmume-cli "2109 - Dragon Quest Monsters - Joker (E)(EXiMiUS).nds"
```

DeSmuME est installé et fonctionnel. Mais surtout, il offre ce qui vous
intéresse vraiment — **observer le code s'exécuter** :

| Fonction DeSmuME | Ce qu'elle montre |
|---|---|
| **Debugger → Disassembler** | Le code ARM9 désassemblé **en direct**, avec le point d'exécution courant |
| **View → Registers** | L'état des 16 registres ARM + le CPSR |
| **View → Memory** | La RAM à l'adresse voulue |
| **Tools → Cheats** | Modifier une valeur mémoire à la volée |
| **Trace log** | L'historique des instructions exécutées |

**La manipulation la plus instructive :**

```
1. Ouvrir le Debugger → Disassembler
2. Aller à l'adresse 0x02000800   ← le point d'entrée qu'on a identifié
3. Poser un point d'arrêt (breakpoint)
4. Lancer le jeu
5. Observer le démarrage instruction par instruction
6. Comparer avec FUN_02000950 dans work/decompiled/arm9.c
```

> **C'est le pont entre le code STATIQUE (votre `arm9.c`) et le code
> VIVANT.** Le rétro-ingénieur utilise l'émulateur comme un microscope,
> pas comme une console de jeu.

**Note :** DeSmuME installé via apt ne fournit que `desmume-cli` (version
console). Pour le débogueur graphique complet, il faut la version GUI
(binaire officiel DeSmuME ou melonDS, qui a un excellent débogueur).

#### Option 2 — Un vrai matériel DS

Le jeu tourne sur une **vraie Nintendo DS** avec un linker (R4, Acekard…).
C'est du matériel ARM — un ARM946E-S et un ARM7TDMI — et le jeu y tourne
parfaitement. Mais :

- Ce n'est pas « une machine ARM capable de la lire » au sens générique :
  c'est ***la*** machine pour laquelle il a été compilé.
- Pour observer le code, il faut un linker avec fonction de débogage, ou
  une DS modifiée avec un port série.

#### Option 3 — Le portage (le plus ambitieux)

On **réécrit** le jeu pour une autre machine en réutilisant ce qu'on a
extrait : les assets (déjà convertis en PNG/WAV par nos outils) et la
logique comprise grâce au décompilé.

C'est ce que font les projets de « port » de jeux DS sur PC. C'est un
travail de plusieurs années-personnes : **7 140 fonctions** à comprendre et
réimplémenter. Le décompilé que vous avez est exactement le point de départ
de ce travail.

### 11.3 Et si on voulait vraiment exécuter l'ARM9 sur un ARM ?

Techniquement concevable, mais il faudrait réimplémenter **toute la
console** :

```
  Ce que le jeu attend                 Ce qu'il faudrait fournir
  ──────────────────────────────       ─────────────────────────────────
  Mémoire à 0x02000000 (4 Mo)    ->    mmap() d'une zone fixe
  Registres 2D/3D à 0x04000000   ->    un émulateur de GPU DS complet
  Contrôleur DMA                 ->    un émulateur de DMA
  Matériel son                   ->    un émulateur audio
  ARM7 partenaire (synchro)      ->    un second cœur + IPC
  BIOS et appels SWI             ->    une réimplémentation du BIOS
  Cartouche (lecture des .bin)   ->    un filesystem virtuel
  Écrans, tactile, boutons       ->    une couche d'entrée/sortie
```

**À ce stade, vous avez écrit un émulateur.** Autant utiliser DeSmuME, qui a
demandé 20 ans de travail à une communauté.

---

## 12. Le tiroir GNOME « Reverse Engineering »

### 12.1 Objectif

Créer un **tiroir d'applications** dans le menu GNOME regroupant tous les
outils de rétro-ingénierie, pour les lancer sans passer par le terminal.

### 12.2 Comment GNOME organise les tiroirs

GNOME Shell 50 ne stocke **pas** les tiroirs dans des fichiers `.desktop`.
Il utilise **dconf** (la base de configuration GNOME), via le schéma
`org.gnome.desktop.app-folders`.

```
Trois clés dconf à manipuler :

1. org.gnome.desktop.app-folders
       folder-children = ['ai', 'dev', ..., 'reverse']
       ↑ la LISTE des tiroirs existants

2. org.gnome.desktop.app-folders.folder:/org/gnome/desktop/app-folders/folders/reverse/
       name = 'Reverse Engineering'
       apps = ['re-extract-nds.desktop', 'ghidra.desktop', ...]
       ↑ la CONFIGURATION du tiroir « reverse »

3. Les fichiers .desktop eux-mêmes
       ~/.local/share/applications/*.desktop
       ↑ définissent chaque application
```

**Commandes utilisées :**

```bash
# Ajouter « reverse » à la liste des tiroirs
gsettings set org.gnome.desktop.app-folders folder-children \
  "['ai', 'dev', 'internet', 'office', 'games', 'multimedia', 'system', 'store', 'kdeconnect', 'reverse']"

# Nommer le tiroir
S="org.gnome.desktop.app-folders.folder:/org/gnome/desktop/app-folders/folders/reverse/"
gsettings set $S name 'Reverse Engineering'

# Y placer les applications
gsettings set $S apps "['ghidra.desktop', 're-console.desktop', ...]"
```

### 12.3 Le piège des catégories .desktop

**Erreur rencontrée :** j'avais mis `Categories=Development;Reverse;` dans
les fichiers `.desktop`. `desktop-file-validate` a refusé :

```
error: value "Development;Reverse;" for key "Categories" contains an
unregistered value "Reverse"; values extending the format should start
with "X-"
```

**Explication :** la spécification freedesktop.org définit une liste
**fermée** de catégories (`Development`, `Game`, `Utility`…). Une catégorie
personnalisée **doit** être préfixée `X-` :

```
[ ] Categories=Development;Reverse;        → invalide
[x] Categories=Development;X-Reverse;      → valide
```

**Deuxième erreur, amusante :** un `sed` appliqué deux fois a produit
`X-X-Reverse`. **Leçon :** toujours **vérifier le résultat** d'une
substitution en masse (`grep` après `sed`), jamais supposer.

### 12.4 Les lanceurs finaux

Le tiroir **« Reverse Engineering »** contient :

| Lanceur | Rôle | Script |
|---|---|---|
| **Extraire une ROM NDS** | En-tête, NitroFS, ARM9/ARM7/overlays, assets | `re-extract-nds` |
| **Analyse Ghidra (ROM)** | Import + auto-analyse dans Ghidra | `re-ghidra-analyze` |
| **Exporter le C (Ghidra)** | Décompilation headless → fichiers `.c` | `re-ghidra-decompile` |
| **radare2 (ARM)** | Console RE configurée pour ARM | `re-radare2` |
| **Console RE** | Terminal dans l'environnement RE | `re-console` |
| **Ghidra** | Interface graphique Ghidra | `ghidra.desktop` |
| **jadx-gui** | Décompilateur Java/Android | `jadx-gui.desktop` |
| **GHex** | Éditeur hexadécimal | `org.gnome.GHex.desktop` |

**Techniques utilisées :**

- **`zenity`** pour les sélecteurs de fichiers graphiques (`--file-selection`)
- **Icônes SVG personnalisées** dans `~/.local/share/icons/`
- **Environnement Python dédié** (`~/.local/share/reverse/venv`) pour
  isoler les dépendances (ndspy, capstone…)
- **Scripts dans `~/.local/bin/`** pour que `Exec=` reste simple

**Vérification faite :**

```bash
for d in *.desktop; do desktop-file-validate "$d"; done
# -> tous OK
```

---

## 13. Tous les outils du dossier

### 13.1 Scripts shell

| Outil | Rôle | Usage |
|---|---|---|
| `tools/nds-inspect.sh` | Découpe complète d'une ROM | `nds-inspect.sh jeu.nds` |
| `tools/nds-decompile.sh` | Décompilation ARM9+ARM7+overlays | `nds-decompile.sh jeu.nds` |
| `tools/decompile_all.sh` | Export C de tous les binaires d'un projet Ghidra | `decompile_all.sh [proj] [nom] [out]` |

### 13.2 Outils Python

| Outil | Rôle | Dépendance |
|---|---|---|
| `tools/nds_header.py` | Parseur d'en-tête NDS, pédagogique et commenté | — |
| `tools/nds_fs.py` | Explorateur NitroFS (FNT/FAT) → CSV | — |
| `tools/extract_code.py` | Extraction complète du code via la copy table | `ndspy` |
| `tools/xref_string.py` | Remonte d'une chaîne au code qui l'utilise | — |
| `tools/d16topng.py` | Images `.d16` → PNG | `Pillow` |
| `tools/sdatextract.py` | Archive `.sdat` → SSEQ/SBNK/SWAR/STRM | — |
| `tools/strmtowav.py` | Flux `.strm` → WAV (PCM8/PCM16/ADPCM) | — |
| `tools/swartowav.py` | Banque `.swar` → WAV (extrait chaque échantillon) | — |

### 13.3 Scripts Ghidra (Java)

| Script | Rôle |
|---|---|
| `ExportDecompiled.java` | Exporte tout le C décompilé (utilisé ici) |
| `ExportDecompiledThumb.java` | Variante forçant le mode Thumb |
| `DecompileAll.java` | Autre export complet, format différent |
| `DecompileAt.java` | Décompile **une** fonction à une adresse donnée |
| `NdsArmSetup.java` | Configure l'environnement ARM d'un projet NDS |

**`DecompileAt.java` est très utile pour l'exploration :**

```bash
analyzeHeadless <projDir> <proj> -process arm9.bin -noanalysis \
    -scriptPath tools/ghidra_scripts \
    -postScript DecompileAt.java 0x02041FD8
```

→ décompile uniquement la fonction qui charge `/sound_data.sdat` (trouvée
au §9.4). Idéal pour explorer sans réexporter 280 000 lignes.

### 13.4 Arborescence des résultats

```
ReverseEngeneering/
├── README.md                          ← ce document
├── EXTRACTION-RESSOURCES.md           ← guide ressources (images/sons)
├── 2109 - ....nds                     ← la ROM
├── tools/                             ← tous les outils
│   ├── *.sh, *.py
│   └── ghidra_scripts/*.java
├── work/
│   ├── extracted/                     ← ROM découpée (ndstool)
│   │   ├── arm9.bin, arm7.bin
│   │   ├── y9.bin
│   │   ├── overlay/
│   │   └── data/                      ← 3 845 fichiers, 117 Mo
│   ├── code/                          ← code découpé par sections (ndspy)
│   │   ├── arm9.bin, arm9_sec_*.bin
│   │   ├── arm7.bin, arm7_sec_*.bin
│   │   ├── overlay_*.bin
│   │   └── manifest.json              ← adresses de base + points d'entrée
│   ├── analysis/                      ← désassemblages bruts (.asm)
│   ├── decompiled/                    ← LE RÉSULTAT : 5 fichiers .c
│   └── fs_listing.csv                 ← inventaire NitroFS (3 849 lignes)
└── out/
    ├── png/                           ← 40 images converties
    ├── sound/                         ← SSEQ/SBNK/SWAR/STRM extraits
    └── wav/                           ← 199 pistes jouables
```

---

## 14. Les erreurs commises, et ce qu'elles enseignent

Cette section est peut-être la plus utile. **Toutes ces erreurs ont été
commises pendant la session**, et chacune a une leçon générale.

### 14.1 Les erreurs techniques

| # | Erreur | Cause | Leçon |
|---|---|---|---|
| 1 | `Cannot open file '../...nds'` | Mauvais nombre de `../` depuis le sous-dossier | **Toujours vérifier la profondeur relative** avant de lancer un outil |
| 2 | Confusion BLZ / motif ARM | `FF DE FF E7` ressemble à une signature | **Désassembler pour trancher**, pas deviner |
| 3 | 558 × « bad instruction » | Langage Ghidra sans `t` | **Un seul caractère = 68 fonctions perdues** (§8) |
| 4 | `X-X-Reverse` dans les .desktop | `sed` appliqué deux fois | **Vérifier après substitution en masse** |
| 5 | « 1 145 849 439 entrées FAT » | Lecture de texte ASCII comme entiers | **Un décompte absurde = erreur de parsing** |
| 6 | `Directory not found` (Ghidra) | Dossier projet non créé avant | Créer le dossier **avant** de lancer |
| 7 | `ndspy` manquant | Dépendance non installée | **Tester chaque outil**, ne pas supposer |
| 8 | `disassemble()` mauvaise signature | API Ghidra mal devinée | **Consulter l'API** (`javap`), pas deviner |
| 9 | Registre `TMode` introuvable | N'existe pas dans Ghidra 12 | Ghidra gère Thumb **par langage**, pas par registre |

### 14.2 Les trois leçons majeures

#### Leçon 1 — L'échec silencieux est le pire ennemi

L'erreur n°3 est de loin la plus dangereuse. Ghidra **n'a pas signalé
d'erreur** : il a produit un fichier plausible, complet en apparence. Il
manquait 68 fonctions.

> **Règle :** toujours **compter** quelque chose d'objectif.
> `grep -c halt_baddata` doit valoir **0**. Pas « ça a l'air bon ».

#### Leçon 2 — Valider par la mesure, pas par l'impression

Appliquée à chaque étape :

| Étape | Mesure objective |
|---|---|
| ROM saine ? | CRC tous `OK` |
| Code décompressé ? | Prologue de démarrage cohérent |
| Décompilation correcte ? | 0 `halt_baddata` |
| Image correcte ? | écart voisins 45/765 (bruit = 400) |
| Audio réel ? | RMS 6409, dynamique pleine |

**Aucune de ces validations n'est visuelle.** Ce sont des **nombres** qui
prouvent le résultat.

#### Leçon 3 — S'appuyer sur les données, pas sur les hypothèses

Pour le SDAT, quatre tentatives de deviner l'encodage des tables ont
échoué. La solution a été de **prendre les données comme source de
vérité** : chercher les signatures `SSEQ`/`SBNK`/`STRM` directement dans
les blocs FAT, plutôt que de suivre une table dont l'encodage était
propriétaire.

> **Règle :** quand un format résiste, **inverser l'approche** — partir des
> données reconnaissables et remonter, au lieu de suivre la structure
> déclarée.

### 14.3 Ce qu'on n'a PAS pu faire

**Honnêteté sur les limites :**

| Objectif | Statut | Raison |
|---|---|---|
| Obtenir le source `.c` original | **Impossible** | Détruit à la compilation. Aucun outil ne le récupérera. |
| Noms de fonctions d'origine | **Impossible** | Idem. `FUN_02012345` restera. |
| Jouer les 133 SSEQ | **Non fait** | `vgmstream` absent des dépôts Ubuntu, à compiler. |
| Exécuter sur ARM générique | **Impossible** | Nécessite un émulateur complet (§11). |
| Convertir les `.nsbmd` (3D) | **Non fait** | Nécessite `apicula` (Rust). |

---

## 15. La bibliothèque ModelBlender

### Le problème

Convertir un modèle en glTF ne suffit pas à le rendre **utilisable**. Un
`.gltf` est un **plan de montage**, pas un colis :

```
m148.gltf   →  « le maillage est dans m148.bin,
                la texture est dans m148_1.png »
m148.bin
m148_1.png
m148_2.png
```

Déplacez le `.gltf` seul et Blender affiche un maillage **gris**, avec une
image de taille `0x0`. C'est exactement le symptôme « je n'ai que la
carcasse ».

Et même avec tous les fichiers, il reste à faire à la main :

- assigner une animation (Blender n'en garde qu'une active)
- masquer les os, qui s'affichent en **formes pleines par-dessus** le
  modèle et le cachent entièrement
- passer le viewport en mode texture

### La solution : 411 fichiers `.blend` autonomes

Le dossier `ModelBlender/` contient **les 411 modèles du jeu**, chacun
converti en un fichier Blender **autonome** :

```
ModelBlender/
├── modeles_animes/        232 modèles avec squelette et animations
│   └── m148/
│       └── m148.blend     ← un seul fichier, rien d'autre à fournir
├── modeles_statiques/     179 modèles sans animation
│   └── bd001/
│       └── bd001.blend
├── apercus/               411 vignettes PNG
│   └── m148.png
├── CATALOGUE.md           index complet, classé par famille
└── ouvrir.sh              lanceur
```

Un `.blend` contient **tout** : le maillage, les **textures embarquées**
(*packed*), l'armature et les animations. Un seul fichier à copier,
ouvrir ou archiver.

### Ce qui est corrigé automatiquement

| Problème | Correction |
|---|---|
| Textures externes manquantes | **Embarquées** dans le fichier (*pack*) |
| Chemin vers un dossier temporaire disparu | Chemin vidé : plus aucun avertissement |
| Os dessinés en formes pleines masquant le modèle | Passés en **`STICK`** (traits fins) |
| Os dessinés **par-dessus** le maillage | `show_in_front = False` |
| Une seule animation conservée | **Toutes** rangées dans des pistes **NLA** |
| Pas de caméra ni d'éclairage | Ajoutés, cadrés sur la taille du modèle |
| Viewport en maillage gris | Mode **texture**, overlays désactivés |

### Comment s'en servir

```bash
cd ModelBlender
./ouvrir.sh m148            # ouvre le monstre 148
./ouvrir.sh --liste         # liste tout
./ouvrir.sh --liste m       # liste seulement les monstres
./ouvrir.sh --planche       # ouvre le dossier des 411 aperçus
./ouvrir.sh --apercu m148   # montre une vignette sans ouvrir Blender
```

Ou simplement **double-cliquer** sur un `.blend`.

Dans Blender :

| Action | Comment |
|---|---|
| Lire l'animation | `ESPACE` |
| Changer d'animation | **Dope Sheet** → mode **Action Editor** → menu près du nom de l'armature |
| Voir toutes les animations | **NLA Editor** (bandes posées bout à bout) |
| Rendre une image | `F12` (caméra et lumières déjà en place) |

### Les familles de modèles

Le préfixe du nom donne la famille — c'est une **observation** déduite de
l'inventaire, pas une documentation officielle :

| Préfixe | Famille | Nombre |
|---|---|---|
| `m` | Monstres (`m000` → `m248`, ordre de `ModelTbl.bin`) | 211 |
| `o` | Objets et décors (interrupteurs, miroirs, panneaux) | 88 |
| `bf` | Décors de combat (*Battle Field*) | 50 |
| `bd` | Bâtiments | 29 |
| `n` | Personnages | 16 |
| autres | Divers (`WF`, `bh`, `Z_`, `be`, `l`) | 17 |

### Deux pièges rencontrés

**Apicula refuse de créer son dossier de sortie.** Il exige que le dossier
**parent** existe déjà, sinon il échoue avec :

```
[ERROR] No such file or directory (os error 2)
```

Les 411 conversions ont échoué d'un coup pour cette seule raison. Quand
*beaucoup* d'éléments échouent simultanément, cherchez **une** cause
systémique, pas 411 causes séparées.

**Apicula plante sur les modèles très animés.** Au-delà d'une vingtaine
d'animations liées d'un coup, il panique :

```
thread 'main' panicked at src/convert/gltf/mod.rs:525:44:
index out of bounds
```

Quatre modèles étaient concernés. La parade : convertir avec un **nombre
limité** d'animations à la fois, en réduisant le lot jusqu'à ce que ça
passe (`cool`, avec 34 animations, n'a accepté que 24).

### Les objets plats

Beaucoup d'objets sont des **panneaux presque 2D** : les panneaux
indicateurs mesurent `52 × 51 × 1.2` unités, et `l000` n'est qu'un **plan
à 4 sommets** de `24 × 0 × 12` portant un logo.

Vus de trois quarts, ces objets sont vus **par la tranche** et
paraissent vides. Le générateur d'aperçus photographie donc les objets
plats **de face**.

Le seuil de détection doit rester **strict** (rapport épaisseur/largeur
inférieur à `0.05`), sans quoi on classe « plat » des objets simplement
allongés : `o_gagoil` mesure `28.8 × 93.5 × 11.0`, soit un rapport de
`0.118`. Avec un seuil de `0.12`, il était pris pour un panneau et
photographié **de dessus** — d'où un aperçu quasi vide.

### Les objets invisibles à la caméra

27 aperçus restent pauvres, et **ce n'est pas un défaut de conversion**.
Ces objets portent un matériau monté ainsi :

```
Light Path.Is Camera Ray  →  Mix Shader.Factor
    si rayon caméra  :  Transparent BSDF    ← donc INVISIBLE au rendu
    sinon            :  Emission
```

C'est le montage classique d'un objet que le jeu ne veut **pas** montrer
directement : source de lumière, volume de collision, déclencheur. Leur
texture a d'ailleurs un canal alpha **entièrement à zéro** — vérifié sur
`o_guideB3` : `alpha min = 0.00, max = 0.00`.

Les concernés sont les `o_guide*` (repères lumineux), `o_daiLight`
(source de lumière piégée) et quelques voisins. Dans le jeu, ils
éclairent ou déclenchent sans jamais être vus.

Pour l'aperçu, le script les rend malgré tout visibles — en repliant la
couleur par l'alpha — sinon on croirait à un échec de conversion.

### Résultat des aperçus

| Mesure | Valeur |
|---|---|
| Aperçus générés | **411 / 411** |
| Modèle nettement visible | **384 (93 %)** |
| Couleurs médianes | ~12 700 |
| Restants pauvres | 27 (objets invisibles ou très fins) |

### La leçon sur la mémoire

Le premier lancement utilisait **8 instances de Blender en parallèle** sur
une machine de 14 Go. Résultat : **13 Go utilisés sur 14**, plus rien de
disponible, et un système au bord du blocage.

Chaque instance de Blender consomme 400 Mo à 1,2 Go : le moteur de rendu
charge la scène entière. La parade n'est pas seulement de réduire le
nombre, c'est de **traiter par vagues** : lancer N rendus, attendre que
**tous** soient terminés, puis continuer. La mémoire est ainsi rendue
entre chaque vague, au lieu de s'accumuler.

Après correction, avec 2 instances : **8 Go disponibles** en permanence,
411 aperçus générés sans incident.

Le script comporte désormais un garde-fou qui **refuse** de dépasser 3
instances sur une machine de moins de 24 Go, et un `trap` qui tue tous
les Blender lancés si on l'interrompt.

---

## 16. Cadre légal

Ce travail relève de la **préservation, de l'étude et de
l'interopérabilité**, trois activités explicitement protégées par :

- **Droit européen** : directive 2009/24/CE, articles 5 et 6
  (observation, étude, décompilation pour interopérabilité)
- **Droit français** : Code de la propriété intellectuelle, article
  L.122-6-1

### Ce qui est légal

- Analyser une ROM qu'on possède, pour comprendre comment elle marche
- Étudier les formats, produire de la documentation
- Modifier sa propre copie à des fins personnelles
- Écrire des outils d'extraction et de conversion

### Ce qui ne l'est pas

- **Distribuer la ROM** ou le code décompilé (œuvre protégée)
- **Publier les assets** (musiques, modèles, textes) de Square Enix
- Vendre quoi que ce soit issu de ce travail
- Contourner des mesures techniques de protection

> **Règle simple : on peut tout analyser, on ne peut rien redistribuer.**
>
> Ce dossier est un espace d'étude personnel — gardez-le ainsi.

---

## 17. Aide-mémoire

### 17.1 Le pipeline complet, de la ROM au code

```bash
cd ~/Documents/ReverseEngeneering
ROM="2109 - Dragon Quest Monsters - Joker (E)(EXiMiUS).nds"

# 1. Vérifier la ROM
ndstool -i "$ROM"

# 2. Découper
tools/nds-inspect.sh "$ROM"

# 3. Inventorier le système de fichiers
python3 tools/nds_fs.py "$ROM" > work/fs_listing.csv

# 4. Extraire le code proprement (par sections)
python3 tools/extract_code.py "$ROM" work/code

# 5. Décompiler tout
tools/nds-decompile.sh "$ROM"

# 6. Extraire les ressources
python3 tools/d16topng.py --all work/extracted/data out/png
python3 tools/sdatextract.py work/extracted/data/sound_data.sdat out/sound
python3 tools/strmtowav.py --all out/sound/STRM out/wav
python3 tools/swartowav.py --all out/sound/SWAR out/wav_swar

# 7. Convertir les modeles 3D pour Blender
~/.local/bin/re-models work/extracted/data out/models

# 8. Construire la bibliotheque ModelBlender (411 .blend autonomes)
python3 tools/build_blender_library.py        # ~40 min
python3 tools/fix_conversion_failures.py                 # les 4 modeles recalcitrants
python3 tools/create_catalog.py                # CATALOGUE.md
tools/generate_previews.sh 8                      # 411 vignettes
```

### 17.2 Commandes utiles au quotidien

```bash
# ── En-tête d'une ROM
ndstool -i jeu.nds

# ── Désassembler un module à la main
arm-none-eabi-objdump -D -b binary -m armv5te -EL arm9.bin > arm9.asm

# ── Désassembler autour d'une adresse (avec les bonnes adresses)
arm-none-eabi-objdump -D -b binary -m armv5te -EL \
    --adjust-vma=0x02000000 --start-address=0x02041FB0 --stop-address=0x02042004 \
    work/code/arm9.bin

# ── radare2 sur l'ARM9
r2 -a arm -b 32 -m 0x02000000 work/code/arm9.bin

# ── Remonter d'une chaîne à son code
python3 tools/xref_string.py work/code/arm9.bin 0x02000000 "SAVE"

# ── Décompiler UNE fonction précise
analyzeHeadless ~/proj DQMJoker -process arm9.bin -noanalysis \
    -scriptPath tools/ghidra_scripts -postScript DecompileAt.java 0x02041FD8

# ── Chercher des chaînes
strings -n 6 work/code/arm9.bin | grep -i save

# ── Compter les erreurs de décompilation
grep -c halt_baddata work/decompiled/arm9.c    # DOIT être 0

# ── Ghidra graphique
ghidraRun

# ── Lancer le jeu (débogage)
desmume-cli "$ROM"
```

### 17.3 Correspondance des adresses ARM9

```
adresse RAM  →  offset fichier
0x02000000   →  0x000000     début du code
0x02000800   →  0x000800     point d'entrée réel (après Secure Area)
0x020777FC   →  0x0777FC     la chaîne "/sound_data.sdat"
0x0207        →  fin du code
```

### 17.4 Les adresses de chargement (pour Ghidra)

| Module | Adresse de base | Langage |
|---|---|---|
| `arm9.bin` | `0x02000000` | `ARM:LE:32:v5t` |
| `arm9_sec_01FF8000.bin` | `0x01FF8000` | `ARM:LE:32:v5t` |
| `arm9_sec_027E0000.bin` | `0x027E0000` | `ARM:LE:32:v5t` |
| `arm7.bin` | `0x02380000` | `ARM:LE:32:v4t` |
| `arm7_sec_037F8000.bin` | `0x037F8000` | `ARM:LE:32:v4t` |
| `arm7_sec_027E0000.bin` | `0x027E0000` | `ARM:LE:32:v4t` |
| `overlay_00/01/02.bin` | `0x02184B40` | `ARM:LE:32:v5t` |

> **[Attention]️ N'oubliez jamais le `t` final** — c'est la leçon du §8.

### 17.5 Format `.d16` (images)

```
0x00  4   "D16\0"
0x04  2   largeur
0x06  2   hauteur
0x08  ... pixels BGR555 (16 bits : 5 bleu, 5 vert, 5 rouge)

Conversion 5→8 bits :  v8 = (v5 << 3) | (v5 >> 2)
```

### 17.6 Format `.sdat` (sons)

```
0x00  4   "SDAT"
0x10  4   offset du bloc SYMB   (variante avec paires)
0x18  4   offset du bloc INFO
0x20  4   offset du bloc FAT
0x28  4   offset du bloc FILE

Bloc INFO → 5 sous-blocs : SSEQ, SBNK, SWAR, STRM, SARC
Bloc FAT  → magic(4) + taille(4) + nb_entrees(4) + entrees(16 o chacune)
```

**Types d'objets :**
- **SSEQ** = partition (MIDI) — **ne sonne pas seule**
- **SBNK** = banque d'instruments
- **SWAR** = échantillons audio
- **STRM** = audio encodé — **directement jouable**

### 17.7 Format `.strm` (audio)

```
0x18  1   codec     (0=PCM8, 1=PCM16, 2=ADPCM)
0x19  1   bouclage
0x1C  2   fréquence
0x24  4   numSamples
0x50  4   "DATA"
```

### 17.8 Où continuer

| Piste | Outil / ressource |
|---|---|
| Explorer l'ARM9 visuellement | Ghidra (`ghidraRun`) |
| Traiter les 3 845 fichiers `data/` | [Tinke](https://github.com/pleonex/tinke), [ndspy](https://github.com/RubenTheCoder/ndspy) |
| Modèles 3D `.nsbmd` | [apicula](https://github.com/pleonex/apicula) |
| Jouer les SSEQ | [vgmstream](https://github.com/vgmstream/vgmstream) |
| Documentation matériel DS | [GBATEK](https://problemkaputt.de/gbatek.htm) |
| Débogage pas à pas | DeSmuME GUI, [melonDS](https://melonds.kuribo64.net/) |

### 17.9 Ce qu'il reste à faire, par ordre de difficulté

1. **Nommer les fonctions du SDK** — les adresses `0x02000000`–`0x02080000`
   contiennent le Nitro SDK. Le reconnaître permet de renommer des
   centaines de fonctions d'un coup.
2. **Suivre les appels depuis `0x02000800`** pour reconstruire la boucle
   principale du jeu.
3. **Exploiter les chaînes** comme points d'ancrage (§9.4) : `"SAVE"` →
   sauvegarde, `"item"` → système d'objets.
4. **Croiser avec les tables de `data/`** : retrouver la fonction qui ouvre
   `ItemTbl.bin` donne accès à toute la structure du jeu.
5. **Documenter les formats restants** : `.enct`, `.efc`, `.map`, `.evt`.

---

### Résumé final

| Question | Réponse |
|---|---|
| Peut-on récupérer le code d'une ROM ? | **Oui** — 7 140 fonctions, 279 930 lignes de C |
| Le source original ? | **Non, jamais.** Détruit à la compilation. |
| Les assets (images, sons) ? | **Oui** — 40 PNG, 199 WAV, 133 partitions |
| Peut-on l'exécuter sur ARM ? | **Non** sur ARM générique. **Oui** via émulateur. |
| Combien de temps ? | Une session, avec les bons outils |
| La difficulté principale ? | Le mode **Thumb** (§8) et les formats propriétaires |

**Le mot de la fin :** le reverse engineering, c'est **90 % de
méthodologie et 10 % de technique**. Observer avant d'agir, valider par la
mesure, ne jamais faire confiance à un résultat qui « a l'air de marcher ».
Les outils changent selon la cible ; la démarche reste la même.
