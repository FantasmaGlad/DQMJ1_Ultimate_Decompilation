# Extraction des ressources et exécution du jeu

Deux questions traitées ici :

1. **Comment obtenir les `.png`, `.mp3` etc. à partir des `.bin` ?**
2. **Comment « lancer » le jeu sur une machine ARM pour voir le code en action ?**

---

# PARTIE 1 — Extraire les ressources

## 1.1 Pourquoi il n'y a ni `.png` ni `.mp3` dans la ROM

C'est le point de départ, et il faut le comprendre avant de chercher des outils.

Un `.png` est un format **de fichier** : une structure avec un en-tête, une
table de couleurs, des blocs `IDAT` compressés en zlib. Un `.mp3` idem, avec
ses trames MPEG. Ces formats ont été conçus pour **le stockage et l'échange
entre ordinateurs**.

La Nintendo DS ne lit **aucun** de ces deux formats :

| Ce que la DS a | Pourquoi |
|---|---|
| Pas de décodeur PNG | Elle a un décodeur de tuiles 2D et un moteur 3D qui lit des textures en BGR555 brut. Décoder du zlib en temps réel coûterait trop cher. |
| Pas de décodeur MP3 | Elle a un matériel audio qui lit du PCM et de l'ADPCM directement. Chaque échantillon doit être jouable instantanément. |
| Pas de GPU au sens PC | Son « GPU » est un ensemble de registres mémoire mappés (`0x04000000`+) qu'on pilote en écrivant des valeurs. |

Conséquence : **le jeu stocke ses ressources dans les formats natifs du
matériel**, pas dans des formats de fichier. Les `.nsbmd`, `.d16`, `.sdat`
ne sont pas des « archives à décompresser » comme un `.zip` : ce sont des
**structures mémoire sérialisées**, prêtes à être copiées en VRAM ou dans
le mélangeur audio.

Il n'existe donc pas de recette unique « convertir les .bin en .png ».
Chaque format demande une **rétro-ingénierie de son agencement**, puis une
conversion vers le format PC équivalent.

## 1.2 La méthode générale (valable pour tout format inconnu)

C'est la démarche à retenir, celle qu'on a appliquée à chaque format :

```
  1. TAILLE      Le fichier fait 98312 octets. Pour une image
                 annoncée 256x192, on attend 256*192*2 = 98304.
                 Écart : 8 octets. -> il y a un en-tête de 8 octets.

  2. SIGNATURE   Les 4 premiers octets sont 44 31 36 00 = "D16\0".
                 -> le format s'appelle D16. C'est la preuve qu'on
                    regarde le bon endroit (un vrai en-tête, pas du bruit).

  3. DIMENSIONS  Les 4 octets suivants, lus en little-endian :
                 0x0100 = 256 et 0x00C0 = 192.
                 -> exactement les dimensions attendues. En-tête confirmé.

  4. CONTENU     Le pixel 0 vaut 0xFBDE. En BGR555 -> R=30, G=30, B=30
                 = gris clair. Cohérent avec le coin d'une image.
                 -> l'interprétation des pixels est la bonne.

  5. VALIDATION  On convertit et on MESURE : écart moyen entre pixels
                 voisins = 45/765. Du bruit aléatoire donnerait ~400.
                 -> l'image est cohérente. Conversion correcte.
```

L'étape 5 est la plus importante et la plus souvent oubliée : **on ne
suppose pas qu'on a réussi, on le vérifie par une mesure objective.**

## 1.3 Les images : `.d16` → PNG

**Ce qu'on a trouvé :** en-tête de 8 octets (`"D16\0"` + largeur + hauteur),
puis des pixels en **BGR555**.

Le BGR555 est le format natif de la DS et de la GBA. 16 bits par pixel :

```
   15  14 13 12 11 10  9  8  7  6  5  4  3  2  1  0
  +---+-------------+----------+------------------+
  | X |    BLEU     |   VERT   |      ROUGE       |
  +---+-------------+----------+------------------+
     ignoré   5 bits     5 bits      5 bits
```

Chaque composante va de 0 à 31 au lieu de 0 à 255. La conversion correcte
n'est pas `× 8` (qui plafonnerait à 248) mais **la répétition des bits de
poids fort** :

```python
r8 = (r5 << 3) | (r5 >> 2)    # 0 -> 0,  31 -> 255 (toute la plage)
```

**Outil :** `tools/d16topng.py`

```bash
python3 tools/d16topng.py --all work/extracted/data out/png
# -> 40/40 convertis, 256x192 chacun
```

**Pour les textures de fonds 2D** (`.SCR`/`.PAL`/`.CHR`, format hérité de
la GBA) : le `.CHR` contient des tuiles 8×8 indexées, le `.PAL` la palette
de couleurs, le `.SCR` la disposition des tuiles à l'écran. Il faut les
trois pour reconstruire une image.

**Pour les modèles 3D** (`.nsbmd`) : ce sont des maillages, pas des images.
Les textures sont stockées à part, souvent dans des `.d16` ou dans le
`.nsbmd` lui-même. L'outil de référence est
[apicula](https://github.com/pleonex/apicula) (écrit en Rust).

## 1.4 Le son : `.sdat` → WAV

### Le piège conceptuel : un SDAT n'est pas un dossier de MP3

Le `.sdat` contient **cinq types d'objets**, et ils ne sont pas
interchangeables :

| Type | Nature | Équivalent PC |
|---|---|---|
| **SSEQ** | Une **partition**. « Joue le do pendant 200 ms avec l'instrument 5. » | Un fichier **MIDI** |
| **SBNK** | Une **banque** : associe chaque instrument à un échantillon | Un *soundfont* |
| **SWAR** | Des **échantillons** audio bruts (PCM/ADPCM) | Des fichiers WAV courts |
| **STRM** | De l'audio **déjà encodé** | Un WAV/MP3 complet |
| **SARC** | Un conteneur imbriqué | Un sous-dossier |

**Le point crucial :** une musique de jeu DS est presque toujours une
**SSEQ**. Et une SSEQ **ne contient pas de son**. Elle décrit *quoi* jouer
et a besoin de la SBNK + du SWAR pour produire de l'audio.

Autrement dit : extraire une SSEQ d'un SDAT vous donne un fichier qui,
ouvert dans un lecteur audio, ne produit **rien**. Ce n'est pas un bug,
c'est sa nature. Pour l'entendre il faut **simuler la console** — un
séquenceur qui lit la partition et synthétise les échantillons.

C'est exactement ce que fait le matériel de la DS en temps réel.

### Ce qu'on a extrait de cette ROM

**Outil :** `tools/sdatextract.py`

```bash
python3 tools/sdatextract.py work/extracted/data/sound_data.sdat out/sound
```

Résultat — l'archive fait 19 Mo et contient :

| Type | Fichiers | Taille | Nature |
|---|---|---|---|
| SSEQ | 133 | 744 K | Partitions (ne sonnent pas seules) |
| SBNK | 31 | 128 K | Banques d'instruments |
| SWAR | 31 | 5,2 M | Échantillons audio |
| STRM | 199 | 14 M | **Audio directement jouable** |

**Outil :** `tools/strmtowav.py`

```bash
python3 tools/strmtowav.py --all out/sound/STRM out/wav
# -> 199/199 convertis, 196 avec audio réel, 6.5 minutes au total
```

Vérification objective : la piste la plus longue (`BANK_BGM_021.wav`) fait
17,93 s, RMS 6409, dynamique de −32256 à +32000. C'est de la vraie musique,
pas du silence ni du bruit.

### Décoder le STRM : le format

Trois codecs possibles selon l'octet à l'offset `0x18` :

| Codec | Nom | Traitement |
|---|---|---|
| 0 | PCM8 | Octets signés, à multiplier par 256 |
| 1 | PCM16 | Mots de 16 bits signés |
| 2 | **ADPCM** | Compression 4 bits/échantillon — le cas intéressant |

L'**ADPCM** est un IMA-ADPCM adaptatif. Principe : on ne stocke pas la
valeur de l'échantillon, mais **la différence** avec le précédent, sur
4 bits. Un « index de pas » s'ajuste à chaque échantillon : quand le signal
varie vite, le pas augmente ; quand il est stable, le pas diminue.

Le format de bloc DS : **4 octets d'en-tête** (prédicteur initial + index)
puis **32 octets** de nibbles, soit 64 échantillons par bloc. Le bloc fait
donc 36 octets pour 64 échantillons — un facteur de compression de 3,5×.

```python
for nibble in (octet & 0x0F, octet >> 4):
    pas  = TABLE_PAS[index]
    diff = (pas >> 3) + ...          # selon les bits du nibble
    if nibble & 8: diff = -diff
    predicteur += diff               # on accumule
    index += TABLE_INDEX[nibble]     # le pas s'adapte
```

### Pour entendre les SSEQ (les vraies musiques)

Il faut simuler la console. L'outil est **vgmstream** — la référence pour
les formats audio de jeux :

```bash
# Installation
sudo apt install vgmstream-cli        # ou build depuis GitHub

# Convertir une partition en WAV (il resout les references SBNK/SWAR)
vgmstream-cli -o musique.wav out/sound/SSEQ/0000_xxx.sseq
```

`vgmstream` sait aussi lire le `.sdat` **entier** et extraire toutes les
SSEQ en les rendant jouables :

```bash
vgmstream-cli -o out/vgm/?s.wav work/extracted/data/sound_data.sdat
```

### Les noms des sons : le bloc SYMB

Découverte intéressante : ce SDAT contient un bloc **`SYMB`** (absent du
format standard) qui donne **562 noms symboliques** :

```
SE_BTL_001    son de combat n°1
SE_SYS_013    son système
SE_FLD_010    son de terrain
BGM_001       musique de fond
SE_DEM_021    son de cinématique
SE_SKL_054    son de compétence
```

Combiné au fichier `sound_data.sadl` (517 `#define` supplémentaires), on
obtient **plus de 1000 noms** qui documentent l'audio du jeu sans avoir à
l'écouter.

> **Leçon :** dans une ROM, les blocs de symboles et les fichiers `.sadl`
> sont de l'or. Ils ont survécu à la compilation parce qu'ils servaient au
> développeur, et ils donnent les noms que le compilateur a détruits
> ailleurs.

---

# PARTIE 2 — « Lancer » le jeu sur une machine ARM

## 2.1 La réponse courte

**Ce n'est pas possible sur une machine ARM ordinaire, et ce n'est pas une
question de puissance.** C'est une question de **matériel spécifique**.

L'ARM9 du jeu n'est pas « du code ARM » au sens d'un programme Linux. C'est
un **micrologiciel qui pilote du matériel**. Il accède directement à des
registres mémoire qui n'existent que dans la Nintendo DS.

Preuve mesurée dans votre ROM — les adresses matérielles utilisées :

```
0x04000000   moteur 2D (fond, sprites, palettes)
0x04100000   moteur 3D (géométrie, matrices)
0x04200000   ??? (registre DS)
0x04300000   ??? 
0x04400000   DMA (transferts mémoire automatiques)
0x04700000   ??? 
0x04800000   son (canaux, mélangeur)
0x04A00000   ???
0x04C00000   ???
0x05000000   palette VRAM
```

Sur un Raspberry Pi, écrire à `0x04000000` provoque un **défaut de
segmentation** ou un comportement indéfini : cette plage est réservée au
noyau. Le code n'a aucun moyen de savoir où il tourne.

De plus, le jeu est **deux processeurs synchronisés**. L'ARM9 et l'ARM7
communiquent par des registres partagés et des interruptions croisées. Un
seul cœur ARM ne peut pas reproduire ça.

## 2.2 Ce qu'on peut faire, par ordre de réalisme

### Option 1 — L'émulateur (recommandé)

C'est **la vraie réponse** à « voir le code en action ». Un émulateur
reproduit le matériel DS en logiciel : il intercepte chaque accès à
`0x04000000` et fait ce que la console ferait.

```bash
desmume-cli "2109 - Dragon Quest Monsters - Joker (E)(EXiMiUS).nds"
```

DeSmuME est installé et fonctionnel. Et surtout, il offre ce qui vous
intéresse vraiment — **voir le code s'exécuter** :

| Fonction DeSmuME | Ce qu'elle montre |
|---|---|
| **Debugger → Disassembler** | Le code ARM9 désassemblé **en direct**, avec le point d'exécution courant |
| **View → Registers** | L'état des 16 registres ARM et du CPSR |
| **View → Memory** | La RAM à l'adresse voulue (mettez `0x02000000` pour voir le code du jeu) |
| **Tools → Cheats** | Modifier une valeur mémoire à la volée |
| **Trace log** | L'historique des instructions exécutées |

**C'est le rétro-ingénieur qui utilise l'émulateur comme microscope, pas
comme console de jeu.** Vous pouvez mettre un point d'arrêt à l'adresse
`0x02000800` (le point d'entrée qu'on a identifié), lancer, et regarder le
jeu démarrer instruction par instruction — en comparant avec le
`FUN_02000950` de votre ARM9 décompilé.

C'est le pont entre le **code statique** (votre `arm9.c`) et le **code
vivant**.

### Option 2 — Un vrai matériel DS

Le jeu tourne sur une **vraie Nintendo DS** avec un linker (R4, Acekard…).
C'est du matériel ARM — un ARM946E-S et un ARM7TDMI — et le jeu y tourne
parfaitement, évidemment. Mais :

- Ce n'est pas « une machine ARM capable de la lire » au sens générique :
  c'est *la* machine pour laquelle il a été compilé.
- Pour observer le code, il faut un linker avec fonction de débogage, ou
  une DS modifiée avec un port série.

### Option 3 — Le portage (le plus ambitieux)

On **réécrit** le jeu pour une autre machine en réutilisant ce qu'on a
extrait : les assets (déjà convertis en PNG/WAV par nos outils) et la
logique comprise grâce au décompilé.

C'est ce que font les projets de « port » de jeux DS sur PC. C'est un
travail de plusieurs années-personnes : **7140 fonctions** à comprendre et
réimplémenter. Le décompilé que vous avez est exactement le point de départ
de ce travail.

## 2.3 Et si on voulait vraiment exécuter l'ARM9 sur un ARM ?

Techniquement concevable, mais il faudrait réimplémenter **toute la
console** :

```
  Ce que le jeu attend                    Ce qu'il faudrait fournir
  ─────────────────────────────────       ──────────────────────────────
  Mémoire à 0x02000000 (4 Mo)      ->     mmap() d'une zone fixe
  Registres 2D/3D à 0x04000000     ->     un émulateur de GPU DS complet
  Contrôleur DMA                   ->     un émulateur de DMA
  Matériel son                     ->     un émulateur audio
  ARM7 partenaire (synchro)        ->     un second cœur + IPC
  BIOS et appels SWI               ->     une réimplémentation du BIOS
  Carte SD (lecture des .bin)      ->     un filesystem virtuel
```

À ce stade, **vous avez écrit un émulateur**. Autant utiliser DeSmuME, qui
a demandé 20 ans de travail à une communauté.

> **Le principe général à retenir :** « exécuter du code ARM » n'a de sens
> que si l'environnement attendu par ce code existe. Un binaire de console
> n'est pas un programme autonome — c'est **la moitié d'un système**.

---

## 2.4 Récapitulatif des outils de ce dossier

| Outil | Rôle | Commande |
|---|---|---|
| `nds-inspect.sh` | Découpe la ROM | `tools/nds-inspect.sh jeu.nds` |
| `nds-decompile.sh` | ARM9/ARM7/overlays → C | `tools/nds-decompile.sh jeu.nds` |
| `d16topng.py` | Images `.d16` → PNG | `tools/d16topng.py --all data out/png` |
| `sdatextract.py` | Archive `.sdat` → SSEQ/SBNK/SWAR/STRM | `tools/sdatextract.py sound.sdat out/sound` |
| `strmtowav.py` | Flux `.strm` → WAV | `tools/strmtowav.py --all out/sound/STRM out/wav` |
| DeSmuME | Exécuter et déboguer le jeu | `desmume-cli jeu.nds` |
| vgmstream | Rendre les SSEQ jouables | `vgmstream-cli -o out.wav in.sseq` |
| apicula | Modèles 3D `.nsbmd` | (Rust, à installer) |

## 2.5 Résultats obtenus sur cette ROM

| Ressource | Extrait | Vérification |
|---|---|---|
| Code | 7140 fonctions, 279 930 lignes de C | 0 `halt_baddata` |
| Images | 40 PNG en 256×192 | écart voisins 45/765 (image réelle) |
| Audio jouable | 199 WAV, 6,5 minutes | RMS 6409 sur 196 fichiers |
| Partitions | 133 SSEQ + 31 SBNK + 31 SWAR | à jouer via vgmstream |
| Noms de sons | 562 symboles SYMB + 517 `#define` | lus depuis la ROM |

---

## 2.6 Cadre légal — rappel

Extraire et étudier : **légal** (préservation, interopérabilité — directive
2009/24/CE, art. 5 et 6 ; CPI art. L.122-6-1).

Redistribuer la ROM, le code décompilé ou les assets : **illégal**.

Règle simple : **on peut tout analyser, on ne peut rien redistribuer.**
