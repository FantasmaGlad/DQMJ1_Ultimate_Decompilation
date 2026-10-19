#!/usr/bin/env python3
import struct
import json
import os

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(RACINE, "work/extracted/data")

def decode(data):
    res = []
    accents = {
        # 0x45 = "É", 0x49 = "Í" trouvés le 2026-09-26 (F « Echanger »/« Equipement », S « Igneo » :
        # tables de compétences) : consommés directement ici (au lieu d'un correctif local par script
        # appelant) pour que toutes les banques mes_* en beneficient, y compris celles generees par
        # extract_multilingual_texts.py qui n'a pas de nettoyage local.
        0x45: "É", 0x49: "Í",
        # 0x57 = "á" trouvé le 2026-09-25 (session objets, "Gáe Bolg") : comble
        # exactement le trou entre à (0x56) et â (0x58), cohérent avec l'ordre
        # Latin-1 (à á â ã ä...) déjà suivi par les autres accents de ce bloc.
        0x56: "à", 0x57: "á", 0x58: "â", 0x5a: "ç", 0x5b: "è", 0x5c: "é",
        0x5d: "ê", 0x61: "î", 0x62: "ï", 0x5e: "ë", 0x66: "ô", 0x68: "œ", 0x6b: "û",
        # 0x9a trouvé le 2026-09-25 (session objets, titres de livres
        # "<9a>Positive Puller'") : ouvre une citation dont 0x9b (déjà mappé)
        # ferme la fin — même simplification en apostrophe droite que 0x9b.
        # Caracteres D/I/S trouves le 2026-09-26 par contexte (Anf<59>llig = Anfaellig, cos<5f> = cosi,
        # pu<64> = puo, pi<69> = piu, Da<63>o = Dano, Miniexplosi<65>n, alg<6a>n, <6e>Estas = Estas avec
        # point d'interrogation inverse, <6f>No = point d'exclamation inverse).
        0x55: "Ü", 0x59: "ä", 0x5f: "ì", 0x60: "í", 0x63: "ñ", 0x64: "ò", 0x65: "ó", 0x67: "ö",
        0x69: "ù", 0x6a: "ú", 0x6c: "ü", 0x6d: "ß", 0x6e: "¿", 0x6f: "¡",
        0x9a: "\x27", 0x9b: "\x27", 0xac: ".", 0xcd: ",", 0xcc: "-"
    }
    for b in data:
        if b == 0x0a: res.append(" ")
        elif b == 0xff: res.append("|")
        elif 0x0b <= b <= 0x24: res.append(chr(b + 0x36))
        elif 0x25 <= b <= 0x3e: res.append(chr(b + 0x3c))
        elif b == 0x01: res.append(" ")
        elif b in accents: res.append(accents[b])
        elif b == 0x00: pass
        else: res.append(f"<{b:02x}>")
    return "".join(res)

def format_fr(s):
    # Capitalize in French: keep de, d', à, en, du, des, etc. in lowercase unless first word
    words = s.split(" ")
    particles = {"de", "d\x27", "à", "en", "du", "des", "l\x27"}
    res = []
    for i, w in enumerate(words):
        parts = w.split("-")
        cap_parts = []
        for j, p in enumerate(parts):
            if i > 0 and p.lower() in particles:
                cap_parts.append(p.lower())
            else:
                if p.lower().startswith("d\x27") and len(p) > 2:
                    cap_parts.append("d\x27" + p[2:].capitalize())
                elif p.lower().startswith("l\x27") and len(p) > 2:
                    cap_parts.append("l\x27" + p[2:].capitalize())
                else:
                    cap_parts.append(p.capitalize())
        res.append("-".join(cap_parts))
    # Specific fixes
    formatted = " ".join(res)
    fixes = {
        "Boïte À Pièges": "Boîte à pièges",
        "Machine À Tuer": "Machine à tuer",
        "Canniboïte": "Canniboîte",
        "Dr Rebelote": "Dr Rebelote",
        "As De Pique": "As de pique",
        "Smilodon De Lait": "Smilodon de lait",
        "Frelon De L'enfer": "Frelon de l'enfer",
        "Chien De L'enfer": "Chien de l'enfer",
        "Seigneur Dragovien": "Seigneur dragovien",
        "Dragon D'albâtre": "Dragon d'albâtre",
        "Baron D'os": "Baron d'os",
        "Golem D'or": "Golem d'or",
        "Main De Boue": "Main de boue",
        "Pantin De Boue": "Pantin de boue",
        "Âme En Peine": "Âme en peine",
        "Face De Crapaud": "Face de crapaud",
        "Dragon De Métal": "Dragon de métal",
        "Roi Gluant De Métal": "Roi gluant de métal",
        "Gluanpereur De Métal": "Gluanpereur de métal",
        "Monte-gluant De Métal": "Monte-gluant de métal",
        "Gluant De Métal": "Gluant de métal",
        "Gluant De Crin": "Gluant de crin",
        "Gluant De Mercure": "Gluant de mercure",
    }
    return fixes.get(formatted, formatted)

def format_en(s):
    words = s.split(" ")
    particles = {"of", "de", "in", "o\x27", "at", "the"}
    res = []
    for i, w in enumerate(words):
        parts = w.split("-")
        cap_parts = []
        for j, p in enumerate(parts):
            if i > 0 and p.lower() in particles:
                cap_parts.append(p.lower())
            else:
                cap_parts.append(p.capitalize())
        res.append("-".join(cap_parts))
    formatted = " ".join(res)
    fixes = {
        "Bags O' Laughs": "Bag o' laughs",
        "Dr Snapped": "Dr. Snapped",
        "Demon-at-arms": "Demon-at-arms",
    }
    return fixes.get(formatted, formatted)

def main():
    with open(os.path.join(DATA, "message0.binE"), "rb") as fp: de = fp.read()
    with open(os.path.join(DATA, "message0.binF"), "rb") as fp: df = fp.read()
    with open(os.path.join(DATA, "ViewChrTbl.bin"), "rb") as f: v = f.read()
    with open(os.path.join(DATA, "ModelTbl.bin"), "rb") as f: mt = f.read()

    models = [mt[i*12:(i+1)*12].split(b"\x00")[0].decode("ascii", errors="ignore") for i in range(len(mt)//12)]
    items_e = [x.strip() for x in decode(de).split("|")]
    items_f = [x.strip() for x in decode(df).split("|")]

    mapping = {}
    for i in range(len(v)//26):
        rec = struct.unpack("<13H", v[i*26:(i+1)*26])
        m_idx = rec[1]
        if 0 < m_idx < len(models):
            m_name = models[m_idx]
            msg_idx = 64 + i
            ne = items_e[msg_idx] if msg_idx < len(items_e) else ""
            nf = items_f[msg_idx] if msg_idx < len(items_f) else ""
            if ne or nf:
                if m_name not in mapping:
                    mapping[m_name] = {
                        "id": m_name,
                        "monster_id": i,
                        "nom_fr": format_fr(nf),
                        "nom_en": format_en(ne)
                    }

    # Add m246_01
    mapping["m246_01"] = {
        "id": "m246_01",
        "monster_id": 223,
        "nom_fr": "Mutancre (Ancre)",
        "nom_en": "Anchorman (Anchor)"
    }

    # Add protagonists
    mapping["cool"] = {
        "id": "cool",
        "monster_id": 0,
        "nom_fr": "Héros",
        "nom_en": "Hero"
    }
    mapping["cool_jet"] = {
        "id": "cool_jet",
        "monster_id": 0,
        "nom_fr": "Héros (Scooter des mers)",
        "nom_en": "Hero (Watercraft)"
    }

    out_file = os.path.join(RACINE, "tools/mapping_monstres.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)

    print(f"Mapping saved: {len(mapping)} models mapped.")

if __name__ == "__main__":
    main()
