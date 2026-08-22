#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The National Plant Protection Organization each country has designated.

WHAT THIS IS FOR, and it is not what the BCH harvest is for. Sixty rows in
resources.json read "No national office identified - quarantine and plant
health" because the office's legal name could not be established. Article VIII.2
of the International Plant Protection Convention requires every contracting
party to designate an official contact point and tell the Secretariat who it is,
and the Secretariat publishes the resulting list. So the name is not a research
question at all: it is published, by the country itself, for about 180 countries.

WHAT IT DOES NOT SUPPLY. There is no website column. This harvest names the
body; it cannot link it. A named office a reader can search for is a large
improvement on "no office identified", and it is not the same thing as a link.

PRIVACY. The source is a contact list: prefixes, first and last names, direct
e-mail addresses and alternates, and postal addresses. NONE of that goes into
the map. Only Country, Region and Organization are kept, and there is an
assertion at the end that no e-mail address and no honorific survived into the
output. This is the same handling bch_focal_points.py applies to the focal-point
list, and the reason bch_authorities.py stays disabled.

THE ENCODING TRAP, which is why this parses rather than reads. The extractor
emits Python BYTES REPRESENTATIONS inside its CSV cells - the literal characters
b'Direction...' - and the text inside them is UTF-8 that has been decoded as
latin-1, so an e arrives as \\xc3\\xa9. Reading the cell as-is puts b' and mojibake
on the map. Both are undone here, and the selftest drives the exact shapes the
live extractor produced.

    python3 harvest/ippc_contacts.py --selftest    # no network
    python3 harvest/ippc_contacts.py --print
    python3 harvest/ippc_contacts.py              # writes harvest/ippc_contacts.json
"""
import csv, io, json, re, sys, pathlib
from urllib.request import Request, urlopen

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "ippc_contacts.json"
URL = "https://ippc.int/en/countriescontacts/extractor/"
UA = "GMO-map/1.0 (public research map; +https://github.com/WelcomeToYourGalaxy/GMO-map)"

EMAIL = re.compile(r"[\w.+-]+@[\w.-]+")
HONORIFIC = re.compile(r"^(Mr|Ms|Mrs|Dr|M|Mme|Mlle|Sr|Sra|Srta|Ing|Prof|Eng|Miss)\.?$", re.I)
BYTES_WRAP = re.compile(r"^b(['\"])(.*)\1$", re.S)

# THE CSV HAS NO WEBSITE COLUMN, BUT THE COUNTRY PAGES DO. I reported the
# opposite after reading only the extractor, and it was wrong: the per-country
# page at /en/countries/<slug>/ prints the contact block with a "Website:" line,
# which is the country's own designation as the Secretariat publishes it. That
# is where afsa.gov.az came from for Azerbaijan after two searches had failed to
# surface it. One request per country, so it is rate-limited and optional.
COUNTRY_PAGE = "https://www.ippc.int/en/countries/%s/"
WEB_LINE = re.compile(r"Website:\s*(https?://\S+|www\.\S+)", re.I)


def slug(country):
    s = country.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def website_for(country, get=None):
    """(url, why) for a country's IPPC page. url is "" when there is none.

    THE FIRST VERSION OF THIS RETURNED "" ON EVERY FAILURE, and the run reported
    "0 of 182 countries with a website on their page" - which reads as 182 pages
    that simply have no Website line, and was in fact 182 requests that never
    got a page. That is the same swallow as `|| echo` in the workflow, written
    by hand: a silent zero is indistinguishable from a working zero.

    So the reason comes back with the result. `why` is one of "ok", "no-line",
    or "fetch:<error>", and the caller counts them separately and prints the
    first few errors verbatim. A zero that says WHY it is zero is a diagnosis;
    a bare zero is not.
    """
    try:
        text = (get or fetch)(COUNTRY_PAGE % slug(country))
    except Exception as e:
        return "", "fetch:%s: %s" % (type(e).__name__, str(e)[:70])
    m = WEB_LINE.search(text)
    if not m:
        return "", "no-line"
    url = m.group(1).rstrip(".,;)\"'")
    return (url if url.lower().startswith("http") else "https://" + url), "ok"

# Columns that carry a person or their contact details. Dropped, never read.
PERSONAL = {"prefix", "first name", "last name", "email", "e-mail",
            "alternate e-mail", "other alternate e-mail", "address", "telephone", "fax"}


def unwrap(cell):
    """b'Direction G\\xc3\\xa9n\\xc3\\xa9rale' -> Direction Generale, accents intact."""
    s = (cell or "").strip()
    m = BYTES_WRAP.match(s)
    if m:
        s = m.group(2)
    s = s.replace("\\r", " ").replace("\\n", " ").replace("\r", " ").replace("\n", " ")
    # The escapes arrive as LITERAL characters - backslash, x, c, 3 - not as
    # bytes, so a latin-1 round-trip alone cannot see them. Turn each \\xNN into
    # the character it names first; the selftest failed on exactly this.
    s = re.sub(r"\\x([0-9a-fA-F]{2})", lambda m: chr(int(m.group(1), 16)), s)
    # What remains is UTF-8 that was decoded as latin-1 somewhere upstream.
    # Re-encoding as latin-1 and decoding as UTF-8 undoes exactly that, and
    # raises harmlessly on text that never went through it.
    try:
        s = s.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass
    return re.sub(r"\s+", " ", s).strip(" ,;")


def fetch(url=None):
    req = Request(url or URL, headers={"User-Agent": UA})
    with urlopen(req, timeout=120) as r:
        return r.read().decode("utf-8-sig", "replace")


def parse(text):
    """One record per country: the designated organization, nothing else."""
    rows = list(csv.DictReader(io.StringIO(text)))
    out, seen = [], set()
    for row in rows:
        norm = {(k or "").strip().lower(): v for k, v in row.items()}
        if "official contact point" not in (norm.get("contact type") or "").lower():
            continue
        country = unwrap(norm.get("country"))
        org = unwrap(norm.get("organization"))
        if not country or not org or country in seen:
            continue
        seen.add(country)
        out.append({"country": country,
                    "region": unwrap(norm.get("region")),
                    "organization": org,
                    "_source": "IPPC official contact points, Art. VIII.2"})
    return out


def scrub_check(records):
    blob = json.dumps(records, ensure_ascii=False)
    assert not EMAIL.search(blob), "an e-mail address survived into the output"
    for token in ("b'", 'b"', "\\x"):
        assert token not in blob, "an unparsed bytes repr survived: %s" % token
    for rec in records:
        for word in rec["organization"].split():
            assert not HONORIFIC.match(word.strip(",")), \
                "an honorific survived, so a personal name may have: %r" % rec["organization"]


def selftest():
    ok = True

    def check(label, got, want):
        nonlocal ok
        good = got == want
        ok = ok and good
        print("  %-56s %s" % (label, "pass" if good else "FAIL got %r" % (got,)))

    check("bytes wrapper removed",
          unwrap("b'Bahamas Agricultural Health and Food Safety Authority'"),
          "Bahamas Agricultural Health and Food Safety Authority")
    check("double-encoded accents repaired",
          unwrap("b'Direction G\\xc3\\xa9n\\xc3\\xa9rale de la Protection des V\\xc3\\xa9g\\xc3\\xa9taux'"),
          "Direction G\u00e9n\u00e9rale de la Protection des V\u00e9g\u00e9taux")
    check("plain text passes through untouched",
          unwrap("Ministry of Agriculture"), "Ministry of Agriculture")
    check("embedded newlines collapse",
          unwrap("b'Bureau of Agriculture,\\r\\nP.O. Box 460'"), "Bureau of Agriculture, P.O. Box 460")
    check("empty stays empty", unwrap(""), "")

    header = ("Country,Region,Contact Type,Prefix,First Name,Last Name,Email,"
              "Alternate E-mail,Other Alternate E-mail,Organization,Address\n")
    body = (
        "Guyana,Latin America and Caribbean,IPPC Official Contact Point,Mr.,b'Aaa',b'Bbb',"
        "x@y.gov.gy,,,b'National Plant Protection Organisation (NPPO)',b'Mon Repos'\n"
        "Niger,Africa,IPPC Official Contact Point,Mme.,b'Ccc',b'Ddd',z@y.fr,,,"
        "b'Direction G\\xc3\\xa9n\\xc3\\xa9rale de la Protection des V\\xc3\\xa9g\\xc3\\xa9taux',b'BP 323'\n"
        "Guyana,Latin America and Caribbean,IPPC Official Contact Point,Mr.,b'Eee',b'Fff',"
        "dupe@y.gov.gy,,,b'A Second Guyana Row',b'Somewhere'\n"
        "Fictionia,Europe,Editor,Mr.,b'Ggg',b'Hhh',e@f.eu,,,b'Not A Contact Point',b'Nowhere'\n"
        "Blankland,Africa,IPPC Official Contact Point,Mr.,b'Iii',b'Jjj',k@l.m,,,,b'No Org'\n")
    recs = parse(header + body)
    check("one record per country", len(recs), 2)
    check("first country kept, duplicate dropped",
          [r["country"] for r in recs], ["Guyana", "Niger"])
    check("organization carried and repaired",
          recs[1]["organization"], "Direction G\u00e9n\u00e9rale de la Protection des V\u00e9g\u00e9taux")
    check("non-contact-point row excluded",
          any(r["country"] == "Fictionia" for r in recs), False)
    check("row with no organization dropped rather than guessed",
          any(r["country"] == "Blankland" for r in recs), False)
    check("no person fields on the record",
          sorted(recs[0]), ["_source", "country", "organization", "region"])

    try:
        scrub_check(recs)
        check("scrub assertions pass on clean output", True, True)
    except AssertionError as e:
        check("scrub assertions pass on clean output", str(e), True)

    # And the assertion must actually fire when something leaks, or it is decoration.
    leaked = [{"country": "X", "region": "Y", "organization": "Mr. Someone x@y.z", "_source": "s"}]
    try:
        scrub_check(leaked)
        check("scrub assertion FIRES on a leak", "did not fire", "fires")
    except AssertionError:
        check("scrub assertion FIRES on a leak", "fires", "fires")

    # The website pass. Driven with a stubbed fetcher so it needs no network.
    PAGE = ("Chief state phytosanitary officer / Head of Plant Health Department "
            "Food Safety Agency Phone: +994 12 565 12 72 Email: someone@afsa.gov.az "
            "Website: http://www.afsa.gov.az Date contact registration: 02 Nov 2021")
    check("website read from the country page",
          website_for("Azerbaijan", lambda u: PAGE), ("http://www.afsa.gov.az", "ok"))
    check("bare www gets a scheme",
          website_for("X", lambda u: "Website: www.example.gov.x"),
          ("https://www.example.gov.x", "ok"))
    check("trailing punctuation stripped",
          website_for("X", lambda u: "Website: http://a.gov.b."), ("http://a.gov.b", "ok"))
    check("no Website line gives empty AND says so",
          website_for("X", lambda u: "Phone: +1 555 0100"), ("", "no-line"))
    def boom(u): raise OSError("HTTP Error 403: Forbidden")
    url, why = website_for("X", boom)
    check("an unreachable page costs nothing", url, "")
    # The distinction the run needed and did not have.
    check("and is NOT reported as a page with no website", why.startswith("fetch"), True)
    check("the error text is carried, not discarded", "403" in why, True)
    check("country slugged for the URL path", slug("C\u00f4te d'Ivoire"), "c-te-d-ivoire")

    print("\n%s" % ("all pass" if ok else "FAILURES ABOVE"))
    return 0 if ok else 1


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    try:
        text = fetch()
    except Exception as e:
        # Exit 0. This runs under `bash -e` in a step that must not take the
        # other harvesters down with it.
        print("could not fetch the IPPC extractor: %s" % e, file=sys.stderr)
        print("leaving %s untouched and continuing" % OUT.name, file=sys.stderr)
        return
    recs = parse(text)
    scrub_check(recs)
    print("  ippc      %5d countries with a designated organization" % len(recs))
    if "--websites" in sys.argv:
        # One request per country against the IPPC country pages, which carry a
        # Website: line the CSV omits. Paced, and a failure on one country is
        # recorded as no website rather than taking the run down.
        import collections, time
        got, why = 0, collections.Counter()
        errors = []
        for r in recs:
            w, reason = website_for(r["country"])
            why[reason.split(":")[0]] += 1
            if reason.startswith("fetch") and len(errors) < 5:
                errors.append("%s -> %s" % (r["country"], reason))
            if w:
                r["website"] = w; got += 1
            time.sleep(0.5)
        print("  ippc      %5d of %d countries with a website on their page"
              % (got, len(recs)))
        print("  ippc            pages read %d, no Website line %d, fetch failed %d"
              % (why["ok"], why["no-line"], why["fetch"]))
        for e in errors:
            print("  ippc            %s" % e)
        if why["fetch"] and not why["ok"]:
            print("  ippc            EVERY request failed - this is not a source with no "
                  "websites, it is a source that was never reached. Do not read the "
                  "zero above as evidence about the IPPC pages.")
        scrub_check(recs)
    if "--print" in sys.argv:
        for r in recs[:20]:
            print("    %-28s %s" % (r["country"][:28], r["organization"][:70]))
        return
    OUT.write_text(json.dumps(
        {"note": ("IPPC official contact points, Article VIII.2. ORGANIZATION ONLY - "
                  "the source is a contact list and every personal field is dropped "
                  "before writing, with an assertion. No website is published in this "
                  "source, so these name a body and do not link it."),
         "generated": __import__("datetime").date.today().isoformat(),
         "contacts": recs}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote %s: %d countries" % (OUT.name, len(recs)))


if __name__ == "__main__":
    main()
