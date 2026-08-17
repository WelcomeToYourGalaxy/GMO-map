#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Three registers the map has been calling unharvestable.

Each was written off for a reason that turns out to be about the website rather
than about the data, so each is worth one more attempt:

  BIOSAFETY CLEARING-HOUSE. CONFIRMED WORKING. The map says its site is a
  JavaScript application that returns nothing to a fetcher. That is true of the
  page and false of the data: the page fills itself from a Solr endpoint at
  api.cbd.int, and

      https://api.cbd.int/api/v2013/index/select
          ?q=schema_s:modifiedOrganism&rows=5&wt=json

  returns JSON in a browser. So the only genuinely cross-national record in this
  field is harvestable after all, and the map's claim that it cannot be reached
  needs correcting once this has run.

  OGTR. robots.txt disallows automated access to ogtr.gov.au, and that is
  respected here. But Australian agencies publish datasets to data.gov.au, a
  CKAN instance with an open API and no such restriction, so the same material
  may be reachable without touching the blocked host at all.

  EU. The map says no European register publishes a bulk file. The Commission's
  register of authorised GM food and feed is published as a spreadsheet as well
  as a search form, which if true makes that claim wrong.

WHY THIS PROBES RATHER THAN ASSUMES. None of these endpoints could be reached
from the machine this was written on, so every URL below is a hypothesis. The
script tries each, prints what came back, and writes only what it actually got.
A probe that fails says so and names the URL, which is worth more than silence.

    python3 harvest/open_registers.py
    python3 harvest/open_registers.py --dry-run
"""

import json, re, sys, time, pathlib
from urllib.request import Request, urlopen
from urllib.parse import urlencode

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "open_registers.json"
UA = "GMO-map/1.0 (public research map)"

# ---------------------------------------------------------------------------
# Endpoint candidates. Ordered cheapest and most likely first. Each is a guess
# until it answers; the point of the list is that one failing does not end the
# attempt.
# ---------------------------------------------------------------------------
BCH = [
    ("BCH search index",
     "https://api.cbd.int/api/v2013/index/select?"
     + urlencode({"q": "schema_s:modifiedOrganism", "rows": 200, "wt": "json"})),
    ("BCH documents",
     "https://api.cbd.int/api/v2013/documents?"
     + urlencode({"q": "schema_s:modifiedOrganism", "rows": 200})),
    ("BCH LMO registry",
     "https://bch.cbd.int/api/v2013/index/select?"
     + urlencode({"q": "schema_s:modifiedOrganism", "rows": 200, "wt": "json"})),
]
CKAN = [
    ("data.gov.au package search",
     "https://data.gov.au/data/api/3/action/package_search?"
     + urlencode({"q": "genetically modified organism licence", "rows": 50})),
    ("data.gov.au organisation OGTR",
     "https://data.gov.au/data/api/3/action/package_search?"
     + urlencode({"q": "organisation:office-of-the-gene-technology-regulator",
                  "rows": 50})),
]
EU = [
    ("EU GMO register landing",
     "https://food.ec.europa.eu/plants/genetically-modified-organisms/"
     "gmo-authorisation/eu-register-authorised-gmos_en"),
]


def fetch(url, timeout=45):
    req = Request(url, headers={"User-Agent": UA, "Accept": "application/json, */*"})
    return urlopen(req, timeout=timeout).read().decode("utf-8", "replace")


def probe(name, url):
    """Returns the body, or None, and always says which."""
    try:
        body = fetch(url)
    except Exception as e:
        print("  %-34s unreachable (%s)" % (name, str(e)[:60]))
        return None
    print("  %-34s answered, %d bytes" % (name, len(body)))
    return body


# ---------------------------------------------------------------------------
def bch_records(body):
    """The BCH search index is Solr-shaped: a response with docs inside."""
    try:
        d = json.loads(body)
    except Exception:
        return []
    docs = (d.get("response") or {}).get("docs") or d.get("docs") or []
    if not isinstance(docs, list):
        return []
    out = []
    for r in docs:
        def g(*names):
            for n in names:
                v = r.get(n)
                if isinstance(v, list) and v:
                    v = v[0]
                if v not in (None, ""):
                    return str(v)
            return ""
        name = g("title_s", "title_en", "name_s", "uniqueIdentifier_s")
        iso = g("government_s", "country_s", "governmentISO_s")[:3].upper()
        if not name:
            continue
        out.append({
            "name": name[:150],
            "iso": iso,
            "identifier": g("uniqueIdentifier_s", "oecdUniqueIdentifier_s"),
            "organism": g("organism_s", "recipientOrganism_s"),
            "trait": g("trait_s", "modifiedTrait_s"),
            "url": "https://bch.cbd.int/database/record?documentid="
                   + g("id", "identifier_s"),
        })
    return out


def ckan_datasets(body):
    try:
        d = json.loads(body)
    except Exception:
        return []
    res = ((d.get("result") or {}).get("results")) or []
    out = []
    for p in res:
        files = [{"name": r.get("name"), "format": r.get("format"),
                  "url": r.get("url")} for r in (p.get("resources") or [])]
        out.append({"title": p.get("title"), "org":
                    ((p.get("organization") or {}).get("title")),
                    "files": files,
                    "url": "https://data.gov.au/data/dataset/" + (p.get("name") or "")})
    return out


def eu_files(body):
    """Any spreadsheet linked from the register page is the bulk file the map
    says does not exist."""
    hits = re.findall(r'href="([^"]+\.(?:xlsx|xls|csv|ods))"', body, re.I)
    return sorted(set(hits))


def main():
    dry = "--dry-run" in sys.argv
    found = {"generated": time.strftime("%Y-%m-%d"), "bch": [], "ogtr": [], "eu": []}

    print("Biosafety Clearing-House")
    for name, url in BCH:
        body = probe(name, url)
        if not body:
            continue
        recs = bch_records(body)
        print("     %d records parsed" % len(recs))
        if recs:
            found["bch"] = recs
            break
    if not found["bch"]:
        print("  nothing from the BCH. The endpoints above are guesses: open "
              "bch.cbd.int, watch the Network tab, and put the URL its own page "
              "calls into BCH[] at the top of this file.")

    print("\nOGTR, via data.gov.au")
    for name, url in CKAN:
        body = probe(name, url)
        if not body:
            continue
        ds = ckan_datasets(body)
        print("     %d datasets" % len(ds))
        for d in ds[:8]:
            fmts = ",".join(sorted({str(f.get("format") or "?") for f in d["files"]}))
            print("       %-52s [%s]" % (str(d["title"])[:50], fmts))
        if ds:
            found["ogtr"] = ds
            break

    print("\nEU register")
    for name, url in EU:
        body = probe(name, url)
        if not body:
            continue
        f = eu_files(body)
        print("     %d spreadsheet links" % len(f))
        for x in f[:6]:
            print("       %s" % x[:110])
        if f:
            found["eu"] = f
            break

    got = sum(len(found[k]) for k in ("bch", "ogtr", "eu"))
    print("\n  %d results across three sources" % got)
    if not got:
        print("  Nothing answered. That is a finding too, and it is not the same "
              "as the data not existing \u2014 every URL tried is printed above.",
              file=sys.stderr)
        return
    if dry:
        print("dry run \u2014 nothing written")
        return
    OUT.write_text(json.dumps(found, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote %s" % OUT.name)


if __name__ == "__main__":
    main()
