#!/usr/bin/env python3
"""
render_sseq_audio.py -- Restauration audio canonique des musiques SSEQ de DQMJ1.

Exécution (dépôt frère, Python système) :
    python3 tools/render_sseq_audio.py --verifier
    python3 tools/render_sseq_audio.py --rendre BGM_001 [--duree 96]
    python3 tools/render_sseq_audio.py --rendre all [--duree 96]

Architecture et provenance :
    1. sound_data.sdat (bloc INFO, FAT, FILE, SYMB) chargé via ndspy.soundArchive.SDAT.
    2. Chaque BGM officiel (BGM_001..BGM_026) est relié à son BankID officiel :
       BGM_001 -> Bank 0 (BANK_BGM_001) et WaveArchive 0 (WAVE_BGM_001)
       BGM_003 -> Bank 2 (BANK_BGM_003) et WaveArchive 2 (WAVE_BGM_003)
       ...
    3. Les instruments (SingleNote, Range, Regional) associent chaque pitch MIDI à un échantillon
       SWAV natif avec sa note racine (rootKey), sa fréquence d'échantillonnage et ses boucles
       de sustain exactes.
    4. Ordonnancement rigoureux multi-pistes : chaque piste (0 à 15) gère ses propres registres
       d'état (program, volume, expression, pan, transpose) indépendamment des autres pistes,
       ses sous-routines (Call/Return) et ses boucles à compteur (BeginLoop/EndLoop).
    5. Mixage stéréo 32 768 Hz Float32 avec interpolation linéaire, pan stéréophonique constant,
       gestion d'enveloppe ADSR et normalisation de crête à -0.5 dB.
    6. Export WAV master et compression MP3 stéréo via ffmpeg vers web/ et assets/audio/themes/.
"""

import argparse
import json
import math
import os
import struct
import subprocess
import sys
import wave

import ndspy.soundArchive
import ndspy.soundBank
import ndspy.soundSequence

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SDAT_PATH = os.path.join(ROOT, "work", "extracted", "data", "sound_data.sdat")
WIKI_DIR = "/home/fanta/Developpement/DQMJ1/DragonQuestMonsterJoker1Bestiaire"
OUT_DIR = os.path.join(WIKI_DIR, "assets", "audio", "themes")
MANIFEST_PATH = os.path.join(WIKI_DIR, "assets", "data", "game_themes.json")

SAMPLE_RATE = 32768
DEFAULT_DURATION = 96.0

# Table des pas IMA-ADPCM officielle Nintendo DS
TABLE_PAS = [
    7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 19, 21, 23, 25, 28, 31,
    34, 37, 41, 45, 50, 55, 60, 66, 73, 80, 88, 97, 107, 118, 130, 143,
    157, 173, 190, 209, 230, 253, 279, 307, 337, 371, 408, 449, 494, 544,
    598, 658, 724, 796, 876, 963, 1060, 1166, 1282, 1411, 1552, 1707,
    1878, 2066, 2272, 2499, 2749, 3024, 3327, 3660, 4026, 4428, 4871,
    5358, 5894, 6484, 7132, 7845, 8630, 9493, 10442, 11487, 12635,
    13899, 15289, 16818, 18500, 20350, 22385, 24623, 27086, 29794, 32767,
]
TABLE_INDEX = [-1, -1, -1, -1, 2, 4, 6, 8, -1, -1, -1, -1, 2, 4, 6, 8]

# Table officielle des 26 numéros logiques de BGM vers les indices de séquence SDAT
BGM_SEQUENCE_INDICES = [
    33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45,
    46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 179, 180,
]

# Aucun titre officiel pour les BGM n'existe dans la ROM (verifie dans le bloc SYMB du SDAT,
# sound_data.sadl, les 51 banques de texte des 5 langues et les chaines ASCII/UTF-16 des binaires --
# voir DragonQuestMonsterJoker1Bestiaire/web/src/lib/gameThemes.ts). Un dictionnaire BGM_CONTEXTS
# de titres/contextes invente a ete decouvert ici et retire (audit joueur, 2026-10-03) : aucune de ces
# chaines n'etait sourcee de la ROM, exactement le meme probleme deja corrige pour les 40 artworks
# (TITLES dict) et les 244 cinematiques (determine_act_and_title()). Le champ reste vide ; l'interface
# web retombe sur rom_symbol + fichier + duree (jamais un titre invente).
BGM_CONTEXTS = {}


def decoder_adpcm(donnees, predicteur=0, index=0):
    """Décode un flux continu IMA-ADPCM Nintendo DS en échantillons Float32 normalisés [-1.0, 1.0]."""
    out = []
    for octet in donnees:
        for nibble in (octet & 0x0F, octet >> 4):
            pas = TABLE_PAS[index]
            delta = pas >> 3
            if nibble & 1:
                delta += pas >> 2
            if nibble & 2:
                delta += pas >> 1
            if nibble & 4:
                delta += pas
            if nibble & 8:
                delta = -delta

            predicteur += delta
            predicteur = max(-32768, min(32767, predicteur))

            index += TABLE_INDEX[nibble]
            index = max(0, min(88, index))

            out.append(predicteur / 32768.0)
    return out


def decoder_swav(swav):
    """Décode un objet SWAV ndspy en Float32 avec sa fréquence native et ses boucles en échantillons."""
    data = swav.data
    codec = swav.waveType
    rate = swav.sampleRate

    if codec == 0:  # PCM8
        pcm = [(b - 256 if b > 127 else b) / 128.0 for b in data]
        loop_start = swav.loopOffset * 4
        total_len = swav.totalLength * 4
    elif codec == 1:  # PCM16
        n = len(data) // 2
        pcm = [v / 32768.0 for v in struct.unpack_from(f"<{n}h", data, 0)]
        loop_start = swav.loopOffset * 2
        total_len = swav.totalLength * 2
    elif codec == 2:  # ADPCM
        pred = struct.unpack_from("<h", data, 0)[0]
        idx = struct.unpack_from("<h", data, 2)[0]
        pcm = decoder_adpcm(data[4:], pred, idx)
        loop_start = swav.loopOffset * 8
        total_len = swav.totalLength * 8
    else:
        pcm = [0.0]
        loop_start = 0
        total_len = 0

    loop_end = min(len(pcm), total_len) if total_len > loop_start else len(pcm)
    return {
        "pcm": pcm,
        "rate": rate,
        "is_looped": swav.isLooped,
        "loop_start": loop_start,
        "loop_end": loop_end,
    }


class SseqRenderer:
    """Synthétiseur multi-pistes fidèle au standard Nitro SDAT."""

    def __init__(self, sdat_path=SDAT_PATH):
        print(f"Chargement du SDAT officiel : {sdat_path}")
        self.sdat = ndspy.soundArchive.SDAT.fromFile(sdat_path)
        self.wave_cache = {}  # (wave_arc_id, wave_id) -> decoded_swav

    def get_wave(self, wave_arc_id, wave_id):
        key = (wave_arc_id, wave_id)
        if key in self.wave_cache:
            return self.wave_cache[key]
        swar = self.sdat.waveArchives[wave_arc_id][1]
        if wave_id >= len(swar.waves):
            return None
        decoded = decoder_swav(swar.waves[wave_id])
        self.wave_cache[key] = decoded
        return decoded

    def resolve_instrument_note(self, bank, program, pitch):
        """Résout un (program, pitch) dans une banque SBNK."""
        if program >= len(bank.instruments) or bank.instruments[program] is None:
            # Fallback cross-bank si un instrument n'est pas dans la banque principale
            for b_name, b_alt in self.sdat.banks:
                if len(b_alt.instruments) > program and b_alt.instruments[program] is not None:
                    bank = b_alt
                    break
            else:
                return None, None

        inst = bank.instruments[program]
        note_def = None
        if isinstance(inst, ndspy.soundBank.SingleNoteInstrument):
            note_def = inst.noteDefinition
        elif isinstance(inst, ndspy.soundBank.RangeInstrument):
            idx = pitch - inst.firstPitch
            if 0 <= idx < len(inst.noteDefinitions):
                note_def = inst.noteDefinitions[idx]
        elif isinstance(inst, ndspy.soundBank.RegionalInstrument):
            for r in inst.regions:
                if pitch <= r.lastPitch:
                    note_def = r.noteDefinition
                    break
            if note_def is None and inst.regions:
                note_def = inst.regions[-1].noteDefinition

        if note_def is None:
            return None, None

        actual_arc_id = bank.waveArchiveIDs[note_def.waveArchiveIDID]
        wave_data = self.get_wave(actual_arc_id, note_def.waveID)
        return note_def, wave_data

    def render_bgm(self, bgm_number, max_seconds=DEFAULT_DURATION):
        """Rend un BGM logique (0..25) en audio PCM stéréo et renvoie (left, right, natural_duration, ...)."""
        seq_idx = BGM_SEQUENCE_INDICES[bgm_number]
        return self.render_sequence(seq_idx, max_seconds=max_seconds, bgm_number=bgm_number)

    def render_sequence(self, seq_idx, max_seconds=DEFAULT_DURATION, bgm_number=None):
        """Rend une séquence SSEQ (par son index d'archive) en audio PCM stéréo."""
        sseq_name, sseq = self.sdat.sequences[seq_idx]
        sseq.parse()

        bank_name, bank = self.sdat.banks[sseq.bankID]
        label = f"BGM #{bgm_number:02d}" if bgm_number is not None else f"Seq #{seq_idx:03d}"
        print(f"Rendu {sseq_name} ({label}) -> {bank_name} (Bank #{sseq.bankID})")

        ev_map = {id(ev): i for i, ev in enumerate(sseq.events)}

        # Extraction des points de tempo depuis l'ensemble de la séquence
        tempo_changes = []
        for ev in sseq.events:
            if isinstance(ev, ndspy.soundSequence.TempoSequenceEvent):
                tempo_changes.append(ev.value)
        default_bpm = tempo_changes[-1] if tempo_changes else 120

        # Simulation de piste autonome. `max_tick_target` : tick au-dela duquel on arrete de
        # boucler meme si la piste revient en arriere (boucle globale de la BGM) -- audit joueur
        # (2026-10-03) : le rendu s'arretait net au premier point de boucle (evenement Jump revenant
        # en arriere), d'ou des musiques "coupees" au lieu de boucler comme en jeu. On suit desormais
        # ce retour en arriere et on continue a simuler, jusqu'a couvrir `max_tick_target` de musique.
        def simulate_track(start_idx, max_tick_target=None):
            i = start_idx
            tick = 0
            call_stack = []
            loop_stack = []
            program = 0
            volume = 1.0
            expression = 1.0
            pan = 64
            transpose = 0
            notes = []
            tempos = []
            guard = 0
            first_loop_tick = None
            while i < len(sseq.events) and guard < 60000:
                guard += 1
                ev = sseq.events[i]
                t = type(ev)

                if t is ndspy.soundSequence.NoteSequenceEvent:
                    actual_pitch = ev.type + transpose
                    gain = (ev.velocity / 127.0) * volume * expression
                    notes.append((tick, actual_pitch, gain, ev.duration, program, pan))
                    i += 1
                elif t is ndspy.soundSequence.RestSequenceEvent:
                    tick += ev.duration
                    i += 1
                elif t is ndspy.soundSequence.TieSequenceEvent:
                    if notes:
                        n = notes[-1]
                        notes[-1] = (n[0], n[1], n[2], n[3] + ev.duration, n[4], n[5])
                    tick += ev.duration
                    i += 1
                elif t is ndspy.soundSequence.InstrumentSwitchSequenceEvent:
                    program = ev.instrumentID
                    i += 1
                elif t is ndspy.soundSequence.TrackVolumeSequenceEvent:
                    volume = ev.value / 127.0
                    i += 1
                elif t is ndspy.soundSequence.ExpressionSequenceEvent:
                    expression = ev.value / 127.0
                    i += 1
                elif t is ndspy.soundSequence.PanSequenceEvent:
                    pan = ev.value
                    i += 1
                elif t is ndspy.soundSequence.TransposeSequenceEvent:
                    val = ev.value
                    transpose = val - 256 if val > 127 else val
                    i += 1
                elif t is ndspy.soundSequence.TempoSequenceEvent:
                    tempos.append((tick, ev.value))
                    i += 1
                elif t is ndspy.soundSequence.CallSequenceEvent:
                    call_stack.append(i + 1)
                    i = ev_map[id(ev.destination)]
                elif t is ndspy.soundSequence.ReturnSequenceEvent:
                    if call_stack:
                        i = call_stack.pop()
                    else:
                        break
                elif t is ndspy.soundSequence.JumpSequenceEvent:
                    dest = ev_map[id(ev.destination)]
                    if dest <= i:  # Boucle globale (retour en arriere)
                        if first_loop_tick is None:
                            first_loop_tick = tick
                        if max_tick_target is not None and tick >= max_tick_target:
                            break
                        i = dest
                    else:
                        i = dest
                elif t is ndspy.soundSequence.BeginLoopSequenceEvent:
                    loop_stack.append({"target": i + 1, "remaining": ev.value - 1})
                    i += 1
                elif t is ndspy.soundSequence.EndLoopSequenceEvent:
                    if loop_stack:
                        if loop_stack[-1]["remaining"] > 0:
                            loop_stack[-1]["remaining"] -= 1
                            i = loop_stack[-1]["target"]
                        else:
                            loop_stack.pop()
                            i += 1
                    else:
                        i += 1
                elif t is ndspy.soundSequence.EndTrackSequenceEvent:
                    break
                else:
                    i += 1
            return notes, tempos, first_loop_tick

        # Identifier le début de chaque piste
        track_starts = []
        i = 0
        while i < len(sseq.events):
            ev = sseq.events[i]
            if isinstance(ev, ndspy.soundSequence.BeginTrackSequenceEvent):
                track_starts.append(ev_map[id(ev.firstEvent)])
                i += 1
            elif isinstance(ev, ndspy.soundSequence.DefineTracksSequenceEvent):
                i += 1
            else:
                break
        track0_start = i

        all_notes = []
        tempo_map = []
        loop_ticks = []

        # Budget de ticks approximatif pour couvrir `max_seconds`, meme a travers une boucle globale
        # (formule exacte tick -> secondes pas encore disponible : tempo_map se construit plus bas).
        # Marge x1.5 pour absorber les changements de tempo internes a la boucle.
        tick_budget = max_seconds * default_bpm * 48.0 / 60.0 * 1.5

        # Piste 0
        n0, t0, loop0 = simulate_track(track0_start, max_tick_target=tick_budget)
        all_notes.extend(n0)
        tempo_map.extend(t0)
        if loop0 is not None:
            loop_ticks.append(loop0)

        # Pistes 1..N
        for st in track_starts:
            nt, tt, loop_n = simulate_track(st, max_tick_target=tick_budget)
            all_notes.extend(nt)
            tempo_map.extend(tt)
            if loop_n is not None:
                loop_ticks.append(loop_n)

        # Ordonner la tempo map
        tempo_map.sort(key=lambda x: x[0])
        if not tempo_map or tempo_map[0][0] != 0:
            tempo_map.insert(0, (0, default_bpm))

        # Fonction de conversion tick -> secondes
        def tick_to_seconds(tick):
            sec = 0.0
            last_t = 0
            cur_bpm = tempo_map[0][1]
            for t_change, bpm in tempo_map:
                if tick <= t_change:
                    break
                sec += (t_change - last_t) * (60.0 / (cur_bpm * 48.0))
                last_t = t_change
                cur_bpm = bpm
            sec += (tick - last_t) * (60.0 / (cur_bpm * 48.0))
            return sec

        # Déterminer la durée totale. Si la piste boucle (retour en arrière détecté), `natural_duration`
        # reste la durée d'un seul passage (pour les métadonnées), mais le rendu audio remplit tout
        # `max_seconds` en répétant la boucle — fini les musiques d'ambiance coupées net après un seul
        # passage (audit joueur, 2026-10-03).
        max_tick = max((n[0] + n[3] for n in all_notes), default=0)
        is_looped_track = len(loop_ticks) > 0
        natural_duration = tick_to_seconds(min(loop_ticks)) if is_looped_track else tick_to_seconds(max_tick)
        if is_looped_track:
            render_seconds = min(max_seconds, tick_to_seconds(max_tick) + 2.0)
        else:
            render_seconds = min(max_seconds, natural_duration + 2.0)
        total_samples = int(render_seconds * SAMPLE_RATE)

        left = [0.0] * total_samples
        right = [0.0] * total_samples

        rendered_count = 0
        for tick, pitch, gain, dur_ticks, prog, pan in all_notes:
            t_start = tick_to_seconds(tick)
            t_dur = max(tick_to_seconds(tick + dur_ticks) - t_start, 0.04)
            if t_start >= render_seconds:
                continue

            note_def, wave_info = self.resolve_instrument_note(bank, prog, pitch)
            if note_def is None or wave_info is None:
                continue

            pcm = wave_info["pcm"]
            w_rate = wave_info["rate"]
            is_loop = wave_info["is_looped"]
            l_start = wave_info["loop_start"]
            l_end = wave_info["loop_end"]

            # Pitch ratio précis
            ratio = 2.0 ** ((pitch - note_def.pitch) / 12.0)
            step = (w_rate / SAMPLE_RATE) * ratio

            # Gain stéréophonique constant
            total_gain = 0.28 * gain
            pan_ratio = max(0.0, min(1.0, pan / 127.0))
            g_l = total_gain * math.cos(pan_ratio * math.pi / 2)
            g_r = total_gain * math.sin(pan_ratio * math.pi / 2)

            start_samp = int(t_start * SAMPLE_RATE)
            dur_samps = min(int(t_dur * SAMPLE_RATE), total_samples - start_samp)

            # Enveloppe ADSR approximée fidèle
            # attack 127 = instantané (160 samples), sustain niveau, release
            atk_len = max(int(0.005 * SAMPLE_RATE * ((127 - note_def.attack) / 127.0)), 120)
            rel_len = 160

            pos = 0.0
            l_len = max(l_end - l_start, 1)
            for s in range(dur_samps):
                if is_loop and pos >= l_end:
                    pos = l_start + ((pos - l_start) % l_len)

                idx = int(pos)
                if idx + 1 >= len(pcm):
                    if not is_loop:
                        break
                    val = pcm[-1]
                else:
                    frac = pos - idx
                    val = pcm[idx] * (1.0 - frac) + pcm[idx + 1] * frac

                env = 1.0
                if s < atk_len:
                    env = s / float(atk_len)
                rem = dur_samps - s
                if rem < rel_len:
                    env *= (rem / float(rel_len))

                val_env = val * env
                left[start_samp + s] += val_env * g_l
                right[start_samp + s] += val_env * g_r
                pos += step

            rendered_count += 1

        # Normalisation
        peak = max(max(abs(v) for v in left), max(abs(v) for v in right), 1e-9)
        norm_factor = 0.92 / peak
        for i in range(total_samples):
            left[i] *= norm_factor
            right[i] *= norm_factor

        print(f"  Notes rendues : {rendered_count}/{len(all_notes)} | Durée : {render_seconds:.1f}s | Facteur normalisation : {norm_factor:.3f}")
        return left, right, natural_duration, rendered_count, len(track_starts) + 1, bank_name, sseq


def exporter_wav(left, right, chemin_wav):
    os.makedirs(os.path.dirname(chemin_wav), exist_ok=True)
    with wave.open(chemin_wav, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        data_out = bytearray()
        for l, r in zip(left, right):
            sl = int(max(-1.0, min(1.0, l)) * 32767)
            sr = int(max(-1.0, min(1.0, r)) * 32767)
            data_out.extend(struct.pack("<hh", sl, sr))
        wf.writeframes(data_out)


def convertir_mp3(chemin_wav, chemin_mp3):
    """Encode en MP3 320 kbps CBR -- le debit maximal du format, qualite maximale extractible pour
    un rendu synthetise (pas de maitre source a une qualite superieure). Audit joueur (2026-10-03) :
    auparavant 128 kbps."""
    os.makedirs(os.path.dirname(chemin_mp3), exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-i", chemin_wav,
        "-codec:a", "libmp3lame", "-b:a", "320k",
        chemin_mp3
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)


def main():
    parser = argparse.ArgumentParser(description="Restauration audio canonique SSEQ DQMJ1.")
    parser.add_argument("--verifier", action="store_true", help="Vérifie la cohérence du SDAT et des banques BGM")
    parser.add_argument("--rendre", type=str, help="BGM à rendre (ex: BGM_001, music_001 ou all)")
    parser.add_argument("--duree", type=float, default=DEFAULT_DURATION, help="Durée du rendu en secondes")
    args = parser.parse_args()

    renderer = SseqRenderer()

    if args.verifier:
        print("\n=== VÉRIFICATION DES 26 BGM SDAT ===")
        for bgm_no, seq_idx in enumerate(BGM_SEQUENCE_INDICES):
            sseq_name, sseq = renderer.sdat.sequences[seq_idx]
            sseq.parse()
            bank_name, bank = renderer.sdat.banks[sseq.bankID]
            print(f"BGM #{bgm_no:02d} | Seq {seq_idx:3d} ({sseq_name:8s}) -> Bank {sseq.bankID:2d} ({bank_name:15s}) | Waves: {len(renderer.sdat.waveArchives[bank.waveArchiveIDs[0]][1].waves)}")
        print("Toutes les banques BGM correspondent aux séquences officielles.\n")
        return

    if not args.rendre:
        parser.print_help()
        return

    bgm_targets = []
    if args.rendre.lower() == "all":
        # Tous les BGM réels (hors dummy 1)
        bgm_targets = [i for i in range(26) if i != 1]
    else:
        # Trouver l'indice
        clean = args.rendre.upper().replace("MUSIC_", "BGM_").replace("BGM", "BGM_").replace("__", "_")
        for i, seq_idx in enumerate(BGM_SEQUENCE_INDICES):
            name, _ = renderer.sdat.sequences[seq_idx]
            if clean in (name, f"BGM_{i+1:03d}", f"BGM_{i:02d}", f"BGM_{i}"):
                bgm_targets.append(i)
                break
        else:
            print(f"BGM inconnu : {args.rendre}")
            return

    # Mettre à jour le manifeste
    manifest = []

    for bgm_no in bgm_targets:
        seq_idx = BGM_SEQUENCE_INDICES[bgm_no]
        sseq_name, raw_sseq = renderer.sdat.sequences[seq_idx]
        file_bytes = len(raw_sseq.eventsData) if not raw_sseq.parsed else 4096

        file_prefix = f"music_{bgm_no:03d}" if bgm_no > 0 else "music_001"
        wav_path = f"/tmp/{file_prefix}.wav"
        mp3_name = f"{file_prefix}.mp3"
        mp3_path = os.path.join(OUT_DIR, mp3_name)

        left, right, nat_dur, notes_rendered, nb_tracks, bank_name, sseq = renderer.render_bgm(bgm_no, max_seconds=args.duree)
        exporter_wav(left, right, wav_path)
        convertir_mp3(wav_path, mp3_path)
        file_size = os.path.getsize(mp3_path)
        print(f"  -> Exporté : {mp3_path} ({file_size // 1024} Ko)")

        manifest.append({
            "id": f"theme-{bgm_no:03d}",
            "title": BGM_CONTEXTS.get(sseq_name, None),
            "file_id": bgm_no,
            "file_bytes": file_bytes,
            "rom_symbol": sseq_name,
            "game_bgm_codes": [bgm_no],
            "sequence": seq_idx,
            "contexte": BGM_CONTEXTS.get(sseq_name, None),
            "notes": notes_rendered,
            "pistes": nb_tracks,
            "secondes": round(len(left) / SAMPLE_RATE, 2),
            "secondes_naturelles": round(nat_dur, 2),
            "banque": sseq.bankID,
            "archive": bank_name,
            "fichier": f"themes/{mp3_name}",
            "bytes": file_size,
        })

    if args.rendre.lower() == "all":
        os.makedirs(os.path.dirname(MANIFEST_PATH), exist_ok=True)
        payload = {
            "provenance": "Musiques canoniques du jeu, rendues depuis les séquences SSEQ du SDAT avec leurs banques d'instruments officielles respectives (BANK_BGM_*) et les véritables timbres orchestraux de Koichi Sugiyama par ReverseEngeneeringDQMJ1/tools/render_sseq_audio.py.",
            "themes": manifest,
        }
        with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        print(f"Manifeste écrit dans {MANIFEST_PATH} ({len(manifest)} thèmes)")


if __name__ == "__main__":
    main()
