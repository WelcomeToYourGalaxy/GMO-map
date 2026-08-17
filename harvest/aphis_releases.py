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
import hashlib, math
from datetime import datetime, date
from urllib.request import Request, urlopen

ROOT = pathlib.Path(__file__).resolve().parent.parent
HERE = ROOT / "harvest"
OUT = ROOT / "projects.json"
CURATED = ROOT / "harvest" / "projects_curated.json"
CFIA = ROOT / "harvest" / "cfia_records.json"
INDUSTRY = ROOT / "harvest" / "industry_points.json"
ESCAPES = ROOT / "harvest" / "escape_records.json"

EFILE = "https://www.aphis.usda.gov/sites/default/files/efile-data.csv"
LEGACY = "https://www.aphis.usda.gov/sites/default/files/brs-public-apps.csv"
UA = "Mozilla/5.0 (compatible; GMO-map APHIS harvester; +https://github.com/WelcomeToYourGalaxy/GMO-map)"

# The whole history, not a recent slice. This was 600, which silently threw
# away ~21,500 authorisations - the map is a record of the industry since it
# began, so the cap is now a guard against a runaway source, not an editorial
# decision. Override with --keep if projects.json gets unwieldy.
DEFAULT_KEEP = 40000

# Statuses that mean a release is live or pending. Anything else is dropped by a
# fail-safe gate: a withdrawn or denied application is not a release.
LIVE = {"issued", "acknowledged", "submitted", "state review", "in review",
        "waiting on customer", "pending"}
# Filled as the gate below runs, and written into the output header.
DROPSTAT = {"seen": 0, "by_status": {}}

NEVER_GRANTED = {"withdrawn", "denied", "void", "voided", "returned",
                 "incomplete", "cancelled", "canceled"}
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


_RETRIES = 4

def fetch(url):
    """Retry with backoff. A transient timeout on one CSV should not lose the run."""
    import time
    last = None
    for attempt in range(1, _RETRIES + 1):
        try:
            req = Request(url, headers={"User-Agent": UA})
            with urlopen(req, timeout=180) as r:
                return r.read().decode("utf-8-sig", "replace")
        except Exception as exc:
            last = exc
            if attempt < _RETRIES:
                wait = 5 * attempt
                print("  fetch attempt %d failed (%s) \u2014 retrying in %ds"
                      % (attempt, exc, wait), file=sys.stderr)
                time.sleep(wait)
    raise last


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



def scatter(lat, lng, key, spread=1.35):
    """Spread records deterministically inside the state they name.

    APHIS publishes a state, not a site. Every record for a state therefore
    lands on one centroid - 24,241 records across ~50 points, six hundred deep,
    and only the top one is clickable. That is not a map.

    So each record is offset inside a disc roughly the size of a state, using a
    hash of its own permit number. Deterministic, so a record does not move
    between runs and the index can fly to what is drawn. `precise` stays false
    and the entry says plainly that the position is a scatter within the state
    rather than a location - inventing a site would be worse than stacking.
    """
    h = hashlib.md5(key.encode("utf-8")).digest()
    a = (h[0] << 8 | h[1]) / 65535.0 * 6.283185
    r = ((h[2] << 8 | h[3]) / 65535.0) ** 0.5 * spread
    return round(lat + math.sin(a) * r * 0.62, 4), round(lng + math.cos(a) * r, 4)

def build(rows, source_label):
    legacy = (source_label == "epermits")
    out = []
    for r in rows:
        status = (r.get("Status") or "").strip()
        sl = status.lower()
        # A withdrawn or denied application was never an authorisation, so it is
        # not a release and never appears. Everything that WAS granted stays -
        # including permits that have since lapsed. This map is a record of the
        # industry since it began, not a list of what is live this morning, and
        # a trial that ran in 1994 happened whether or not the paperwork is
        # still in date.
        # Counted as well as dropped. The map says it drops these and could not
        # say how many, because the count died right here - the reader was asked
        # to take "some records are excluded" on trust. Published in the file's
        # header so the sentence can carry a real number.
        DROPSTAT["seen"] += 1
        if sl in NEVER_GRANTED:
            DROPSTAT["by_status"][sl] = DROPSTAT["by_status"].get(sl, 0) + 1
            continue
        states = release_states(get(r, "Location(s)", legacy))
        if not states:
            continue                      # no environmental release component
        eff = parse_date(get(r, "Effective Date", legacy))
        exp = parse_date(get(r, "Expiration Date", legacy))
        lapsed = bool(exp and exp < date.today())
        if legacy and not exp:
            # ePermits stopped accepting applications on 30 September 2022, so a
            # legacy record with no expiry date cannot be shown to be current.
            # It is still a real authorisation that was granted, so it is kept
            # and marked past rather than discarded.
            lapsed = True
        if False:
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
                   redaction + " The dot is scattered inside the state, not placed at a site: APHIS "
                   "publishes the state and the number of release locations, never the "
                   "locations themselves. Australia is the only regulator in the world "
                   "that publishes field trial sites."))

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
            # `lapsed` marks an authorisation that was granted and has since
            # run out. The map's "Show dormant / defunct" switch reads it.
            "lapsed": lapsed,
            "status": (status + (" \u2014 expired" if lapsed else "")).strip(),
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
        # Exit 0: the workflow step stops on any non-zero status, and an
        # unreachable source must not block the rest of the run.
        print("nothing harvested; leaving projects.json alone", file=sys.stderr)
        return

    records.sort(key=lambda x: x.get("date", ""), reverse=True)
    records = records[:keep]


    # Anything else the run produced. These used to be build inputs, embedded
    # into index.html at build time - which meant a harvester could succeed and
    # its 2,210 records would still never reach the map without a rebuild.
    # They are merged into projects.json instead, which the map fetches.
    # Two harvesters were missing from this list. fertility_clinics.py and
    # animal_testing_facilities.py ran every week, wrote their JSON, had it
    # committed, and stopped there: nothing read the files, so 21 records never
    # reached the map. They also write under their own key ("clinics",
    # "facilities") rather than "projects", and their rows carry lat/lng as
    # strings with no source field, so they need converting rather than
    # appending.
    # A tag and an organism as well as a source. An industry record with no tags
    # is not hidden by default, but it disappears the moment a reader picks a
    # lens - so an untagged record is one that works until somebody uses the
    # filters. These are clinic registers and laboratory-animal registers, and
    # they belong in the facets of those names.
    EXTRAS = (("clinical_sponsors.json", "projects", None, None, None),
              ("register_records.json", "projects", None, None, None),
              ("animal_facilities.json", "projects", None, None, None),
              ("ogtr_trials.json", "projects", None, None, None),
              ("bch_decisions.json", "projects", None, None, None),
              # Clinic-level files. These already arrive in the map's shape and
              # carry their own tags, so they pass through unconverted.
              ("cdc_art_clinics.json", "projects", None, None, None),
              ("osm_facilities.json", "projects", None, None, None),
              ("aaalac_facilities.json", "projects", None, None, None),
              ("hfea_clinics.json", "projects", None, None, None),
              ("aphis_animal_facilities.json", "projects", None, None, None),
              ("china_nhc_art.json", "projects", None, None, None),
              ("ccac_redlara.json", "projects", None, None, None),
              ("advocacy_facilities.json", "projects", None, None, None),
              ("biolabs_facilities.json", "projects", None, None, None),
              ("biolabs.json", "projects", None, None, None),
              ("india_nartsr.json", "projects", None, None, None),
              ("fertility_clinics.json", "clinics", "industry:repro",
               ["repro:clinics"], ["human"]),
              ("animal_testing_facilities.json", "facilities", "industry:animals",
               ["animals:services"], ["lab_animals"]))

    def _as_record(row, source, tags=None, species=None):
        """One register pointer, in the shape the map reads."""
        try:
            lat, lng = float(row["lat"]), float(row["lng"])
        except (KeyError, TypeError, ValueError):
            return None
        return {"name": str(row.get("name", "")).strip()[:150],
                "source": source,
                "type": row.get("type") or "Register",
                "lat": lat, "lng": lng,
                "state": row.get("country") or row.get("iso") or "",
                # A national register has no address. Saying so is the whole
                # difference between a centroid and a place.
                "precise": False, "addr_grade": "centroid", "impact": 2,
                "company": "", "size": "", "status": "Register",
                "phase": "post", "date": "", "otype": "registry",
                "tags": list(tags or []), "species": list(species or []),
                "url": row.get("url", ""), "desc": row.get("desc", ""),
                "checked": ""}

    # These pointers overlap the hand-written industry entries - the HFEA
    # register is already on the map under its own name. Two dots on one
    # register is worse than one, so a record whose URL is already present is
    # dropped, and the count is printed rather than swallowed.
    seen_urls = {str(r.get("url", "")) for r in records if r.get("url")}

    for extra_file, key, source, tags, species in EXTRAS:
        fp = HERE / extra_file
        if not fp.exists():
            continue
        try:
            got = json.loads(fp.read_text(encoding="utf-8")).get(key, [])
        except Exception as e:
            print("  ! %s unreadable (%s)" % (extra_file, e), file=sys.stderr); continue
        if source:
            conv, dup, bad = [], 0, 0
            for row in got:
                rec = _as_record(row, source, tags, species)
                if not rec:
                    bad += 1; continue
                if rec["url"] and rec["url"] in seen_urls:
                    dup += 1; continue
                seen_urls.add(rec["url"]); conv.append(rec)
            got = conv
            if dup:
                print("  %s: %d already on the map under another name" % (extra_file, dup))
            if bad:
                print("  %s: %d rows with no usable coordinates" % (extra_file, bad))
        else:
            for r in got:
                if r.get("url"):
                    seen_urls.add(str(r["url"]))
        if got:
            records.extend(got)
            print("  merging %5d records from %s" % (len(got), extra_file))

    # Canadian approvals, if cfia_approvals.py has been run
    extra = []
    if CFIA.exists():
        try:
            extra = json.loads(CFIA.read_text(encoding="utf-8")).get("projects", [])
            print("  merging %d CFIA records" % len(extra))
        except Exception as e:
            print("  ! %s could not be read: %s" % (CFIA.name, e), file=sys.stderr)

    # Industry organisations and the escape record are embedded in index.html
    # instead, so this file stays machine-maintained. The map unions the two at
    # load time, keyed on url, so nothing appears twice.
    extra = []

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
        "dropped": {"reason": "never authorised \u2014 withdrawn, denied, void, "
                              "returned, incomplete or cancelled",
                    "by_status": DROPSTAT["by_status"],
                    "total": sum(DROPSTAT["by_status"].values()),
                    "seen": DROPSTAT["seen"],
                    "share_pct": (round(100.0 * sum(DROPSTAT["by_status"].values())
                                        / DROPSTAT["seen"], 1)
                                  if DROPSTAT["seen"] else 0)},
        "source": "APHIS BRS public data files, " + date.today().isoformat(),
        "projects": curated + extra + records,
    }

    lap = sum(1 for r in records if r.get("lapsed"))
    print("  live: %d | granted and since expired: %d" % (len(records) - lap, lap))
    pre = sum(1 for r in records if r["phase"] == "pre")
    print("\n%d release records (%d under assessment, %d consented) + %d curated"
          % (len(records), pre, len(records) - pre, len(curated)))
    orgs = {}
    for r in records:
        k = norm_org(r["company"])
        orgs[k] = orgs.get(k, 0) + 1
    # GROUP EVERY RELEASE RECORD BY PLACE, WHATEVER THE SOURCE.
    # Grouping each source separately left three markers stacked on one centroid
    # - one from APHIS, one from the Cartagena filing, one from CFIA - which is
    # the same unclickable pile, just wearing three hats. A reader does not care
    # which register a permit came from until after they have found the place.
    #
    # So: one marker per coordinate. The popup then breaks down BY SOURCE, each
    # with its own count and its own expandable list, because that is the point
    # at which provenance starts to matter.
    from collections import defaultdict, OrderedDict
    SRCNAME = {"aphis": "US APHIS permits and notifications",
               "bch": "National decisions filed to the Cartagena Protocol",
               "cfia": "Canadian approvals (CFIA)",
               "ogtr": "Australian licences (OGTR)"}
    at = defaultdict(list)
    for r in records:
        at[(round(r["lat"], 3), round(r["lng"], 3))].append(r)

    merged = []
    for (la, ln), rs in at.items():
        if len(rs) == 1:
            merged.append(rs[0]); continue
        by_src = OrderedDict()
        for r in sorted(rs, key=lambda x: x.get("date", ""), reverse=True):
            k = str(r.get("source", "")).split(":")[0]
            by_src.setdefault(k, []).append(r)
        place = rs[0].get("state") or "Unstated"
        yrs = [x["date"][:4] for x in rs if x.get("date")]
        span = ("%s\u2013%s" % (min(yrs), max(yrs))) if yrs else ""
        merged.append({
            "name": "%s \u2014 %d release records" % (place, len(rs)),
            "source": rs[0]["source"],
            "type": "Release records, all sources",
            "lat": la, "lng": ln, "state": place, "precise": False,
            # The 1-5 scale impact_for() computes per record was being replaced
            # with a flat 2-or-3 here, so every grouped marker drew as medium or
            # largest and the Small and Large steps of the scale filter had
            # nothing in them. A place is as big as its biggest release.
            "impact": max([r.get("impact", 1) for r in rs] or [1]),
            "company": "",
            "size": "%d records" % len(rs),
            "status": ("%s, %d source%s" % (span or "date not stated", len(by_src),
                                            "" if len(by_src) == 1 else "s")),
            # Same for consent phase: forcing "post" hid every under-assessment
            # record inside a consented marker. A place with anything still in
            # review is a place in review.
            "phase": ("pre" if any(r.get("phase") == "pre" for r in rs) else "post"),
            "date": rs[0].get("date", ""),
            "lapsed": all(x.get("lapsed") for x in rs),
            "level": rs[0].get("level", ""), "parent": rs[0].get("parent", ""),
            "records_total": len(rs),
            # Every date under this marker, so the recency filter can ask whether
            # ANY record here is recent rather than only the newest one.
            "dates": sorted({r.get("date", "")[:10] for r in rs if r.get("date")}),
            "sources": [{"k": k, "label": SRCNAME.get(k, k), "n": len(v),
                         "records": [{"n": x["name"][:110], "d": x.get("date", ""),
                                      "s": x.get("status", ""), "u": x.get("url", ""),
                                      "c": x.get("company", ""),
                                      # type is "<organism>, environmental release",
                                      # so the panel's type filter becomes an organism filter
                                      "t": x.get("type", "")} for x in v]}
                        for k, v in by_src.items()],
            "url": rs[0]["url"],
            "desc": ("WHAT. %d release records at this point%s, from %s. "
                     "WHERE IT SITS. Registers publish a state or a country, almost never a site, "
                     "so every record for a place shares one coordinate. "
                     "WHY IT MATTERS. They are one marker rather than a stack because a pile of "
                     "pins on one centroid cannot be clicked past. Open it and each register is "
                     "listed separately with its own count. **Australia is the only regulator in "
                     "the world that publishes field trial sites.**"
                     % (len(rs), (", %s" % span) if span else "",
                        ", ".join(SRCNAME.get(k, k) for k in by_src))),
            "checked": "",
        })
    # A country marker above the US state markers. This was written in an
    # earlier round and lost when the grouping was rewritten to merge across
    # sources - so the map had state markers with no parent to collapse into,
    # which is why both levels appeared at once.
    #
    # `parent` must equal the country marker's own key exactly, or the map hides
    # the country and never reveals its states.
    US_KEY = "United States"
    kids = [g for g in merged
            if str(g.get("source", "")).startswith("aphis") and len(str(g.get("state", ""))) <= 24]
    for g in kids:
        g["level"] = "state"
        g["parent"] = US_KEY
    if kids:
        tot = sum(g.get("records_total", 1) for g in kids)
        merged.append({
            "name": "United States \u2014 %s release records" % format(tot, ","),
            "source": kids[0]["source"], "type": "Release records, by state",
            "lat": 39.8, "lng": -98.6, "state": US_KEY, "precise": False,
            "impact": 3, "company": "", "size": "%s records across %d states" % (format(tot, ","), len(kids)),
            "status": "Click to break into states", "phase": "post", "date": "",
            "lapsed": False, "level": "country", "parent": US_KEY,
            "children": [{"n": g.get("state", ""), "c": g.get("records_total", 1),
                          "la": g["lat"], "lo": g["lng"]}
                         for g in sorted(kids, key=lambda x: -x.get("records_total", 1))],
            "records_total": tot,
            "url": kids[0]["url"],
            "desc": ("WHAT. Every US release record on this map, %s of them across %d states. "
                     "WHERE IT SITS. Above the state markers, which appear when this is clicked "
                     "and replace it \u2014 the two never draw together, because one contains the "
                     "others and side by side they would read as peers. "
                     "WHY IT MATTERS. There is no level below state. APHIS publishes the states a "
                     "permit covers and how many sites are in each, never the coordinates, so a "
                     "marker is a state or a country and never a field. **Australia\u2019s OGTR is "
                     "the only regulator in the world that publishes field trial sites.**"
                     % (format(tot, ","), len(kids))),
            "checked": "",
        })
        print("  + 1 country marker over %d US state markers" % len(kids))
    print("  %d records \u2192 %d place markers (all sources merged)" % (len(records), len(merged)))
    records = merged

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
    # The map fetches projects.json.gz FIRST - the raw JSON is past GitHub's
    # file-size limit, so the gzipped copy is the one it actually reads. Nothing
    # was writing it, so a stale .gz from an old run has been served on every
    # visit while every fresh harvest sat unread in projects.json. Write both.
    import gzip
    gzp = pathlib.Path(str(OUT) + ".gz")
    with gzip.open(str(gzp), "wb", compresslevel=9) as gz:
        gz.write(json.dumps(doc, ensure_ascii=False).encode("utf-8"))
    print("wrote %s (%d KB) - THIS is the file the map loads"
          % (gzp.name, gzp.stat().st_size // 1024))
    print("\nwrote %s" % OUT.name)


if __name__ == "__main__":
    main()
