#!/usr/bin/env python3
"""Extrait les tirades des PNJ (dialogues) depuis les 80 scripts d'événements
`.evt` de la ROM — item 12 de docs/DATA_RESEARCH_PLAN.md du projet bestiaire.

## Provenance et niveau de confiance (session du 2026-09-25, suite 17)

Format du fichier `.evt` et table des 256 opcodes **repris d'un outil de
modding communautaire open source**
(github.com/ExcaliburZero/dqmj1_randomizer, module `randomize/evt.py` +
`randomize/character_encoding.py` + `data/event_instructions.csv`), pas
réimplémentés depuis un désassemblage. Ce projet ne clone ni n'exécute ce
dépôt : les trois fichiers de référence ont été lus (`WebFetch`/`curl` sur
les raw GitHub, mis en cache localement) puis **le format a été réécrit ici
en Python indépendant**, pour rester cohérent avec la convention de ce
dossier (un script par donnée, pas de dépendance externe exécutée).

**Ce qui est vérifié par nous-mêmes, pas seulement recopié** :
- Les 4 premiers octets de chaque `.evt` sont le magique `"SCR\0"` (vérifié
  sur plusieurs fichiers), cohérent avec l'outil externe qui les ignore sans
  les nommer.
- Après le magique, un bloc de 4096 o (`0x1000`) de données non décodées
  (probablement une table de constantes/valeurs référencée par les
  instructions, pas du texte) — traité en bloc opaque, pas interprété plus
  finement, exactement comme le fait l'outil externe.
- Ensuite, un flux d'instructions TLV : `u32` type + `u32` longueur totale
  (instruction incluse) + `longueur-8` octets de charge utile. Vérifié en
  parcourant les 80 fichiers jusqu'à la fin exacte de chaque flux (aucune
  erreur d'alignement, aucun octet restant non consommé) — preuve forte que
  le découpage TLV est correct pour notre ROM.
- Seuls 2 des 256 opcodes nous intéressent ici : `0x29 SetDialog [String]`
  et `0x2A SpeakerName [String]` (les autres sont ignorés, pas décodés).
  Chaque `SetDialog` est attribué au dernier `SpeakerName` rencontré avant
  lui dans le flux du script (hypothèse d'appariement séquentiel, cohérente
  avec le fonctionnement habituel de ce genre de moteur de script de
  dialogue — pas confirmée par désassemblage, mais aucune tirade n'est
  publiée sans un `SpeakerName` précédent : pas de nom inventé).
- Table de caractères EU/Amérique du Nord reprise de `character_encoding.py`
  (chiffres 0x00-0x09, majuscules 0x0B-0x24, minuscules 0x25-0x3E, quelques
  signes de ponctuation, terminateur `0xFF`). **Différente** de
  `extraire_mapping.py::decode` utilisé pour les banques `mes_*.bin` : ici
  `0x00`-`0x09` sont de vrais chiffres (utile pour des tirades avec des
  nombres), alors que dans les banques `mes_*.bin` `0x00` sert de
  padding/séparateur. Les deux tables ne sont pas interchangeables — ne pas
  réutiliser l'une pour l'autre contexte.

**Limite assumée** : les 22 noms de dresseurs déjà connus
(`mes_master_name.binE`, voir item 7) ne couvrent pas tous les `SpeakerName`
possibles — de nombreux PNJ ont un nom de scène spécifique non répertorié
ailleurs. Les noms publiés ici sont donc **tels que trouvés dans les
scripts**, sans tentative de les relier à un id de personnage/modèle 3D (ceci
resterait à faire, voir item 11 "PNJ (identité/rôle)").
"""
import json
import os
import struct

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(RACINE, "work/extracted/data")

DATA_BLOCK_SIZE = 0x1000  # 4096 o après le magique

# Sous-ensemble de BYTE_TO_CHAR_MAP_NA_AND_EU (dqmj1_randomizer/character_encoding.py)
# utile aux tirades de dialogue. Terminateur 0xFF géré à part (pas dans la table).
CHAR_MAP = {
    **{i: str(i) for i in range(0, 10)},  # 0x00-0x09 = chiffres '0'-'9'
    0x0A: " ",
    **{0x0B + i: chr(ord("A") + i) for i in range(26)},  # 0x0B-0x24 = A-Z
    **{0x25 + i: chr(ord("a") + i) for i in range(26)},  # 0x25-0x3E = a-z
    0x55: "Ü",
    0x57: "á",
    0x70: "!",
    0x71: "?",
    0x87: "+",
    0x8D: "II",
    0x8E: "III",
    0x9A: "‘",
    0x9B: "’",
    0xAC: ".",
    0xAD: "&",
    0xCC: "-",
    0xCD: ",",
    0xFE: "\n",
}


def decode_evt_string(payload):
    chars = []
    for b in payload:
        if b == 0xFF:
            break
        chars.append(CHAR_MAP.get(b, f"[{b:02x}]"))
    return "".join(chars)


def read_instructions(data):
    """Générateur (type_id, payload) pour le flux d'instructions TLV après
    le magique (4 o) et le bloc data (4096 o)."""
    offset = 4 + DATA_BLOCK_SIZE
    n = len(data)
    while offset + 8 <= n:
        type_id, length = struct.unpack_from("<II", data, offset)
        payload_start = offset + 8
        payload_end = offset + length
        if length < 8 or payload_end > n:
            break  # fin de flux non alignée : on arrête plutôt que deviner
        yield type_id, data[payload_start:payload_end]
        offset = payload_end


def extract_dialogues_from_file(path):
    with open(path, "rb") as f:
        data = f.read()
    if data[:4] != b"SCR\x00":
        return []

    lines = []
    current_speaker = None
    for type_id, payload in read_instructions(data):
        if type_id == 0x2A:  # SpeakerName
            current_speaker = decode_evt_string(payload).strip()
        elif type_id == 0x29:  # SetDialog
            text = decode_evt_string(payload).strip()
            if text and current_speaker:
                lines.append({"speaker": current_speaker, "text": text})
    return lines


def main():
    evt_files = sorted(f for f in os.listdir(DATA) if f.endswith(".evt"))
    result = {}
    total_lines = 0
    for filename in evt_files:
        script_id = filename[:-4]
        lines = extract_dialogues_from_file(os.path.join(DATA, filename))
        if lines:
            result[script_id] = lines
            total_lines += len(lines)

    out_file = os.path.join(RACINE, "tools/dialogues.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)

    wiki_out = os.path.join(RACINE, "../DragonQuestMonsterJoker1Bestiaire/assets/data/dialogues.json")
    if os.path.exists(os.path.dirname(wiki_out)):
        with open(wiki_out, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=1)

    print(f"Scripts avec dialogue : {len(result)} / {len(evt_files)}")
    print(f"Tirades extraites : {total_lines}")
    speakers = sorted({line["speaker"] for lines in result.values() for line in lines})
    print(f"Locuteurs distincts : {len(speakers)}")
    print(speakers[:40])


if __name__ == "__main__":
    main()

