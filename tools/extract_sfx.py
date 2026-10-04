#!/usr/bin/env python3
"""
extract_sfx.py
Extraction et synthèse exhaustive des 292 bruitages du jeu Dragon Quest Monsters: Joker (Nintendo DS).
Source de vérité : sound_data.sdat (blocs SYMB, INFO, FAT, FILE) et constantes de sound_data.sadl.

Extrait :
  1. 187 flux audio STRM PCM8 (SE_SKL_001 à 115, SE_DEM_*, SE_FLD_*, SE_SYS_013)
  2. 105 séquences audio SSEQ (SE_BTL_001 à 043, SE_SYS_001 à 017, SE_FLD_010 à 052, SE_DEM_*, SE_SHA_*)

Audit suite 100 (2026-10-02) : les 14 flux ST_ME_001 à 014 sont retirés de cette extraction (doublon
exact, déjà catalogués par `extract_jingles.py` -> `game_jingles.json`), ramenant le total de 306 à
292. Voir le commentaire dans la boucle STRM ci-dessous.

Produit :
  - DragonQuestMonsterJoker1Bestiaire/assets/audio/sfx/*.mp3 (292 fichiers MP3 à 128 kbps)
  - DragonQuestMonsterJoker1Bestiaire/assets/data/game_sfx.json
"""

import json
import os
import struct
import subprocess
import sys
import tempfile
import time
import wave

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from rendre_sequences_sseq import SseqRenderer, SAMPLE_RATE, exporter_wav, convertir_mp3

SDAT_PATH = os.path.join(ROOT, "work", "extracted", "data", "sound_data.sdat")
DEST_AUDIO_DIR = os.path.abspath(
    os.path.join(ROOT, "..", "DragonQuestMonsterJoker1Bestiaire", "assets", "audio", "sfx")
)
DEST_JSON_PATH = os.path.abspath(
    os.path.join(ROOT, "..", "DragonQuestMonsterJoker1Bestiaire", "assets", "data", "game_sfx.json")
)


def classifier_sfx(symbol):
    """Classe un symbole officiel en catégorie et sous-catégorie fonctionnelle."""
    if symbol.startswith("SE_SKL_"):
        return "combat", "skills", "Combats", "Sorts & Compétences", "Combat", "Spells & Skills"
    elif symbol.startswith("SE_BTL_"):
        return "combat", "actions", "Combats", "Attaques & Actions", "Combat", "Attacks & Actions"
    elif symbol.startswith("SE_SYS_"):
        return "system", "menu", "Système", "Menus & Interface", "System", "Menus & UI"
    elif symbol.startswith("SE_FLD_"):
        return "field", "exploration", "Exploration", "Terrain & Environnement", "Field", "Exploration & Environment"
    elif symbol.startswith("ST_ME_"):
        return "fanfare", "jingles", "Fanfares", "Jingles & Événements", "Fanfares", "Jingles & Events"
    elif symbol.startswith("SE_DEM_") or symbol.startswith("SE_SHA_"):
        return "cinematic", "cutscenes", "Cinématiques", "Scènes & Démos", "Cinematics", "Cutscenes & Demos"
    else:
        return "other", "sfx", "Autres", "Effets sonores", "Other", "Sound Effects"


def main():
    os.makedirs(DEST_AUDIO_DIR, exist_ok=True)
    renderer = SseqRenderer(SDAT_PATH)
    sdat = renderer.sdat

    sfx_list = []
    tmp_dir = tempfile.mkdtemp(prefix="dqmj_sfx_")

    print("\n=== 1. Extraction des flux STRM natifs PCM8 (187 flux) ===")
    strm_count = 0
    t0 = time.time()
    for item in sdat.streams:
        if not item or not item[0] or item[0].startswith("DUMMY"):
            continue
        symbol, strm = item
        if symbol.startswith("ST_ME_"):
            # Audit suite 100 (2026-10-02, depot Bestiaire) : les 14 fanfares ST_ME_001..014 sont
            # deja extraites et cataloguees par tools/extract_jingles.py (assets/data/game_jingles.json,
            # categorie "event"), avec des titres et descriptions plus riches. Les inclure aussi ici
            # dupliquait le meme fichier audio (meme empreinte md5) sous une deuxieme fiche SFX, visible
            # a la fois dans l'onglet Bruitages et l'onglet Fanfares de /musiques -- signale par le
            # proprietaire comme "sons dupliques". Seul leur catalogue dans les jingles fait foi.
            continue
        cat, subcat, cat_lbl, subcat_lbl, cat_lbl_en, subcat_lbl_en = classifier_sfx(symbol)
        rate = strm.sampleRate
        n_chan = len(strm.channels)
        chan_blocks = [b"".join(c) for c in strm.channels]
        min_len = min(len(b) for b in chan_blocks)
        dur = round(min_len / rate, 2)

        wav_path = os.path.join(tmp_dir, f"{symbol}.wav")
        with wave.open(wav_path, "wb") as wf:
            wf.setnchannels(n_chan)
            wf.setsampwidth(2)
            wf.setframerate(rate)
            frames = bytearray()
            for i in range(min_len):
                for c in range(n_chan):
                    val8 = struct.unpack("<b", chan_blocks[c][i:i+1])[0]
                    val16 = max(-32768, min(32767, val8 * 256))
                    frames.extend(struct.pack("<h", val16))
            wf.writeframes(frames)

        mp3_path = os.path.join(DEST_AUDIO_DIR, f"{symbol}.mp3")
        convertir_mp3(wav_path, mp3_path)
        bytes_size = os.path.getsize(mp3_path)

        sfx_id = f"sfx-{symbol.lower().replace('_', '-')}"
        sfx_list.append({
            "id": sfx_id,
            "symbol": symbol,
            "category": cat,
            "subcategory": subcat,
            "categoryLabel": cat_lbl,
            "subcategoryLabel": subcat_lbl,
            "categoryLabelEn": cat_lbl_en,
            "subcategoryLabelEn": subcat_lbl_en,
            "durationSeconds": dur,
            "sourceType": "STRM",
            "sampleRate": rate,
            "channels": n_chan,
            "file": f"sfx/{symbol}.mp3",
            "bytes": bytes_size,
        })
        strm_count += 1
        if strm_count % 30 == 0:
            print(f"  STRM : {strm_count}/187 traités ({time.time()-t0:.1f}s)...")

    print(f"-> {strm_count} flux STRM extraits et encodés en {time.time()-t0:.2f}s")

    print("\n=== 2. Rendu des séquences SSEQ SFX (105 séquences) ===")
    seq_count = 0
    t1 = time.time()
    for idx, item in enumerate(sdat.sequences):
        if not item or not item[0] or not (item[0].startswith("SE_") or item[0].startswith("ST_")):
            continue
        symbol, _ = item
        cat, subcat, cat_lbl, subcat_lbl, cat_lbl_en, subcat_lbl_en = classifier_sfx(symbol)
        
        # Rend la séquence avec une limite de 6 secondes (les bruitages durent de 0.2s à 3s)
        left, right, dur, notes_count, tracks_count, bank_name, _ = renderer.render_sequence(idx, max_seconds=6.0)
        dur = round(dur, 2)

        wav_path = os.path.join(tmp_dir, f"{symbol}.wav")
        exporter_wav(left, right, wav_path)

        mp3_path = os.path.join(DEST_AUDIO_DIR, f"{symbol}.mp3")
        convertir_mp3(wav_path, mp3_path)
        bytes_size = os.path.getsize(mp3_path)

        sfx_id = f"sfx-{symbol.lower().replace('_', '-')}"
        sfx_list.append({
            "id": sfx_id,
            "symbol": symbol,
            "category": cat,
            "subcategory": subcat,
            "categoryLabel": cat_lbl,
            "subcategoryLabel": subcat_lbl,
            "categoryLabelEn": cat_lbl_en,
            "subcategoryLabelEn": subcat_lbl_en,
            "durationSeconds": dur,
            "sourceType": "SSEQ",
            "sampleRate": SAMPLE_RATE,
            "channels": 2,
            "file": f"sfx/{symbol}.mp3",
            "bytes": bytes_size,
        })
        seq_count += 1
        if seq_count % 20 == 0:
            print(f"  SSEQ : {seq_count}/105 traitées ({time.time()-t1:.1f}s)...")

    print(f"-> {seq_count} séquences SSEQ rendues et encodées en {time.time()-t1:.2f}s")

    # Trier la liste par symbole canonique
    sfx_list.sort(key=lambda x: x["symbol"])

    # Construction des statistiques de catégories
    category_order = ["combat", "system", "field", "fanfare", "cinematic"]
    categories_meta = []
    for cat_id in category_order:
        cat_items = [x for x in sfx_list if x["category"] == cat_id]
        if not cat_items:
            continue
        first = cat_items[0]
        subcats_dict = {}
        for it in cat_items:
            s_id = it["subcategory"]
            if s_id not in subcats_dict:
                subcats_dict[s_id] = {
                    "id": s_id,
                    "label": it["subcategoryLabel"],
                    "labelEn": it["subcategoryLabelEn"],
                    "count": 0,
                    "ids": []
                }
            subcats_dict[s_id]["count"] += 1
            subcats_dict[s_id]["ids"].append(it["id"])

        categories_meta.append({
            "id": cat_id,
            "label": first["categoryLabel"],
            "labelEn": first["categoryLabelEn"],
            "count": len(cat_items),
            "subcategories": list(subcats_dict.values()),
            "ids": [x["id"] for x in cat_items]
        })

    payload = {
        "provenance": (
            "Extrait du SDAT officiel (sound_data.sdat) de Dragon Quest Monsters: Joker (Nintendo DS). "
            "Symboles officiels issus du bloc SYMB et des constantes de sound_data.sadl (pilote Procyon Studio)."
        ),
        "total": len(sfx_list),
        "categories": categories_meta,
        "sfx": sfx_list
    }

    with open(DEST_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"\nTerminé avec succès !")
    print(f"  Fichiers MP3 écrits dans : {DEST_AUDIO_DIR} ({len(sfx_list)} fichiers)")
    print(f"  Catalogue JSON écrit dans : {DEST_JSON_PATH}")


if __name__ == "__main__":
    main()
