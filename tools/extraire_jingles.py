#!/usr/bin/env python3
"""
extraire_jingles.py -- Extraction et rendu des 19 fanfares et jingles d'événements de DQMJ1.

Sources de vérité :
  - sound_data.sdat (blocs SYMB, INFO, FAT, FILE)
  - sound_data.sadl (constantes des pilotes Procyon Studio)
  - rendre_sequences_sseq.py (moteur de synthèse orchestrale Sugiyama)

Extrait :
  1. 14 flux STRM natifs (ST_ME_001 à ST_ME_014), lus directement depuis sound_data.sdat
     (sdat.streams) -- indépendant de extraire_bruitages_sfx.py, qui n'extrait plus ces symboles
     depuis l'audit suite 100 (doublon de catalogue corrigé) et ne peut donc plus servir de source
     intermédiaire.
  2. 5 fanfares séquencées SSEQ rendues à leur durée naturelle sans bouclage artificiel :
     BGM_010, BGM_015, BGM_024, BGM_025, BGM_026.

Produit :
  - assets/audio/jingles/*.mp3 (19 fichiers MP3 haute qualité)
  - assets/data/game_jingles.json (catalogue structuré)

Audit joueur (2026-10-03) : ce fichier contenait un titre et une description francais/anglais
invente pour chacun des 19 jingles (ex. "lorsqu'un monstre sauvage decide spontanement de rejoindre
le dresseur"), ainsi qu'une categorie thematique (victory/church/progression/discovery/event)
attribuee sans aucune preuve ROM -- aucun opcode de script, aucune banque de texte ne nomme ni ne
categorise ces 19 symboles. Retire, meme principe que les titres d'artworks (suite 100) et de
cinematiques : le catalogue ne publie que ce que la ROM prouve (symbole, type de source, duree,
caracteristiques audio) ; le regroupement affiche cote web se fait sur `sourceType` (STRM natif vs
SSEQ rendu), seule distinction techniquement reelle.
"""

import json
import os
import struct
import subprocess
import sys
import tempfile
import wave

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from rendre_sequences_sseq import SseqRenderer, exporter_wav, convertir_mp3, SDAT_PATH, SAMPLE_RATE

WIKI_DIR = "/home/fanta/Developpement/DQMJ1/DragonQuestMonsterJoker1Bestiaire"
DEST_AUDIO_DIR = os.path.join(WIKI_DIR, "assets", "audio", "jingles")
DEST_JSON_PATH = os.path.join(WIKI_DIR, "assets", "data", "game_jingles.json")

# 1. Les 14 flux STRM natifs (symbole officiel du bloc SYMB, prouve).
STRM_SYMBOLS = [f"ST_ME_{i:03d}" for i in range(1, 15)]

# 2. Les 5 fanfares SSEQ, avec leur indice de sequence (BGM_SEQUENCE_INDICES) et une duree limite
# choisie a l'oreille pour couper apres la phrase musicale complete (evite la boucle infinie du
# moteur SSEQ sur une fanfare qui n'est censee jouer qu'une fois).
SSEQ_JINGLES = [
    {"symbol": "BGM_010", "sequence": 42, "durationLimit": 14.5},
    {"symbol": "BGM_015", "sequence": 47, "durationLimit": 8.5},
    {"symbol": "BGM_024", "sequence": 56, "durationLimit": 17.0},
    {"symbol": "BGM_025", "sequence": 179, "durationLimit": 9.0},
    {"symbol": "BGM_026", "sequence": 180, "durationLimit": 22.0},
]


def main():
    print("=== Extraction et rendu des 19 fanfares et jingles de DQMJ1 ===")
    os.makedirs(DEST_AUDIO_DIR, exist_ok=True)
    tmp_dir = tempfile.mkdtemp(prefix="dqmj_jingles_")

    renderer = SseqRenderer(SDAT_PATH)
    jingles_catalog = []

    # 1. Flux STRM natifs, lus directement depuis sdat.streams (plus de dependance a un fichier
    # intermediaire ecrit par un autre script). Meme garde que extraire_bruitages_sfx.py : certaines
    # entrees de sdat.streams sont None ou ont un symbole vide/DUMMY.
    streams_by_symbol = {}
    for item in renderer.sdat.streams:
        if not item or not item[0] or item[0].startswith("DUMMY"):
            continue
        symbol, strm = item
        streams_by_symbol[symbol] = strm
    for idx, sym in enumerate(STRM_SYMBOLS, start=1):
        strm = streams_by_symbol.get(sym)
        if strm is None:
            print(f"Erreur : symbole STRM introuvable dans sound_data.sdat : {sym}")
            continue
        dest_filename = f"{sym}.mp3"
        dest_mp3_path = os.path.join(DEST_AUDIO_DIR, dest_filename)
        wav_path = os.path.join(tmp_dir, f"{sym}.wav")

        # Decodage PCM8 -> PCM16 identique a extraire_bruitages_sfx.py (meme table STRM source) :
        # octet signe 8 bits mis a l'echelle *256 vers 16 bits, ecriture WAV entrelacee standard.
        rate = strm.sampleRate
        chan_blocks = [b"".join(c) for c in strm.channels]
        n_chan = len(chan_blocks)
        min_len = min(len(b) for b in chan_blocks)
        with wave.open(wav_path, "wb") as wf:
            wf.setnchannels(n_chan)
            wf.setsampwidth(2)
            wf.setframerate(rate)
            frames = bytearray()
            for i in range(min_len):
                for c in range(n_chan):
                    val8 = struct.unpack("<b", chan_blocks[c][i:i + 1])[0]
                    val16 = max(-32768, min(32767, val8 * 256))
                    frames.extend(struct.pack("<h", val16))
            wf.writeframes(frames)
        convertir_mp3(wav_path, dest_mp3_path)
        dur = round(min_len / rate, 2)

        jingles_catalog.append({
            "id": f"jingle-me-{idx:03d}",
            "symbol": sym,
            "sourceType": "STRM",
            "file": f"jingles/{dest_filename}",
            "sampleRate": rate,
            "channels": len(chan_blocks),
            "durationSeconds": dur,
            "bytes": os.path.getsize(dest_mp3_path),
            "url": f"/api/assets/audio/jingles/{dest_filename}",
        })
        print(f"  OK {sym} : {dur}s")

    # 2. Fanfares séquencées SSEQ.
    for idx, item in enumerate(SSEQ_JINGLES, start=1):
        sym = item["symbol"]
        seq_idx = item["sequence"]
        dur_limit = item["durationLimit"]
        dest_filename = f"{sym}.mp3"
        dest_mp3_path = os.path.join(DEST_AUDIO_DIR, dest_filename)
        print(f"Rendu SSEQ de {sym} (Seq #{seq_idx}, limite {dur_limit}s)...")
        left, right, natural_dur, notes, tracks, bank, _ = renderer.render_sequence(seq_idx, max_seconds=dur_limit)

        wav_path = os.path.join(tmp_dir, f"{sym}.wav")
        exporter_wav(left, right, wav_path)
        convertir_mp3(wav_path, dest_mp3_path)
        dur = round(len(left) / SAMPLE_RATE, 2)

        jingles_catalog.append({
            "id": f"jingle-sseq-{idx:03d}",
            "symbol": sym,
            "sourceType": "SSEQ",
            "file": f"jingles/{dest_filename}",
            "sampleRate": SAMPLE_RATE,
            "channels": 2,
            "sequence": seq_idx,
            "durationSeconds": dur,
            "bytes": os.path.getsize(dest_mp3_path),
            "url": f"/api/assets/audio/jingles/{dest_filename}",
        })
        print(f"  OK {sym} : {dur}s")

    payload = {
        "provenance": (
            "Fanfares et jingles officiels de Dragon Quest Monsters: Joker (Nintendo DS). "
            "14 flux STRM natifs extraits de sound_data.sdat et 5 séquences SSEQ orchestrales "
            "rendues avec les banques d'instruments officielles de Koichi Sugiyama à durée naturelle. "
            "Aucun titre, description ou categorie thematique officiels n'existent dans la ROM pour "
            "ces symboles (verifie : bloc SYMB, sound_data.sadl, 51 banques de texte des 5 langues) -- "
            "seul `sourceType` (STRM natif / SSEQ rendu) est une distinction technique reelle."
        ),
        "total": len(jingles_catalog),
        "jingles": jingles_catalog,
    }

    with open(DEST_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"\nTerminé avec succès !")
    print(f"  Fichiers audio : {DEST_AUDIO_DIR} ({len(jingles_catalog)} fichiers)")
    print(f"  Catalogue JSON : {DEST_JSON_PATH}")


if __name__ == "__main__":
    main()
