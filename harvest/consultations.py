#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Consultations that are open right now, with the date they shut.

Everything else on this map is true next year. A comment window is worthless
the day after it closes, which makes this the only thing here that has to be
fetched rather than written.

It follows the wire's pattern rather than the browser's: harvested here,
written to a file, read by the map. A browser cannot fetch these sources
cross-origin reliably, and a feed that silently fails is worse than none - a
reader would see "no consultations open" and believe it.

SOURCES, and what each one actually is

  WTO / ePing        THE one that makes this global. Every WTO member must
                     notify a draft technical or sanitary regulation before
                     enforcing it, with a comment deadline attached. The
                     Secretariat regenerates a single spreadsheet of every
                     notification since 1995, daily, with no key and no login:
                       https://eping.wto.org/NotificationExcelFiles/Notification_EN.xlsx
                     160-odd countries file into one downloadable file. The
                     epingalert.org JSON API this script used to call does not
                     exist, and the eping.wto.org search page is a scrape that
                     answers one hour and not the next - which is how the panel
                     lost every non-US row between two runs on the same day.

  Federal Register   a real JSON API, filterable by publication date. The
                     comment-date condition this used to send is NOT a
                     documented condition, and the API IGNORES conditions it
                     does not recognise rather than refusing them, so the query
                     silently widened to the whole Register. Filter the closing
                     date in Python instead, which is correct whether or not
                     that condition ever exists.

  OGTR               a listing page, parsed for links and any date near them.

  EFSA               NOT harvestable and no longer scraped. /en/consultations
                     is a 404; /en/calls/consultations is an archive of closed
                     calls; open ones moved to a Salesforce app that renders
                     from JavaScript and serves a fetcher nothing. Reported as
                     a venue.

  Biosafety          NOT a feed. Article 23 obliges parties to consult the
  Clearing-House     public but does not require the consultation to be filed,
                     and the BCH publishes no open-window schema. The decision
                     records this used to query document a decision already
                     TAKEN (Article 20: filed within 15 days OF deciding), so
                     any consultation preceding one is over. Reported as a
                     venue. If this ever changes, look for a schema with a
                     deadline field - not another field name on the decision
                     schema.

Anything that cannot be parsed is reported and skipped. The output says when it
was generated and which sources answered, so the map can tell a failed fetch
apart from an empty world instead of asserting the stronger claim on no
evidence. If every FEED fails, nothing is written and the run exits 1: an empty
file would be read by every reader as "no consultation is open anywhere".

    python3 harvest/consultations.py
    python3 harvest/consultations.py --dry-run
    python3 harvest/consultations.py --selftest        # no network
    python3 harvest/consultations.py --dump-headers    # print the real columns
"""

import io
import json
import re
import sys
import pathlib
import zipfile
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta
from urllib.request import Request, urlopen
from urllib.parse import urlencode

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "consultations.json"
UA = "GMO-map/1.0 (public research map)"

WTO_XLSX = "https://eping.wto.org/NotificationExcelFiles/Notification_EN.xlsx"
WTO_HOME = "https://eping.wto.org/en/Search/Index"
FR_API = "https://www.federalregister.gov/api/v1/documents.json"
OGTR = ("https://www.ogtr.gov.au/what-weve-approved/"
        "dealings-involving-intentional-release")
EFSA_VENUE = "https://connect.efsa.europa.eu/RM/s/consultations"
BCH_VENUE = "https://bch.cbd.int/"


# ===================================================== SUBJECT MATCHING ======
#
# TWO TIERS, because the fields are not equally reliable.
#
# A notification's TITLE and its "products covered" field are short and
# specific: if the subject is named there, the notification is about it. A
# member's "objective" or "description" field is a paragraph of prose that
# mentions all sorts of things once - halal certification "including products
# derived from biotechnology", entry-exit animal quarantine. Seven of the
# twelve rows in the first live run matched on nothing but such a paragraph.
#
# So SUBJECT applies to the short fields. A long prose field needs a STRONG
# phrase, one that cannot mean anything else.
#
# `biotechnology` is deliberately NOT in STRONG. It is a CATEGORY word and it
# turns up in the objective of halal, food-additive and cosmetics
# notifications that are not about an engineered organism. A notification that
# really is about one names the organism or the modification.

SUBJECT = [
    # English
    "genetically modified", "genetically engineered", "genetic modification",
    "genetic engineering", "genome edit", "gene edit", "gene-edit",
    "gene drive", "living modified organism", "modified organism",
    "transgenic", "biosafety", "biotechnolog", "bioengineered",
    "recombinant", "crispr", "cisgenic", "intragenic", "synthetic biology",
    "novel food", "novel trait", "plant-incorporated protectant",
    "nonregulated status", "deliberate release", "new genomic technique",
    # Spanish
    "organismos vivos modificados", "organismos gen\u00e9ticamente modificados",
    "organismos geneticamente modificados", "gen\u00e9ticamente modificad",
    "geneticamente modificad", "modificados gen\u00e9ticamente",
    "transg\u00e9nic", "bioseguridad", "biotecnolog", "edici\u00f3n g\u00e9nica",
    # French
    "organismes vivants modifi", "g\u00e9n\u00e9tiquement modifi",
    "biotechnolog", "bios\u00e9curit", "\u00e9dition du g\u00e9nome",
    # Portuguese
    "organismos geneticamente modificados", "transg\u00eanic",
    "biosseguran", "edi\u00e7\u00e3o g\u00eanica",
]
# 'biosecurit' UNACCENTED is deliberately absent. In English it means pest and
# disease quarantine - mangosteen import requirements, entry-exit animal
# inspection - and it put two fruit-import notices into the panel on the first
# live run. The accented French spelling is unambiguous and stays;
# bioseguridad / biosseguranca are unambiguous too.

STRONG = [
    "genetically modified", "genetically engineered", "genetic modification",
    "living modified organism", "transgenic", "gene drive", "genome edit",
    "gene edit", "gene-edit", "crispr", "nonregulated status",
    "organismos vivos modificados", "gen\u00e9ticamente modificad",
    "geneticamente modificad", "g\u00e9n\u00e9tiquement modifi",
    "organismes vivants modifi", "transg\u00e9nic", "transg\u00eanic",
    "bioseguridad", "biosseguran", "bios\u00e9curit",
]

# Short forms need a word boundary. 'gm' inside 'alignment' and 'lmo' inside
# 'filmore' are the kind of match that puts a fisheries notice on this map.
WORDS = re.compile(r"\b(gm|gmos?|lmos?|ogm|ovm|vgm)\b", re.I)

# A body whose entire remit is this subject. Its consultations qualify on the
# agency alone: OGTR publishes nothing off-topic here, and a licence
# application titled "DIR 200 - Commercial release of..." matches no term.
AGENCIES = re.compile(
    r"ogtr|gene technology regulator|ctnbio|cibiogem|geac|biosafety|"
    r"biotechnology regulatory", re.I)

# A chemical is a different subject even when the crop it is sprayed on is
# engineered.
NOT_SUBJECT = re.compile(
    r"tolerances?\b|pesticide product registration|registration review|"
    r"inert ingredient|antimicrobial|residue limit|air quality|"
    r"drinking water|significant new use|premanufacture notice", re.I)


def _hit(text, terms):
    t = (text or "").lower()
    return any(term in t for term in terms)


def on_topic(short="", long="", agency=""):
    """short: title, products covered. long: objective, description."""
    if AGENCIES.search(agency or ""):
        return True
    if NOT_SUBJECT.search(short or ""):
        return False
    if _hit(short, SUBJECT) or WORDS.search(short or ""):
        return True
    return _hit(long, STRONG)


# ============================================================ FETCHING =======

def get(url, timeout=90, binary=False):
    req = Request(url, headers={
        "User-Agent": UA,
        "Accept": "application/json, application/vnd.openxmlformats-officedocument"
                  ".spreadsheetml.sheet, text/html",
    })
    raw = urlopen(req, timeout=timeout).read()
    return raw if binary else raw.decode("utf-8", "replace")


# ================================================= XLSX, WITHOUT OPENPYXL ====
#
# openpyxl is not installed in CI, and adding a pip step to a job that needs
# none is the worse trade. This reads the sheet as a stream: the shared-string
# table first, then row by row, clearing each element as it goes, so a 100k-row
# file never lands in memory whole.

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"

# EXCEL'S EPOCH IS 1899-12-30, NOT 1900-01-01, because Excel believes 1900 was
# a leap year. Verified by writing date(2026, 9, 15) and reading the raw value
# back: 46280. Getting this wrong shifts every deadline in the panel by two
# days with no visible error anywhere.
EXCEL_EPOCH = date(1899, 12, 30)


def _col_letters(ref):
    return "".join(ch for ch in ref if ch.isalpha())


def _col_index(ref):
    n = 0
    for ch in _col_letters(ref):
        n = n * 26 + (ord(ch.upper()) - 64)
    return n - 1


def xlsx_rows(data):
    """Yield each row of the first worksheet as a list of strings."""
    zf = zipfile.ZipFile(io.BytesIO(data))
    shared = []
    if "xl/sharedStrings.xml" in zf.namelist():
        for _, el in ET.iterparse(zf.open("xl/sharedStrings.xml"), ("end",)):
            if el.tag == NS + "si":
                shared.append("".join(t.text or "" for t in el.iter(NS + "t")))
                el.clear()
    sheet = next((n for n in zf.namelist()
                  if n.startswith("xl/worksheets/sheet")), None)
    if not sheet:
        raise RuntimeError("no worksheet in the workbook")
    for _, row in ET.iterparse(zf.open(sheet), ("end",)):
        if row.tag != NS + "row":
            continue
        cells = {}
        for c in row.findall(NS + "c"):
            ref = c.get("r") or ""
            idx = _col_index(ref) if ref else len(cells)
            t = c.get("t")
            v = c.find(NS + "v")
            if t == "s" and v is not None:
                try:
                    val = shared[int(v.text)]
                except Exception:
                    val = ""
            elif t == "inlineStr":
                is_ = c.find(NS + "is")
                val = "".join(x.text or "" for x in is_.iter(NS + "t")) if is_ is not None else ""
            else:
                val = v.text if v is not None else ""
            cells[idx] = val or ""
        if cells:
            yield [cells.get(i, "") for i in range(max(cells) + 1)]
        row.clear()


def cell_date(val):
    """A cell may hold an ISO date, a written date, or an Excel serial."""
    s = str(val or "").strip()
    if not s:
        return None
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        try:
            return date(*map(int, m.groups()))
        except ValueError:
            return None
    for fmt in ("%d/%m/%Y", "%m/%d/%Y", "%d-%b-%Y", "%d %B %Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    try:
        n = float(s)
    except ValueError:
        return None
    if 1 <= n <= 200000:
        return EXCEL_EPOCH + timedelta(days=int(n))
    return None


# Headers are matched by SUBSTRING NAME, never by position, and several
# spellings each: the column order is the WTO's to change and a positional read
# breaks silently the first time they do.
COLS = {
    "member":   ["notifying member", "member", "country"],
    "title":    ["title", "notification title"],
    "products": ["products covered", "product covered", "products"],
    "objective":["objective", "description of content", "description"],
    "deadline": ["final date for comments", "comment deadline",
                 "final date comments", "deadline"],
    "symbol":   ["notification symbol", "symbol", "document symbol",
                 "notification number"],
    "link":     ["link", "url", "document link", "document address"],
    "date":     ["date of notification", "notification date"],
}


def match_headers(header):
    low = [re.sub(r"\s+", " ", str(h or "")).strip().lower() for h in header]
    found = {}
    for key, names in COLS.items():
        for i, h in enumerate(low):
            if any(n in h for n in names):
                found[key] = i
                break
    return found


def wto_eping(data=None, today=None):
    """Every WTO SPS and TBT notification, filtered to this subject."""
    today = today or date.today()
    if data is None:
        data = get(WTO_XLSX, timeout=180, binary=True)
    rows = xlsx_rows(data)
    try:
        header = next(rows)
    except StopIteration:
        raise RuntimeError("the workbook is empty")
    cols = match_headers(header)
    if "deadline" not in cols:
        # A missing deadline column is a LOUD failure, never a silent empty
        # file: without it every row is dropped and the panel reports that
        # nothing is open anywhere.
        raise RuntimeError(
            "no comment-deadline column found. Real columns: "
            + " | ".join(str(h) for h in header[:40])
            + "  (run --dump-headers)")
    out, scanned, on_subject = [], 0, 0
    for r in rows:
        scanned += 1
        def cell(k):
            i = cols.get(k)
            return r[i] if i is not None and i < len(r) else ""
        title = str(cell("title") or "").strip()
        products = str(cell("products") or "").strip()
        objective = str(cell("objective") or "").strip()
        if not (title or products):
            continue
        if not on_topic(short=title + " " + products, long=objective):
            continue
        on_subject += 1
        close = cell_date(cell("deadline"))
        if not close or close < today:
            continue
        member = str(cell("member") or "").strip() or "Worldwide"
        link = str(cell("link") or "").strip()
        out.append({
            "title": (title or products)[:200],
            "agency": _wto_agency(cell("symbol")),
            "closes": close.isoformat(),
            "url": link if link.startswith("http") else WTO_HOME,
            "country": member,
            "ref": str(cell("symbol") or "").strip() or None,
        })
    seen, uniq = set(), []
    for r in out:
        k = r.get("ref") or (r["url"] + r["title"][:40])
        if k in seen:
            continue
        seen.add(k)
        uniq.append(r)
    print("  %-34s %d rows scanned, %d on subject, %d still open"
          % ("WTO / ePing", scanned, on_subject, len(uniq)))
    return uniq


def _wto_agency(symbol):
    """Say it once. '"WTO %s notification" % kind' produced "WTO Addendum to
    Regular Notification notification" in the live panel."""
    s = str(symbol or "")
    kind = "SPS" if "/SPS/" in s.upper() else ("TBT" if "/TBT/" in s.upper() else "")
    return ("WTO %s notification" % kind).replace("  ", " ").strip()


def federal_register(today=None):
    today = today or date.today()
    iso = today.isoformat()
    terms = ["genetically engineered organism", "modified organism",
             "petition for determination of nonregulated status",
             "plant-incorporated protectant", "bioengineered food",
             "gene drive", "genetically engineered animal"]
    out, reached = [], False
    for term in terms:
        q = urlencode({
            "conditions[term]": term,
            # DOCUMENTED condition. conditions[comment_date][gte] is not one,
            # and the API ignores conditions it does not recognise rather than
            # refusing them, so that query silently returned the whole
            # Register - a subject search came back holding airworthiness
            # directives. The closing date is filtered below instead.
            "conditions[publication_date][gte]":
                (today - timedelta(days=120)).isoformat(),
            "per_page": 60, "order": "newest",
        }, doseq=True)
        q += "&fields[]=" + "&fields[]=".join(
            ["title", "html_url", "comments_close_on", "agencies",
             "publication_date", "document_number"])
        try:
            d = json.loads(get(FR_API + "?" + q))
            reached = True
        except Exception as e:
            print("  Federal Register (%s): %s" % (term[:24], str(e)[:50]))
            continue
        for r in d.get("results") or []:
            close = r.get("comments_close_on")
            if not close or close < iso:
                continue
            title = r.get("title") or ""
            if not on_topic(short=title):
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
    for r in out:
        k = r.get("ref") or r["url"]
        if k in seen:
            continue
        seen.add(k)
        uniq.append(r)
    print("  %-34s %d open" % ("Federal Register", len(uniq)))
    if not reached:
        raise RuntimeError("every Federal Register query failed")
    return uniq


def _dates(text):
    out = []
    for m in re.finditer(r"(\d{1,2})\s+(January|February|March|April|May|June|"
                         r"July|August|September|October|November|December)"
                         r"\s+(\d{4})", text):
        try:
            out.append(datetime.strptime(" ".join(m.groups()), "%d %B %Y").date())
        except ValueError:
            pass
    for m in re.finditer(r"(\d{4})-(\d{2})-(\d{2})", text):
        try:
            out.append(date(*map(int, m.groups())))
        except ValueError:
            pass
    return out


def listing(url, country, label, html=None, today=None):
    """A listing page rather than an API. Pull the links and any date near
    them; a link with no future date is reported, not guessed at.

    The anchor regex used to demand a bare text node of 15-160 characters AND a
    consultation word in that text. An OGTR link reads "DIR 200 - Commercial
    release of..." - no consultation word - and any <span>-wrapped label did
    not match at all. Nested markup is allowed and stripped, and the subject
    test carries the agency, which for OGTR is enough on its own.
    """
    today = today or date.today()
    if html is None:
        try:
            html = get(url)
        except Exception as e:
            print("  %-34s unreachable (%s)" % (label, str(e)[:40]))
            raise
    out = []
    for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>(.{5,400}?)</a>',
                         html, re.S):
        href = m.group(1)
        title = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(2))).strip()
        if len(title) < 12:
            continue
        if not on_topic(short=title, agency=label):
            continue
        window = html[m.start(): m.start() + 900]
        fut = [d for d in _dates(window)
               if today <= d <= today + timedelta(days=400)]
        if not fut:
            continue
        if href.startswith("/"):
            href = re.match(r"(https?://[^/]+)", url).group(1) + href
        out.append({"title": title[:200], "agency": label,
                    "closes": min(fut).isoformat(), "url": href,
                    "country": country})
    seen, uniq = set(), []
    for r in out:
        if r["url"] in seen:
            continue
        seen.add(r["url"])
        uniq.append(r)
    print("  %-34s %d open" % (label, len(uniq)))
    return uniq


# ================================================================ MAIN =======

def _report(name, kind, ok, detail=""):
    return {"name": name, "kind": kind, "ok": bool(ok), "detail": detail}


def harvest():
    """Returns (rows, sources). `kind` is feed or note, and only FEEDS count
    towards sources_reached: a venue row always 'succeeds' and would otherwise
    stop the everything-failed guard from ever firing."""
    rows, sources = [], []

    for name, fn in (("WTO / ePing", wto_eping),
                     ("Federal Register", federal_register)):
        try:
            got = fn()
            rows += got
            sources.append(_report(name, "feed", True, "%d open" % len(got)))
        except Exception as e:
            print("  %-34s FAILED: %s" % (name, str(e)[:120]))
            sources.append(_report(name, "feed", False, str(e)[:160]))

    try:
        got = listing(OGTR, "Australia", "OGTR")
        rows += got
        sources.append(_report("OGTR", "feed", True, "%d open" % len(got)))
    except Exception as e:
        sources.append(_report("OGTR", "feed", False, str(e)[:160]))

    sources.append(_report(
        "EFSA", "note", True,
        "Open consultations moved to a JavaScript application that serves a "
        "fetcher nothing. Listed as a venue: " + EFSA_VENUE))
    sources.append(_report(
        "Biosafety Clearing-House", "note", True,
        "The Protocol obliges parties to consult but not to file the "
        "consultation, and the BCH publishes no open-window schema. Listed as "
        "a venue: " + BCH_VENUE))

    rows.sort(key=lambda r: r["closes"])
    return rows, sources


def main():
    argv = sys.argv[1:]
    if "--selftest" in argv:
        return selftest()
    if "--dump-headers" in argv:
        data = get(WTO_XLSX, timeout=180, binary=True)
        header = next(xlsx_rows(data))
        for i, h in enumerate(header):
            print("%3d  %s" % (i, h))
        print("\nmatched:", match_headers(header))
        return 0

    print("Consultations open as of %s" % date.today().isoformat())
    rows, sources = harvest()

    feeds = [s for s in sources if s["kind"] == "feed"]
    reached = sum(1 for s in feeds if s["ok"])
    print("\n  %d open, %d of %d feeds answered"
          % (len(rows), reached, len(feeds)))
    for r in rows[:10]:
        print("     %s  %-16s %s" % (r["closes"], r["country"][:16],
                                     r["title"][:60]))

    if reached == 0:
        print("\nEvery feed failed. Nothing written: an empty file is read by "
              "every reader as 'no consultation is open anywhere', which is a "
              "stronger claim than the evidence supports.", file=sys.stderr)
        return 1

    if "--dry-run" in argv:
        print("dry run \u2014 nothing written")
        return 0

    OUT.write_text(json.dumps({
        "generated": date.today().isoformat(),
        "note": ("Comment windows open at the time of harvest. The map checks "
                 "the generated date and refuses to show this list if it is "
                 "stale, because a closed window presented as open is worse "
                 "than no list at all."),
        "sources": sources,
        "sources_reached": reached,
        "sources_total": len(feeds),
        "consultations": rows,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote %s: %d" % (OUT.name, len(rows)))
    return 0


# ============================================================ SELFTEST =======

def _mini_xlsx(rows):
    """A workbook built by hand, so the reader is exercised without openpyxl."""
    def esc(s):
        return (str(s).replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;"))
    body = []
    for ri, row in enumerate(rows, start=1):
        cells = []
        for ci, val in enumerate(row):
            ref = ""
            n = ci
            while True:
                ref = chr(65 + n % 26) + ref
                n = n // 26 - 1
                if n < 0:
                    break
            if isinstance(val, (int, float)):
                cells.append('<c r="%s%d"><v>%s</v></c>' % (ref, ri, val))
            else:
                cells.append('<c r="%s%d" t="inlineStr"><is><t>%s</t></is></c>'
                             % (ref, ri, esc(val)))
        body.append("<row r=\"%d\">%s</row>" % (ri, "".join(cells)))
    sheet = ('<?xml version="1.0"?><worksheet xmlns="http://schemas.openxml'
             'formats.org/spreadsheetml/2006/main"><sheetData>%s</sheetData>'
             '</worksheet>' % "".join(body))
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("[Content_Types].xml", '<?xml version="1.0"?><Types/>')
        z.writestr("xl/worksheets/sheet1.xml", sheet)
    return buf.getvalue()


def selftest():
    fails = []

    def ck(name, got, want):
        if got != want:
            fails.append("%s: got %r want %r" % (name, got, want))

    # the epoch, which is the one error nothing else would catch
    ck("excel serial 46280", cell_date("46280"), date(2026, 9, 15))
    ck("iso date", cell_date("2026-10-06"), date(2026, 10, 6))
    ck("written date", cell_date("6 October 2026"), date(2026, 10, 6))
    ck("empty date", cell_date(""), None)

    # two tiers
    ck("title match", on_topic(short="Labelling Standards for Genetically "
                                     "Modified Foods"), True)
    ck("prose-only, weak term", on_topic(
        short="Draft halal product assurance regulation",
        long="Objective: certification of products including those derived "
             "from biotechnology."), False)
    ck("prose-only, strong term", on_topic(
        short="Draft decree",
        long="Rules for the deliberate release of genetically modified maize."),
        True)
    ck("quarantine is not this subject", on_topic(
        short="Mangosteen fruit from Malaysia: biosecurity import requirements"),
        False)
    ck("accented french kept", on_topic(short="Cadre national de bios\u00e9curit\u00e9"), True)
    ck("spanish kept", on_topic(
        short="Reglamento sobre organismos vivos modificados"), True)
    ck("portuguese kept", on_topic(short="Lei de biosseguran\u00e7a"), True)
    ck("agency alone", on_topic(short="DIR 200 - Commercial release",
                                agency="OGTR"), True)
    ck("word boundary", on_topic(short="Alignment of filmore port fees"), False)
    ck("chemical excluded", on_topic(
        short="Pesticide tolerances for glyphosate residue limits"), False)

    # headers by name, in a deliberately shuffled order
    header = ["Notification Symbol", "Date of notification",
              "Notifying Member", "Products Covered", "Title",
              "Objective", "Final date for comments", "Link"]
    cols = match_headers(header)
    ck("header: deadline", cols.get("deadline"), 6)
    ck("header: member", cols.get("member"), 2)
    ck("header: title", cols.get("title"), 4)

    # a missing deadline column must FAIL, not return nothing
    try:
        wto_eping(data=_mini_xlsx([["Title", "Notifying Member"],
                                   ["x", "y"]]))
        fails.append("missing deadline column returned instead of failing")
    except RuntimeError as e:
        if "deadline" not in str(e):
            fails.append("wrong error for missing deadline: %s" % e)

    # a round trip through the reader and the selection logic
    today = date(2026, 8, 21)
    data = _mini_xlsx([
        header,
        ["G/TBT/N/KOR/1", "2026-08-01", "Korea, Republic of", "Foods",
         "Proposed amendments to the Labelling Standards for Genetically "
         "Modified Foods", "Labelling.", 46280, "https://docs.wto.org/a"],
        ["G/SPS/N/AUS/1", "2026-08-01", "Australia", "Mangosteen",
         "Mangosteen fruit from Malaysia: biosecurity import requirements",
         "Quarantine.", 46280, "https://docs.wto.org/b"],
        ["G/TBT/N/PER/1", "2026-08-01", "Peru", "Alimentos",
         "Reglamento sobre organismos vivos modificados", "Etiquetado.",
         "2026-09-30", "https://docs.wto.org/c"],
        ["G/TBT/N/IDN/1", "2026-08-01", "Indonesia", "Halal",
         "Draft halal product assurance regulation",
         "Certification of products including those derived from "
         "biotechnology.", 46280, "https://docs.wto.org/d"],
        ["G/TBT/N/OLD/1", "2026-01-01", "Chile", "Semillas",
         "Reglamento sobre organismos vivos modificados", "Cerrado.",
         "2026-01-30", "https://docs.wto.org/e"],
    ])
    rows = wto_eping(data=data, today=today)
    ck("xlsx kept", sorted(r["country"] for r in rows),
       ["Korea, Republic of", "Peru"])
    ck("xlsx deadline", next(r["closes"] for r in rows
                             if r["country"] == "Korea, Republic of"),
       "2026-09-15")
    ck("agency said once", next(r["agency"] for r in rows
                                if r["country"] == "Peru"),
       "WTO TBT notification")

    # nested markup in an anchor
    html = ('<a href="/dir-200"><span>DIR 200</span> - Commercial release of '
            'GM cotton</a> Comments close 30 September 2026')
    got = listing("https://www.ogtr.gov.au/x", "Australia", "OGTR",
                  html=html, today=today)
    ck("nested anchor parsed", [r["closes"] for r in got], ["2026-09-30"])

    if fails:
        print("SELFTEST FAILED")
        for f in fails:
            print("  -", f)
        return 1
    print("selftest: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
