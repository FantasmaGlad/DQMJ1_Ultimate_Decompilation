#!/usr/bin/env python3
"""Extrait les listes de stock des boutiques (overlay_0000.bin) vers assets/data/shop_stock.json.

Structure prouvee par desassemblage de FUN_02194088 (overlay_0000, 0x02194088), qui construit le stock
affiche par l'ecran de boutique :
  - table de 11 enregistrements de 16 octets a 0x021de0a8 (pointeur en 0x021941ac) :
      +0  u32 cle (octet compare a la valeur renvoyee par 0x02054650 = octet 0x0216f440)
      +4  pointeur vers les bornes basses de progression (octets ; pointeur bss = zeros = 0)
      +8  pointeur vers les bornes hautes de progression (octets)
      +12 pointeur vers la liste d'item_id (octets, terminee par 0)
  - un objet i est vendu quand borne_basse[i] <= P <= borne_haute[i], P = getter 0x0203ad74(0) = octet 0 du
    tableau d'etat 0x0209a2ec ;
  - choix de l'enregistrement : cle 0 -> enregistrement 0 ; cle 2 -> selon l'octet *0x021941a8 :
    0 -> 3, 1 -> 5, 3 -> 10, sinon 4 ; autre cle -> premier enregistrement portant cette cle.
NON prouve : ce que designent la cle et l'octet secondaire pour une boutique donnee du jeu (quelle carte,
quel batiment) ; la nature exacte de P (compteur d'avancement de 0 a 29).
"""
import json, os, struct

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BESTIAIRE = os.path.join(os.path.dirname(RACINE), "DragonQuestMonsterJoker1Bestiaire")
BASE = 0x02184B40
TABLE = 0x021DE0A8
N = 11
# choix de l'enregistrement pour la cle 2 (code de FUN_02194088)
SOUS_CLE = {0: 3, 1: 5, 3: 10}
SOUS_CLE_AUTRE = 4


def main():
    b = open(os.path.join(RACINE, "work/extracted/overlay/overlay_0000.bin"), "rb").read()
    items = json.load(open(os.path.join(BESTIAIRE, "assets/data/items.json"), encoding="utf-8"))
    items = {i["item_id"]: i for i in (items if isinstance(items, list) else items.get("items", list(items.values())))}
    ok = lambda p: BASE <= p < BASE + len(b)
    fo = lambda p: p - BASE

    first_by_key = {}
    records = []
    for k in range(N):
        key, mn, mx, its = struct.unpack_from("<IIII", b, fo(TABLE) + 16 * k)
        first_by_key.setdefault(key, k)
        rows = []
        if ok(its):
            i = 0
            while b[fo(its) + i] != 0:
                v = b[fo(its) + i]
                lo = b[fo(mn) + i] if ok(mn) else 0
                hi = b[fo(mx) + i] if ok(mx) else 0xFF
                it = items.get(v)
                rows.append({"item_id": v, "name_en": it["name_en"] if it else None, "name_fr": it["name_fr"] if it else None,
                             "price": it["buy_price"] if it else None, "progress_min": lo, "progress_max": hi})
                i += 1
        records.append({"record": k, "key": key, "items": rows})

    reach = {}
    for k, r in enumerate(records):
        if r["key"] == 2:
            reach[k] = next((f"key 2, secondary byte {s}" for s, t in SOUS_CLE.items() if t == k), "key 2, any other secondary byte" if k == SOUS_CLE_AUTRE else None)
        elif r["key"] == 0:
            reach[k] = None
        else:
            reach[k] = f"key {r['key']}" if first_by_key[r["key"]] == k else None
    for k, r in enumerate(records):
        r["selected_when"] = reach[k]

    out = {
        "provenance": "ROM : overlay_0000.bin, table a 0x021de0a8 lue par FUN_02194088 (voir tools/extract_shop_stocks.py)",
        "note": "Quelle boutique du jeu utilise quel enregistrement n'est pas prouve ; progress = octet 0 du tableau d'etat 0x0209a2ec (0 a 29).",
        "records": records,
    }
    dest = os.path.join(BESTIAIRE, "assets/data/shop_stock.json")
    json.dump(out, open(dest, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(dest, sum(len(r["items"]) for r in records), "lignes")


if __name__ == "__main__":
    main()
