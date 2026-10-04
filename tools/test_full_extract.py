import glob, struct, os, json

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(RACINE, "work/extracted/data")

CHAR_MAP_LOCALIZED = {
    **{i: str(i) for i in range(0, 10)},
    0x0A: " ",
    **{0x0B + i: chr(ord("A") + i) for i in range(26)},
    **{0x25 + i: chr(ord("a") + i) for i in range(26)},
    0x43: "Ç", 0x45: "É", 0x49: "Í", 0x4E: "Ñ", 0x50: "Ó", 0x54: "Ú",
    0x55: "Ü", 0x56: "à", 0x57: "á", 0x58: "à", 0x59: "â", 0x5A: "ä",
    0x5B: "ê", 0x5C: "é", 0x5D: "è", 0x5E: "ë", 0x5F: "ç",
    0x60: "í", 0x61: "î", 0x62: "ï", 0x63: "ô", 0x65: "ñ", 0x67: "ô",
    0x68: "ö", 0x6C: "ù", 0x6D: "û", 0x6E: "ü", 0x6F: "ß",
    0x70: "!", 0x71: "?", 0x73: "¡", 0x74: "¿", 0x87: "+",
    0x8D: "II", 0x8E: "III", 0x97: "«", 0x98: "»",
    0x9A: "‘", 0x9B: "’", 0xAC: ".", 0xAD: "&", 0xCC: "-", 0xCD: ",", 0xC9: "!", 0xCE: "?",
    0xFE: " ",
}

def clean_text(payload: bytes) -> str:
    p = payload.split(b"\xff")[0]
    out = []
    for b in p:
        out.append(CHAR_MAP_LOCALIZED.get(b, f"[{b:02x}]"))
    t = "".join(out).strip()
    while t.endswith("-"):
        t = t[:-1]
    return t.strip()

def parse_fpk(data: bytes):
    if len(data) < 8 or data[:4] != b"FPK\x00": return {}
    count = struct.unpack("<I", data[4:8])[0]
    entries = {}
    for i in range(count):
        entry = data[8 + i*40 : 8 + (i+1)*40]
        name = entry[:32].split(b"\x00")[0].decode("latin1", errors="replace")
        offset, size = struct.unpack("<II", entry[32:40])
        entries[name] = data[offset : offset + size]
    return entries

def parse_scr(ev_data: bytes):
    if len(ev_data) < 4100 or ev_data[:4] != b"SCR\x00": return 0, [], [], []
    cursor = 4100
    file_len = len(ev_data)
    dialogues, comments, audio_triggers = [], [], []
    instructions_count = 0
    current_speaker = ""
    while cursor + 8 <= file_len:
        opcode, length = struct.unpack_from("<II", ev_data, cursor)
        if length < 8 or cursor + length > file_len: break
        payload = ev_data[cursor + 8 : cursor + length]
        instructions_count += 1
        if opcode == 0xaa:
            comm = payload.split(b"\x00")[0].decode("cp932", errors="replace").strip()
            if comm: comments.append(comm)
        elif opcode == 0x2a:
            current_speaker = clean_text(payload)
        elif opcode == 0x29:
            txt = clean_text(payload)
            if txt: dialogues.append({"speaker": current_speaker or "Inhabitant", "text": txt})
        elif opcode == 0x48 and len(payload) >= 4:
            audio_triggers.append({"type": "bgm", "id": struct.unpack("<I", payload[:4])[0]})
        elif opcode == 0x4a and len(payload) >= 4:
            audio_triggers.append({"type": "sfx", "id": struct.unpack("<I", payload[:4])[0]})
        elif opcode in (0x02, 0x0c):
            current_speaker = ""
        cursor += length
    return instructions_count, comments, dialogues, audio_triggers

def parse_pos(pos_data: bytes):
    if len(pos_data) < 8 or pos_data[:4] != b"POS\x00": return [], []
    count = struct.unpack("<I", pos_data[4:8])[0]
    cameras, actors = {}, []
    for i in range(count):
        entry = pos_data[8 + i*72 : 8 + (i+1)*72]
        name = entry[:32].split(b"\x00")[0].decode("latin1", errors="replace")
        x, y, z = struct.unpack("<iii", entry[32:44])
        rx, ry, rz = struct.unpack("<iii", entry[44:56])
        pos_m = [round(x / 4096.0, 2), round(y / 4096.0, 2), round(z / 4096.0, 2)]
        rot_deg = [round(rx / 4096.0 * 360.0 / 65536.0, 1), round(ry / 4096.0 * 360.0 / 65536.0, 1), round(rz / 4096.0 * 360.0 / 65536.0, 1)]
        if name.startswith("eye"):
            s_id = name.replace("eye", "")
            if s_id not in cameras: cameras[s_id] = {}
            cameras[s_id]["eye"] = pos_m
        elif name.startswith("tgt"):
            s_id = name.replace("tgt", "")
            if s_id not in cameras: cameras[s_id] = {}
            cameras[s_id]["target"] = pos_m
        elif name != "world_root":
            actors.append({"identifier": name, "position": pos_m, "rotation": rot_deg})
    cam_shots = []
    for k in sorted(cameras.keys()):
        shot = {"shot_id": k}
        if "eye" in cameras[k]: shot["eye"] = cameras[k]["eye"]
        if "target" in cameras[k]: shot["target"] = cameras[k]["target"]
        cam_shots.append(shot)
    return cam_shots, actors

# Scan all 244 demo files
all_demos = []
total_dialogues_count = 0
total_cameras_count = 0

for idx in range(244):
    demo_id = f"demo{idx:03d}"
    bin_path = os.path.join(DATA_DIR, f"{demo_id}.bin")
    pos_path = os.path.join(DATA_DIR, f"{demo_id}.pos")
    if not os.path.exists(bin_path): continue
    
    with open(bin_path, "rb") as f:
        bin_data = f.read()
    entries = parse_fpk(bin_data)
    
    langs_data = {}
    for code, ext in [("en", "evE"), ("fr", "evF"), ("de", "evD"), ("it", "evI"), ("es", "evS")]:
        key = f"{demo_id}.{ext}"
        if key in entries:
            cnt, comms, dlgs, aud = parse_scr(entries[key])
            langs_data[code] = (cnt, comms, dlgs, aud)
        elif f"{demo_id}.evE" in entries:
            cnt, comms, dlgs, aud = parse_scr(entries[f"{demo_id}.evE"])
            langs_data[code] = (cnt, comms, dlgs, aud)
    
    base_cnt, comments, base_dlgs, audio = langs_data.get("en", (0, [], [], []))
    
    # Multilingual dialogues alignment
    aligned_dialogues = []
    for line_idx in range(len(base_dlgs)):
        line_item = {
            "index": line_idx + 1,
            "speaker": base_dlgs[line_idx]["speaker"],
            "text": {}
        }
        for code in ["en", "fr", "de", "it", "es"]:
            d_list = langs_data.get(code, (0, [], [], []))[2]
            if line_idx < len(d_list):
                line_item["text"][code] = d_list[line_idx]["text"]
            else:
                line_item["text"][code] = base_dlgs[line_idx]["text"]
        aligned_dialogues.append(line_item)
    
    total_dialogues_count += len(aligned_dialogues)
    
    # Parse .pos
    cam_shots, actors = [], []
    if os.path.exists(pos_path):
        with open(pos_path, "rb") as pf:
            cam_shots, actors = parse_pos(pf.read())
    total_cameras_count += len(cam_shots)
    
    all_demos.append({
        "id": demo_id,
        "instructions_count": base_cnt,
        "dialogue_count": len(aligned_dialogues),
        "camera_shots_count": len(cam_shots),
        "actors_count": len(actors),
        "developer_comments": comments
    })

print(f"Extraction terminée pour {len(all_demos)} cinématiques.")
print(f"Total répliques cinématiques alignées : {total_dialogues_count}")
print(f"Total plans de caméra 3D extraits : {total_cameras_count}")
