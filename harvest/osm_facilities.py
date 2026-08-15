#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OpenStreetMap facilities: fertility clinics, and sites of companies whose
business is animal research.

This replaces osm_fertility.py and treats OSM as what it is. It is not a
register and it is not used as one. Two different jobs are done here, and they
have different standing, so they are graded differently in what they write.

FERTILITY. healthcare:speciality=fertility is an approved tag, and
healthcare=fertility_clinic is also in use. Both are queried. Coverage is thin
and lopsided - a few thousand objects worldwide, concentrated in Germany, Poland
and wherever a local mapper ran a project - against roughly 450 reporting
clinics in the United States alone. So these points are a CROSS-CHECK layer, not
a census: where an OSM object sits within a few hundred metres of a clinic this
map already holds from a national register, that is independent confirmation the
address is real and current. Where OSM has a clinic no register lists, that is a
lead. Neither is a count, and the record says so.

healthcare:speciality=gynaecology is deliberately NOT queried. It sweeps in
every obstetrics practice in Europe and would swamp the layer with clinics that
do no assisted reproduction at all.

ANIMAL RESEARCH. There is no tag for this and there should not be one. Whether a
building runs toxicology studies is not observable from the street, and OSM's
verifiability principle means a research=animal_testing tag sourced from an
APHIS registration would be an import of an external claim onto a physical
object - the kind of edit that gets reverted. amenity=vivarium looks like the
answer and is a false friend: it means an enclosure with simulated conditions,
and in practice tags terrariums and zoo enclosures.

What CAN be done honestly is to find the mapped sites of companies whose
business IS animal research, matched on the operator or brand a mapper recorded.
The claim then comes from the company's own name on its own site, not from an
inference about what happens inside a building. These records say "a site of"
rather than "a facility performing", because a company's mapped site may be an
office.

    python3 harvest/osm_facilities.py
    python3 harvest/osm_facilities.py --dry-run
"""

import json, re, sys, time, pathlib
from urllib.request import Request, urlopen
from urllib.parse import urlencode

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "osm_facilities.json"

ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.osm.ch/api/interpreter",
]

# Contract research organisations, laboratory-animal breeders and suppliers.
# Named because animal research is their stated business, not because of
# anything inferred about a building.
LAB_FIRMS = [
    "Charles River", "Inotiv", "Envigo", "Covance", "Labcorp Early Development",
    "Jackson Laboratory", "Taconic", "Janvier Labs", "Marshall BioResources",
    "WuXi AppTec", "Vivotecnia", "LPT Laboratory of Pharmacology",
    "Harlan", "Noveprim", "Cyagen", "GemPharmatech", "Ozgene",
    "Crown Bioscience", "Vital River",
]
FIRM_RE = "|".join(re.escape(x) for x in LAB_FIRMS)

# nwr is node|way|relation in one. out center gives a point for the ways and
# relations, which is what a marker needs.
Q_FERTILITY = """
[out:json][timeout:240];
(
  nwr["healthcare:speciality"~"fertility",i];
  nwr["healthcare"="fertility_clinic"];
);
out center tags;
"""

# The name filter runs on operator, brand and name. "Charles River" is also a
# river in Boston and a county in Texas, so waterways, natural features and
# boundaries are excluded outright - without that, the layer's flagship entry
# would be a stretch of water.
Q_LABS = """
[out:json][timeout:240];
(
  nwr["operator"~"%s",i][!"waterway"][!"natural"][!"boundary"];
  nwr["brand"~"%s",i][!"waterway"][!"natural"][!"boundary"];
  nwr["name"~"%s",i][!"waterway"][!"natural"][!"boundary"]["office"];
  nwr["name"~"%s",i][!"waterway"][!"natural"][!"boundary"]["amenity"="research_institute"];
  nwr["name"~"%s",i][!"waterway"][!"natural"][!"boundary"]["building"="industrial"];
);
out center tags;
""" % (FIRM_RE, FIRM_RE, FIRM_RE, FIRM_RE, FIRM_RE)


def run(query):
    last = None
    for ep in ENDPOINTS:
        try:
            req = Request(ep, data=urlencode({"data": query}).encode(),
                          headers={"User-Agent": "GMO-map/1.0 (public research map)"})
            return json.loads(urlopen(req, timeout=300).read().decode("utf-8", "replace"))
        except Exception as e:
            last = e
            print("  %s refused (%s)" % (ep.split("/")[2], e), file=sys.stderr)
            time.sleep(5)
    raise last


def point(el):
    lat = el.get("lat") or (el.get("center") or {}).get("lat")
    lon = el.get("lon") or (el.get("center") or {}).get("lon")
    return (lat, lon)


def where_of(t):
    return ", ".join([x for x in (t.get("addr:city", ""),
                                  t.get("addr:country", "")) if x])


def base(el, t, nm, kind_tags, species, typ, blurb, impact):
    lat, lon = point(el)
    return {
        "name": nm[:150],
        "source": "industry:repro" if species == ["human"] else "industry:animals",
        "type": typ,
        "lat": round(float(lat), 5), "lng": round(float(lon), 5),
        "state": where_of(t),
        # A mapper stood there or traced it from imagery. Either way this is a
        # position, not a country centroid.
        "precise": True,
        # Somebody stood there or traced it from imagery. That is a different
        # kind of fact from an address on a registration form.
        "addr_grade": "mapped",
        "impact": impact,
        "company": t.get("operator") or t.get("brand") or "",
        "size": "",
        "status": "Mapped in OpenStreetMap",
        "phase": "post", "date": "",
        "otype": "company",
        "tags": kind_tags, "species": species,
        "url": "https://www.openstreetmap.org/%s/%s" % (el.get("type", "node"),
                                                        el.get("id", "")),
        "desc": blurb,
        "checked": "",
    }


OSM_CAVEAT = ("OpenStreetMap holds what somebody chose to map, so a country with "
              "few points here may be thinly mapped rather than thinly served. "
              "That is the reverse of the national registers alongside it, which "
              "are close to complete for one country and silent everywhere else. "
              "This layer is a cross-check and a source of leads, not a count.")


def fertility(els):
    out, unnamed, skipped = [], 0, 0
    seen = set()
    for el in els:
        t = el.get("tags") or {}
        lat, lon = point(el)
        if lat is None or lon is None:
            skipped += 1
            continue
        nm = (t.get("name") or t.get("official_name") or "").strip()
        if not nm:
            # A clinic with no name is still a clinic, and this is where OSM's
            # unevenness shows. Counted, and said.
            unnamed += 1
            nm = "Fertility clinic (unnamed in OpenStreetMap)"
        k = "%s|%.4f|%.4f" % (nm.lower(), lat, lon)
        if k in seen:
            continue
        seen.add(k)
        bits = ["A clinic mapped in OpenStreetMap as offering fertility treatment."]
        if t.get("operator"):
            bits.append("Operated by %s." % t["operator"])
        if t.get("wikidata"):
            bits.append("Wikidata: %s." % t["wikidata"])
        bits.append(OSM_CAVEAT)
        out.append(base(el, t, nm, ["repro:clinics"], ["human"],
                        "Fertility clinic (OpenStreetMap)", " ".join(bits), 1))
    return out, unnamed, skipped


def labs(els):
    out, skipped = [], 0
    seen = set()
    for el in els:
        t = el.get("tags") or {}
        lat, lon = point(el)
        if lat is None or lon is None:
            skipped += 1
            continue
        nm = (t.get("name") or t.get("operator") or t.get("brand") or "").strip()
        if not nm:
            skipped += 1
            continue
        k = "%s|%.4f|%.4f" % (nm.lower(), lat, lon)
        if k in seen:
            continue
        seen.add(k)
        firm = next((f for f in LAB_FIRMS if f.lower() in
                     (nm + " " + t.get("operator", "") + " " + t.get("brand", "")).lower()), "")
        bits = ["A mapped site of %s, a company whose business is animal research, "
                "breeding laboratory animals, or both." % (firm or nm)]
        bits.append("What this record says is that the company has a site here. It "
                    "does not say animals are used at this address: a mapped "
                    "corporate site may be an office, and no regulator publishes a "
                    "worldwide list of the buildings where the work happens.")
        bits.append("There is no OpenStreetMap tag for an animal research facility "
                    "and there should not be one \u2014 whether a building runs "
                    "toxicology studies is not visible from the street, which is "
                    "the test OpenStreetMap applies to everything it records.")
        out.append(base(el, t, nm, ["animals:services"], ["lab_animals"],
                        "Animal research company site (OpenStreetMap)",
                        " ".join(bits), 2))
    return out, skipped


def main():
    dry = "--dry-run" in sys.argv
    projects = []

    try:
        d = run(Q_FERTILITY)
        got, unnamed, skipped = fertility(d.get("elements") or [])
        print("  fertility: %d elements, %d kept, %d unnamed in the source"
              % (len(d.get("elements") or []), len(got), unnamed))
        projects += got
    except Exception as e:
        print("  fertility query failed on every mirror (%s)" % e, file=sys.stderr)

    try:
        d = run(Q_LABS)
        got, skipped = labs(d.get("elements") or [])
        print("  animal research company sites: %d elements, %d kept"
              % (len(d.get("elements") or []), len(got)))
        projects += got
    except Exception as e:
        print("  company-site query failed on every mirror (%s)" % e, file=sys.stderr)

    if not projects:
        # No file written. A stale file pretending to be fresh is worse than an
        # absent one, and an empty overlay is honest.
        print("Nothing usable came back. The previous file, if any, is left "
              "alone.", file=sys.stderr)
        return
    if dry:
        print("dry run \u2014 nothing written")
        return
    OUT.write_text(json.dumps({
        "generated": time.strftime("%Y-%m-%d"),
        "note": ("OpenStreetMap facilities. Fertility clinics tagged "
                 "healthcare:speciality=fertility or healthcare=fertility_clinic, "
                 "and mapped sites of named animal-research companies. Coverage "
                 "follows mapper density, not facility density. Data (c) "
                 "OpenStreetMap contributors, ODbL."),
        "projects": projects}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote %s: %d records" % (OUT.name, len(projects)))


if __name__ == "__main__":
    main()
