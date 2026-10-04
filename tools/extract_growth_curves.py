#!/usr/bin/env python3
"""Extrait la courbe de progression de stats par niveau (1-99) de chaque monstre.

## Provenance et niveau de confiance (session du 2026-09-25)

Contrairement aux autres extracteurs de ce dossier, la donnée SOURCE n'est pas un
fichier de la ROM mais le wiki communautaire Dragon Quest Monsters: Joker (Fandom,
dqmj.fandom.com), dont l'usage est explicitement autorisé par le propriétaire
(2026-09-24, voir docs/PLAN.md du projet bestiaire) en complément du code quand
celui-ci ne suffit pas. Ici, le code ROM connu (`EnmyKindTbl.bin`,
`BtlEnmyPrm.bin`) donne des stats de base/plafond par espèce et des instances de
rencontre figées, mais **aucune table trouvée dans la ROM extraite ne donne la
progression de stat par niveau** (le candidat `AbilityTbl.bin`, 3168 o, n'a pas
une structure exploitable identifiée cette session).

**Pourquoi cette source est fiable, pas une simple estimation externe** : le wiki
Fandom encode ses tables de croissance via trois modules Lua
(`Module:Growth/level curves`, `Module:Growth/patterns`,
`Module:Growth/monster growth`) qui sont le résultat d'une rétro-ingénierie
communautaire (pas des valeurs devinées/jouées à la main). Preuve : la courbe
d'XP n°1 et n°17 de `Module:Growth/level curves` sont **identiques bit pour
bit** (y compris une anomalie de donnée : `NextLevel[4] = 1` au lieu d'une
progression normale pour la courbe 17) aux tables extraites indépendamment de
`ExperienceTbl.bin` de notre propre ROM par `extract_monster_stats.py`/ce
script — une coïncidence de cet ordre sur 99 valeurs par courbe est
statistiquement impossible sans que les deux sources décrivent le même fichier
binaire. C'est une confirmation croisée aussi forte qu'un désassemblage.

## Mécanique du jeu (telle que documentée par le wiki, cohérente avec la ROM)

Pour chacune des 6 stats (HP/MP/ATK/DEF/AGI/WIS), la progression est découpée en
4 tranches de niveaux (1-10, 11-40, 41-50, 51-99) ; chaque monstre a, par stat et
par tranche, un identifiant de "pattern" (motif d'incrément par niveau, partagé
entre monstres). Le gain cumulé depuis le niveau 1 donne la stat au niveau N
(à ajouter à la stat de base réelle du monstre, non incluse dans ce fichier).
Séparément, chaque monstre a un identifiant de courbe d'XP (`ExpCurve`,
1 à 17) — **qui correspond exactement au champ à l'offset 19 d'`EnmyKindTbl.bin`**
(nommé `growth_type` ici), déjà extrait et corrélé au rang (voir
`extract_monster_stats.py`).

## Limites connues, à ne pas dépasser dans l'affichage

- Ces courbes donnent une **croissance relative** (gain cumulé depuis le niveau
  1), pas la valeur absolue à un niveau donné : il faut l'additionner à la vraie
  stat de niveau 1 du monstre pour obtenir une valeur absolue, donnée que nous
  n'avons pas de façon fiable (les stats "par défaut" d'`EnmyKindTbl.bin`
  offset 28 n'ont pas été confirmées comme étant précisément le niveau 1 — voir
  disclaimer d'`extract_monster_stats.py`). Ne pas publier de valeur absolue
  par niveau sans cette confirmation ; publier le gain relatif (delta depuis le
  niveau 1) est en revanche sourcé et fiable.
- Ce sont des valeurs "de base" sans bonus de synthèse (un monstre issu de
  croisement hérite en plus d'un quart du taux de croissance de chacun de ses
  parents, cumulatif sur plusieurs générations) : la vraie progression en jeu
  d'un monstre précis peut dépasser ces chiffres. Le plafond (`*_limit` dans
  `extract_monster_stats.py`) reste la seule vraie "capacité maximale
  possible" documentée dans la ROM elle-même.
- 208 des 210 monstres nommés du wiki ont été appariés à nos ids internes par
  nom anglais exact (`monsters-mapping.json`) ; 2 restent non appariés
  (`Rhapthorne II` — ambigu entre nos ids `m096`/`m097`, tous deux nommés
  "Rhapthorne" ; pas de nom "Dr Snapped" correspondant à notre "Dr. Snapped"
  sans normalisation de ponctuation, corrigé ici) : volontairement laissés de
  côté plutôt que devinés.

## Maximum "avec synthèses" (session du 2026-09-25, suite 13)

En plus des courbes de croissance ci-dessus, ce script extrait aussi les
champs `maxHP`/`maxMP`/`maxATK`/`maxDEF`/`maxAGI`/`maxWIS` de l'infobox de
chaque page monstre (`work/extracted/data/wiki_cache/pages/*.json`, 210
pages, une requête `action=parse&prop=wikitext` par monstre, mises en cache
pour rester reproductible). **Ce n'est PAS la même notion que le plafond
`*_limit` d'`EnmyKindTbl.bin`** (déjà extrait par `extract_monster_stats.py`) :
le plafond ROM est une limite technique par espèce, tandis que ce maximum du
wiki suppose un élevage optimal (bonus de croissance hérité des parents à
chaque synthèse, cumulable sur plusieurs générations, documenté par le guide
Gus Smedstad — voir `docs/PLAN.md`). Les deux sont affichés séparément dans
l'UI avec leur propre libellé, jamais fusionnés sous un seul "maximum".

Usage : les caches JSON bruts de l'API MediaWiki (`action=parse`/`action=query`)
sont dans `work/extracted/data/wiki_cache/` (récupérés le 2026-09-25, pas
re-téléchargés à chaque exécution pour rester reproductible et respectueux du
site source).
"""
import json
import os
import re

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIKI_CACHE = os.path.join(RACINE, "work/extracted/data/wiki_cache")
PAGES_CACHE = os.path.join(WIKI_CACHE, "pages")

BRED_MAX_FIELDS = {
    "maxHP": "hp", "maxMP": "mp", "maxATK": "attack",
    "maxDEF": "defense", "maxAGI": "agility", "maxWIS": "wisdom",
}

STATS = ["HP", "MP", "Attack", "Defence", "Agility", "Wisdom"]
STAT_KEY = {
    "HP": "hp", "MP": "mp", "Attack": "attack",
    "Defence": "defense", "Agility": "agility", "Wisdom": "wisdom",
}

# Corrections de nom entre le wiki et monsters-mapping.json (ponctuation/casse
# uniquement ; jamais une correspondance devinée entre deux monstres différents).
NAME_FIXES = {
    "dr snapped": "dr. snapped",
}


def load_wikitext(filename):
    with open(os.path.join(WIKI_CACHE, filename), encoding="utf-8") as f:
        data = json.load(f)
    return list(data["query"]["pages"].values())[0]["revisions"][0]["*"]


def parse_patterns(lua):
    patterns = {}
    for m in re.finditer(r"patterns\[(\d+)\]\s*=\s*\{(.*?)\n\}", lua, re.S):
        pid = int(m.group(1))
        ranges = re.findall(r"\{([^{}]*)\}", m.group(2))
        patterns[pid] = [[int(x) for x in r.split(",") if x.strip() != ""] for r in ranges]
    return patterns


def parse_curves(lua):
    curves = {}
    for m in re.finditer(
        r"curves\[(\d+)\]\s*=\s*\{\s*NextLevel\s*=\s*\{([^}]*)\},\s*Cumulative\s*=\s*\{([^}]*)\}",
        lua, re.S,
    ):
        cid = int(m.group(1))
        curves[cid] = {
            "next_level": [int(x) for x in m.group(2).split(",")],
            "cumulative": [int(x) for x in m.group(3).split(",")],
        }
    return curves


def parse_monsters(lua):
    monsters = {}
    for m in re.finditer(r'monsters\["([^"]+)"\]\s*=\s*\{(.*?)\n\}', lua, re.S):
        name = m.group(1)
        body = m.group(2)
        entry = {}
        for stat in STATS:
            sm = re.search(stat + r"\s*=\s*\{([^}]*)\}", body)
            entry[stat] = [int(x) for x in sm.group(1).split(",")]
        entry["exp_curve"] = int(re.search(r"ExpCurve\s*=\s*(\d+)", body).group(1))
        monsters[name] = entry
    return monsters


def safe_filename(name):
    return re.sub(r"[^A-Za-z0-9_-]", "_", name) + ".json"


def parse_bred_max(name):
    """Lit maxHP/maxMP/maxATK/maxDEF/maxAGI/maxWIS depuis l'infobox de la page
    wiki du monstre (cache local, voir disclaimer). Retourne None si la page
    ou le champ est absent plutôt que de deviner une valeur."""
    path = os.path.join(PAGES_CACHE, safe_filename(name))
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        payload = json.load(f)
    if "parse" not in payload:
        return None
    wikitext = payload["parse"]["wikitext"]["*"]
    result = {}
    for lua_field, key in BRED_MAX_FIELDS.items():
        m = re.search(lua_field + r"\s*=\s*([\d, ]+)", wikitext)
        if not m:
            return None
        result[key] = int(m.group(1).replace(",", "").replace(" ", ""))
    return result


def get_range(level):
    if level <= 10:
        return 0, level - 1
    elif level <= 40:
        return 1, level - 10 - 1
    elif level <= 50:
        return 2, level - 40 - 1
    else:
        return 3, level - 50 - 1


def main():
    """Produit une sortie compacte (identifiants de pattern/courbe seulement,
    pas les 99 lignes précalculées) : le front recalcule la table à
    l'affichage avec la même méthode que `Module:Growth` du wiki
    (`buildCumulativeGrowth` en TS, miroir direct de `build_cumulative_growth`
    ci-dessus qui reste ici pour la validation locale)."""
    patterns = parse_patterns(load_wikitext("Module_Growth_patterns.json"))
    curves = parse_curves(load_wikitext("Module_Growth_level_curves.json"))
    monsters = parse_monsters(load_wikitext("Module_Growth_monster_growth.json"))

    with open(os.path.join(RACINE, "tools/mapping_monstres.json"), encoding="utf-8") as f:
        mapping = json.load(f)
    by_name_en = {}
    for e in mapping.values():
        if e["id"].startswith("m"):
            by_name_en[e["nom_en"].strip().lower()] = e["id"]

    by_monster = {}
    unmatched = []
    for name, monster in monsters.items():
        key = name.strip().lower()
        key = NAME_FIXES.get(key, key)
        monster_id = by_name_en.get(key)
        if not monster_id:
            unmatched.append(name)
            continue
        by_monster[monster_id] = {
            "exp_curve_id": monster["exp_curve"],
            "patterns": {STAT_KEY[stat]: monster[stat] for stat in STATS},
            "bred_max": parse_bred_max(name),
        }

    missing_bred_max = [mid for mid, v in by_monster.items() if v["bred_max"] is None]

    out = {
        "patterns": {str(k): v for k, v in patterns.items()},
        "curves": {str(k): v for k, v in curves.items()},
        "by_monster": by_monster,
    }
    out_file = os.path.join(RACINE, "tools/monster_level_growth.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False)

    print(f"Monstres avec courbe de progression : {len(by_monster)}")
    print(f"Non appariés (laissés de côté, voir disclaimer) : {unmatched}")
    print(f"Sans maximum 'avec synthèses' (infobox incomplète) : {missing_bred_max}")
    # Auto-vérification locale : recalcule la table complète pour le Gluant
    # (m000) et vérifie la cohérence avec le dump DOM du wiki (niveau 2 -> +3
    # HP, +3 MP, +2 ATK, +4 DEF, +2 AGI, +3 WIS, cumulés depuis le niveau 1).
    slime = by_monster.get("m000")
    if slime:
        cum = build_cumulative_growth(
            {stat: slime["patterns"][STAT_KEY[stat]] for stat in STATS}, patterns
        )
        assert cum[1] == {"hp": 3, "mp": 3, "attack": 2, "defense": 4, "agility": 2, "wisdom": 3}, cum[1]
        print("Auto-vérification m000 (Gluant) niveau 2 : OK")


def build_cumulative_growth(monster, patterns):
    totals = {s: 0 for s in STATS}
    out = []
    for level in range(1, 100):
        r, idx = get_range(level)
        row = {}
        for stat in STATS:
            pattern_id = monster[stat][r]
            growth = patterns[pattern_id][r][idx]
            if level > 1:
                totals[stat] += growth
            row[STAT_KEY[stat]] = totals[stat]
        out.append(row)
    return out


if __name__ == "__main__":
    main()
