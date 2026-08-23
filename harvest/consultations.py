#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Consultations that are open right now, with the date they shut.

Everything else on this map is true next year. A comment window is worthless
the day after it closes, which makes this the only thing here that has to be
fetched rather than written.

WHAT CHANGED, AND WHY THE OLD FILE COULD NOT WORK
-------------------------------------------------
The previous version queried five sources and returned two rows, both United
States, every night. Not one of the four non-US sources could have returned
anything:

  ePing          pointed at epingalert.org/api/notifications - the legacy alert
                 site, and no such endpoint. This was the whole of the map's
                 worldwide coverage, so its death is why the panel was American.
  EFSA           efsa.europa.eu/en/consultations is a 404. Open calls moved to
                 a Salesforce app that renders from JavaScript and serves a
                 fetcher an empty shell. It is no longer harvestable and is
                 reported as a venue rather than scraped.
  BCH            asked for schema_s:biosafetyDecision, then filtered on a
                 comment deadline. Wrong RECORD TYPE, not a wrong field name: a
                 decision record documents a decision already taken (Cartagena
                 Art. 20 - filed within 15 days OF deciding), so any
                 consultation preceding it is over. Art. 23 obliges parties to
                 consult the public but does not require the consultation to be
                 filed, and the BCH publishes no open-window schema. Venue, not
                 feed. If that ever changes, look for a schema with a deadline
                 field, not another field name on the decision schema.
  OGTR          reachable, but `listing()` required the ANCHOR TEXT to match a
                 consultation word AND a genetics word inside a bare text node.
                 An OGTR link reads "DIR 200 - Commercial release of ..." and
                 contains no consultation word, and its label is wrapped in a
                 span, so the regex never saw it.

And the Federal Register query asked for `conditions[comment_date][gte]`, which
is not a documented condition. The API IGNORES unrecognised conditions rather
than refusing them, so the search silently widened to the whole Register.

SOURCES NOW

  WTO / ePing        Every WTO member must notify a draft technical or
                     sanitary regulation before enforcing it, with a comment
                     period attached. 160-odd members file into one workbook,
                     regenerated daily, no key and no login:
                       eping.wto.org/NotificationExcelFiles/Notification_EN.xlsx
                     listed as a resource on the WTO's own catalogue entry,
                     data.wto.org/en/dataset/ext_eping. The API at
                     apiportal.wto.org needs a subscription key; the workbook
                     does not. This is the only source here with worldwide
                     coverage and it carries the notifying member per row.
  Federal Register   a real JSON API, documented and filterable.
  OGTR               a listing page, parsed for licence applications open for
                     submissions.

  EFSA and the BCH   reported as venues with a standing address, carrying
                     kind:"note". They are counted in `sources_total` but not
                     in `sources_reached`, because a venue cannot fail and
                     must not be able to disguise a night when every real feed
                     did.

Output always states when it was generated and which feeds answered, so the
map can tell a failed fetch from an empty world instead of asserting the
stronger claim on no evidence.

    python3 harvest/consultations.py
    python3 harvest/consultations.py --dry-run
    python3 harvest/consultations.py --selftest        # no network
    python3 harvest/consultations.py --dump-headers    # print the WTO columns
"""

import io
import json
import pathlib
import re
import sys
import zipfile
from datetime import date, datetime, timedelta, timezone
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "consultations.json"
UA = "GMO-map/1.0 (public research map)"

FR_API = "https://www.federalregister.gov/api/v1/documents.json"
WTO_XLSX = "https://eping.wto.org/NotificationExcelFiles/Notification_EN.xlsx"
WTO_PORTAL = "https://eping.wto.org/en/Search"
OGTR = "https://www.ogtr.gov.au/what-weve-approved/dealings-involving-intentional-release"
EFSA_VENUE = "https://connect.efsa.europa.eu/RM/s/consultations"
BCH_VENUE = "https://bch.cbd.int/"


def today_utc():
    """The runner's UTC date. The map parses `generated` with an explicit Z
    for this reason; do not switch this to date.today()."""
    return datetime.now(timezone.utc).date()


def get(url, timeout=60):
    req = Request(url, headers={"User-Agent": UA,
                                "Accept": "application/json, text/html, */*"})
    return urlopen(req, timeout=timeout).read().decode("utf-8", "replace")


def get_bytes(url, timeout=180):
    req = Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    return urlopen(req, timeout=timeout).read()


# ================================================================ SUBJECT ====
#
# Two tiers, because one list applied to everything is what put fruit imports
# in this panel.
#
# SUBJECT is matched against SHORT, SPECIFIC fields only - a title, a products
# column. A category word is fine here: a notification whose TITLE says
# biotechnology is about biotechnology.
#
# STRONG is matched against long prose - an objective or description paragraph
# that mentions many things. Seven of the first live run's twelve rows matched
# on such a paragraph and none of them were about an engineered organism:
# halal certification "including products derived from biotechnology",
# entry-exit animal quarantine. A phrase here has to be unable to mean anything
# else. `biotechnolog` is deliberately absent for exactly that reason.

SUBJECT = [
    "genetic", "genetically", "genome", "genomic", "transgen", "gmo",
    "living modified", "biosafety", "biotechnolog", "bioengineered",
    "crispr", "gene edit", "gene-edit", "genome edit", "gene drive",
    "recombinant", "engineered organism", "intentional genomic alteration",
    "plant-incorporated protectant", "plant incorporated protectant",
    "deliberate release", "novel food", "novel trait", "cisgenic",
    "intragenic", "synthetic biology", "germline",
    # The members this source exists to reach are largely not Anglophone. An
    # English-only filter leaves a "global" feed that is quietly Anglophone:
    # a stub run kept Kenya and Viet Nam and dropped Peru's "Reglamento sobre
    # organismos vivos modificados". Accented and unaccented forms both appear.
    "organismos vivos modificados", "organismes vivants modifi",
    "organismos geneticamente modificados", "geneticamente modificad",
    "gen\u00e9ticamente modificad", "g\u00e9n\u00e9tiquement modifi",
    "modificados geneticamente", "transg\u00e9n", "transg\u00eanic",
    "bioseguridad", "biosseguran", "bioseguran", "biotecnolog",
    # ACCENTED ONLY. Unaccented "biosecurit" is English for plant and animal
    # QUARANTINE - mangosteen imports, entry-exit inspection - and it put two
    # fruit notices in the panel on the first live run. The French
    # biosecurite/biosecurite spellings are unambiguous; the English one is not.
    "bios\u00e9curit", "bios\u00e9curite", "biose\u0301curit",
]

STRONG = [
    "genetically modified organism", "genetically engineered",
    "genetically modified", "living modified organism", "gene drive",
    "transgenic", "genome editing", "gene editing", "crispr",
    "organismos vivos modificados", "organismos geneticamente modificados",
    "organismes vivants modifi", "g\u00e9n\u00e9tiquement modifi",
    "gen\u00e9ticamente modificad", "geneticamente modificad",
    "transg\u00e9nic", "transg\u00eanic",
]

# Short forms need a word boundary. "gm" inside "alignment" and "lmo" inside
# "filmore" are the kind of match that puts a fisheries notice on this map.
WORDS = re.compile(r"\b(gm|gmos?|lmos?|ogm|ovm|vgm|bt)\b", re.I)

# A body whose entire remit is this subject. Its consultations qualify on the
# agency alone: OGTR publishes nothing off-topic here, and a licence
# application titled "DIR 200" matches no term in either list above.
AGENCY_OK = [
    "ogtr", "gene technology regulator", "ctnbio", "cibiogem", "geac",
    "biosafety", "aphis biotechnology", "nbma", "clearing-house",
]

# A chemical is a different subject even when the crop it is sprayed on is
# engineered.
TITLE_NO = re.compile(
    r"tolerances?\b|pesticide product registration|registration review|"
    r"inert ingredient|antimicrobial|residue|air quality|drinking water|"
    r"significant new use|premanufacture notice", re.I)


def on_topic(short, long_text="", agency=""):
    """short: title and products. long_text: objective, description, prose."""
    ag = (agency or "").lower()
    for a in AGENCY_OK:
        if a in ag:
            return True
    s = (short or "").lower()
    if TITLE_NO.search(s):
        return False
    for t in SUBJECT:
        if t in s:
            return True
    if WORDS.search(s):
        return True
    l = (long_text or "").lower()
    for t in STRONG:
        if t in l:
            return True
    return False


# =================================================================== DATES ===

# Excel's epoch is 1899-12-30, not 1900-01-01: it believes 1900 was a leap
# year. Verified by writing date(2026, 9, 15) with openpyxl and reading the
# raw <v> back - 46280. Getting this wrong shifts every deadline in the panel
# by four days with nothing anywhere reporting an error.
EXCEL_EPOCH = date(1899, 12, 30)

_ISO = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
_DMY = re.compile(r"\b(\d{1,2})[/.-](\d{1,2})[/.-](\d{4})\b")
_LONG = re.compile(r"(\d{1,2})\s+(January|February|March|April|May|June|July|"
                   r"August|September|October|November|December)\s+(\d{4})", re.I)


def cell_date(v):
    """A date out of a spreadsheet cell or a page, in any shape these use."""
    if v is None:
        return None
    s = str(v).strip()
    if not s:
        return None
    m = _ISO.search(s)
    if m:
        try:
            return date(*map(int, m.groups()))
        except ValueError:
            return None
    m = _DMY.search(s)
    if m:
        d, mo, y = map(int, m.groups())
        # The WTO writes day first. Where the first number cannot be a day the
        # order is taken the other way round rather than dropping the row.
        if d > 12 >= mo or mo <= 12 >= d:
            try:
                return date(y, mo, d)
            except ValueError:
                pass
        try:
            return date(y, d, mo)
        except ValueError:
            return None
    m = _LONG.search(s)
    if m:
        try:
            return datetime.strptime(" ".join(m.groups()).title(),
                                     "%d %B %Y").date()
        except ValueError:
            return None
    try:
        n = float(s)
    except ValueError:
        return None
    if 20000 < n < 80000:                       # a plausible Excel serial
        return EXCEL_EPOCH + timedelta(days=int(n))
    return None


def dates_in(text):
    out = []
    for rx in (_LONG, _ISO):
        for m in rx.finditer(text):
            d = cell_date(m.group(0))
            if d:
                out.append(d)
    return out


# ==================================================================== XLSX ===
#
# A streaming reader on the standard library. openpyxl is NOT installed in CI
# and adding a pip step to a job that needs none is the worse trade; the
# workbook is also 100,000+ rows, which is a reason to stream it rather than
# hold it.

_NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def _col(ref):
    return "".join(ch for ch in (ref or "") if ch.isalpha())


def xlsx_rows(blob):
    """Yield each sheet row as {column letter: text}."""
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        names = z.namelist()
        shared = []
        if "xl/sharedStrings.xml" in names:
            with z.open("xl/sharedStrings.xml") as fh:
                ctx = ET.iterparse(fh, ("start", "end"))
                _, root = next(ctx)
                for ev, el in ctx:
                    if ev == "end" and el.tag == _NS + "si":
                        shared.append("".join(t.text or ""
                                              for t in el.iter(_NS + "t")))
                        root.clear()
        sheets = sorted(n for n in names
                        if n.startswith("xl/worksheets/sheet") and n.endswith(".xml"))
        if not sheets:
            raise RuntimeError("no worksheet in the workbook")
        with z.open(sheets[0]) as fh:
            ctx = ET.iterparse(fh, ("start", "end"))
            _, root = next(ctx)
            for ev, el in ctx:
                if ev != "end" or el.tag != _NS + "row":
                    continue
                cells = {}
                for c in el.findall(_NS + "c"):
                    t = c.get("t")
                    if t == "inlineStr":
                        node = c.find(_NS + "is")
                        v = ("".join(x.text or "" for x in node.iter(_NS + "t"))
                             if node is not None else "")
                    else:
                        node = c.find(_NS + "v")
                        v = node.text if node is not None and node.text else ""
                        if t == "s" and v != "":
                            try:
                                v = shared[int(v)]
                            except (ValueError, IndexError):
                                v = ""
                    cells[_col(c.get("r"))] = v
                yield cells
                root.clear()                    # or the sheet accumulates


# Headers are matched by SUBSTRING NAME, never by position, and with several
# spellings each: the column order is the WTO's to change and a positional read
# breaks silently the first time they do. --dump-headers prints the real ones.
WANT = {
    "deadline": ["final date for comments", "final date for comment",
                 "comment deadline", "deadline for comments", "final date",
                 "comments due", "deadline"],
    "member":   ["notifying member", "notifying country", "member", "country"],
    "title":    ["title"],
    "products": ["products covered", "product covered", "products", "product"],
    "objective": ["objective", "description", "abstract", "summary",
                  "content", "rationale"],
    "link":     ["document link", "notification link", "link", "url",
                 "document"],
    "symbol":   ["notification symbol", "symbol", "reference", "id"],
    "kind":     ["notification type", "type of notification", "type",
                 "agreement"],
    "date":     ["distribution date", "date of distribution", "notified on"],
}


def map_headers(header_row):
    """{field: column letter} for whatever the workbook calls its columns."""
    found, taken = {}, set()
    norm = {k: re.sub(r"\s+", " ", (v or "").strip().lower())
            for k, v in header_row.items()}
    for field, spellings in WANT.items():
        for want in spellings:                  # most specific spelling first
            hit = None
            for colletter, text in norm.items():
                if colletter in taken or not text:
                    continue
                if want in text:
                    hit = colletter
                    break
            if hit:
                found[field] = hit
                taken.add(hit)
                break
    return found


def _wto_agency(kind):
    """"WTO %s notification" % kind produced "WTO Addendum to Regular
    Notification notification" on the live map. Say it once."""
    k = re.sub(r"\s+", " ", str(kind or "")).strip()
    if not k:
        return "WTO notification"
    if re.search(r"notification", k, re.I):
        return "WTO " + k
    return "WTO %s notification" % k


def wto_notifications(blob, today=None, report_headers=False):
    """Select the open, on-subject rows out of the workbook.

    Kept separate from the download so the selftest can drive it against a
    workbook it builds itself, with no network.
    """
    today = today or today_utc()
    rows = xlsx_rows(blob)
    try:
        header = next(rows)
    except StopIteration:
        raise RuntimeError("the workbook is empty")
    cols = map_headers(header)
    if report_headers:
        print("  columns as the workbook names them:")
        for letter in sorted(header, key=lambda c: (len(c), c)):
            print("    %-4s %s" % (letter, header[letter]))
        print("  matched: " + ", ".join("%s=%s" % (k, v)
                                        for k, v in sorted(cols.items())))
    if "deadline" not in cols:
        # Loud, never a silent empty. Without a deadline column every row is
        # unusable and a zero here would read exactly like a quiet world.
        raise RuntimeError(
            "no comment-deadline column found in the WTO workbook. Its "
            "headers are: " + "; ".join(sorted(v for v in header.values() if v))
            + ". Run --dump-headers and add the new spelling to WANT.")
    out, scanned, on_subject = [], 0, 0
    for cells in rows:
        scanned += 1
        close = cell_date(cells.get(cols["deadline"], ""))
        if not close:
            continue
        title = (cells.get(cols.get("title", ""), "") or "").strip()
        products = (cells.get(cols.get("products", ""), "") or "").strip()
        objective = (cells.get(cols.get("objective", ""), "") or "").strip()
        short = (title + " " + products).strip()
        if not on_topic(short, objective):
            continue
        on_subject += 1
        if close < today:
            continue
        member = re.sub(r"\s+", " ",
                        (cells.get(cols.get("member", ""), "") or "")).strip()
        url = (cells.get(cols.get("link", ""), "") or "").strip()
        if not url.startswith("http"):
            url = WTO_PORTAL
        out.append({
            "title": (title or products or "WTO notification")[:200],
            "agency": _wto_agency(cells.get(cols.get("kind", ""), "")),
            "closes": close.isoformat(),
            "url": url,
            "country": member or "Worldwide",
            "ref": (cells.get(cols.get("symbol", ""), "") or "").strip() or None,
        })
    seen, uniq = set(), []
    for r in out:
        k = r.get("ref") or (r["url"] + r["title"][:40])
        if k in seen:
            continue
        seen.add(k)
        uniq.append(r)
    return uniq, scanned, on_subject


def wto(report):
    label = "WTO / ePing notifications"
    try:
        blob = get_bytes(WTO_XLSX)
    except Exception as e:
        print("  %-30s unreachable (%s)" % (label, str(e)[:44]))
        report.append({"name": label, "kind": "feed", "ok": False, "rows": 0,
                       "url": WTO_PORTAL,
                       "message": "could not be fetched on the last run"})
        return []
    try:
        rows, scanned, on_subject = wto_notifications(
            blob, report_headers="--dump-headers" in sys.argv)
    except Exception as e:
        print("  %-30s FAILED: %s" % (label, str(e)[:200]))
        report.append({"name": label, "kind": "feed", "ok": False, "rows": 0,
                       "url": WTO_PORTAL,
                       "message": "the workbook was fetched but could not be "
                                  "read: " + str(e)[:120]})
        return []
    if not rows:
        # Reached and read. This looks identical in the output file to a
        # failure and is the opposite problem.
        print("  %-30s reachable, 0 open (%d rows scanned, %d on subject)"
              % (label, scanned, on_subject))
    else:
        print("  %-30s %d open (%d rows scanned, %d on subject)"
              % (label, len(rows), scanned, on_subject))
    report.append({"name": label, "kind": "feed", "ok": True, "rows": len(rows),
                   "url": WTO_PORTAL,
                   "message": "%d notifications scanned" % scanned})
    return rows


# ======================================================== FEDERAL REGISTER ===

FR_TERMS = ["genetically engineered organism", "modified organism",
            "petition for determination of nonregulated status",
            "plant-incorporated protectant", "bioengineered food",
            "gene drive", "genetically engineered animal"]

TITLE_OK = re.compile(
    r"genetic|engineered|bioengineer|nonregulated status|"
    r"plant-incorporated|gene drive|biotechnolog|transgenic|"
    r"modified organism", re.I)


def federal_register(report):
    label = "Federal Register"
    out, today = [], today_utc()
    since = (today - timedelta(days=270)).isoformat()
    answered = 0
    for term in FR_TERMS:
        # `conditions[comment_date][gte]` is NOT a documented condition, and
        # the API ignores conditions it does not recognise rather than
        # refusing them - so that query silently widened to the whole
        # Register and came back holding airworthiness directives. Filter the
        # publication date, which IS documented, and test the closing date
        # here: correct whether or not the other condition exists.
        q = urlencode({
            "conditions[term]": term,
            "conditions[publication_date][gte]": since,
            "per_page": 100,
            "order": "newest",
            "fields[]": "title",
        }, doseq=True)
        q += "&fields[]=" + "&fields[]=".join(
            ["html_url", "comments_close_on", "agencies", "publication_date",
             "document_number"])
        try:
            d = json.loads(get(FR_API + "?" + q))
        except Exception as e:
            print("  %-30s %s  [%s]" % (label, str(e)[:40], term[:28]))
            continue
        answered += 1
        for r in d.get("results") or []:
            close = r.get("comments_close_on")
            if not close or close < today.isoformat():
                continue
            title = r.get("title") or ""
            if not TITLE_OK.search(title) or TITLE_NO.search(title):
                continue
            ag = r.get("agencies") or []
            out.append({
                "title": title[:200],
                "agency": (ag[0].get("name") if ag and isinstance(ag[0], dict)
                           else "US federal agency"),
                "closes": close,
                "url": r.get("html_url"),
                "country": "United States",
                "ref": r.get("document_number"),
            })
    seen, uniq = set(), []
    for r in out:                               # one document matches several terms
        k = r.get("ref") or r["url"]
        if k in seen:
            continue
        seen.add(k)
        uniq.append(r)
    if not answered:
        # Reporting 0 here rather than FAIL is how a total outage once counted
        # as a source that answered.
        print("  %-30s FAILED: no query answered" % label)
        report.append({"name": label, "kind": "feed", "ok": False, "rows": 0,
                       "url": "https://www.federalregister.gov/",
                       "message": "could not be fetched on the last run"})
        return []
    print("  %-30s %d open (%d of %d queries answered)"
          % (label, len(uniq), answered, len(FR_TERMS)))
    report.append({"name": label, "kind": "feed", "ok": True, "rows": len(uniq),
                   "url": "https://www.federalregister.gov/",
                   "message": "%d of %d queries answered" % (answered, len(FR_TERMS))})
    return uniq


# ================================================================= LISTING ===

_TAGS = re.compile(r"<[^>]+>")


def listing(url, country, label, agency, report):
    """OGTR publishes a listing rather than an API.

    Two things the old version got wrong. It demanded a bare text node
    (`>([^<]{15,160})<`), so any label wrapped in a span did not match at all;
    and it required a consultation word AND a subject word in the anchor text,
    which an application titled "DIR 200 - Commercial release of ..." does not
    have. The agency qualifies the row on its own here.
    """
    try:
        html = get(url)
    except Exception as e:
        print("  %-30s unreachable (%s)" % (label, str(e)[:40]))
        report.append({"name": label, "kind": "feed", "ok": False, "rows": 0,
                       "url": url,
                       "message": "could not be fetched on the last run"})
        return []
    uniq, anchors = _parse_listing(html, url, country, agency)
    if not uniq:
        print("  %-30s reachable, 0 open (%d links read)" % (label, anchors))
    else:
        print("  %-30s %d open (%d links read)" % (label, len(uniq), anchors))
    report.append({"name": label, "kind": "feed", "ok": True, "rows": len(uniq),
                   "url": url, "message": "%d links read" % anchors})
    return uniq


# =================================================================== NOTES ===

def venues(report):
    """Two bodies that hold consultations and publish no fetchable list of
    open ones. Carried as venues so the panel can send a reader there, and
    marked kind:"note" so they cannot be counted as feeds that answered."""
    report.append({
        "name": "EFSA", "kind": "note", "ok": True, "rows": 0,
        "url": EFSA_VENUE,
        "message": "EFSA's open calls sit in an application that renders from "
                   "JavaScript, so this list cannot be read by a fetcher. The "
                   "old address, /en/consultations, is a 404, and "
                   "/en/calls/consultations is an archive of expired calls. "
                   "Open the venue directly."})
    report.append({
        "name": "Biosafety Clearing-House", "kind": "note", "ok": True, "rows": 0,
        "url": BCH_VENUE,
        "message": "The Cartagena Protocol obliges a party to consult the "
                   "public (Art. 23) but does not require the consultation to "
                   "be filed, and the BCH publishes no open-window record "
                   "type. Its decision records document decisions already "
                   "taken. Search the national records for your own country."})


# ==================================================================== MAIN ===

NOTE = ("Comment windows open at the time of harvest. The map checks the "
        "generated date and refuses to show this list if it is stale, because "
        "a closed window presented as open is worse than no list at all. "
        "sources_reached counts FEEDS that answered; a venue with no fetchable "
        "list is carried as kind:\"note\" and is not counted.")


def main():
    dry = "--dry-run" in sys.argv
    today = today_utc()
    print("Consultations open as of %s (UTC)" % today.isoformat())
    report, rows = [], []
    rows += federal_register(report)
    rows += listing(OGTR, "Australia", "OGTR",
                    "Office of the Gene Technology Regulator", report)
    rows += wto(report)
    venues(report)

    feeds = [s for s in report if s.get("kind") == "feed"]
    reached = sum(1 for s in feeds if s.get("ok"))
    if reached == 0:
        # Nothing answered. Writing an empty file here would be read by every
        # reader as "no consultation is open anywhere", which is a far worse
        # lie than yesterday's list: the workflow leaves the previous file in
        # place when this exits non-zero.
        print("\nEVERY FEED FAILED. Nothing written - the previous file stands.",
              file=sys.stderr)
        sys.exit(1)

    rows.sort(key=lambda r: (r["closes"], r["country"], r["title"][:40]))
    soon = [r for r in rows
            if r["closes"] <= (today + timedelta(days=14)).isoformat()]
    countries = sorted({r["country"] for r in rows})
    print("\n  %d open across %d countries, %d closing within a fortnight"
          % (len(rows), len(countries), len(soon)))
    print("  feeds answered: %d of %d" % (reached, len(feeds)))
    for r in rows[:10]:
        print("     %s  %-16s %s" % (r["closes"], r["country"][:16], r["title"][:60]))

    if dry:
        print("dry run - nothing written")
        return
    OUT.write_text(json.dumps({
        "generated": today.isoformat(),
        "note": NOTE,
        "sources": report,
        "sources_reached": reached,
        "sources_total": len(feeds),
        "consultations": rows}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote %s: %d" % (OUT.name, len(rows)))


# ================================================================ SELFTEST ===

def _fixture_xlsx(rows):
    """Build a workbook by hand. openpyxl is not in CI, so the test that
    proves the reader works cannot depend on it either."""
    def esc(s):
        return (str(s).replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;"))
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    xml = ['<?xml version="1.0"?><worksheet xmlns="http://schemas.'
           'openxmlformats.org/spreadsheetml/2006/main"><sheetData>']
    for i, row in enumerate(rows, start=1):
        cells = []
        for j, v in enumerate(row):
            ref = letters[j] + str(i)
            if isinstance(v, (int, float)):
                cells.append('<c r="%s"><v>%s</v></c>' % (ref, v))
            else:
                cells.append('<c r="%s" t="inlineStr"><is><t>%s</t></is></c>'
                             % (ref, esc(v)))
        xml.append("<row r='%d'>%s</row>" % (i, "".join(cells)))
    xml.append("</sheetData></worksheet>")
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("[Content_Types].xml", '<?xml version="1.0"?><Types '
                   'xmlns="http://schemas.openxmlformats.org/package/2006/'
                   'content-types"/>')
        z.writestr("xl/worksheets/sheet1.xml", "".join(xml))
    return buf.getvalue()


def selftest():
    ok = True

    def check(name, cond):
        nonlocal ok
        print("  %-58s %s" % (name, "ok" if cond else "FAIL"))
        if not cond:
            ok = False

    # Dates. 46280 is the serial openpyxl writes for 2026-09-15; an epoch of
    # 1900-01-01 gives 2026-09-19 and nothing anywhere would report it.
    check("excel serial 46280 -> 2026-09-15",
          cell_date("46280") == date(2026, 9, 15))
    check("iso date", cell_date("2026-09-15T00:00:00") == date(2026, 9, 15))
    check("day-first date", cell_date("15/09/2026") == date(2026, 9, 15))
    check("long date", cell_date("15 September 2026") == date(2026, 9, 15))
    check("empty cell -> None", cell_date("") is None and cell_date(None) is None)

    # Subject, two tiers.
    check("english title kept",
          on_topic("Draft rule on genetically modified maize", ""))
    check("spanish title kept",
          on_topic("Reglamento sobre organismos vivos modificados", ""))
    check("french title kept",
          on_topic("Cadre national de bios\u00e9curit\u00e9", ""))
    check("portuguese title kept",
          on_topic("Normas de biosseguran\u00e7a para OGM", ""))
    check("english quarantine notice dropped",
          not on_topic("Mangosteen fruit from Malaysia: biosecurity import "
                       "requirements", "biosecurity requirements for the "
                       "importation of fresh fruit"))
    check("prose mentioning biotechnology once dropped",
          not on_topic("Halal certification requirements",
                       "requirements for products including those derived "
                       "from biotechnology and their labelling"))
    check("prose naming the modification kept",
          on_topic("Feed additive authorisation",
                   "authorisation of an additive produced by a genetically "
                   "modified strain"))
    check("pesticide tolerance dropped",
          not on_topic("Fluazinam; pesticide tolerances", ""))
    check("agency alone qualifies",
          on_topic("DIR 200 - Commercial release", "",
                   "Office of the Gene Technology Regulator"))
    check("word-boundary short form", on_topic("Labelling of GM food", "")
          and not on_topic("Alignment of vehicle headlamps", ""))

    # The workbook reader and the selection on top of it.
    soon = (today_utc() + timedelta(days=30))
    past = (today_utc() - timedelta(days=30))
    blob = _fixture_xlsx([
        ["Notification symbol", "Notifying Member", "Title",
         "Products covered", "Objective", "Final date for comments",
         "Notification type", "Document link"],
        ["G/TBT/N/PER/1", "Peru", "Reglamento sobre organismos vivos "
         "modificados", "OVM", "Establecer requisitos",
         (soon - EXCEL_EPOCH).days, "Regular Notification",
         "https://docs.wto.org/imrd/directdoc.asp?x=1"],
        ["G/SPS/N/KEN/2", "Kenya", "Draft standard for genetically modified "
         "maize", "Maize", "Food safety", soon.isoformat(),
         "Addendum to Regular Notification", ""],
        ["G/TBT/N/MYS/3", "Malaysia", "Mangosteen fruit: biosecurity import "
         "requirements", "Fresh fruit", "Plant quarantine",
         soon.isoformat(), "Regular Notification", ""],
        ["G/TBT/N/VNM/4", "Viet Nam", "Circular on transgenic crop labelling",
         "Food", "Labelling", past.isoformat(), "Regular Notification", ""],
    ])
    rows, scanned, on_subj = wto_notifications(blob)
    check("workbook read: 4 data rows scanned", scanned == 4)
    check("3 on subject, quarantine row not among them", on_subj == 3)
    check("2 still open (the closed one dropped)", len(rows) == 2)
    got = sorted(r["country"] for r in rows)
    check("countries are Kenya and Peru", got == ["Kenya", "Peru"])
    peru = [r for r in rows if r["country"] == "Peru"][0]
    check("excel serial deadline read as a date",
          peru["closes"] == soon.isoformat())
    check("per-notice link kept",
          peru["url"].startswith("https://docs.wto.org/"))
    kenya = [r for r in rows if r["country"] == "Kenya"][0]
    check("agency says notification once",
          kenya["agency"] == "WTO Addendum to Regular Notification")

    # Headers by name, not position: same workbook, columns reordered and
    # respelled the way the WTO is entitled to change them.
    blob2 = _fixture_xlsx([
        ["Title", "Deadline for comments", "Notifying country"],
        ["Draft biosafety regulation", soon.isoformat(), "Ghana"],
    ])
    rows2, _, _ = wto_notifications(blob2)
    check("columns matched by name after a reorder",
          len(rows2) == 1 and rows2[0]["country"] == "Ghana")

    # No deadline column must be loud, never an empty list.
    blob3 = _fixture_xlsx([["Title", "Notifying Member"],
                           ["Draft biosafety regulation", "Ghana"]])
    try:
        wto_notifications(blob3)
        check("no deadline column raises", False)
    except RuntimeError as e:
        check("no deadline column raises loudly",
              "deadline" in str(e).lower())

    # Nested markup in an anchor, which the old regex could not see.
    html = ('<div><a href="/applications/dir-200"><span class="t">DIR 200 - '
            'Commercial release of insect resistant cotton</span></a>'
            '<p>Submissions close ' + soon.strftime("%d %B %Y") + '</p></div>')
    got, anchors = _parse_listing(html, "https://www.ogtr.gov.au/x",
                                  "Australia",
                                  "Office of the Gene Technology Regulator")
    check("span-wrapped OGTR anchor parsed",
          len(got) == 1 and got[0]["closes"] == soon.isoformat())
    check("absolute url built from a root-relative href",
          got and got[0]["url"] == "https://www.ogtr.gov.au/applications/dir-200")

    print("\nselftest: " + ("all checks pass" if ok else "FAILURES ABOVE"))
    return 0 if ok else 1


def _parse_listing(html, url, country, agency):
    """The body of listing(), with the fetch taken out so the selftest drives
    the real parser rather than a copy of it. Returns (rows, anchors read)."""
    out, today, anchors = [], today_utc(), 0
    for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', html,
                         re.S | re.I):
        href = m.group(1)
        title = re.sub(r"\s+", " ", _TAGS.sub(" ", m.group(2))).strip()
        if len(title) < 12 or len(title) > 200:
            continue
        anchors += 1
        if not on_topic(title, "", agency):
            continue
        window = html[m.start(): m.start() + 1200]
        fut = [d for d in dates_in(window)
               if today <= d <= today + timedelta(days=400)]
        if not fut:
            continue
        if href.startswith("/"):
            href = re.match(r"(https?://[^/]+)", url).group(1) + href
        out.append({"title": title[:200], "agency": agency,
                    "closes": min(fut).isoformat(), "url": href,
                    "country": country})
    seen, uniq = set(), []
    for r in out:
        if r["url"] in seen:
            continue
        seen.add(r["url"])
        uniq.append(r)
    return uniq, anchors


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    main()
