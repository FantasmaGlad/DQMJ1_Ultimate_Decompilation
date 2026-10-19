#!/usr/bin/env python3
"""Explorateur de scripts d'evenements (.evt) : machine a pile, deux branches a chaque condition.

Semantique (desassemblee dans overlay_0000, dispatcheur FUN_021c9824) :
  instruction = TLV (u32 type, u32 longueur totale) apres l'en-tete de 4096 o (table des points d'entree, u32,
  0xFFFFFFFF = aucun) ; operandes = (nature, valeur flottante) ; nature 0 = variable, 1 = argument, 2 = litteral ;
  0x15 affectation dest := src ; 0x0c saut ; 0x0d/0x0e saut conditionnel (les deux branches sont explorees) ;
  0x09 appel ; 0x02 retour ; 0xaa commentaire japonais (cp932). Cibles de saut = decalage depuis le debut du flux
  (fichier - 0x1004).
explore() renvoie ({opcode: {(8 arguments courants)}}, contextes, nombre de pas) pour les opcodes de `watch`.
"""
import collections, struct

def load(f):
    d = open(f, "rb").read(); o = 4 + 0x1000; seq = []
    while o + 8 <= len(d):
        t, l = struct.unpack_from("<II", d, o)
        if l < 8: break
        seq.append((o - 0x1004, t, d[o + 8:o + l])); o += l
    return d, seq

def explore(seq, entries, watch=(0x62,), maxsteps=3_000_000):
    """Etat = (variables suivies, arguments, pile d'appels). Toutes les variables recevant un litteral sont suivies."""
    idx_of = {o: i for i, (o, t, p) in enumerate(seq)}
    res = collections.defaultdict(set)
    ctx = collections.defaultdict(set)
    comment_before = []; last = ""
    for o, t, p in seq:  # commentaire japonais (0xaa) le plus proche avant chaque instruction, dans l'ordre du fichier
        if t == 0xaa: last = p.split(b"\0")[0].decode("cp932", "replace")
        comment_before.append(last)
    seen = set(); steps = 0
    E = ((), (None,) * 8, ())
    st = [(0,) + E] + [(idx_of[e],) + E for e in entries if e in idx_of]
    while st and steps < maxsteps:
        i, vars_, args, stack = st.pop()
        while i < len(seq):
            key = (i, vars_, args, stack)
            if key in seen: break
            seen.add(key); steps += 1
            o, t, p = seq[i]
            if t == 0x15 and len(p) == 16:
                dk, di, sk, sv = struct.unpack("<IfIf", p); di = int(di)
                vd = dict(vars_)
                if sk == 2: val = round(sv, 3)
                elif sk == 0: val = vd.get(int(sv))
                else: val = None
                if dk == 0:
                    if val is None: vd.pop(di, None)
                    else: vd[di] = val
                    vars_ = tuple(sorted(vd.items()))
                elif dk == 1 and 0 <= di < 8:
                    a = list(args); a[di] = val; args = tuple(a)
            elif t in watch:
                res[t].add(tuple(args))
                ctx[(t, tuple(args))].add(comment_before[i])
            elif t == 0xc:
                tgt = struct.unpack("<I", p[:4])[0]
                if tgt in idx_of: i = idx_of[tgt]; continue
                break
            elif t in (0xd, 0xe):
                tgt = struct.unpack("<I", p[:4])[0]
                if tgt in idx_of: st.append((idx_of[tgt], vars_, args, stack))
            elif t == 0x9:
                tgt = struct.unpack("<I", p[:4])[0]
                if tgt in idx_of: stack = stack + (i + 1,); i = idx_of[tgt]; continue
                break
            elif t == 0x2:
                if stack: i = stack[-1]; stack = stack[:-1]; continue
                break
            i += 1
    return res, ctx, steps

