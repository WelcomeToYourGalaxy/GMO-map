#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AAALAC accredited organisations — animal research facilities worldwide.

This is the only facility-level handle that exists for most of the world. The
national registers are strong in three or four countries and absent everywhere
else; AAALAC's directory names roughly 1,160 organisations across 121 countries,
including 151 in China, 33 in Japan, 32 in India, 23 in South Korea and 16 in
Taiwan, none of which publish a facility register anyone can read.

What it is NOT is a register, and the difference matters enough to say on every
record. Accreditation is voluntary and paid for. An organisation appears here
because it applied and passed, so absence means "not accredited", never "does no
animal research". The largest users in several countries are absent for exactly
that reason. Read as a census this list is badly wrong; read as a list of
organisations that chose to be inspected, it is exactly right.

The directory gives an organisation, its parent where it has one, and a city,
state and country - no street address. So every point here is graded
'administrative': it is the place an organisation is registered to, not the
building where animals are held. That grade is the difference between a map that
is careful and a map that is confidently wrong.

Parsed against the real page: each record is a div.row holding a div.col-sm-9
with one <p>, whose bold <span> is the parent organisation and whose following
<br/>-separated lines are the member organisation and its location.

    python3 harvest/aaalac_facilities.py
    python3 harvest/aaalac_facilities.py --dry-run
    python3 harvest/aaalac_facilities.py --from-file page.htm
"""

import json, re, sys, time, pathlib
from urllib.request import Request, urlopen
from urllib.parse import quote

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "aaalac_facilities.json"
CACHE = HERE / "_geocache.json"

SEARCH = ("https://www.aaalac.org/accreditation/directory/"
          "directory-of-accredited-organizations-search-result/")

# City-level geocoding only, because city level is all the source gives. Photon
# copes with institutional and non-Latin place names better than Nominatim.
PHOTON = "https://photon.komoot.io/api/?limit=1&q="

# Country centroids, for rows whose city cannot be resolved. A country centroid
# is not a location and the record says so.
FALLBACK = {
    "UNITED STATES": (39.83, -98.58), "P.R. CHINA": (35.86, 104.19),
    "JAPAN": (36.20, 138.25), "INDIA": (20.59, 78.96),
    "REPUBLIC OF KOREA": (35.91, 127.77), "FRANCE": (46.23, 2.21),
    "UNITED KINGDOM": (55.38, -3.44), "GERMANY": (51.17, 10.45),
    "TAIWAN/R.O.C.": (23.70, 120.96), "THAILAND": (15.87, 100.99),
    "SPAIN": (40.46, -3.75), "CANADA": (56.13, -106.35),
    "SINGAPORE": (1.35, 103.82), "BRAZIL": (-14.24, -51.93),
    "ITALY": (41.87, 12.57), "SWITZERLAND": (46.82, 8.23),
    "BELGIUM": (50.50, 4.47), "NETHERLANDS": (52.13, 5.29),
    "SWEDEN": (60.13, 18.64), "DENMARK": (56.26, 9.50),
    "AUSTRALIA": (-25.27, 133.78), "ISRAEL": (31.05, 34.85),
    "MEXICO": (23.63, -102.55), "IRELAND": (53.41, -8.24),
}


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


def parse(html):
    """Records out of the directory's markup.

    Deliberately not BeautifulSoup: this runs in a workflow with no third-party
    packages installed, and the structure is regular enough to cut with a
    regular expression that fails visibly rather than silently.
    """
    out = []
    for blk in re.findall(r'<div class="col-sm-9">\s*<p>(.*?)</p>', html, re.S):
        span = re.search(r'<span[^>]*>(.*?)</span>', blk, re.S)
        if not span:
            continue
        parent = re.sub(r"<[^>]+>", " ", span.group(1))
        parent = re.sub(r"\s+", " ", parent).strip()
        rest = blk[span.end():]
        lines = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()
                 for x in re.split(r"<br\s*/?>", rest)]
        lines = [x for x in lines if x]
        if not lines:
            # A parent with no member line is the whole record.
            out.append((parent, "", ""))
            continue
        loc = lines[-1]
        member = " ".join(lines[:-1]).strip()
        out.append((parent, member, loc))
    return out


def load_cache():
    if CACHE.exists():
        try:
            return json.loads(CACHE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def geocode(place, cache):
    if place in cache:
        return cache[place]
    try:
        d = json.loads(get(PHOTON + quote(place), tries=2))
        fs = d.get("features") or []
        if fs:
            c = fs[0]["geometry"]["coordinates"]
            cache[place] = [round(c[1], 5), round(c[0], 5)]
            return cache[place]
    except Exception:
        pass
    cache[place] = None
    return None


def main():
    dry = "--dry-run" in sys.argv
    if "--from-file" in sys.argv:
        html = pathlib.Path(sys.argv[sys.argv.index("--from-file") + 1]
                            ).read_text(encoding="utf-8", errors="replace")
    else:
        try:
            html = get(SEARCH)
        except Exception as e:
            print("AAALAC directory unreachable (%s). Nothing written; the "
                  "previous file, if any, is left alone." % e, file=sys.stderr)
            return

    rows = parse(html)
    print("  %d rows parsed" % len(rows))
    if len(rows) < 50:
        # The directory holds over a thousand. A handful means the markup moved,
        # and writing the handful would look like the sector shrank by 99%.
        print("  only %d rows — the page structure has changed. Nothing written; "
              "check the div.col-sm-9 > p markup in parse()." % len(rows),
              file=sys.stderr)
        return

    cache = load_cache()
    out, seen, placed, centro = [], set(), 0, 0
    for parent, member, loc in rows:
        name = member or parent
        if not name:
            continue
        key = (name.lower(), loc.lower())
        if key in seen:      # the directory repeats some entries verbatim
            continue
        seen.add(key)

        country = loc.split(",")[-1].strip().upper() if loc else ""
        latlng, exact = None, False
        if loc:
            latlng = geocode(loc, cache)
            exact = latlng is not None
        if latlng is None:
            latlng = FALLBACK.get(country)
        if latlng is None:
            continue
        placed += 1 if exact else 0
        centro += 0 if exact else 1

        bits = ["An organisation accredited by AAALAC International for its care "
                "and use of laboratory animals."]
        if member and parent and member != parent:
            bits.append("Part of %s." % parent)
        bits.append("Accreditation is voluntary and paid for, so this is a list of "
                    "organisations that chose to be inspected rather than a "
                    "register of everyone doing the work. An organisation absent "
                    "from it is not accredited; that says nothing about whether it "
                    "uses animals. In several countries the largest users are "
                    "absent for exactly that reason.")
        bits.append("The directory gives a city and country and no street address, "
                    "so this point marks where the organisation is registered "
                    "rather than the building where animals are held."
                    if exact else
                    "The city could not be resolved, so this sits at the centre of "
                    "the country. It is not a location.")

        out.append({
            "name": name[:150],
            "source": "industry:animals",
            "type": "Accredited animal research organisation",
            "lat": latlng[0], "lng": latlng[1],
            "state": loc,
            "precise": False,
            # Never 'operational'. The source has no street address to offer.
            "addr_grade": ("administrative" if exact else "centroid"),
            "impact": 2,
            "company": parent if parent != name else "",
            "size": "", "status": "AAALAC accredited",
            "phase": "post", "date": "",
            "otype": "institute",
            "tags": ["animals:services"], "species": ["lab_animals"],
            "url": SEARCH,
            "desc": " ".join(bits),
            "checked": "",
        })
        if len(out) % 40 == 0:
            time.sleep(0.6)      # Photon asks for restraint and gets it

    from collections import Counter
    by = Counter(r["state"].split(",")[-1].strip() for r in out)
    print("  %d organisations across %d countries" % (len(out), len(by)))
    print("  %d placed at a city, %d at a country centroid" % (placed, centro))
    for k, v in by.most_common(6):
        print("     %-24s %d" % (k, v))

    if dry:
        print("dry run — nothing written")
        return
    CACHE.write_text(json.dumps(cache, indent=0), encoding="utf-8")
    OUT.write_text(json.dumps({
        "generated": time.strftime("%Y-%m-%d"),
        "note": ("AAALAC International accredited organisations. Voluntary "
                 "accreditation, not a register: absence means not accredited, "
                 "not no animal research. City-level positions only."),
        "projects": out}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote %s" % OUT.name)


if __name__ == "__main__":
    main()
