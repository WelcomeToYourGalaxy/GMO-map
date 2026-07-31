#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build per-country trackerdata entries from the CBD's official BCH national
focal point list.

Source: https://www.cbd.int/doc/lists/bch-fp.pdf  (Secretariat of the Convention
on Biological Diversity, regenerated periodically; the header carries its date).
189 countries as of the 6 July 2026 edition.

Why this and not the BCH portal: bch.cbd.int is a JavaScript application, so its
record pages return nothing to a fetcher. This PDF is the same information in a
form that can actually be parsed, and it is published by the Secretariat itself.

PRIVACY: the list contains named officials, their direct e-mail addresses and
their phone numbers. None of that goes into the map. This script extracts the
INSTITUTION and, where the entry gives one, the institution's WEBSITE. Person
names, e-mails, faxes and phone numbers are dropped, and there is an assertion at
the end that none survived into the output.

    pip install pypdf
    python3 harvest/bch_focal_points.py            # writes bch_stubs.json
    python3 harvest/bch_focal_points.py --print    # print, write nothing

The output is a review queue, not a drop-in file. Each stub carries the country,
the institution and the URL; a human writes the CAN / CAN'T / FOR description and
moves it into trackerdata.json. The point is that the country list and the
institution names stop being anybody's recollection.
"""
import io, json, re, sys, pathlib
from urllib.request import Request, urlopen

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "bch_stubs.json"
PDF_URL = "https://www.cbd.int/doc/lists/bch-fp.pdf"
UA = "Mozilla/5.0 (compatible; GMO-map BCH focal point harvester)"

# Lines that are page furniture rather than content.
SKIP = re.compile(r"^(Tel\.?:|Fax:|E-Mail:|Web:|P\.?O\.? Box|BP |B\.P\.|\d{4}-\d\d-\d\d|"
                  r"Convention on Biological Diversity|Biosafety Clearing-House|"
                  r"National Focal Points|For more information|Secretariat of the)", re.I)
EMAIL = re.compile(r"[\w.+-]+@[\w.-]+")
PHONE = re.compile(r"^\+?[\d\s().,+-]{7,}$")
WEB = re.compile(r"Web:\s*(\S+)", re.I)
NUMBERED = re.compile(r"^\s*(\d{1,3})\.\s*$")
# Honorifics that mark the personal-name line at the end of each entry.
PERSON = re.compile(r"^(Mr\.|Ms\.|Mrs\.|Dr\.|M\.|Mme|Mlle|Sr\.|Sra\.|Srta\.|Don |H\.E\.|Hon\.|"
                    r"Ing\.|Lic\.|Mtra\.|Prof\.|Madame|Miss)", re.I)
# Words that mark an institution rather than a job title or a street.
INST = re.compile(r"(ministry|minist[e\u00e8]re|ministerio|ministero|department|direcci[o\u00f3]n|"
                  r"direction|agency|agence|authority|autorit|institute|instituto|institut|"
                  r"office|oficina|bureau|commission|comisi[o\u00f3]n|council|consejo|centre|"
                  r"center|centro|service|servicio|servi[c\u00e7]o|secretariat|secretar[i\u00ed]a|"
                  r"administration|board|committee|comit|national|federal|state |bundes|"
                  r"environment|environnement|ambiente|agriculture|biosafety|bios[e\u00e9]curit|"
                  r"bioseguridad|protection|conservation|university|universi)", re.I)


def fetch_pdf():
    req = Request(PDF_URL, headers={"User-Agent": UA})
    with urlopen(req, timeout=60) as r:
        return r.read()


def pdf_text(raw):
    try:
        from pypdf import PdfReader
    except ImportError:
        sys.exit("pypdf not installed:  pip install pypdf")
    reader = PdfReader(io.BytesIO(raw))
    return "\n".join((p.extract_text() or "") for p in reader.pages)


def parse(text):
    """Walk the flat text. Each entry starts with a country line followed by a
    bare number; the institution is the best INST-matching line before the
    contact block."""
    lines = [l.rstrip() for l in text.split("\n")]
    entries, i = [], 0
    while i < len(lines) - 1:
        if NUMBERED.match(lines[i + 1] or "") and lines[i].strip():
            country = lines[i].strip()
            j, block = i + 2, []
            while j < len(lines) and not (j + 1 < len(lines) and NUMBERED.match(lines[j + 1] or "")):
                block.append(lines[j]); j += 1
            entries.append((country, block))
            i = j
        else:
            i += 1
    out = []
    for country, block in entries:
        web = ""
        inst = []
        for ln in block:
            m = WEB.search(ln)
            if m and not web:
                web = m.group(1).strip().rstrip(".,;")
            s = ln.strip()
            if not s or SKIP.match(s) or EMAIL.search(s) or PHONE.match(s) or PERSON.match(s):
                continue
            if INST.search(s):
                inst.append(s)
        if not inst:
            continue
        # the longest institution-looking line is almost always the body itself
        # rather than the sub-unit or the job title
        name = max(inst, key=len).strip()
        if web and not web.lower().startswith("http"):
            web = "https://" + web
        out.append({"country": country, "institution": name, "url": web})
    return out


def to_stubs(rows):
    stubs = []
    for r in rows:
        if not r["url"]:
            continue                      # no verifiable link: leave it out
        stubs.append({
            "country": r["country"],
            "name": r["institution"] + " \u2014 BCH national focal point",
            "url": r["url"],
            "desc": ("TODO write CAN / CAN'T / FOR. This is the office that files the country's "
                     "records to the Biosafety Clearing-House under the Cartagena Protocol. It is "
                     "not always the same body that decides approvals \u2014 check before describing "
                     "it as the regulator."),
            "tags": ["projects:nepa", "records:publications"],
            "kind": "structured", "voice": "official", "skind": "database",
            "type": "records-data", "trust": "record",
            "_source": "CBD BCH national focal point list",
        })
    return stubs


def main():
    raw = fetch_pdf()
    rows = parse(pdf_text(raw))
    stubs = to_stubs(rows)

    blob = json.dumps(stubs, ensure_ascii=False)
    assert not EMAIL.search(blob), "an e-mail address survived into the output"
    for h in ("Mr.", "Ms.", "Mrs.", "Dr.", "Mme", "Sr.", "Sra."):
        assert h not in blob, "a personal name survived into the output: " + h

    if "--print" in sys.argv:
        for s in stubs:
            print("%-42s %s" % (s["country"][:42], s["url"]))
        print("\n%d countries parsed, %d with a usable URL" % (len(rows), len(stubs)))
        return
    OUT.write_text(json.dumps(stubs, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote %s: %d countries parsed, %d stubs with a URL" % (OUT.name, len(rows), len(stubs)))
    print("These are a review queue. Write the descriptions, then merge into trackerdata.json.")


if __name__ == "__main__":
    main()
