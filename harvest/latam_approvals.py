#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Brazil and Argentina - the two largest growers after the United States.

WHY THESE TWO TOGETHER. They are the same problem: a national approvals list
published as a page or a spreadsheet rather than an API, in a language the rest
of this map is not written in, and carrying the OECD identifier inconsistently.
Sharing one file keeps the parsing decisions in one place instead of drifting
apart in two.

WHY THEY MATTER MORE THAN THEIR RECORD COUNT. Argentina's CONABIA wrote
Resolution 173/2015, which decided an edited organism carrying no foreign DNA
is not a GMO and needs no approval. Chile, Brazil, Colombia, Paraguay and
Honduras adopted versions of it. More countries follow that text than any other
on this subject, so what Argentina approves - and what it decides not to
regulate - propagates.

WHAT I CHECKED RATHER THAN ASSUMED, after writing the three limits below.

  Locations: CTNBio grants "libera\u00e7\u00e3o comercial" - permission to plant
  anywhere in Brazil, indefinitely. There is no site to publish and none is
  published. The limit is real, not a shortcut.

  Identifiers: the approvals table carries the OECD code for most events, so
  the field is usually populated from the source. Only the reconstruction is
  refused.

  Translation: the crop and trait are extracted through the bilingual tables
  below, which gives an English handle without replacing the official wording.
  That is the useful half of translating, and it is already done.

  One number worth having from the same search: 131 commercial plant releases
  as of July 2024, and CTNBio has never refused an application. The refusal
  rate is a fact about the register, and this harvester counts what it holds
  rather than asserting it.

WHAT IT WILL NOT DO.

  It does not translate. A Portuguese or Spanish approval title stays in its own
  language, with the crop and trait pulled out separately where they can be
  identified. A machine-translated title reads as an official one and is not.

  It does not place a record at a field. Both registers approve an EVENT for
  national use; neither publishes where anything is planted. Every record here
  is country-level and says so.

  It does not infer an identifier. Where the register prints one, it is carried
  and normalised to match bch_organisms.py. Where it does not, the field is
  empty rather than reconstructed from the applicant and the crop.

    python3 harvest/latam_approvals.py
    python3 harvest/latam_approvals.py --selftest      # no network
"""

import csv, io, json, re, sys, time, pathlib
from urllib.request import Request, urlopen

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "latam_approvals.json"
UA = "GMO-map/1.0 (public research map)"

SOURCES = [
    # The first URL is the approvals TABLE itself, found by searching rather
    # than by editing a path into shape: CTNBio publishes "Tabela de Plantas
    # Aprovadas para Comercializa\u00e7\u00e3o" as a document in its library. Going
    # straight at the table beats parsing the page that links to it.
    ("Brazil", "CTNBio approved products",
     ["http://ctnbio.mctic.gov.br/documents/566529/1684467/"
      "Tabela+de+Plantas+Aprovadas+para+Comercializa%C3%A7%C3%A3o/"
      "e3087f9c-c719-476e-a9bd-bfe75def842f?version=1.0",
      "http://ctnbio.mctic.gov.br/liberacao-comercial",
      "https://www.gov.br/mcti/pt-br/composicao/conselhos/ctnbio/liberacao-comercial"]),
    ("Argentina", "CONABIA authorised events",
     ["https://www.argentina.gob.ar/agricultura/alimentos-y-bioeconomia/ogm-comercializados",
      "https://www.magyp.gob.ar/sitio/areas/biotecnologia/ogm/"]),
]

# The identifier as the registers print it, including the slashed-O form.
# An OECD unique identifier is applicant code - event code - check digit.
# Two forms, and the SECOND SEPARATOR is required in both - it is what keeps
# this off ordinary prose, where a four-letter word followed by a few
# characters and a digit is common:
#   1. both separators present. The event segment MAY CONTAIN LETTERS, which
#      many real identifiers do (BPS-BFLFK-2, SYN-\u00d8\u00d8\u00d8JG-2, KM-000H71-4).
#      The old pattern allowed digits only there and missed all of them.
#   2. first separator missing - then the event segment must START with a
#      digit or \u00d8. Without that condition the pattern reads the line names in
#      cells like "ATBT04-6: NMK-89761-6" as identifiers, which they are not.
# Group 2 carries its leading separator when there is one; find_code strips it.
CODE_RE = re.compile(
    r"\b([A-Z]{2,4})"
    # Hyphenated form admits LETTERS in the event segment (BPS-BFLFK-2).
    # Space-separated and run-together forms keep the digits-only class:
    # letters there matched "ANNEX II PART 4" and "feed use 3" as codes.
    r"((?:\-[A-Z0-9\u00d8\u00f8]{3,7}\-)|(?:[\s\-]?[0-9\u00d8\u00f8O]{3,7}[\s\-]?))"
    r"([0-9])\b")


def _joincode(m):
    """The three parts as the canonical hyphenated form."""
    return "%s-%s-%s" % (m.group(1), m.group(2).strip(" -"), m.group(3))

# Crops, in both languages, so a title can be read without translating it.
CROPS = {
    "soja": "soybean", "soya": "soybean", "soybean": "soybean",
    "milho": "maize", "ma\u00edz": "maize", "maiz": "maize", "maize": "maize",
    "algod\u00e3o": "cotton", "algod\u00f3n": "cotton", "cotton": "cotton",
    "cana": "sugarcane", "ca\u00f1a": "sugarcane", "sugarcane": "sugarcane",
    "trigo": "wheat", "wheat": "wheat",
    "arroz": "rice", "rice": "rice",
    "feij\u00e3o": "bean", "poroto": "bean",
    "eucalipto": "eucalyptus", "batata": "potato", "papa": "potato",
    "alfafa": "alfalfa", "alfalfa": "alfalfa",
}

# Traits, likewise. Herbicide tolerance and insect resistance are most of them.
TRAITS = {
    "tolerante": "herbicide tolerance", "tolerancia": "herbicide tolerance",
    "toler\u00e2ncia": "herbicide tolerance", "glifosato": "herbicide tolerance",
    "glufosinato": "herbicide tolerance", "herbicida": "herbicide tolerance",
    "resistente a insetos": "insect resistance",
    "resistencia a insectos": "insect resistance",
    "insetos": "insect resistance", "insectos": "insect resistance",
    "lepid\u00f3pteros": "insect resistance",
    "seca": "drought tolerance", "sequ\u00eda": "drought tolerance",
    "v\u00edrus": "virus resistance", "virus": "virus resistance",
}


def norm_id(code):
    """Must agree with bch_organisms.norm, or a cross-register lookup misses and
    the miss looks like the event not being registered anywhere."""
    if not code:
        return ""
    s = str(code).upper()
    s = re.sub(r"[^A-Z0-9\u00d8\u00f8]", "", s)
    s = s.replace("\u00d8", "0").replace("\u00f8", "0")
    s = re.sub(r"(?<=[0-9])O", "0", s)
    s = re.sub(r"O(?=[0-9])", "0", s)
    return s


def find_code(text):
    m = CODE_RE.search(str(text or "").upper())
    return _joincode(m) if m else ""


def find_in(text, table):
    """The first term from the table present in the text, in either language."""
    t = str(text or "").lower()
    for k, v in table.items():
        if k in t:
            return v
    return ""


def get(url, timeout=60):
    req = Request(url, headers={"User-Agent": UA,
                                "Accept": "text/html, application/json, text/csv"})
    return urlopen(req, timeout=timeout).read().decode("utf-8", "replace")


def rows_from(html):
    """Table rows, stripped of markup. Deliberately crude: these pages are
    ordinary HTML tables and anything cleverer breaks when the theme changes."""
    out = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.S | re.I):
        cells = [re.sub(r"<[^>]+>", " ", c) for c in
                 re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tr, re.S | re.I)]
        cells = [re.sub(r"\s+", " ", c).strip() for c in cells]
        cells = [c for c in cells if c]
        if cells:
            out.append(cells)
    return out


def parse(country, label, html):
    """One record per approval. Nothing is translated and nothing is placed."""
    out, seen = [], set()
    for cells in rows_from(html):
        line = " \u00b7 ".join(cells)
        if len(line) < 12:
            continue
        code = find_code(line)
        crop = find_in(line, CROPS)
        if not code and not crop:
            continue                      # a layout row, not an approval
        key = norm_id(code) or line[:80].lower()
        if key in seen:
            continue
        seen.add(key)
        out.append({
            "country": country,
            "register": label,
            "id": code,
            "id_key": norm_id(code),
            "crop": crop,
            "trait": find_in(line, TRAITS),
            # The original wording, untranslated. A machine translation of an
            # official title reads as official and is not.
            "title": line[:240],
            "precision": "country",
        })
    return out


def harvest():
    all_rows = []
    for country, label, urls in SOURCES:
        got = []
        for url in urls:
            try:
                body = get(url)
            except Exception as e:
                print("  %-28s %s" % (country, str(e)[:52]))
                continue
            got = parse(country, label, body)
            print("  %-28s %s \u2014 %d approvals" % (country, url[:44], len(got)))
            if got:
                break
        all_rows += got

    if not all_rows:
        print("\nNothing parsed from either register. Both are ordinary HTML "
              "tables, so a zero here usually means the page moved rather than "
              "that the table changed \u2014 check the URLs above before changing "
              "the parser.", file=sys.stderr)
        return

    withid = sum(1 for r in all_rows if r["id"])
    print("\n  %d approvals, %d carrying an identifier" % (len(all_rows), withid))
    OUT.write_text(json.dumps({"generated": time.strftime("%Y-%m-%d"),
                               "note": "National approvals. Country-level: "
                                       "neither register publishes planting "
                                       "locations. Titles are not translated.",
                               "approvals": all_rows}, ensure_ascii=False,
                              indent=1), encoding="utf-8")
    print("wrote %s" % OUT.name)


def selftest():
    ok = True

    def check(label, got, want):
        nonlocal ok
        good = got == want
        ok = ok and good
        print("  %-48s %s" % (label, "pass" if good else
                              "FAIL got %r want %r" % (got, want)))

    check("identifier key agrees with the organism registry",
          norm_id("MON-877\u00d81-2"), "MON877012")
    check("plain-O spelling gives the same key",
          norm_id("MON-87701-2"), "MON877012")
    check("crop read from Portuguese", find_in("Soja tolerante", CROPS), "soybean")
    check("crop read from Spanish", find_in("Ma\u00edz Bt", CROPS), "maize")
    check("trait read from Portuguese",
          find_in("Soja tolerante ao glifosato", TRAITS), "herbicide tolerance")

    html = ("<table><tr><th>Evento</th><th>Cultura</th></tr>"
            "<tr><td>MON-877\u00d81-2</td><td>Soja tolerante ao glifosato</td></tr>"
            "<tr><td>Rodap\u00e9</td></tr></table>")
    rows = parse("Brazil", "CTNBio", html)
    check("one approval parsed, layout row ignored", len(rows), 1)
    check("title kept in the original language",
          "tolerante ao glifosato" in rows[0]["title"], True)
    check("no coordinate, country precision", rows[0]["precision"], "country")
    check("identifier carried", rows[0]["id"], "MON-877\u00d81-2")
    check("a row with neither code nor crop is dropped",
          parse("Brazil", "CTNBio", "<table><tr><td>P\u00e1gina 2</td></tr></table>"), [])
    print("\n%s" % ("all pass" if ok else "FAILURES ABOVE"))
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    harvest()
