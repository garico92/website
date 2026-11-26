#!/usr/bin/env python3
"""Build data/publications.yaml for the website from the CV sources.

Single source of truth: the CV folder.
  CV/references.bib                 -> bibliographic data (title, authors, journal, DOI, arXiv, ADS)
  CV/complete_publication_list.tex  -> grouping of each paper (first/corresponding author,
                                       major contribution, other), read from its \\fullcite{...} / \\pubitem{...} keys

Usage (from the repository root):
    python scripts/cv_publications.py            # writes data/publications.yaml
    python scripts/cv_publications.py --check    # only prints what it would write

No dependencies beyond the standard library (PyYAML is used if available, otherwise a
small built-in writer is used).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "CV" / "references.bib"
LIST_TEX = ROOT / "CV" / "complete_publication_list.tex"
OUT = ROOT / "data" / "publications.yaml"

ME = "aricò"  # surname, compared after accent normalisation
MAX_AUTHORS = 6  # authors kept per paper; the page adds "et al." and my position if I come later

# Section headings of complete_publication_list.tex -> role keys used on the website
ROLE_PATTERNS = [
    (re.compile(r"first or corresponding", re.I), "lead"),
    (re.compile(r"second author|major", re.I), "major"),
    (re.compile(r"other publications", re.I), "other"),
    (re.compile(r"in publication|submitted|in prep", re.I), "submitted"),
]

JOURNALS = {
    r"\aap": ("Astronomy & Astrophysics", "A&A"),
    r"\mnras": ("Monthly Notices of the Royal Astronomical Society", "MNRAS"),
    r"\jcap": ("Journal of Cosmology and Astroparticle Physics", "JCAP"),
    r"\apj": ("The Astrophysical Journal", "ApJ"),
    r"\prd": ("Physical Review D", "PRD"),
}
SHORT = {
    "Monthly Notices of the Royal Astronomical Society": "MNRAS",
    "Astronomy and Astrophysics": "A&A",
    "Astronomy & Astrophysics": "A&A",
    "Journal of Cosmology and Astroparticle Physics": "JCAP",
    "The Open Journal of Astrophysics": "OJAp",
    "Open Research Europe": "ORE",
    "The Astrophysical Journal": "ApJ",
    "Physical Review D": "PRD",
}

# ---------------------------------------------------------------------------- LaTeX -> text
ACCENTS = {"`": "\u0300", "'": "\u0301", "^": "\u0302", "~": "\u0303", '"': "\u0308",
           "=": "\u0304", ".": "\u0307", "u": "\u0306", "v": "\u030C", "H": "\u030B", "c": "\u0327"}


def delatex(s: str) -> str:
    s = s.replace("\\i", "i").replace("{\\i}", "i")
    # \'{a}, {\'a}, \'a
    def acc(m):
        mark, ch = m.group(1), m.group(2)
        return unicodedata.normalize("NFC", ch + ACCENTS.get(mark, ""))
    for _ in range(2):
        s = re.sub(r"\{?\\([`'^~\"=.])\{?([A-Za-z])\}?\}?", acc, s)
        s = re.sub(r"\{?\\([uvHc])\{([A-Za-z])\}\}?", acc, s)
    s = re.sub(r"\\ensuremath\{\\Lambda\}", "Λ", s)
    s = s.replace("\\Lambda", "Λ").replace("$", "")
    s = s.replace("\\%", "%").replace("\\&", "&").replace("~", " ")
    s = re.sub(r"\\[a-zA-Z]+\s*", "", s)          # drop remaining commands
    s = s.replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", s).strip()


def fold(s: str) -> str:
    """lower case, no accents: for name comparison."""
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


# ---------------------------------------------------------------------------- tiny bib parser
def parse_bib(text: str) -> dict[str, dict]:
    entries = {}
    i = 0
    while True:
        m = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", re.S).search(text, i)
        if not m:
            break
        kind, key = m.group(1).lower(), m.group(2)
        j = m.end()
        depth, k = 1, j
        while k < len(text) and depth:
            depth += {"{": 1, "}": -1}.get(text[k], 0)
            k += 1
        body = text[j:k - 1]
        entries[key] = {"_type": kind, **parse_fields(body)}
        i = k
    return entries


def parse_fields(body: str) -> dict[str, str]:
    out, i, n = {}, 0, len(body)
    while i < n:
        m = re.compile(r"\s*([A-Za-z_]+)\s*=\s*", re.S).match(body, i)
        if not m:
            i += 1
            continue
        name, i = m.group(1).lower(), m.end()
        if i < n and body[i] == "{":
            depth, k = 1, i + 1
            while k < n and depth:
                depth += {"{": 1, "}": -1}.get(body[k], 0)
                k += 1
            val, i = body[i + 1:k - 1], k
        elif i < n and body[i] == '"':
            k = i + 1
            depth = 0
            while k < n and not (body[k] == '"' and depth == 0):
                depth += {"{": 1, "}": -1}.get(body[k], 0)
                k += 1
            val, i = body[i + 1:k], k + 1
        else:
            k = i
            while k < n and body[k] not in ",\n}":
                k += 1
            val, i = body[i:k].strip(), k
        out[name] = re.sub(r"\s+", " ", val).strip()
    return out


def split_authors(a: str) -> list[str]:
    parts, depth, cur = [], 0, ""
    tokens = re.split(r"(\s+and\s+|[{}])", a)
    for t in tokens:
        if t == "{":
            depth += 1
        elif t == "}":
            depth -= 1
        if depth == 0 and t and re.fullmatch(r"\s+and\s+", t):
            parts.append(cur)
            cur = ""
        else:
            cur += t
    parts.append(cur)
    names = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if "," in delatex(p):
            last, first = [x.strip() for x in delatex(p).split(",", 1)]
        else:
            last, first = delatex(p), ""
        initials = " ".join(w[0] + "." for w in re.split(r"[\s]+", first.replace(".", " ")) if w and w[0].isalpha())
        initials = re.sub(r"(\w)\.-(\w)", r"\1.-\2", initials)
        names.append({"last": last, "first": first, "short": (f"{initials} {last}".strip() if last else first)})
    return names


# ---------------------------------------------------------------------------- roles from the tex list
def roles_from_tex(tex: str) -> dict[str, str]:
    roles, current = {}, "other"
    for line in tex.splitlines():
        line = line.split("%", 1)[0]
        for pat, role in ROLE_PATTERNS:
            if pat.search(line) and "textbf" in line:
                current = role
        for key in re.findall(r"\\(?:fullcite|pubitem)\{([^}]+)\}", line):
            roles.setdefault(key.strip(), current)
    return roles


# ---------------------------------------------------------------------------- build
def build() -> list[dict]:
    bib = parse_bib(BIB.read_text(encoding="utf-8"))
    roles = roles_from_tex(LIST_TEX.read_text(encoding="utf-8")) if LIST_TEX.exists() else {}
    pubs = []
    for key, e in bib.items():
        if e["_type"] not in {"article", "inproceedings", "misc", "unpublished"}:
            continue
        authors = split_authors(e.get("author", ""))
        pos = next((i + 1 for i, a in enumerate(authors) if fold(a["last"]) == fold(ME)), None)
        jraw = e.get("journal", "").strip()
        if jraw in JOURNALS:
            journal, short = JOURNALS[jraw]
        else:
            journal = delatex(jraw)
            short = SHORT.get(journal, journal)
            journal = {"Astronomy and Astrophysics": "Astronomy & Astrophysics"}.get(journal, journal)
        doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", e.get("doi", "")).strip()
        arxiv = e.get("eprint", "").strip()
        ads = e.get("adsurl", "").strip()
        vol, pages = e.get("volume", "").strip(), e.get("pages", "").strip()
        if e.get("eid", "").strip() and not e.get("eid", "").lower().startswith("arxiv"):
            pages = e["eid"].strip()  # article number (e.g. A188) rather than a page count
        if pages.lower().startswith("arxiv"):
            pages = ""
        role = roles.get(key, "lead" if pos == 1 else "other")
        n = len(authors)
        collab = any("collaboration" in a["last"].lower() for a in authors)
        pubs.append({
            "key": key,
            "title": delatex(e.get("title", "")),
            "year": int(re.sub(r"\D", "", e.get("year", "0")) or 0),
            "journal": journal,
            "journal_short": short,
            "volume": vol,
            "pages": pages,
            "doi": doi,
            "arxiv": arxiv,
            "ads": ads,
            "authors": [a["short"] for a in authors[:MAX_AUTHORS]],
            "n_authors": n,
            "me": pos or 0,
            "role": role,
            "collaboration": collab,
        })
    order = {"lead": 0, "major": 1, "other": 2, "submitted": 3}
    pubs.sort(key=lambda p: (-p["year"], order.get(p["role"], 9), p["me"] or 99))
    return pubs


def to_yaml(pubs: list[dict]) -> str:
    try:
        import yaml  # type: ignore
        return yaml.safe_dump({"publications": pubs}, allow_unicode=True, sort_keys=False, width=1000)
    except ImportError:  # JSON is valid YAML
        return json.dumps({"publications": pubs}, ensure_ascii=False, indent=1)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="print a summary, do not write")
    args = ap.parse_args()
    pubs = build()
    head = ("# Generated by scripts/cv_publications.py from CV/references.bib and\n"
            "# CV/complete_publication_list.tex. Do not edit by hand: edit the CV and re-run.\n")
    for p in pubs:
        flag = "" if p["me"] else "   <-- own name not found in author list"
        print(f'{p["year"]} {p["role"]:6s} {p["journal_short"]:6s} me={p["me"]:<3} {p["title"][:70]}{flag}')
    print(f"{len(pubs)} publications")
    if not args.check:
        OUT.parent.mkdir(exist_ok=True)
        OUT.write_text(head + to_yaml(pubs), encoding="utf-8")
        print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
