#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Harvest US environmental-release authorisations into projects.json.

Source: APHIS Biotechnology Regulatory Services publishes its full permit and
notification file as CSV, updated every business day, in the public domain
(CC0). Two files:

  https://www.aphis.usda.gov/sites/default/files/efile-data.csv    (eFile, current)
  https://www.aphis.usda.gov/sites/default/files/brs-public-apps.csv (ePermits, legacy)

Verified schema (eFile):
  Authorization Number, Type, Purpose of Permit, Movement Type, Application Type,
  Organization, Organism, Received Date, Status, Issued Date, Effective Date,
  Expiration Date, Location(s), CBI, Number of Release Locations,
  Intended Trait(s), Genotype(s)

Why this and not OGTR: the OGTR record is the better register — it publishes
field-trial site locations, which almost nothing else does — but ogtr.gov.au
disallows automated access in robots.txt. APHIS explicitly publishes a bulk file
for reuse. Take the register that invites you in.

    python3 harvest/aphis_releases.py              # write projects.json
    python3 harvest/aphis_releases.py --dry-run    # print a summary, write nothing
    python3 harvest/aphis_releases.py --keep 400   # cap the record count

Standard library only.
"""
import csv, io, json, sys, pathlib, re
from datetime import datetime, date
from urllib.request import Request, urlopen

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "projects.json"
CURATED = ROOT / "harvest" / "projects_curated.json"
CFIA = ROOT / "harvest" / "cfia_records.json"
INDUSTRY = ROOT / "harvest" / "industry_points.json"
ESCAPES = ROOT / "harvest" / "escape_records.json"

EFILE = "https://www.aphis.usda.gov/sites/default/files/efile-data.csv"
LEGACY = "https://www.aphis.usda.gov/sites/default/files/brs-public-apps.csv"
UA = "Mozilla/5.0 (compatible; GMO-map APHIS harvester; +https://github.com/WelcomeToYourGalaxy/GMO-map)"

DEFAULT_KEEP = 600

# Statuses that mean a release is live or pending. Anything else is dropped by a
# fail-safe gate: a withdrawn or denied application is not a release.
LIVE = {"issued", "acknowledged", "submitted", "state review", "in review",
        "waiting on customer", "pending"}
DEAD = {"withdrawn", "denied", "superceded", "superseded", "expired",
        "cancelled", "canceled", "voided", "terminated"}

# Statuses that mean the release is authorised, versus still under assessment.
# This drives the map's consent-phase filter.
CONSENTED = {"issued", "acknowledged"}

# State centroids. Release locations in the source are state codes, never
# coordinates, so every record is precise:false and draws as a dashed ring.
STATES = {
 "AL":(32.8,-86.8),"AK":(64.0,-152.0),"AZ":(34.3,-111.7),"AR":(34.9,-92.4),
 "CA":(37.2,-119.5),"CO":(39.0,-105.5),"CT":(41.6,-72.7),"DE":(39.0,-75.5),
 "DC":(38.9,-77.0),"FL":(28.6,-82.4),"GA":(32.6,-83.4),"HI":(20.3,-156.4),
 "ID":(44.4,-114.6),"IL":(40.0,-89.2),"IN":(39.9,-86.3),"IA":(42.1,-93.5),
 "KS":(38.5,-98.4),"KY":(37.5,-85.3),"LA":(31.1,-92.0),"ME":(45.4,-69.2),
 "MD":(39.0,-76.8),"MA":(42.3,-71.8),"MI":(44.3,-85.4),"MN":(46.3,-94.3),
 "MS":(32.7,-89.7),"MO":(38.4,-92.5),"MT":(47.0,-109.6),"NE":(41.5,-99.8),
 "NV":(39.3,-116.6),"NH":(43.7,-71.6),"NJ":(40.2,-74.7),"NM":(34.4,-106.1),
 "NY":(42.9,-75.5),"NC":(35.5,-79.4),"ND":(47.4,-100.5),"OH":(40.3,-82.8),
 "OK":(35.6,-97.5),"OR":(43.9,-120.6),"PA":(40.9,-77.8),"PR":(18.2,-66.4),
 "RI":(41.7,-71.6),"SC":(33.9,-80.9),"SD":(44.4,-100.2),"TN":(35.8,-86.4),
 "TX":(31.4,-99.3),"UT":(39.3,-111.7),"VT":(44.1,-72.7),"VA":(37.5,-78.8),
 "WA":(47.4,-120.5),"WV":(38.6,-80.6),"WI":(44.6,-89.7),"WY":(43.0,-107.5),
 "VI":(18.3,-64.9),"GU":(13.4,144.8),"AS":(-14.3,-170.7),"MP":(15.2,145.7),
}

# Trait prefix codes used in the Intended Trait(s) column.
TRAITS = {
 "HR":"herbicide resistance","IR":"insect resistance","FR":"fungal resistance",
 "BR":"bacterial resistance","VR":"virus resistance","NR":"nematode resistance",
 "AP":"agronomic properties","PQ":"product quality","MG":"marker gene",
 "OO":"other",
}


def fetch(url):
    req = Request(url, headers={"User-Agent": UA})
    with urlopen(req, timeout=120) as r:
        return r.read().decode("utf-8-sig", "replace")


def parse_date(s):
    s = (s or "").strip()
    # The two files use different date formats. eFile writes 5/2/2026; ePermits
    # writes 01-May-2029. %d-%b-%Y must come before %d-%b-%y or every four-digit
    # legacy year fails to parse - which is what let 20,344 dead legacy records
    # through the expiry gate as though they had no expiry date at all.
    for fmt in ("%m/%d/%Y", "%Y-%m-%d", "%d-%b-%Y", "%d-%b-%y", "%m/%d/%y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


# The two files do NOT share a schema. Verified by reading both headers:
#   eFile:    Authorization Number / Organization / Organism / Location(s) /
#             Number of Release Locations / Intended Trait(s) / Expiration Date
#   ePermits: Permit Number / Institution / Article / Locations / Sites /
#             Acres / Phenotypes / Expire Date
# Assuming one schema for both is why the legacy file returned zero records.
LEGACY_MAP = {
    "Authorization Number": "Permit Number",
    "Organization": "Institution",
    "Organism": "Article",
    "Location(s)": "Locations",
    "Number of Release Locations": "Sites",
    "Intended Trait(s)": "Phenotypes",
    "Expiration Date": "Expire Date",
    "Received Date": "Receive Date",
    "Issued Date": "Issue Date",
    "Movement Type": "Action",
}


def get(row, field, legacy):
    """Read a field by its eFile name, mapping to the legacy name when needed."""
    if legacy and field in LEGACY_MAP:
        return row.get(LEGACY_MAP[field], "")
    return row.get(field, "")


def release_states(loc):
    """Pull the states under the 'Rel' component. Import and interstate movement
    are not environmental releases and are deliberately excluded.
    Separators differ between the files: eFile writes 'Rel - HI-PR', ePermits
    writes 'Rel-IA,IL,IN'. Accept both."""
    m = re.search(r"Rel\s*-\s*([A-Z][A-Z,\- ]*)", loc or "")
    if not m:
        return []
    raw = re.split(r"[,\-\s]+", m.group(1))
    out, seen = [], set()
    for s in raw:
        if s in STATES and s not in seen:
            seen.add(s); out.append(s)
    return out


def traits_of(raw):
    out, seen = [], set()
    for part in (raw or "").split("/"):
        part = part.strip()
        m = re.match(r"^([A-Z]{2})-", part)
        if not m:
            continue
        label = TRAITS.get(m.group(1))
        if label and label not in seen:
            seen.add(label); out.append(label)
    return out


# Applicants file under inconsistent names: "Pioneer Hi-Bred International" and
# "Pioneer Hi-Bred International, Inc." are one company, and counting them apart
# UNDERSTATES concentration. Normalise for the summary only - each record keeps
# the name exactly as filed.
SUFFIX = re.compile(r"[,]?\s*\b(inc|llc|ltd|l\.?l\.?c|corp|corporation|company|co|"
                    r"plc|gmbh|ag|sa|s\.a|bv|nv|pty|limited)\b\.?\s*$", re.I)
GROUPS = [("bayer", "Bayer"), ("monsanto", "Bayer"), ("syngenta", "Syngenta"),
          ("pioneer hi-bred", "Corteva (Pioneer)"), ("corteva", "Corteva (Pioneer)"),
          ("basf", "BASF"), ("dow agro", "Corteva (Pioneer)")]


def norm_org(name):
    s = (name or "").strip()
    low = s.lower()
    for needle, group in GROUPS:
        if needle in low:
            return group
    prev = None
    while prev != s:
        prev = s
        s = SUFFIX.sub("", s).strip()
    return s or "Not stated"


def impact_for(n_locs, states):
    """Rated scale, 1-5. Based on how many release locations the applicant
    declared and how many states it spans. Not a measured area - the source
    does not publish one - so it sorts rather than quantifies."""
    n = n_locs or 0
    span = len(states)
    if n >= 40 or span >= 10: return 5
    if n >= 10 or span >= 5:  return 4
    if n >= 4  or span >= 3:  return 3
    if n >= 2  or span >= 2:  return 2
    return 1


def build(rows, source_label):
    legacy = (source_label == "epermits")
    out = []
    for r in rows:
        status = (r.get("Status") or "").strip()
        sl = status.lower()
        if sl in DEAD or sl not in LIVE:
            continue
        states = release_states(get(r, "Location(s)", legacy))
        if not states:
            continue                      # no environmental release component
        eff = parse_date(get(r, "Effective Date", legacy))
        exp = parse_date(get(r, "Expiration Date", legacy))
        if exp and exp < date.today():
            continue                      # lapsed authorisation is not a live release
        if legacy and not exp:
            # ePermits stopped accepting applications on 30 September 2022 and its
            # permits expire on their own terms. A legacy record with no expiry
            # date cannot be shown to be current, so it is not a live release.
            # Without this gate 20,344 dead legacy records passed as live.
            continue
        try:
            n_locs = int(float(get(r, "Number of Release Locations", legacy) or 0))
        except ValueError:
            n_locs = 0

        org = (get(r, "Organization", legacy) or "").strip() or "Not stated"
        organism = (get(r, "Organism", legacy) or "").strip().replace(" ; ", ", ") or "Not stated"
        auth = (get(r, "Authorization Number", legacy) or "").strip()
        kind = (r.get("Type") or "Permit").strip()
        cbi = (r.get("CBI") or r.get("Cbi") or "").strip().lower() in ("yes", "cbi")
        tr = traits_of(get(r, "Intended Trait(s)", legacy))
        lat, lng = STATES[states[0]]

        acres = (r.get("Acres") or "").strip() if legacy else ""
        try:
            acres = ("%g acres" % float(acres)) if acres else ""
        except ValueError:
            acres = ""

        redaction = (" The applicant claimed confidential business information on this "
                     "record, so the trait description is partly withheld as [CBI] in the "
                     "source." if cbi else "")
        desc = ("%s to release genetically engineered %s at %d declared location%s in %s. "
                "Applicant: %s. Status: %s.%s%s Position is a state centroid, not the site "
                "\u2014 APHIS publishes release states, never coordinates."
                % (kind, organism.lower(), n_locs, "" if n_locs == 1 else "s",
                   ", ".join(states), org, status,
                   (" Declared traits: " + ", ".join(tr) + ".") if tr else "",
                   redaction))

        out.append({
            "name": "%s \u2014 %s (%s)" % (auth, organism, org),
            "source": "aphis:" + source_label,
            "type": "%s, environmental release" % organism,
            "lat": lat, "lng": lng,
            "state": ", ".join(states),
            "precise": False,
            "impact": impact_for(n_locs, states),
            "company": org,
            "size": ("%d declared release location%s across %d state%s%s"
                     % (n_locs, "" if n_locs == 1 else "s", len(states),
                        "" if len(states) == 1 else "s",
                        (", " + acres) if acres else "")),
            "status": status,
            "phase": "post" if sl in CONSENTED else "pre",
            "date": eff.isoformat() if eff else "",
            "url": "https://www.aphis.usda.gov/biotechnology-permits/releases",
            "desc": desc,
        })
    return out


def main():
    keep = DEFAULT_KEEP
    if "--keep" in sys.argv:
        keep = int(sys.argv[sys.argv.index("--keep") + 1])

    records = []
    for url, label in ((EFILE, "efile"), (LEGACY, "epermits")):
        try:
            text = fetch(url)
        except Exception as e:
            print("  ! could not fetch %s: %s" % (label, e), file=sys.stderr)
            continue
        rows = list(csv.DictReader(io.StringIO(text)))
        got = build(rows, label)
        print("  %-9s %6d rows \u2192 %5d live releases" % (label, len(rows), len(got)))
        records.extend(got)

    if not records:
        print("nothing harvested; leaving projects.json alone", file=sys.stderr)
        sys.exit(1)

    records.sort(key=lambda x: x.get("date", ""), reverse=True)
    records = records[:keep]

    # Canadian approvals, if cfia_approvals.py has been run
    extra = []
    if CFIA.exists():
        try:
            extra = json.loads(CFIA.read_text(encoding="utf-8")).get("projects", [])
            print("  merging %d CFIA records" % len(extra))
        except Exception as e:
            print("  ! %s could not be read: %s" % (CFIA.name, e), file=sys.stderr)

    # industry organisations and documented escapes are points on the same layer
    for path, label in ((INDUSTRY, "industry"), (ESCAPES, "escape")):
        if path.exists():
            try:
                got = json.loads(path.read_text(encoding="utf-8")).get("projects", [])
                extra.extend(got)
                print("  merging %d %s points" % (len(got), label))
            except Exception as e:
                print("  ! %s could not be read: %s" % (path.name, e), file=sys.stderr)
        else:
            print("  ! %s not found" % path.name, file=sys.stderr)

    # keep the hand-written OGTR records alongside, if they were preserved
    curated = []
    if CURATED.exists():
        try:
            curated = json.loads(CURATED.read_text(encoding="utf-8")).get("projects", [])
        except Exception as e:
            print("  ! %s exists but could not be read: %s" % (CURATED.name, e),
                  file=sys.stderr)
    else:
        print("  ! %s not found \u2014 hand-written records will not be merged.\n"
              "    If you have them, add the file at harvest/%s and re-run."
              % (CURATED.name, CURATED.name), file=sys.stderr)

    doc = {
        "note": ("US environmental-release authorisations harvested from the APHIS BRS "
                 "public data files (public domain), plus hand-curated records from other "
                 "registers. Only records with a release component are included \u2014 import "
                 "and interstate movement are not releases. Every position is a state "
                 "centroid: APHIS publishes release states, never coordinates, so every "
                 "record is precise:false and draws as a dashed ring. Canadian records come "
                 "from the CFIA PNT dataset and sit at the national centroid, because that "
                 "register records a national approval rather than a planting location. "
                 "Everywhere else is not yet harvested."),
        "generated": date.today().isoformat(),
        "source": "APHIS BRS public data files, " + date.today().isoformat(),
        "projects": curated + extra + records,
    }

    pre = sum(1 for r in records if r["phase"] == "pre")
    print("\n%d release records (%d under assessment, %d consented) + %d curated"
          % (len(records), pre, len(records) - pre, len(curated)))
    orgs = {}
    for r in records:
        k = norm_org(r["company"])
        orgs[k] = orgs.get(k, 0) + 1
    ranked = sorted(orgs.items(), key=lambda x: -x[1])
    print("top applicants (%d distinct, corporate groups merged):" % len(orgs))
    for o, c in ranked[:10]:
        print("  %3d  %4.1f%%  %s" % (c, 100.0 * c / len(records), o[:56]))
    top3 = sum(c for _, c in ranked[:3])
    print("\ntop 3 applicants hold %d of %d records (%.0f%%)"
          % (top3, len(records), 100.0 * top3 / len(records)))

    if "--dry-run" in sys.argv:
        print("\ndry run \u2014 nothing written")
        return
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nwrote %s" % OUT.name)


if __name__ == "__main__":
    main()
