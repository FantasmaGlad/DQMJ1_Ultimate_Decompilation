#!/usr/bin/env python3
"""Extrait les sorts/bonus débloqués par palier de compétence, pour les 128
panneaux dont une page dédiée existe sur le wiki communautaire
dragon-quest.org — item 17 de docs/DATA_RESEARCH_PLAN.md du projet
bestiaire.

## Provenance et niveau de confiance (session du 2026-09-25, suite 22)

**Sourcé wiki, PAS extrait de la ROM ni confirmé par désassemblage** (les
240 octets internes de chaque entrée de `SkillTbl.bin` ne sont toujours pas
décodés — voir item 15/17). Source : catégorie "Dragon Quest Monsters: Joker
skill sets" de dragon-quest.org (122 pages), complétée par une recherche
ciblée pour 6 pages "élément + Ward" supplémentaires non catégorisées
pareil (`<Élément> Ward (Talent)`) — 128 pages au total, mises en cache
localement (`work/extracted/data/wiki_cache/dq_org_skillsets/` et
`dq_org_skillsets_wards/`, `action=parse&prop=wikitext`, User-Agent
navigateur nécessaire — l'API renvoie 403 sans).

**Deux formats de page rencontrés, tous deux gérés** :
1. Panneaux génériques (classes, éléments, capacités) : titres `===Nom===`,
   `===Nom II===`, `===Nom III===` chacun suivi d'un tableau wiki
   `{| ... |}` à 2 colonnes (Capacité, Points).
2. Panneaux de "Talent" (compétences uniques de boss/personnages, ex.
   Estark, Rhapthorne) : gabarit `{{Spell Infobox}}` avec une section par
   jeu (`=={{DQMJ}}==` ou `==={{DQMJ}}===`) — seule la section `{{DQMJ}}`
   (Joker 1, notre jeu) est extraite, `{{DQMJ2}}`/`{{DQM3}}` ignorées.

**20 panneaux "Ward" élémentaires/de statut cités dans `skills.json`
n'ont PAS de page individuelle trouvée sur ce wiki** (`Antimagic Ward`,
`Confusion Ward`, `Poison Ward`... — recherche par titre exact et par le
moteur de recherche du wiki, aucune page trouvée pour 14 des 20 ; seuls les
6 correspondant aux éléments de sort de base — Frizz/Bang/Woosh/Crack/
Zap/Zam Ward — existent). Ces 14 restent non couverts : **rien publié pour
eux plutôt que deviner**.

**Correction d'une erreur de données de la session précédente** : la
première extraction manuelle de "Frizz & Bang" (7 panneaux publiés le
2026-09-25) contenait des noms de sorts incorrects pour les paliers 1 et 3
(comparaison octet à octet avec le wikitext brut actuel du wiki source, qui
ne correspondait pas du tout — probablement une erreur de transcription de
cette session-là, pas un changement du wiki). Ce script republie
l'intégralité des 128 panneaux à partir d'une extraction automatisée
directement depuis le wikitext brut mis en cache, éliminant ce risque de
transcription manuelle erronée pour l'avenir. Les coquilles visibles du wiki
source lui-même (ex. "Kafizzle" au lieu de "Kafrizzle" sur la page "Mage")
sont conservées telles quelles — fidélité à la source citée, pas de
correction silencieuse qui ferait croire à une vérification qui n'a pas eu
lieu.
"""
import json
import os
import re

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIRS = [
    os.path.join(RACINE, "work/extracted/data/wiki_cache/dq_org_skillsets"),
    os.path.join(RACINE, "work/extracted/data/wiki_cache/dq_org_skillsets_wards"),
]
SKILLS_PATH = os.path.join(RACINE, "tools/skills.json")


def load_pages():
    pages = {}
    for cache_dir in CACHE_DIRS:
        if not os.path.isdir(cache_dir):
            continue
        for filename in os.listdir(cache_dir):
            with open(os.path.join(cache_dir, filename), encoding="utf-8") as f:
                payload = json.load(f)
            if "parse" not in payload:
                continue
            title = payload["parse"]["title"]
            pages[title] = payload["parse"]["wikitext"]["*"]
    return pages


def find_tables(text):
    return [m.group(0) for m in re.finditer(r"\{\|.*?\n\|\}", text, re.S)]


def parse_table(text):
    rows = []
    for row in text.split("|-"):
        row = row.strip()
        if not row or row.startswith("!"):
            continue
        cells = [c.strip() for c in row.split("||")]
        if len(cells) < 2:
            continue
        name_cell = cells[0].lstrip("|").strip()
        points_cell = cells[1].strip()
        m = re.match(r"^\[\[([^\]|]+)(\|([^\]]+))?\]\]$", name_cell)
        if m:
            name = m.group(3) or m.group(1)
        else:
            name = re.sub(
                r"\[\[([^\]|]+)(\|([^\]]+))?\]\]",
                lambda mm: mm.group(3) or mm.group(1),
                name_cell,
            )
            name = re.sub(r"'''?", "", name).strip()
        name = re.sub(r"<[^>]+>", "", name).strip()
        points_match = re.search(r"\d+", points_cell)
        if not points_match:
            continue
        if name:
            rows.append({"points": int(points_match.group(0)), "name": name})
    return rows


def extract_generic(wikitext):
    heading_re = re.compile(r"^===\s*([^=]+?)\s*===\s*$", re.M)
    headings = list(heading_re.finditer(wikitext))
    if not headings:
        return None
    tiers = []
    for i, heading in enumerate(headings):
        start = heading.end()
        end = headings[i + 1].start() if i + 1 < len(headings) else len(wikitext)
        tables = find_tables(wikitext[start:end])
        if not tables:
            continue
        unlocks = parse_table(tables[0])
        if unlocks:
            tiers.append(unlocks)
    return tiers or None


def extract_talent(wikitext):
    m = re.search(r"={2,3}\s*\{\{DQMJ\}\}\s*={2,3}(.*?)(?=\n={2,3}[^=]|\Z)", wikitext, re.S)
    if not m:
        return None
    tables = find_tables(m.group(1))
    if not tables:
        return None
    unlocks = parse_table(tables[0])
    return [unlocks] if unlocks else None


def extract_single(wikitext):
    tables = find_tables(wikitext)
    if len(tables) != 1:
        return None
    unlocks = parse_table(tables[0])
    return [unlocks] if unlocks else None


def strip_title_suffix(title):
    return re.sub(r"\s*\((skill|Skill|skillset|Talent)\)\s*$", "", title).strip()


def main():
    pages = load_pages()
    with open(SKILLS_PATH, encoding="utf-8") as f:
        skills = json.load(f)

    by_base = {}
    for s in skills.values():
        by_base.setdefault(s["base_name"], {})[s["tier"]] = s["name_display_en"]

    result = {}
    unresolved = []

    for title, wikitext in pages.items():
        base = strip_title_suffix(title)
        if base not in by_base:
            continue

        tier_sections = extract_talent(wikitext) or extract_generic(wikitext) or extract_single(wikitext)
        if not tier_sections:
            unresolved.append(title)
            continue

        max_tier = max(by_base[base].keys())
        tiers_out = []
        for idx, unlocks in enumerate(tier_sections, start=1):
            if idx > max_tier:
                break
            tiers_out.append(
                {
                    "tier": idx,
                    "points_to_master": max(u["points"] for u in unlocks),
                    "unlocks": unlocks,
                }
            )
        if tiers_out:
            result[base] = {"tiers": tiers_out}

    result["_provenance"] = (
        "Sourcé du wiki communautaire dragon-quest.org (catégorie \"Dragon Quest "
        "Monsters: Joker skill sets\" + 6 pages \"<élément> Ward (Talent)\" trouvées "
        "séparément), recherche web autorisée par le propriétaire le 2026-09-25 — "
        "PAS extrait de la ROM ni confirmé par désassemblage. Voir "
        "docs/DATA_RESEARCH_PLAN.md item 17. Clé = nom réel du panneau "
        "(base_name dans skills.json). Couverture : 128/142 panneaux distincts — "
        "14 panneaux \"Ward\" (altérations de statut/éléments composés) n'ont "
        "aucune page dédiée trouvée sur ce wiki, volontairement absents plutôt "
        "que devinés. Remplace intégralement une extraction manuelle antérieure "
        "du 2026-09-25 dont le panneau \"Frizz & Bang\" contenait des noms "
        "incorrects pour 2 des 3 paliers (erreur corrigée par cette extraction "
        "automatisée directement depuis le wikitext brut mis en cache)."
    )

    missing_bases = sorted(set(by_base.keys()) - set(result.keys()) - {"_provenance"})

    out_file = os.path.join(RACINE, "tools/skill_tiers_wiki.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)

    print(f"Panneaux publiés : {len(result) - 1}")
    print(f"Pages sans table exploitable : {unresolved}")
    print(f"Panneaux sans page wiki trouvée ({len(missing_bases)}): {missing_bases}")


if __name__ == "__main__":
    main()
