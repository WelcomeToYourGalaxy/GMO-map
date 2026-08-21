#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Consultations that are open right now, with the date they shut.

Everything else on this map is true next year. A comment window is worthless
the day after it closes, which makes this the only thing here that has to be
fetched rather than written.

WHY THIS WAS REWRITTEN

The panel was showing "No window on this subject is open right now" and listing
portals instead. That was not a rendering problem - index.html builds the rows
correctly the moment the file contains any. The harvester was returning nothing,
for four separate reasons, three of which could never have returned anything:

  eping()            pointed at epingalert.org/api/notifications. That is the
                     legacy alert site, not the platform, and there is no such
                     JSON endpoint on it. It also had a control-flow bug: the
                     `except` did `return out` from inside the keyword loop, so
                     a failure on the first keyword skipped the second.

  bch_consultations() queried fq=schema_s:biosafetyDecision and then filtered on
                     commentDeadline_dt. A decision record is the record of a
                     decision ALREADY TAKEN. It carries no comment deadline,
                     because by the time it exists the comment period is over.
                     The query could return 200 rows and still yield zero. See
                     bch_note() below - this is not a fixable field name, it is
                     the wrong record type, and the BCH does not publish an
                     open-window record type at all.

  listing()          required the ANCHOR TEXT to match a consultation word AND
                     a genetics word, both, in 15-160 characters. An OGTR link
                     reads "DIR 200 - Commercial release of ..." and contains no
                     consultation word; an EFSA link often carries the subject in
                     the surrounding block rather than the link itself. Requiring
                     both of one short string is close to a guarantee of zero.
                     The regex also demanded the link text be a single bare text
                     node - `>([^<]{15,160})<` - so any anchor wrapping its label
                     in a <span> did not match at all.

  federal_register() asked for conditions[comment_date][gte], which is not among
                     the documented search conditions. An unrecognised condition
                     is ignored rather than refused, so the query silently widens
                     to the whole Register. It now filters on comments_close_on
                     in Python, which is correct whether or not that condition is
                     ever supported.

SOURCES NOW

  ePing / WTO TBT+SPS  THE ONE THAT MAKES THIS GLOBAL. Every WTO member must
                       notify a draft technical or sanitary regulation before
                       enforcing it, with a comment period attached, and the WTO
                       publishes every notification since 1995 as a single
                       spreadsheet regenerated daily:
                         https://eping.wto.org/NotificationExcelFiles/Notification_EN.xlsx
                       No key, no login, no JavaScript. 160-odd members filing
                       into one file, each row carrying the notifying member and
                       the final date for comments. That is a per-country live
                       feed, which is what was wanted and what no national portal
                       can give.

  Federal Register     A real JSON API. United States.

  EFSA, OGTR           Listing pages, parsed. Two countries, and they stay
                       because they are the two regulators that publish the
                       actual assessment alongside the window.

  BCH                  Reported, not harvested. Explained in bch_note().

Every run prints a per-source table and writes it into the JSON, so a zero is
attributable. A silent zero is what produced the panel this replaces.

    python3 harvest/consultations.py
    python3 harvest/consultations.py --dry-run
    python3 harvest/consultations.py --selftest       # no network
    python3 harvest/consultations.py --only eping
    python3 harvest/consultations.py --dump-headers   # print the ePing columns
"""

import json, re, sys, io, zipfile, pathlib
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta
from urllib.request import Request, urlopen
from urllib.parse import urlencode

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "consultations.json"
UA = "GMO-map/1.0 (public research map)"

# How each source reported. Written into the output so the map can say "4 of 5
# sources answered" instead of showing an unexplained empty box.
REPORT = []


def note(name, n, detail="", kind="feed"):
    """kind='feed' is a source that was fetched and can therefore fail.
    kind='note' is a standing explanation that fetches nothing, and must not be
    counted as a source that answered - otherwise a night on which every real
    source was unreachable still looks like two sources reporting zero, and the
    empty file gets written."""
    REPORT.append({"source": name, "rows": n, "detail": detail, "kind": kind})
    mark = n if n is not None else ("-" if kind == "note" else "FAIL")
    print("  %-30s %4s  %s" % (name, mark, detail))


def get(url, timeout=90, binary=False, cap=140 * 1024 * 1024):
    req = Request(url, headers={"User-Agent": UA,
                                "Accept": "application/json, text/html, */*"})
    with urlopen(req, timeout=timeout) as r:
        raw = r.read(cap + 1)
    if len(raw) > cap:
        raise ValueError("response larger than %d MB - refusing to hold it in "
                         "memory" % (cap // (1024 * 1024)))
    return raw if binary else raw.decode("utf-8", "replace")


# ============================================================ SUBJECT =========
#
# An allow-list, not a stop-list. The things this map covers are a short
# nameable set; the things it does not are unbounded. Applied to the title, and
# for ePing also to the product-covered and objective columns, because a TBT
# notification often carries the subject there rather than in its title.

SUBJECT = re.compile(
    # English
    r"genetic|engineered|bioengineer|biotechnolog|biosafety|"
    r"living modified|modified organism|\bGMO?s?\b|\bLMOs?\b|gene[ -]?driv|"
    r"gene[ -]?edit|genome[ -]?edit|new genomic techni|\bNGT\b|"
    r"nonregulated status|plant[- ]incorporated protectant|"
    r"recombinant|cisgeni|intragen|synthetic biolog|novel food|novel trait|"
    # Spanish, French, Portuguese. The file is the English edition, but members
    # routinely file a title in their own language and the WTO carries it as
    # submitted - and the whole reason for using this source is the countries
    # that do not publish in English. Dropping those rows would leave a "global"
    # feed that is quietly Anglophone.
    r"transg[eéê]nic|"                       # transgenic/transgénico/transgênico
    r"organismos? vivos? modificados?|organismes? vivants? modifi|"
    r"organismos? geneticamente modificados?|"
    r"g[eé]n[eé]ticamente modificad|modificad[oa]s? gen[eé]ticamente|"
    r"g[eé]n[eé]tiquement modifi|"
    r"bios[eé]gur|biosseguran|bios[eé]curit|"                 # biosafety
    r"biotecnolog|edici[oó]n g[eé]n|edi[cç][aã]o gen|\bOVM\b|\bOGM\b",
    re.I)

# Notices about a chemical are a different subject even when the crop it is
# sprayed on is engineered. Applied after SUBJECT, and only to titles.
NOT_SUBJECT = re.compile(
    r"tolerances?\b|pesticide product registration|registration review|"
    r"inert ingredient|antimicrobial|residue limits?|air quality|"
    r"drinking water|significant new use|premanufacture notice",
    re.I)


def on_subject(*parts):
    hay = " ".join(str(p or "") for p in parts)
    return bool(SUBJECT.search(hay)) and not NOT_SUBJECT.search(hay)


# ============================================================ DATES ===========

_MONTHS = ("january february march april may june july august september "
           "october november december").split()


def as_date(v):
    """A date out of any of the shapes these sources use, including the one an
    xlsx uses, which is not a date at all.

    Excel stores a date as a day count and puts the formatting in a separate
    styles part. Read the cell without the styles - which is what a stdlib
    parser does - and a comment deadline comes back as "45930". Left unhandled
    that is not a wrong date, it is a row silently dropped for having no date,
    which is exactly the failure this file exists to stop repeating.
    """
    if v is None:
        return None
    s = str(v).strip()
    if not s:
        return None
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        try:
            return date(*map(int, m.groups()))
        except ValueError:
            return None
    m = re.match(r"^(\d{1,2})[/.-](\d{1,2})[/.-](\d{4})$", s)
    if m:
        d, mo, y = map(int, m.groups())
        if mo > 12 and d <= 12:          # a US-ordered file
            d, mo = mo, d
        try:
            return date(y, mo, d)
        except ValueError:
            return None
    m = re.match(r"^(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})$", s)
    if m and m.group(2).lower() in _MONTHS:
        return date(int(m.group(3)), _MONTHS.index(m.group(2).lower()) + 1,
                    int(m.group(1)))
    m = re.match(r"^([A-Za-z]+)\s+(\d{1,2}),?\s+(\d{4})$", s)
    if m and m.group(1).lower() in _MONTHS:
        return date(int(m.group(3)), _MONTHS.index(m.group(1).lower()) + 1,
                    int(m.group(2)))
    # Excel serial. 1899-12-30 rather than 1900-01-01, because Excel believes
    # 1900 was a leap year and every date after 1900-02-28 is a day out if you
    # do not absorb the phantom day into the epoch.
    if re.match(r"^\d{5}(\.\d+)?$", s):
        n = int(float(s))
        if 20000 < n < 80000:
            return date(1899, 12, 30) + timedelta(days=n)
    return None


def dates_in(text):
    """Every date in a block of prose, for the listing parsers."""
    out = []
    for m in re.finditer(r"(\d{1,2})\s+(" + "|".join(_MONTHS) + r")\s+(\d{4})",
                         text, re.I):
        d = as_date(" ".join(m.groups()))
        if d:
            out.append(d)
    for m in re.finditer(r"(" + "|".join(_MONTHS) + r")\s+(\d{1,2}),?\s+(\d{4})",
                         text, re.I):
        d = as_date(" ".join(m.groups()))
        if d:
            out.append(d)
    for m in re.finditer(r"\d{4}-\d{2}-\d{2}", text):
        d = as_date(m.group(0))
        if d:
            out.append(d)
    return out


# ============================================================ XLSX ============
#
# An xlsx is a zip of XML. openpyxl would be one line, and it is not installed
# in the workflow runner - and adding a pip step to a job that currently needs
# none is a worse trade than forty lines of parser. Streamed, so the file size
# does not become a memory ceiling.

def _colnum(ref):
    n = 0
    for ch in ref:
        if ch.isalpha():
            n = n * 26 + (ord(ch.upper()) - 64)
        else:
            break
    return n - 1


def _strip_ns(tag):
    return tag.rsplit("}", 1)[-1]


def xlsx_rows(raw, limit=400000):
    """Yield each row of the first worksheet as a list of strings."""
    zf = zipfile.ZipFile(io.BytesIO(raw))

    shared = []
    if "xl/sharedStrings.xml" in zf.namelist():
        with zf.open("xl/sharedStrings.xml") as fh:
            ctx = ET.iterparse(fh, events=("start", "end"))
            _, root = next(ctx)
            for ev, el in ctx:
                if ev == "end" and _strip_ns(el.tag) == "si":
                    shared.append("".join(
                        t.text or "" for t in el.iter()
                        if _strip_ns(t.tag) == "t"))
                    root.clear()

    sheets = sorted(n for n in zf.namelist()
                    if re.match(r"xl/worksheets/sheet\d+\.xml$", n))
    if not sheets:
        raise ValueError("no worksheet in the workbook")

    with zf.open(sheets[0]) as fh:
        ctx = ET.iterparse(fh, events=("start", "end"))
        _, root = next(ctx)
        seen = 0
        for ev, el in ctx:
            if ev != "end" or _strip_ns(el.tag) != "row":
                continue
            cells = {}
            for c in el:
                if _strip_ns(c.tag) != "c":
                    continue
                idx = _colnum(c.get("r") or "A1")
                typ = c.get("t")
                val = ""
                for child in c:
                    tag = _strip_ns(child.tag)
                    if tag == "v":
                        val = child.text or ""
                    elif tag == "is":
                        val = "".join(t.text or "" for t in child.iter()
                                      if _strip_ns(t.tag) == "t")
                if typ == "s" and val.isdigit():
                    i = int(val)
                    val = shared[i] if i < len(shared) else ""
                cells[idx] = val.strip()
            if cells:
                width = max(cells) + 1
                yield [cells.get(i, "") for i in range(width)]
            root.clear()
            seen += 1
            if seen >= limit:
                return


# ============================================================ ePing ===========

EPING_XLSX = "https://eping.wto.org/NotificationExcelFiles/Notification_EN.xlsx"
EPING_PORTAL = "https://eping.wto.org/en/Search"

# Matched as substrings against the lowercased header row. Several spellings per
# field, because the column order and wording of this file are the WTO's to
# change and a positional read would break silently the first time they did.
# First match wins, so the more specific spelling is listed first.
EPING_COLS = {
    "closes":  ["final date for comments", "comment deadline", "final date",
                "deadline for comments", "comments due"],
    "country": ["notifying member", "notifying wto member", "member",
                "country"],
    "title":   ["title", "description of content", "products covered",
                "product covered", "objective"],
    "extra":   ["products covered", "product covered", "objective",
                "description of content", "keywords", "hs codes"],
    "symbol":  ["document symbol", "notification symbol", "symbol",
                "notification number", "document number"],
    "url":     ["link", "url", "document link", "web link"],
    "kind":    ["notification type", "agreement", "type"],
}


def _map_headers(header):
    low = [str(h or "").strip().lower() for h in header]
    found = {}
    for field, names in EPING_COLS.items():
        for want in names:
            for i, h in enumerate(low):
                if want in h and i not in found.values():
                    found[field] = i
                    break
            if field in found:
                break
    return found, low


def eping(dump_headers=False):
    """WTO SPS and TBT notifications, filtered to this subject.

    The value is coverage rather than depth. A notification from Kenya or Peru
    or Viet Nam sits in the same file as one from the European Union, with the
    same fields and the same deadline, which no national portal gives - and it
    is frequently the earliest public sight of a rule, including from countries
    whose own consultation pages are decorative.
    """
    try:
        raw = get(EPING_XLSX, timeout=300, binary=True)
    except Exception as e:
        note("ePing / WTO (SPS+TBT)", None,
             "unreachable: %s" % str(e)[:60])
        return []

    try:
        rows = xlsx_rows(raw)
        header = next(rows)
    except Exception as e:
        note("ePing / WTO (SPS+TBT)", None, "unreadable: %s" % str(e)[:60])
        return []

    cols, low = _map_headers(header)
    if dump_headers:
        print("\n  ePing columns as published:")
        for i, h in enumerate(low):
            print("    %2d  %s" % (i, h))
        print("  mapped: %s\n" % cols)

    if "closes" not in cols:
        # The one failure that must never be silent. Without a deadline column
        # every row is dropped, and a reader would see an empty panel with no
        # way to know why.
        note("ePing / WTO (SPS+TBT)", None,
             "no comment-deadline column. Headers: %s"
             % ", ".join(h for h in low if h)[:160])
        return []

    today = date.today()
    horizon = today + timedelta(days=400)
    out, scanned, subject_hits = [], 0, 0

    for r in rows:
        scanned += 1

        def cell(field):
            i = cols.get(field)
            return r[i] if i is not None and i < len(r) else ""

        title = cell("title") or cell("extra")
        if not title:
            continue
        if not on_subject(title, cell("extra")):
            continue
        subject_hits += 1
        close = as_date(cell("closes"))
        if not close or close < today or close > horizon:
            continue
        country = (cell("country") or "").strip() or "Worldwide"
        sym = (cell("symbol") or "").strip()
        url = (cell("url") or "").strip()
        if not url.startswith("http"):
            url = EPING_PORTAL
        out.append({
            "title": (title[:200]).strip(),
            "agency": ("WTO %s notification" % (cell("kind") or "TBT/SPS").strip()
                       ).replace("  ", " "),
            "closes": close.isoformat(),
            "url": url,
            "country": country,
            "ref": sym or (country + "|" + title[:40]),
        })

    seen, uniq = set(), []
    for r in out:
        if r["ref"] in seen:
            continue
        seen.add(r["ref"])
        uniq.append(r)

    note("ePing / WTO (SPS+TBT)", len(uniq),
         "%d rows scanned, %d on subject, %d still open"
         % (scanned, subject_hits, len(uniq)))
    return uniq


# ============================================================ FED REG =========

FR_API = "https://www.federalregister.gov/api/v1/documents.json"

# Phrases that only appear when an engineered ORGANISM is the subject. A bare
# term search returns every notice that mentions the words in passing, and most
# of what came back was chemical review with one incidental sentence.
FR_TERMS = ["genetically engineered organism", "modified organism",
            "petition for determination of nonregulated status",
            "plant-incorporated protectant", "bioengineered food",
            "gene drive", "genetically engineered animal"]


def federal_register():
    """Documents published recently whose comment period has not yet closed.

    The window is applied HERE rather than in the query. conditions[term] and
    conditions[publication_date][gte] are documented and honoured;
    conditions[comment_date][gte] is not documented, and this API ignores an
    unrecognised condition rather than rejecting it - so asking for it produced
    a query with no date filter at all, which is how a subject search came back
    holding airworthiness directives.
    """
    today = date.today()
    since = (today - timedelta(days=120)).isoformat()
    out = []
    fields = ["title", "html_url", "comments_close_on", "agencies",
              "publication_date", "document_number"]
    failures = 0
    for term in FR_TERMS:
        q = urlencode({"conditions[term]": term,
                       "conditions[publication_date][gte]": since,
                       "per_page": 100, "order": "newest"})
        q += "".join("&fields[]=" + f for f in fields)
        try:
            d = json.loads(get(FR_API + "?" + q, timeout=60))
        except Exception:
            failures += 1
            continue
        for r in d.get("results") or []:
            close = as_date(r.get("comments_close_on"))
            if not close or close < today:
                continue
            title = r.get("title") or ""
            if not on_subject(title):
                continue
            ag = r.get("agencies") or []
            out.append({
                "title": title[:200],
                "agency": (ag[0].get("name") if ag and isinstance(ag[0], dict)
                           else "US federal agency"),
                "closes": close.isoformat(),
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
    if failures == len(FR_TERMS):
        # Every query failed, so this is a fetch failure and not a finding.
        # Reporting it as zero is the exact mistake that let an empty file be
        # written and read as "no consultation is open anywhere".
        note("Federal Register", None,
             "all %d term queries failed - treated as unreachable, not empty"
             % failures)
        return []
    note("Federal Register", len(uniq),
         "%d of %d term queries failed" % (failures, len(FR_TERMS))
         if failures else "")
    return uniq


# ============================================================ LISTINGS ========

EFSA = "https://www.efsa.europa.eu/en/consultations"
OGTR = ("https://www.ogtr.gov.au/what-weve-approved/"
        "dealings-involving-intentional-release")

# An anchor, allowing nested markup inside it. The old pattern was
# `>([^<]{15,160})<`, which requires the label to be one bare text node, so any
# link wrapping its text in a <span> - which is most of them now - did not match
# the anchor at all, let alone fail a subject test.
A_TAG = re.compile(r'<a[^>]+href="([^"#][^"]*)"[^>]*>(.{5,400}?)</a>',
                   re.I | re.S)
TAGS = re.compile(r"<[^>]+>")


def listing(url, country, label, agency_is_on_topic=False):
    """EFSA and OGTR publish listings rather than an API.

    `agency_is_on_topic` says the whole register is this subject, so a row does
    not have to prove it in its own title. OGTR publishes nothing off-topic and
    names its applications "DIR 200", which matches no subject term ever
    written - requiring one is how that source returned zero for months.
    """
    try:
        html = get(url, timeout=60)
    except Exception as e:
        note(label, None, "unreachable: %s" % str(e)[:60])
        return []

    today, out = date.today(), []
    for m in A_TAG.finditer(html):
        href = m.group(1)
        title = re.sub(r"\s+", " ", TAGS.sub(" ", m.group(2))).strip()
        if len(title) < 12:
            continue
        # The block around the link, which is where a listing usually puts the
        # dates and often the subject too.
        block = html[max(0, m.start() - 400): m.start() + 1200]
        block_text = re.sub(r"\s+", " ", TAGS.sub(" ", block))
        if not agency_is_on_topic and not on_subject(title, block_text[:600]):
            continue
        if NOT_SUBJECT.search(title):
            continue
        fut = [d for d in dates_in(block_text)
               if today <= d <= today + timedelta(days=400)]
        if not fut:
            continue
        if href.startswith("/"):
            href = re.match(r"(https?://[^/]+)", url).group(1) + href
        elif not href.startswith("http"):
            continue
        out.append({"title": title[:200], "agency": label,
                    "closes": min(fut).isoformat(), "url": href,
                    "country": country, "ref": href})

    seen, uniq = set(), []
    for r in out:
        if r["url"] in seen:
            continue
        seen.add(r["url"])
        uniq.append(r)
    note(label, len(uniq),
         "listing parsed but nothing carried a future date"
         if not uniq else "")
    return uniq


# ============================================================ BCH =============

def bch_note():
    """Why the Clearing-House is not harvested here, recorded rather than
    silently returning zero every night.

    The old function asked api.cbd.int for schema_s:biosafetyDecision and then
    filtered on a commentDeadline_dt field. A decision record documents a
    decision that has been TAKEN. Article 20 requires a party to file it within
    fifteen days OF DECIDING - so by the time the record exists, any consultation
    that preceded it is over. There is no comment deadline on it because there
    cannot be one.

    Article 23 does oblige parties to consult the public before deciding, and
    that obligation is what the map's BCH row is for. But the Protocol does not
    require the consultation to be FILED, and the Clearing-House publishes no
    open-window record type. So the BCH belongs in this panel as a venue - where
    to look, and the article to cite where a country runs no consultation at all
    - and not as a feed. Listing it as a feed that returns nothing every night
    is what made the whole panel look broken.

    If this changes, the thing to look for is a record schema with a deadline
    field, not a different field name on the decision schema.
    """
    note("Biosafety Clearing-House", None,
         "not a live-window source - see bch_note(); the BCH row stays a venue",
         kind="note")
    return []


# ============================================================ SELFTEST ========

def selftest():
    """Exercise the parsing offline. The sandbox cannot reach any of these
    hosts, so 'it ran without an exception' proves nothing about whether it
    would have kept the right rows."""
    ok = True

    def check(name, got, want):
        nonlocal ok
        good = got == want
        ok = good and ok
        print("  %-46s %s  (got %r)" % (name, "ok" if good else "FAIL", got))

    print("dates")
    check("ISO", as_date("2026-09-15"), date(2026, 9, 15))
    check("15 September 2026", as_date("15 September 2026"), date(2026, 9, 15))
    check("September 15, 2026", as_date("September 15, 2026"), date(2026, 9, 15))
    check("15/09/2026", as_date("15/09/2026"), date(2026, 9, 15))
    # 46280, not 46276. Verified by writing date(2026,9,15) to a real workbook
    # and reading the <v> back out: Excel stores 46280. The four-day gap is the
    # 1900 leap-year fiction, and getting it wrong shifts every deadline in the
    # panel by four days without producing a single visible error.
    check("excel serial 46280", as_date("46280"), date(2026, 9, 15))
    check("junk", as_date("not a date"), None)
    check("empty", as_date(""), None)

    print("subject")
    check("GM maize notification",
          on_subject("Draft rules on genetically modified maize"), True)
    check("pesticide tolerance rejected",
          on_subject("Fluazinam; Pesticide Tolerances"), False)
    check("gene drive", on_subject("Gene drive mosquitoes"), True)
    check("port fees", on_subject("Notice of harbour maintenance fees"), False)
    check("es: organismos vivos modificados",
          on_subject("Reglamento sobre organismos vivos modificados"), True)
    check("es: genéticamente modificado",
          on_subject("Maíz gen\u00e9ticamente modificado"), True)
    check("es: bioseguridad", on_subject("Ley de bioseguridad"), True)
    check("pt: geneticamente modificados",
          on_subject("Organismos geneticamente modificados"), True)
    check("pt: biossegurança", on_subject("Normas de biossegurança"), True)
    check("fr: génétiquement modifiés",
          on_subject("Organismes g\u00e9n\u00e9tiquement modifi\u00e9s"), True)
    check("fr: biosécurité", on_subject("Cadre de bios\u00e9curit\u00e9"), True)
    check("es: unrelated still rejected",
          on_subject("Reglamento sobre tuber\u00edas de acero"), False)
    check("subject in the extra column",
          on_subject("Order No. 44/2026", "Products covered: living modified "
                     "organisms for food"), True)

    print("anchors with nested markup")
    html = ('<a href="/dir-200"><span class="t">DIR 200 - Commercial '
            'release of herbicide tolerant cotton</span></a>'
            '<p>Comments close 30 September 2026</p>')
    got = A_TAG.findall(html)
    check("nested span still matches", len(got), 1)

    print("xlsx")
    try:
        import openpyxl
    except ImportError:
        print("  openpyxl absent here - skipping the fixture "
              "(the harvester itself never imports it)")
        return ok
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.append(["Document symbol", "Notifying Member", "Title",
               "Products covered", "Final date for comments",
               "Notification type"])
    soon = (date.today() + timedelta(days=30))
    past = (date.today() - timedelta(days=5))
    ws.append(["G/TBT/N/KEN/1", "Kenya", "Draft standard for genetically "
               "modified maize", "maize", soon, "TBT"])
    ws.append(["G/TBT/N/PER/2", "Peru", "Reglamento de bioseguridad",
               "living modified organisms", soon, "TBT"])
    ws.append(["G/TBT/N/USA/3", "United States", "Steel pipe tolerances",
               "pipe", soon, "TBT"])
    ws.append(["G/TBT/N/VNM/4", "Viet Nam", "Gene drive mosquito release",
               "insects", past, "SPS"])
    ws.append(["G/TBT/N/KEN/1", "Kenya", "Draft standard for genetically "
               "modified maize", "maize", soon, "TBT"])
    buf = io.BytesIO()
    wb.save(buf)
    raw = buf.getvalue()

    rows = list(xlsx_rows(raw))
    check("header read", rows[0][0], "Document symbol")
    cols, _low = _map_headers(rows[0])
    check("deadline column located", cols.get("closes"), 4)
    check("country column located", cols.get("country"), 1)

    # Drive the real selection logic over the fixture.
    today = date.today()
    kept = []
    for r in rows[1:]:
        title = r[cols["title"]]
        if not on_subject(title, r[cols["extra"]]):
            continue
        c = as_date(r[cols["closes"]])
        if not c or c < today:
            continue
        kept.append((r[cols["country"]], r[cols["symbol"]]))
    seen, uniq = set(), []
    for c, s in kept:
        if s in seen:
            continue
        seen.add(s)
        uniq.append(c)
    check("off-subject row dropped", "United States" in uniq, False)
    check("closed row dropped", "Viet Nam" in uniq, False)
    check("duplicate symbol collapsed", len(uniq), 2)
    check("Kenya and Peru kept", sorted(uniq), ["Kenya", "Peru"])
    return ok


# ============================================================ MAIN ============

def main():
    if "--selftest" in sys.argv:
        print("selftest - no network")
        sys.exit(0 if selftest() else 1)

    dump = "--dump-headers" in sys.argv
    only = None
    for i, a in enumerate(sys.argv):
        if a == "--only" and i + 1 < len(sys.argv):
            only = sys.argv[i + 1]

    print("Consultations open as of %s" % date.today().isoformat())
    rows = []
    if only in (None, "eping"):
        rows += eping(dump_headers=dump)
    if only in (None, "fr", "federal_register"):
        rows += federal_register()
    if only in (None, "efsa"):
        rows += listing(EFSA, "European Union", "EFSA")
    if only in (None, "ogtr"):
        rows += listing(OGTR, "Australia", "OGTR", agency_is_on_topic=True)
    if only is None:
        bch_note()

    rows.sort(key=lambda r: r["closes"])
    feeds = [s for s in REPORT if s["kind"] == "feed"]
    reached = sum(1 for s in feeds if s["rows"] is not None)

    if reached == 0:
        print("\nEvery source failed to fetch. That is NOT the same as nothing "
              "being open, and the file is deliberately not written - the map "
              "holds the last good one, and its own three-week staleness check "
              "will retire it in due course. Writing an empty list here would "
              "tell every reader in the world that no consultation is open "
              "anywhere, on the strength of a network error.", file=sys.stderr)
        sys.exit(1)

    soon = [r for r in rows
            if r["closes"] <= (date.today() + timedelta(days=14)).isoformat()]
    by_country = {}
    for r in rows:
        by_country[r["country"]] = by_country.get(r["country"], 0) + 1
    print("\n  %d open across %d countries, %d closing within a fortnight"
          % (len(rows), len(by_country), len(soon)))
    for r in rows[:12]:
        print("     %s  %-18s %s" % (r["closes"], r["country"][:18],
                                     r["title"][:58]))

    if dump or "--dry-run" in sys.argv:
        print("dry run \u2014 nothing written")
        return

    OUT.write_text(json.dumps({
        "generated": date.today().isoformat(),
        "sources": REPORT,
        "sources_reached": reached,
        "sources_total": len(feeds),
        "note": ("Comment windows open at the time of harvest. The map checks "
                 "the generated date and refuses to show this list if it is "
                 "stale, because a closed window presented as open is worse "
                 "than no list at all. `sources` records what each source "
                 "returned, so an empty list can be told apart from a failed "
                 "fetch."),
        "consultations": rows}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote %s: %d" % (OUT.name, len(rows)))


if __name__ == "__main__":
    main()
