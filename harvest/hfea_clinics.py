#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HFEA licensed fertility clinics — the UK, at street level.

The HFEA is the only fertility regulator in the world that licenses every
clinic, inspects them, and publishes the result clinic by clinic. Around 107
licensed treatment clinics, plus satellites, each with a postal address, phone,
email and website. That address is where treatment happens, so these are the
only fertility points on this map graded 'operational' outside the United
States.

The search form posts with an ASP.NET verification token, which is a scrape that
breaks the first time the token handling changes. The A-Z listing pages need no
token and no session: twenty-six plain pages, one per letter. Fewer moving parts
is the whole reason this route was chosen.

Satellite clinics are kept, and named as satellites. A satellite is where a
patient is actually seen even though the licence sits with a parent clinic, so
dropping them would put the map's dots where the paperwork is rather than where
the treatment is - the exact failure this map grades addresses to avoid.

Parsed against the real page: each clinic is a div.row.pb-20.clinic-row holding
an h2 with the name, p.clinic-desc lines naming any parent, and two
ul.list-unstyled - the first the address, the second contact details.

    python3 harvest/hfea_clinics.py
    python3 harvest/hfea_clinics.py --dry-run
    python3 harvest/hfea_clinics.py --from-file page.htm
"""

import json, re, sys, time, pathlib
from urllib.request import Request, urlopen
from urllib.parse import quote

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "hfea_clinics.json"
CACHE = HERE / "_geocache.json"

# Read off the saved page rather than guessed at. The letter is a query
# parameter on one path, not a path segment: every one of the 26 guesses
# returned 404 and the harvester dutifully reported 26 gaps.
BASE = "https://www.hfea.gov.uk/choose-a-fertility-clinic/search/all-clinics/?alpha="
LETTERS = "abcdefghijklmnopqrstuvwxyz"

# A UK postcode resolves to a street, free and without a key. Better than a
# general geocoder here because HFEA prints the postcode on every clinic.
POSTCODES = "https://api.postcodes.io/postcodes/"
POSTCODE_RE = re.compile(r"\b([A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2})\b")

UK_CENTRE = (54.00, -2.55)


def get(url, tries=3):
    for i in range(tries):
        try:
            r = Request(url, headers={"User-Agent":
                                      "GMO-map/1.0 (public research map)"})
            return urlopen(r, timeout=90).read().decode("utf-8", "replace")
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(3 * (i + 1))


import html as _html


def _text(s):
    """Tags out, entities decoded. The address lines carry &amp; - printing
    "Obstetrics &amp; Gynaecology" on a marker is the sort of thing nobody
    notices in review and everybody notices on the map."""
    return re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def parse(html):
    """One record per clinic-row. Returns dicts of raw strings."""
    out = []
    for blk in re.split(r'<div class="row pb-20 clinic-row">', html)[1:]:
        name = re.search(r"<h2[^>]*>(.*?)</h2>", blk, re.S)
        if not name:
            continue
        nm = _text(name.group(1))
        if not nm:
            continue

        parents = [_text(x) for x in
                   re.findall(r'<p class="clinic-desc">(.*?)</p>', blk, re.S)]

        lists = re.findall(r'<ul class="list-unstyled">(.*?)</ul>', blk, re.S)
        addr, contact = [], []
        if lists:
            addr = [_text(x) for x in re.findall(r"<li>(.*?)</li>", lists[0], re.S)]
            addr = [x for x in addr if x]
        if len(lists) > 1:
            contact = [_text(x) for x in re.findall(r"<li>(.*?)</li>", lists[1], re.S)]
            contact = [x for x in contact if x]

        out.append({"name": nm, "parents": parents,
                    "address": addr, "contact": contact})
    return out


def load_cache():
    if CACHE.exists():
        try:
            return json.loads(CACHE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def geocode_postcode(pc, cache):
    key = "UKPC:" + pc
    if key in cache:
        return cache[key]
    try:
        d = json.loads(get(POSTCODES + quote(pc), tries=2))
        r = d.get("result") or {}
        if r.get("latitude") is not None:
            cache[key] = [round(r["latitude"], 5), round(r["longitude"], 5)]
            return cache[key]
    except Exception:
        pass
    cache[key] = None
    return None


def main():
    dry = "--dry-run" in sys.argv
    pages = []
    if "--from-file" in sys.argv:
        pages = [pathlib.Path(sys.argv[sys.argv.index("--from-file") + 1]
                              ).read_text(encoding="utf-8", errors="replace")]
    else:
        for ch in LETTERS:
            try:
                pages.append(get(BASE + ch))
            except Exception as e:
                # One letter missing is a gap of a few clinics, not a reason to
                # write nothing. It is printed so the gap is visible.
                print("  letter %s unreachable (%s)" % (ch, e), file=sys.stderr)
            time.sleep(1)

    if not pages:
        print("  every letter page failed. That is the URL being wrong, not the "
              "register being empty - check BASE. Nothing written.",
              file=sys.stderr)
        return
    rows = []
    for p in pages:
        rows += parse(p)
    print("  %d clinic rows parsed from %d pages" % (len(rows), len(pages)))
    if not rows:
        print("  nothing parsed — the clinic-row markup has changed. Nothing "
              "written.", file=sys.stderr)
        return

    cache = load_cache()
    out, seen, exact_n, approx_n = [], set(), 0, 0
    for r in rows:
        if r["name"].lower() in seen:
            continue
        seen.add(r["name"].lower())

        joined = ", ".join(r["address"])
        pc = POSTCODE_RE.search(joined.upper())
        latlng, exact = None, False
        if pc:
            latlng = geocode_postcode(pc.group(1).replace(" ", ""), cache)
            exact = latlng is not None
        if latlng is None:
            latlng = UK_CENTRE
        exact_n += 1 if exact else 0
        approx_n += 0 if exact else 1

        sat = [x for x in r["parents"] if "satellite" in x.lower()]
        tel = next((x for x in r["contact"] if x.lower().startswith("tel")), "")
        web = next((x for x in r["contact"] if x.lower().startswith("website")), "")

        bits = ["A fertility clinic licensed and inspected by the Human "
                "Fertilisation and Embryology Authority."]
        if sat:
            bits.append(sat[0].rstrip(".") + ".")
            bits.append("A satellite is where patients are seen; the licence sits "
                        "with the parent clinic, so the regulator's paperwork and "
                        "the treatment are in different places.")
        bits.append("A fertility clinic is where human embryos are made, selected and "
                "stored, and where assisted reproduction happens, like IVF, "
                "ICSI, egg and sperm donation, freezing embryos and eggs for "
                "later.")
        bits.append("The HFEA licenses every clinic in the United Kingdom, "
                    "inspects them, and publishes findings and success rates "
                    "clinic by clinic. No other fertility regulator publishes at "
                    "this level, which makes the UK the one country where this "
                    "sector can be read rather than estimated.")
        if not exact:
            bits.append("The postcode did not resolve, so this point sits at the "
                        "centre of the country rather than at the clinic.")

        out.append({
            "name": r["name"][:150],
            "source": "industry:repro",
            "type": "Fertility clinic",
            "lat": latlng[0], "lng": latlng[1],
            "state": joined[:120],
            "precise": bool(exact),
            # A clinic's published address is its treatment address.
            "addr_grade": ("operational" if exact else "centroid"),
            "impact": 2,
            "company": (sat[0][:80] if sat else ""),
            "size": "",
            "status": ("HFEA licensed — satellite" if sat else "HFEA licensed"),
            "phase": "post", "date": "",
            "otype": "company",
            "tags": ["repro:clinics"], "species": ["human"],
            "url": (web.split(":", 1)[1].strip() if web and ":" in web
                    else "https://www.hfea.gov.uk/choose-a-fertility-clinic/"),
            "desc": " ".join(bits),
            "checked": "",
        })

    print("  %d clinics: %d at their postcode, %d unresolved"
          % (len(out), exact_n, approx_n))
    if dry:
        print("dry run — nothing written")
        return
    CACHE.write_text(json.dumps(cache, indent=0), encoding="utf-8")
    OUT.write_text(json.dumps({
        "generated": time.strftime("%Y-%m-%d"),
        "note": ("HFEA licensed fertility clinics, from the A-Z listing. "
                 "Positions from the published postcode."),
        "projects": out}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote %s" % OUT.name)


if __name__ == "__main__":
    main()
