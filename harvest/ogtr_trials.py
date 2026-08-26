#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OGTR crop field trial sites — the one register that publishes site locations.

Australia's Office of the Gene Technology Regulator runs an interactive map of
current and post-harvest-monitoring GMO crop field trials, carrying the licence,
the holder, the crop and trait, the area, the council area and the state:

    https://www.ogtr.gov.au/what-weve-approved/crop-field-trial-map

**The site list is rendered into that page as an HTML table.** That is the route
this script now takes first. The previous version went looking for a JSON
endpoint and treated the page as a place to find one; the page already carries
every field except the marker coordinates, so the table is the data and the
endpoint is an upgrade to it, not a prerequisite.

**It checks robots.txt first and stops if the path is disallowed.** Where the
host will not answer a robots request at all, it reads the archived copy of
robots.txt rather than proceeding without an answer or refusing on a technical
failure — see _robots().

    python3 harvest/ogtr_trials.py --diagnose      # is the host reachable, and how does it fail
    python3 harvest/ogtr_trials.py --selftest      # no network
    python3 harvest/ogtr_trials.py --dry-run
    python3 harvest/ogtr_trials.py

Writes harvest/ogtr_trials.json, merged into projects.json by aphis_releases.py.

# ---------------------------------------------------------------------------
# WHAT THE PREVIOUS VERSION SAID, AND WHY IT IS DELETED
#
# It carried, in two adjacent comment blocks, both of these:
#
#   "It is simply not reachable from the United States ... every 'refused' this
#    script has ever printed is neither a robots rule nor a dead host. It is
#    geography."
#
#   "Correction to the above: the endpoint is not blocked by a bot filter.
#    ogtr.gov.au's robots.txt DISALLOWS this path, and the script checks it and
#    stops."
#
# Those cannot both be why it stopped, and neither was verified. The page was
# subsequently retrieved in full — all 33 site rows, licence number through crop
# status — by a US-based client that is not a whitelisted search crawler. So the
# geography claim is false as stated, and the robots claim was never read off
# the file.
#
# Deleted with them: "the next person should not spend a round trying." That
# line's only effect was to stop the attempt that works.
#
# What the failures actually looked like: connection accepted, nothing ever
# returned, from two clients both identifying as GMO-map-harvest/1.0. A geo rule
# normally answers fast — a reset, or a 403 page. Silence after a completed
# connection is what a request filter does. --diagnose separates those: DNS,
# TCP, TLS and HTTP are asked in order, and the stage that fails is named.
# ---------------------------------------------------------------------------
"""
import json, os, re, socket, ssl, sys, time, pathlib, urllib.parse
from html.parser import HTMLParser

# EVERY socket in this process gets a ceiling.
#
# A run printed "checking robots.txt for each candidate path" and then produced
# nothing for six minutes until `timeout` killed it. The next line it owed was
# the robots.txt status, so it hung inside the robots fetch - and the version
# running still called RobotFileParser.read(), which does urlopen(self.url)
# with NO timeout argument. urlopen's default is None, which means block
# forever. Behind a proxy that accepts the connection and never answers, that
# is a hang with no ceiling and no output.
#
# _robots() no longer calls rp.read() at all, so that specific path is gone.
# This line is the guard for the next one: an explicit timeout on a call is a
# promise the author remembered to make, and this file has now been bitten
# twice by a call where nobody did.
socket.setdefaulttimeout(60)
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "harvest" / "ogtr_trials.json"
LGA_FILE = ROOT / "harvest" / "au_lga_centroids.json"

BASE = "https://www.ogtr.gov.au"
HOST = "www.ogtr.gov.au"
PAGE = BASE + "/what-weve-approved/crop-field-trial-map"

UA = "GMO-map-harvest/1.0 (+https://github.com/WelcomeToYourGalaxy/GMO-map)"
HDRS = {"User-Agent": UA,
        "Accept": "text/html,application/json;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-AU,en;q=0.9",
        "Referer": PAGE}

# A browser user-agent, used by --diagnose ONLY, to answer one question: does
# this host answer the same request differently depending on who asks. It is
# never used to fetch data. If it turns out to be the difference, that is a
# finding to act on deliberately - not a switch to flip in the harvester.
UA_BROWSER = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
              "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36")

# Set OGTR_RELAY to the URL of a fetch relay in ap-southeast-2 and every request
# below goes through it. Contract: GET {RELAY}?url=<percent-encoded absolute
# URL> returns the upstream body verbatim. Nothing else about it is assumed, so
# any of Lambda-with-a-Function-URL, a Sydney VM or a Worker satisfies it. See
# relay/README.md.
RELAY = os.environ.get("OGTR_RELAY", "").strip()

# Wayback. `id_` returns the archived bytes unrewritten, which matters for
# robots.txt (a rewritten copy is not the file) and for finding the map's own
# inline data (the rewriter mangles script contents).
WB_AVAIL = "https://archive.org/wayback/available?url=%s"
WB_RAW = "https://web.archive.org/web/%sid_/%s"

# Drupal exposes a view as JSON at several conventional paths. Kept, because a
# real endpoint carries the marker coordinates and the table does not - but it is
# no longer the only route, so a run that finds none of these still produces
# data.
ENDPOINTS = [
    "/jsonapi/node/field_trial",
    "/jsonapi/node/crop_field_trial",
    "/api/crop-field-trials",
    "/what-weve-approved/crop-field-trial-map?_format=json",
    "/what-weve-approved/crop-field-trial-map/data",
    "/sites/default/files/crop-field-trial-map.geojson",
    "/views/ajax?view_name=crop_field_trial_map&view_display_id=default",
]

# Australia's rough bounds, used to reject anything that is not a site coordinate
AU = (-44.0, -9.0, 112.0, 154.0)

# There is NO state-level fallback. A trial placed at the middle of Western
# Australia is a marker on a map that says nothing: the state is already in the
# record text, the point adds no information the reader did not have, and it
# invites a reader to think a release happened somewhere it did not. A row that
# cannot be placed at its council area or better is dropped, and the count of
# dropped rows is printed so the gap is visible rather than papered over.
STATE_NAME = {
    "NSW": "New South Wales", "VIC": "Victoria", "QLD": "Queensland",
    "SA": "South Australia", "WA": "Western Australia", "TAS": "Tasmania",
    "NT": "Northern Territory", "ACT": "Australian Capital Territory",
}
_STATE_ALIAS = {
    "new south wales": "NSW", "victoria": "VIC", "queensland": "QLD",
    "south australia": "SA", "western australia": "WA", "tasmania": "TAS",
    "northern territory": "NT", "australian capital territory": "ACT",
    "act": "ACT", "nsw": "NSW", "vic": "VIC", "qld": "QLD", "sa": "SA",
    "wa": "WA", "tas": "TAS", "nt": "NT",
}


# ---------------------------------------------------------------------------
# Reachability
# ---------------------------------------------------------------------------

def _relay(url):
    if not RELAY:
        return url
    sep = "&" if "?" in RELAY else "?"
    return RELAY + sep + "url=" + urllib.parse.quote(url, safe="")


# Set the first time a request to the origin fails at a stage that means the
# host is not answering this runner. Every later live request is then skipped
# rather than attempted.
#
# The 2026-08-24 run spent 4m10s of a 6m budget waiting: 78s on robots.txt, 55s
# on one endpoint, 116s on the map page, all with the identical failure
# ("connected, no HTTP response"), and about a second doing the actual work off
# the archived copy. Each wait was a fresh attempt to learn something the
# previous wait had already established.
LIVE_DEAD = []


def _dead(reason=""):
    if not LIVE_DEAD:
        LIVE_DEAD.append(reason or "unspecified")
        print("  the origin is not answering this runner (%s). Skipping the "
              "remaining live requests and going to the archived copy."
              % LIVE_DEAD[0])
    return LIVE_DEAD[0]


def fetch(url, timeout=25, tries=1, hdrs=None, raw=False):
    """One request, with the failing STAGE named in the exception text.

    `str(e)[:60]` was the whole diagnostic before, and for a socket timeout that
    string is "timed out" - true of a DNS failure, a dropped SYN, an unfinished
    TLS handshake and a server that accepts and never writes. Those are four
    different problems with four different fixes, and the log could not tell
    them apart. The stage is now attached to the message.
    """
    last = None
    target = _relay(url)
    if LIVE_DEAD and HOST in url and not RELAY:
        raise RuntimeError("skipped [%s]" % LIVE_DEAD[0])
    for attempt in range(tries):
        try:
            r = urlopen(Request(target, headers=hdrs or HDRS), timeout=timeout)
            body = r.read()
            return body if raw else body.decode("utf-8", "replace")
        except Exception as e:
            last = e
            code = getattr(e, "code", None)
            if code in (401, 403, 404, 410):
                break               # an answer, not a transient failure
            time.sleep(1.5 * (attempt + 1))
    stage = _classify(url, last)
    # A stage at or below HTTP means the host is not talking to this runner at
    # all, and it will not talk to it about the next URL either. A 404 or a 403
    # is an ANSWER and says nothing about the next path, so it does not trip
    # the breaker.
    if HOST in url and stage in ("DNS", "TCP connect", "TLS handshake",
                                 "connected, no HTTP response"):
        _dead(stage)
    raise RuntimeError("%s [%s] %s" % (type(last).__name__, stage, str(last)[:70]))


def _classify(url, err):
    """Which layer gave out. Cheap - one DNS lookup and one connect attempt."""
    if getattr(err, "code", None):
        return "HTTP %s" % err.code
    host = urllib.parse.urlsplit(_relay(url)).hostname or HOST
    try:
        socket.getaddrinfo(host, 443, proto=socket.IPPROTO_TCP)
    except Exception:
        return "DNS"
    try:
        s = socket.create_connection((host, 443), timeout=8)
    except Exception:
        return "TCP connect"
    try:
        ssl.create_default_context().wrap_socket(s, server_hostname=host).close()
    except Exception:
        return "TLS handshake"
    else:
        s.close()
    return "connected, no HTTP response"


def _probe(label, fn):
    t = time.time()
    try:
        detail = fn()
        print("  %-34s ok    %5.1fs  %s" % (label, time.time() - t, detail or ""))
        return True
    except Exception as e:
        print("  %-34s FAIL  %5.1fs  %s: %s"
              % (label, time.time() - t, type(e).__name__, str(e)[:64]))
        return False


def diagnose():
    """Ask the four layers in order, then ask whether the answer depends on who
    is asking. This is the round that should have run first, and every claim in
    the deleted comment block above would have been settled by it."""
    print("reachability of %s\n" % HOST)
    if RELAY:
        print("  OGTR_RELAY is set; the direct probes below still go direct.\n")

    def dns(family):
        def f():
            got = socket.getaddrinfo(HOST, 443, family, socket.SOCK_STREAM)
            return ", ".join(sorted({a[4][0] for a in got}))
        return f

    def tcp(family):
        def f():
            infos = socket.getaddrinfo(HOST, 443, family, socket.SOCK_STREAM)
            s = socket.socket(infos[0][0], socket.SOCK_STREAM)
            s.settimeout(12)
            s.connect(infos[0][4])
            s.close()
            return infos[0][4][0]
        return f

    def tls():
        c = ssl.create_default_context()
        s = c.wrap_socket(socket.create_connection((HOST, 443), timeout=12),
                          server_hostname=HOST)
        v = s.version()
        s.close()
        return v

    def http(hdrs, method="GET", path="/robots.txt"):
        def f():
            req = Request(BASE + path, headers=hdrs)
            req.get_method = lambda: method
            r = urlopen(req, timeout=25)
            return "HTTP %s, %s bytes" % (r.getcode(), len(r.read()))
        return f

    _probe("DNS, IPv4", dns(socket.AF_INET))
    _probe("DNS, IPv6", dns(socket.AF_INET6))
    v4 = _probe("TCP 443, IPv4", tcp(socket.AF_INET))
    v6 = _probe("TCP 443, IPv6", tcp(socket.AF_INET6))
    tl = _probe("TLS handshake", tls)
    a = _probe("GET /robots.txt, harvester UA", http(HDRS))
    b = _probe("HEAD /robots.txt, harvester UA", http(HDRS, "HEAD"))
    c = _probe("GET /robots.txt, browser UA",
               http({"User-Agent": UA_BROWSER, "Accept": "*/*"}))
    d = _probe("GET the map page, harvester UA",
               http(HDRS, "GET", "/what-weve-approved/crop-field-trial-map"))

    print("\nreading:")
    if not (v4 or v6):
        print("  Nothing above the network layer was reached. Either this "
              "machine has no route to the host or the packets are dropped "
              "before they arrive. Run the same probe from another network "
              "before concluding it is the host.")
    elif v6 and not v4:
        print("  IPv6 connects and IPv4 does not. A client preferring IPv4 "
              "will hang. This is a local routing problem, not the host's.")
    elif v4 and not v6:
        print("  IPv4 connects and IPv6 does not. A client preferring IPv6 - "
              "which macOS does - hangs on the AAAA record while IPv4 would "
              "have worked. Fetch with the address family pinned.")
    elif not tl:
        print("  TCP completes and TLS does not. Something is terminating the "
              "connection at the handshake: a middlebox, or the host refusing "
              "this client before HTTP is spoken.")
    elif c and not a:
        print("  The SAME request succeeds with a browser user-agent and fails "
              "with the harvester's. That is a request filter, not geography, "
              "and it is a decision to make rather than a switch to flip: the "
              "identity in UA is honest about what this is, and the way past a "
              "filter is to ask the office for the data, not to dress up as "
              "something else.")
    elif a and not b:
        print("  GET is answered and HEAD is not. `curl -sI` sends HEAD, so a "
              "silent `curl -sI` here means nothing at all about whether the "
              "site is reachable.")
    elif a and not d:
        print("  robots.txt is served and the map page is not. That is a rule "
              "or a filter on that path specifically - check the robots answer "
              "below before treating it as a block.")
    elif a and d:
        print("  The host answers this machine. Any 'refused' from a previous "
              "run was not the network.")
    print("\nrobots.txt, as the site itself states it:")
    _robots()


# ---------------------------------------------------------------------------
# robots.txt
# ---------------------------------------------------------------------------

def allowed(url):
    """Ask robots.txt about THIS path, not about the site.

    The check runs per endpoint: a Drupal site commonly disallows /views/ajax
    and leaves /sites/default/files/ and the JSON API open, and those are
    different paths with different answers. The refusal is honoured; what one
    disallowed path no longer does is stand in for all of them.
    """
    rp = _robots()
    if rp is None:
        return False, ("robots.txt could not be read live OR from the archive. "
                       "Treating that as a refusal rather than a licence.")
    ok = rp.can_fetch(UA, url)
    if not ok and getattr(rp, "disallow_all", False):
        # NOT the same answer as a Disallow line, and it used to print as one.
        return False, ("robots.txt could not be READ (401/403), so every path "
                       "reads as disallowed. This is a block on the fetcher, "
                       "not the site's rule.")
    return ok, ("robots.txt permits %s" % url if ok else
                "robots.txt disallows %s" % url)


_ROBOTS = []
ROBOTS_SRC = [""]


def _robots():
    """Fetch robots.txt ONCE and say what came back, live or archived.

    RobotFileParser.read() SWALLOWS 401 and 403: it sets disallow_all and
    raises nothing. So a WAF on the runner's IP produced a parser that refuses
    every path, printed by the caller as "refused" - the same word as a real
    Disallow line. Fetching the file directly gives the status code, which is
    the thing that distinguishes those two.

    THE ADDITION: when the host answers nothing at all, the archived copy is
    read instead. This is the way out of a circle the previous version sat in -
    the run needed to know the site's rule, the only place the rule is written
    is on a host that would not answer, and an unreadable rule was treated as a
    refusal, so the script could never learn whether it was actually refused.
    An archived copy of a public robots.txt is the site's own statement of its
    own rule; reading it is not a way around the rule, it is how you find out
    what it says. Its date is printed, because a rule can change.
    """
    if _ROBOTS:
        return _ROBOTS[0]
    url = BASE + "/robots.txt"
    code, note, body = None, "", None
    # ONE attempt at 20s, not three at 60. This is the first request of the run,
    # so it is also the cheapest place to find out that the host is silent, and
    # a retry has never once turned a silence into an answer here.
    try:
        r = urlopen(Request(_relay(url), headers=HDRS), timeout=20)
        code, note = r.getcode(), ""
        body = r.read().decode("utf-8", "replace")
        ROBOTS_SRC[0] = "live"
    except Exception as e:
        code = getattr(e, "code", None)
        note = "%s: %s" % (type(e).__name__, str(e)[:60])
        if code is None:
            _dead(_classify(url, e))

    if body is None and code is None:
        arch, when = _archived(url)
        if arch is not None:
            body, code = arch, "archived"
            ROBOTS_SRC[0] = "archive %s" % when
            print("  robots.txt: the host answered nothing (%s). Read the "
                  "ARCHIVED copy instead, snapshot %s." % (note, when))

    rp = RobotFileParser()
    rp.set_url(url)
    if body is not None:
        try:
            rp.parse(body.splitlines())
        except Exception as e:
            print("  robots.txt: %s but parsing it raised %s" % (code, str(e)[:60]))
            _ROBOTS.append(None)
            return None
    elif code in (401, 403):
        rp.disallow_all = True             # same rule the stdlib applies
    elif code is not None and 400 <= code < 500:
        rp.allow_all = True                # a 404 is not a refusal
    else:
        print("  robots.txt: no response and no archived copy (%s)"
              % (note or "no reason recorded"))
        _ROBOTS.append(None)
        return None

    print("  robots.txt: %s [%s] | disallow_all=%s allow_all=%s"
          % (code, ROBOTS_SRC[0] or "live",
             getattr(rp, "disallow_all", False), getattr(rp, "allow_all", False)))
    if body is not None:
        rules = [l.strip() for l in body.splitlines()
                 if l.strip().lower().startswith("disallow")]
        print("     %d Disallow lines; map path permitted=%s"
              % (len(rules), rp.can_fetch(UA, PAGE)))
    if getattr(rp, "disallow_all", False):
        print("     ^ 401/403 on robots.txt. Every path below will read as "
              "refused. That is this fetcher being blocked, NOT the site "
              "publishing a rule against these paths.")
    _ROBOTS.append(rp)
    return rp


def permitted_endpoints():
    """Which candidate paths the site allows. Printed in full, so a run says
    what was tried and what was refused rather than only that it failed."""
    out = []
    for ep in ENDPOINTS:
        url = BASE + ep
        ok, _ = allowed(url)
        print("  %-52s %s" % (ep[:52], "allowed" if ok else "refused"))
        if ok:
            out.append(url)
    if not out:
        rp = _robots()
        if rp is None or getattr(rp, "disallow_all", False):
            print("  NOTHING WAS LEARNED about this site's rules. robots.txt "
                  "was not read - not live, not from the archive - so every "
                  "path reads as refused. This run does NOT show the route is "
                  "closed. Run --diagnose, then repeat from an unblocked "
                  "network or through OGTR_RELAY.")
        else:
            print("  every candidate path is disallowed by a rule in "
                  "robots.txt. Nothing here is a workaround for that: the "
                  "route that does not need permission is to ask the office "
                  "for the site list, which is a dataset they publish anyway.")
    return out


# ---------------------------------------------------------------------------
# The archive
# ---------------------------------------------------------------------------

# Wayback refuses bursts. On 2026-08-26 the robots.txt snapshot came back fine
# and the map-page request four seconds later got ECONNREFUSED - not a 429,
# just a closed socket, which reads like a dead archive rather than a rate
# limit. Two archive requests are wanted per run, so they are spaced and
# retried rather than fired back to back.
_ARCH_LAST = [0.0]
ARCH_GAP = 6.0


def _wb_get(url, timeout, tries=3):
    last = None
    for attempt in range(tries):
        wait = ARCH_GAP - (time.time() - _ARCH_LAST[0])
        if wait > 0:
            time.sleep(wait)
        _ARCH_LAST[0] = time.time()
        try:
            return urlopen(Request(url, headers={"User-Agent": UA}),
                           timeout=timeout).read().decode("utf-8", "replace")
        except Exception as e:
            last = e
            code = getattr(e, "code", None)
            if code == 404:
                break                      # no snapshot; retrying cannot help
            if attempt < tries - 1:
                # Refusals here are volumetric, so the backoff is generous.
                # This is the only route left when the origin is silent.
                time.sleep(8 * (attempt + 1))
    raise last


def _archived(url):
    """Newest snapshot of `url`, as bytes-decoded text, plus its timestamp.

    Reachable when the origin is not, and it holds something the live page does
    not: the table lists current and post-harvest-monitoring trials only, so
    snapshots are the only route to trials that have since closed out.
    """
    try:
        meta = json.loads(_wb_get(WB_AVAIL % urllib.parse.quote(url, safe=""), 30))
    except Exception as e:
        print("  archive lookup failed after 3 tries: %s: %s"
              % (type(e).__name__, str(e)[:60]))
        return None, ""
    snap = ((meta.get("archived_snapshots") or {}).get("closest") or {})
    if not snap.get("available") or not snap.get("timestamp"):
        return None, ""
    ts = snap["timestamp"]
    when = "%s-%s-%s" % (ts[:4], ts[4:6], ts[6:8])
    try:
        raw = _wb_get(WB_RAW % (ts, url), 45)
    except Exception as e:
        print("  archive fetch failed after 3 tries: %s: %s"
              % (type(e).__name__, str(e)[:60]))
        return None, ""
    return raw, when


# ---------------------------------------------------------------------------
# The page: the table, and any coordinates written into it
# ---------------------------------------------------------------------------

class _Tables(HTMLParser):
    """Every table in the document as rows of plain-text cells.

    HTMLParser rather than a regex because the cells are not flat - the fetched
    page puts the organism and the trait inside their own block elements, so a
    `<td>(.*?)</td>` capture returns markup and a cell's text arrives in
    several pieces.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tables, self._t, self._r, self._c = [], None, None, None

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self._t = []
        elif tag == "tr" and self._t is not None:
            self._r = []
        elif tag in ("td", "th") and self._r is not None:
            self._c = []

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self._c is not None:
            self._r.append(re.sub(r"\s+", " ", "".join(self._c)).strip())
            self._c = None
        elif tag == "tr" and self._r is not None:
            if any(self._r):
                self._t.append(self._r)
            self._r = None
        elif tag == "table" and self._t is not None:
            self.tables.append(self._t)
            self._t = None

    def handle_data(self, data):
        if self._c is not None:
            self._c.append(data)


# Header word -> the key the rest of the file uses. `sitenumber`, not `site`:
# pick() matches a name that runs on only into more letters, so a key called
# `site` would win the location lookup with a row number in it - the same trap
# the pick() docstring describes for `website` and `real_estate`, one column
# over.
# ORDER MATTERS: _colkey returns on the first word that appears in the header,
# so every entry must be checked before any entry that is a substring of the
# same header. Caught in the selftest: OGTR's last column is headed "Crop
# status", ("crop", "organism") sat above ("status", "status"), and the status
# column was read as a second organism. setdefault kept the real organism, so
# nothing looked wrong - the crop status simply vanished from every row, and
# every record fell back to the default "Licensed field trial".
_COLS = [
    ("licence number", "licence"), ("license number", "licence"),
    ("crop status", "status"), ("status", "status"),
    ("site number", "sitenumber"),
    ("organisation", "organisation"), ("organization", "organisation"),
    ("parent organism", "organism"), ("organism", "organism"),
    ("modified trait", "trait"), ("trait", "trait"), ("modif", "trait"),
    ("local government", "lga"), ("council", "lga"), ("shire", "lga"),
    ("state", "state"), ("territory", "state"),
    ("area", "area"),
    ("latitude", "_lat"), ("longitude", "_lng"),
    ("licence", "licence"), ("license", "licence"),
    ("crop", "organism"), ("species", "organism"),
    ("site", "sitenumber"),
]


def _colkey(header):
    h = (header or "").lower()
    for word, key in _COLS:
        if word in h:
            return key
    return ""


def parse_page_table(html):
    """The site list, from the table the page renders it into.

    Chooses the table by its HEADER, not by position: a Drupal page carries
    layout and related-content tables too, and "the first table" is a
    positional assumption that breaks on the next redesign.
    """
    p = _Tables()
    try:
        p.feed(html)
        p.close()
    except Exception as e:
        print("  page markup could not be parsed: %s" % str(e)[:60])
        return []
    best, rows = None, []
    for t in p.tables:
        if len(t) < 2:
            continue
        head = [_colkey(c) for c in t[0]]
        score = sum(1 for k in ("licence", "organism", "lga", "state") if k in head)
        if score >= 3 and (best is None or score > best[0]):
            best = (score, head, t[1:])
    if best is None:
        return []
    _, head, body = best
    for r in body:
        row = {}
        for i, cell in enumerate(r):
            if i < len(head) and head[i] and cell:
                row.setdefault(head[i], cell)
        if row.get("licence") or row.get("organism"):
            rows.append(row)
    print("  page table: %d site rows, columns %s"
          % (len(rows), ", ".join(k for k in head if k)))
    return rows


def _json_blobs(text, cap=400):
    """Balanced JSON objects and arrays embedded in the document.

    A map draws markers from coordinates that are somewhere, and "somewhere" is
    an endpoint OR a literal in the page. The previous version only looked for
    endpoint URLs, so a page carrying its own marker array read as having no
    data at all.
    """
    out, i, n = [], 0, len(text)
    while i < n and len(out) < cap:
        ch = text[i]
        if ch not in "[{":
            i += 1
            continue
        close = "]" if ch == "[" else "}"
        depth, j, instr, esc = 0, i, False, False
        while j < n and j - i < 400000:
            c = text[j]
            if instr:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == '"':
                    instr = False
            elif c == '"':
                instr = True
            elif c in "[{":
                depth += 1
            elif c in "]}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        if j < n and depth == 0 and text[j] == close:
            chunk = text[i:j + 1]
            if re.search(r"lat|lng|lon", chunk, re.I):
                try:
                    out.append(json.loads(chunk))
                except Exception:
                    pass
            i = j + 1
        else:
            i += 1
    return out


def find_inline_coords(html):
    """Site coordinates written into the page, keyed for merging onto the table.

    Returns {(licence, site number): (lat, lng)}. Only pairs inside Australia
    are kept - a page also carries a map default centre, a bounding box and
    sometimes an office address, and any of those would place a trial somewhere
    it is not.
    """
    found = {}
    for blob in _json_blobs(html):
        rows = blob if isinstance(blob, list) else [blob]
        for r in rows:
            if not isinstance(r, dict):
                continue
            la, ln = coords(r)
            if la is None:
                continue
            key = _key(pick(r, "licence", "license", "dir"),
                       pick(r, "sitenumber", "site_number", "site_no"))
            found.setdefault(key, (la, ln))
    if found:
        print("  %d coordinate pairs inside Australia found in the page markup"
              % len(found))
    return found


def _key(lic, site):
    lic = re.sub(r"[^a-z0-9]", "", (lic or "").lower())
    return (lic, re.sub(r"[^a-z0-9]", "", (site or "").lower()))


def merge_coords(rows, coord_map):
    """Attach a coordinate to a table row where one was published for it."""
    hit = 0
    for r in rows:
        k = _key(r.get("licence"), r.get("sitenumber"))
        pt = coord_map.get(k) or (coord_map.get((k[0], "")) if len(coord_map) else None)
        if pt:
            r["_lat"], r["_lng"] = pt[0], pt[1]
            hit += 1
    if coord_map:
        print("  %d of %d rows matched a published coordinate" % (hit, len(rows)))
    return rows


def find_endpoints(page):
    """Candidate data URLs referenced by the map page, most specific first."""
    out = []
    for pat in (r'["\'](/[^"\']*?(?:geojson|/api/|jsonapi|views/ajax|export)[^"\']*)["\']',
                r'["\'](https?://[^"\']*?(?:geojson|/api/|jsonapi)[^"\']*)["\']',
                r'data-[a-z-]*url=["\']([^"\']+)["\']'):
        for u in re.findall(pat, page, re.I):
            u = u if u.startswith("http") else BASE + u
            if u not in out:
                out.append(u)
    return out


def harvest_rows(payload):
    """Pull site rows out of whatever shape the endpoint returns."""
    try:
        data = json.loads(payload)
    except Exception:
        return []
    if isinstance(data, dict) and data.get("type") == "FeatureCollection":
        rows = []
        for f in data.get("features", []):
            g = (f.get("geometry") or {}).get("coordinates") or []
            p = dict(f.get("properties") or {})
            if len(g) >= 2:
                p["_lng"], p["_lat"] = g[0], g[1]
            rows.append(p)
        return rows
    if isinstance(data, list):
        return [r for r in data if isinstance(r, dict)]
    for k in ("rows", "data", "results", "items", "features"):
        v = data.get(k) if isinstance(data, dict) else None
        if isinstance(v, list):
            return [r for r in v if isinstance(r, dict)]
    return []


def pick(row, *names):
    """First value whose KEY contains one of these names as a whole word.

    It used to be a bare substring test, and every Drupal jsonapi node carries
    `revision_translation_affected` - "translation" contains "lat". Asked for a
    latitude, pick returned True, float() rejected it, coords() returned
    (None, None), and to_record() dropped the row - for EVERY row, so a jsonapi
    endpoint answering correctly with forty trials reported "0 of 40 usable".

    Four more sat on the same trap: `site` matched website, `state` matched
    real_estate, `size` matched filesize, `dir` matched director.
    """
    for n in names:
        pat = re.compile(r"(?:^|[^a-z])" + re.escape(n.lstrip("_")) + r"(?![a-z])")
        for k, v in row.items():
            if not k or v in (None, ""):
                continue
            key = str(k).lower()
            if n.startswith("_"):
                if n not in key:            # internal keys we set ourselves
                    continue
            elif not pat.search(key):
                continue
            return str(v).strip()
    return ""


def coords(row):
    la = pick(row, "_lat", "lat", "latitude")
    ln = pick(row, "_lng", "lon", "lng", "longitude")
    try:
        la, ln = float(la), float(ln)
    except Exception:
        return None, None
    if not (AU[0] <= la <= AU[1] and AU[2] <= ln <= AU[3]):
        return None, None       # not an Australian site coordinate
    return la, ln


# ---------------------------------------------------------------------------
# Placement
# ---------------------------------------------------------------------------

# Rough extents of each state and territory. Used ONLY to reject a geocoder
# result that landed in the wrong one - never to place anything. "Hilltops
# Council" and "Central Highlands Regional Council" both have namesakes, and a
# lookup that answers with the wrong continent's version of a name is the exact
# failure that produces a plausible-looking pair of floats.
STATE_BOX = {
    "NSW": (-37.6, -28.1, 140.9, 153.7), "VIC": (-39.3, -33.9, 140.9, 150.1),
    "QLD": (-29.2, -9.0, 137.9, 153.6), "SA": (-38.2, -25.9, 128.9, 141.1),
    "WA": (-35.2, -13.6, 112.8, 129.1), "TAS": (-43.7, -39.1, 143.7, 148.6),
    "NT": (-26.1, -10.9, 128.9, 138.1), "ACT": (-36.0, -35.1, 148.7, 149.5),
}

NOMINATIM = "https://nominatim.openstreetmap.org/search"
GEO_UA = ("GMO-map-harvest/1.0 (+https://github.com/WelcomeToYourGalaxy/GMO-map)")


def resolve_councils(rows, budget=150.0):
    """Fill harvest/au_lga_centroids.json for the councils these rows name.

    Only the councils that appear, not all 560-odd nationally: the table names
    about thirty, the answer is cached, and a national boundary download is
    several hundred megabytes for a lookup this uses a page of.

    Every entry keeps the OSM object it came from, so a suspect point can be
    opened and checked rather than argued about. A result that is not an
    administrative boundary, or that falls outside the state OGTR named for
    that site, is DISCARDED and the site stays at state grade - a missing
    upgrade costs resolution, a wrong one puts a trial in the wrong place.
    """
    if "--no-geocode" in sys.argv:
        print("  --no-geocode: council areas will not be resolved, so every "
              "row without a published coordinate will be dropped")
        return
    want = {}
    for r in rows:
        lga = (r.get("lga") or "").strip()
        st = _statecode(r.get("state"))
        if lga and st and _lganorm(lga) not in _load_lga():
            want.setdefault(_lganorm(lga), (lga, st))
    if not want:
        return
    print("  resolving %d council areas not yet in %s" % (len(want), LGA_FILE.name))
    store = {}
    if LGA_FILE.exists():
        try:
            store = json.loads(LGA_FILE.read_text(encoding="utf-8"))
        except Exception:
            store = {}
    store.setdefault("centroids", {})
    store.setdefault("note", "Council-area points for OGTR field trial sites, "
                             "from OpenStreetMap administrative boundaries via "
                             "Nominatim. Each entry names the OSM object it "
                             "came from. Rejected where the point fell outside "
                             "the state OGTR named.")
    t0, added, refused = time.time(), 0, 0
    for key, (name, st) in sorted(want.items()):
        if time.time() - t0 > budget:
            print("  geocoding budget spent; %d left for the next run"
                  % (len(want) - added - refused))
            break
        q = urllib.parse.urlencode({
            "q": "%s, %s, Australia" % (name, STATE_NAME.get(st, "")),
            "format": "jsonv2", "limit": "5", "addressdetails": "1"})
        try:
            # Nominatim asks for one request a second and an identifying
            # user-agent. Both are honoured; this is somebody else's server.
            time.sleep(1.2)
            body = urlopen(Request(NOMINATIM + "?" + q,
                                   headers={"User-Agent": GEO_UA}),
                           timeout=25).read().decode("utf-8", "replace")
            hits = json.loads(body)
        except Exception as e:
            print("     %-42s lookup failed (%s)" % (name[:42], str(e)[:40]))
            refused += 1
            continue
        got = None
        for h in hits if isinstance(hits, list) else []:
            if h.get("category") != "boundary" or h.get("type") != "administrative":
                continue
            try:
                la, ln = float(h["lat"]), float(h["lon"])
            except Exception:
                continue
            box = STATE_BOX.get(st)
            if not box or not (box[0] <= la <= box[1] and box[2] <= ln <= box[3]):
                continue
            got = (la, ln, "%s/%s" % (h.get("osm_type", "?"), h.get("osm_id", "?")),
                   h.get("display_name", "")[:120])
            break
        if not got:
            print("     %-42s no administrative boundary inside %s" % (name[:42], st))
            refused += 1
            continue
        store["centroids"][key] = {"lat": got[0], "lng": got[1], "name": name,
                                   "state": st, "osm": got[2], "matched": got[3]}
        _LGA[key] = (got[0], got[1])
        added += 1
    if added:
        LGA_FILE.parent.mkdir(parents=True, exist_ok=True)
        LGA_FILE.write_text(json.dumps(store, ensure_ascii=False, indent=1),
                            encoding="utf-8")
        print("  %d resolved, %d refused; %s now holds %d councils"
              % (added, refused, LGA_FILE.name, len(store["centroids"])))
    if refused:
        print("  %d council area(s) unresolved; those sites will be DROPPED, "
              "not placed at a coarser point" % refused)


_LGA = {}


def _load_lga():
    """Optional: {normalised council name: [lat, lng]}, built from the ABS
    boundaries by whatever step produces the file. Absent is the normal case
    and costs a resolution step, not a record."""
    if _LGA or not LGA_FILE.exists():
        return _LGA
    try:
        raw = json.loads(LGA_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        print("  %s exists but could not be read (%s)" % (LGA_FILE.name, str(e)[:50]))
        return _LGA
    for k, v in (raw.get("centroids") or raw).items():
        try:
            if isinstance(v, dict):
                _LGA[_lganorm(k)] = (float(v["lat"]), float(v["lng"]))
            else:
                _LGA[_lganorm(k)] = (float(v[0]), float(v[1]))
        except Exception:
            continue
    print("  council centroid lookup: %d entries" % len(_LGA))
    return _LGA


def _lganorm(name):
    s = (name or "").lower()
    s = re.sub(r"\b(shire|regional|rural|municipal(ity)?|city|council|of|the)\b", " ", s)
    return re.sub(r"[^a-z]", "", s)


def _statecode(s):
    s = re.sub(r"\s+", " ", (s or "").strip().lower()).strip(".")
    return _STATE_ALIAS.get(s, "")


def place(row):
    """(lat, lng, grade, precise) or (None, None, "", False).

    Two grades:
      site - a coordinate OGTR published for this site
      lga  - the point of the council area OGTR named, resolved and checked
             against that council's state

    Nothing coarser. A row whose council will not resolve is dropped.
    """
    la, ln = coords(row)
    if la is not None:
        return la, ln, "site", True
    lga = pick(row, "lga", "council", "shire")
    if lga:
        pt = _load_lga().get(_lganorm(lga))
        if pt:
            return pt[0], pt[1], "lga", False
    return None, None, "", False


def _phase(status):
    """'post' only where the status actually says the trial is over, 'live' only
    where it says the crop is in the ground.

    "licens", "approv" and "issued" were in the live list and are gone. They
    describe a decision about a licence, not the state of a crop - a licence can
    be current for years after the last planting - and the default status this
    file substitutes when the source states none is the string "Licensed field
    trial", which matched "licens". So a row whose status was never published
    was reported as a running trial. The selftest for this asserted the
    behaviour the comment claimed and failed on the behaviour the code had.
    """
    t = (status or "").lower()
    if any(w in t for w in ("complet", "expired", "surrender", "revoked",
                            "finish", "closed", "ceased", "monitor")):
        return "post"
    if any(w in t for w in ("current", "active", "growing", "planted",
                            "in progress", "ongoing")):
        return "live"
    return ""


_DESC_SITE = (
    "WHAT. A licensed GMO crop field trial site%(extra)s. "
    "WHERE IT SITS. Australia's OGTR publishes the location of every current and "
    "post-harvest-monitoring trial site alongside the full risk assessment and the "
    "licence conditions imposed on it. "
    "WHY IT MATTERS. Every other release record on this map sits at a country or "
    "state fallback because the register published no location. This point sits "
    "where the trial is, which settles the question of whether publishing site "
    "locations is possible.")

_DESC_COARSE = (
    "WHAT. A licensed GMO crop field trial site%(extra)s. "
    "WHERE IT SITS. OGTR named the council area this site is in and published "
    "no coordinate on the page this was read from, so this marker sits in that "
    "council area and not at the trial itself. "
    "WHY IT MATTERS. OGTR names the council area of every licensed site, its "
    "area in hectares and the licence it runs under. No other register on this "
    "map states where a release is at all, which is the comparison worth making "
    "even at this resolution.")


def to_record(row):
    la, ln, grade, precise = place(row)
    if la is None:
        return None
    lic = pick(row, "licence", "license", "dir", "permit")
    site = pick(row, "sitenumber", "site_number", "site_no")
    crop = pick(row, "organism", "crop", "species")
    trait = pick(row, "trait", "modification")
    holder = pick(row, "organisation", "holder", "licensee", "company")
    lga = pick(row, "lga", "council", "shire")
    st = _statecode(pick(row, "state", "territory"))
    # "site" LAST in this list: on a table row it holds a row number, and on a
    # JSON payload it may hold a place name. Asked after the columns that
    # certainly hold a place, it can only win when nothing else answered.
    where = lga or STATE_NAME.get(st, "")
    stated = pick(row, "status", "stage")
    status = stated or "Licensed field trial"
    area = pick(row, "area", "hectare", "size")

    extra = "".join([", %s" % trait if trait else "",
                     ", held by %s" % holder if holder else ""])
    desc = (_DESC_SITE if grade == "site" else _DESC_COARSE) % {"extra": extra}

    name = "%s \u2014 %s field trial" % (lic or "OGTR licence", crop or "GM crop")
    if site:
        name += " (site %s)" % site
    if lga:
        name += ", %s" % lga
    return {
        "name": name[:180],
        "source": "ogtr",
        "type": (crop or "Crop") + ", licensed field trial",
        "lat": la, "lng": ln,
        "state": where or "Australia",
        "country": "Australia",
        "licence": lic,
        "site_number": site,
        "lga": lga,
        # precise is TRUE only for a coordinate the source published. The
        # previous version hardcoded True and dropped every row without a
        # coordinate, so the field was consistent by leaving the data out.
        "precise": precise,
        # Round 87: a record with no addr_grade read as coarse, and every
        # hand-placed point went down the clustering path. CHECK THIS VALUE
        # against the `_coarse` test in index.html before the next release -
        # "site"/"lga"/"state" is this file's vocabulary and the map's may
        # differ.
        "addr_grade": grade,
        "impact": 3,
        "company": holder,
        "size": area,
        "status": status,
        # Derived where the status says so, and left EMPTY where it does not,
        # rather than asserting a stage the source never stated.
        "phase": _phase(stated),
        "date": "",
        "url": PAGE,
        "desc": desc,
        "checked": "",
    }


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def _from_page(html, src):
    """Table first, coordinates merged onto it, endpoints only as an upgrade."""
    rows = parse_page_table(html)
    if rows:
        merge_coords(rows, find_inline_coords(html))
        # Only for the rows that still have no coordinate. If OGTR published
        # one, that is the position and a geocoder has nothing to add.
        unplaced = [r for r in rows if coords(r)[0] is None]
        if unplaced:
            resolve_councils(unplaced)
        return rows
    return []


def main():
    if "--diagnose" in sys.argv:
        return diagnose()
    if "--selftest" in sys.argv:
        return selftest()

    _purge_state_grade()

    t_start = time.time()
    BUDGET = 300.0
    if RELAY:
        print("fetching through OGTR_RELAY (%s)" % urllib.parse.urlsplit(RELAY).netloc)

    for i, a in enumerate(sys.argv):
        if a == "--from-file" and i + 1 < len(sys.argv):
            # The right answer, not a workaround, whenever a page has been
            # saved by hand - the same reasoning that fixed the contamination
            # register.
            html = pathlib.Path(sys.argv[i + 1]).read_text(encoding="utf-8", errors="replace")
            rows = _from_page(html, "file")
            if rows:
                _emit(rows, "saved page %s" % sys.argv[i + 1])
            return

    print("checking robots.txt")
    open_paths = permitted_endpoints()
    ok, why = allowed(PAGE)
    print(" ", why)

    rp = _robots()
    if rp is not None and not getattr(rp, "disallow_all", False) and not ok:
        # A stated rule, read off the file. Nothing below is a way around it.
        print("The map path is disallowed by a rule in robots.txt, so this "
              "script stops. Moving the request to another network does not "
              "change what the rule says. The route that needs no permission: "
              "ask OGTR for the site list through the contact form on "
              "%s - it is a dataset they publish anyway, and a copy from the "
              "office is citable and does not break on a redesign." % BASE)
        return

    # 1. Any permitted data path, first, because a real endpoint carries the
    #    coordinates the table does not.
    if LIVE_DEAD and not RELAY:
        print("  not probing the %d permitted endpoints: they are on the host "
              "that is not answering" % len(open_paths))
        open_paths = []
    for url in open_paths:
        if time.time() - t_start > BUDGET * 0.4:
            print("  endpoint probing stopped at 40%% of the budget; the page "
                  "is the better route and it has not been tried yet")
            break
        try:
            body = fetch(url)
        except Exception as e:
            print("  %s: %s" % (url.replace(BASE, ""), str(e)[:80])); continue
        try:
            rows = harvest_rows(body)
        except Exception as e:
            print("  %s: could not be parsed (%s)"
                  % (url.replace(BASE, ""), str(e)[:50])); continue
        if rows:
            print("  %s answered with %d records" % (url.replace(BASE, ""), len(rows)))
            if _emit(rows, "robots-permitted endpoint %s" % url.replace(BASE, "")):
                return None
            # It parsed and nothing usable came out. Keep going: the page may
            # carry what this lacked.
        else:
            print("  %s answered, and held no trial records" % url.replace(BASE, ""))

    if not ok:
        return

    # 2. The page. This is now the main route, not a place to hunt for one.
    html, src = None, ""
    try:
        html = fetch(PAGE, timeout=25, tries=1)
        src = "map page"
    except Exception as e:
        print("  the map page could not be fetched: %s" % str(e)[:90])

    # 3. The archive, when the host will not answer. Same public page, and it
    #    reaches trials that have since dropped off the live list.
    if html is None:
        print("  falling back to the archived copy of the same page")
        html, when = _archived(PAGE)
        src = "archived map page, snapshot %s" % when if html else ""
        if html is None:
            if OUT.exists():
                # NOT a data loss, and the old wording read like one. Nothing
                # is written, so the committed file stands and the map keeps
                # the trials it had. Worth saying, because the next line in the
                # workflow log is the merge picking that file up.
                try:
                    n = len(json.loads(OUT.read_text(encoding="utf-8"))
                            .get("projects", []))
                except Exception:
                    n = 0
                print("  neither the origin nor the archive answered, so "
                      "nothing was written. %s stands with its %d records and "
                      "the merge will use it. Run --diagnose if this repeats."
                      % (OUT.name, n))
            else:
                print("  no live page and no archived copy, and no previous "
                      "%s to fall back on. Run --diagnose: the stage that "
                      "fails names the fix." % OUT.name, file=sys.stderr)
            return

    rows = _from_page(html, src)
    if rows:
        _emit(rows, src)
        return

    # 4. Nothing in the markup. Fall back to the old endpoint hunt, budgeted.
    cands = find_endpoints(html)

    def likely(u):
        u = u.lower()
        return (0 if "geojson" in u else 1 if "/api/" in u or "jsonapi" in u
                else 2 if "views/ajax" in u or "export" in u else 3)

    cands = sorted(set(cands), key=likely)[:8]
    print("  no site table in the markup; %d candidate endpoints" % len(cands))
    tried, rows = [], []
    for u in cands:
        if time.time() - t_start > BUDGET - 20:
            tried.append("stopped with %.0fs used; the rest were not probed"
                         % (time.time() - t_start))
            break
        if not allowed(u)[0]:
            continue
        try:
            got = harvest_rows(fetch(u))
        except Exception as e:
            # NOT a bare continue. Three runs in a row failed and the workflow
            # log carried nothing but "!! ogtr trials failed", because every
            # candidate's error was discarded here. A reason nobody can read is
            # the same as no reason.
            tried.append("%s -> %s" % (u[:70], str(e)[:70]))
            continue
        if got:
            print("  data from %s (%d rows)" % (u[:90], len(got)))
            rows = got
            break

    if not rows:
        for t in tried[:8]:
            print("     %s" % t)
        print("  no site data found in the page or at any endpoint. Open %s in "
              "a browser, read the network tab, and add the URL to ENDPOINTS."
              % PAGE, file=sys.stderr)
        return
    _emit(rows, "page-referenced endpoint")


def _purge_state_grade():
    """Remove a previously committed file that still holds state-point records.

    Self-limiting: place() can no longer produce a "state" grade, so a file
    containing one is necessarily a leftover from before that rule changed.
    Deleting it here rather than by hand means the change takes effect on the
    next scheduled run with nothing to remember.

    If this run then fails to reach the page, the merge finds no OGTR file and
    the map shows no trials. That is the intended outcome: the point of the
    rule is that a marker in the middle of Western Australia is worse than no
    marker.
    """
    if not OUT.exists():
        return
    try:
        old = json.loads(OUT.read_text(encoding="utf-8")).get("projects", [])
    except Exception:
        return
    stale = [r for r in old if r.get("addr_grade") == "state"]
    if not stale:
        return
    OUT.unlink()
    print("  removed %s: %d of its %d records sat on state reference points, "
          "which this script no longer produces. Rebuilding from scratch."
          % (OUT.name, len(stale), len(old)))


def _emit(rows, src):
    """The single writer."""
    out = [r for r in (to_record(x) for x in rows) if r]
    lost = [(x.get("licence") or "?", x.get("lga") or x.get("state") or "?")
            for x in rows if to_record(x) is None]
    grades = {}
    for r in out:
        grades[r["addr_grade"]] = grades.get(r["addr_grade"], 0) + 1
    print("  usable site records: %d of %d rows (from %s)" % (len(out), len(rows), src))
    print("  placement: %s" % (", ".join("%s %d" % (k, v)
                                         for k, v in sorted(grades.items())) or "none"))
    for lic, where in lost[:12]:
        print("     dropped %-10s no coordinate and no resolved council (%s)"
              % (lic, where[:48]))
    if len(lost) > 12:
        print("     ... and %d more" % (len(lost) - 12))
    if not out:
        print("  every row was dropped, so this route gave nothing usable. "
              "Nothing written: an empty file reaches the map as 'OGTR "
              "licenses no trials', which is the opposite of true.",
              file=sys.stderr)
        return False
    if "--dry-run" in sys.argv:
        print(json.dumps(out[0], ensure_ascii=False, indent=1)[:900])
        print("\ndry run \u2014 nothing written")
        return True
    note = ("OGTR licensed crop field trial sites, read from the site list the "
            "regulator publishes on its crop field trial map page. `precise` is "
            "true only where OGTR published a coordinate for the site; "
            "otherwise the marker sits at the council area or state it named, "
            "and `addr_grade` says which.")
    if src.startswith("archived"):
        note += (" READ FROM AN ARCHIVED COPY of that page - the live host did "
                 "not answer this run, so this reflects the list as at the "
                 "snapshot date in `source`, not today.")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"note": note, "source": src, "projects": out},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nwrote %s (%d records)" % (OUT.name, len(out)))
    return True


# ---------------------------------------------------------------------------
# selftest - no network
# ---------------------------------------------------------------------------

_FIXTURE = """<html><body>
<table><tr><th>Related</th><th>Links</th></tr><tr><td>a</td><td>b</td></tr></table>
<table>
<thead><tr><th>Licence number</th><th>Site number</th><th>Organisation</th>
<th>Parent organism</th><th>Modified trait</th><th>Local government area</th>
<th>State</th><th>Area (ha)</th><th>Crop status</th></tr></thead>
<tbody>
<tr><td>DIR 209</td><td>1</td><td>The University of Queensland</td>
<td><p>Sorghum</p></td><td><p>Asexual seed
production</p></td><td>Lockyer Valley Regional Council</td><td>QLD</td>
<td>1</td><td>Current</td></tr>
<tr><td>DIR 205</td><td>2</td><td>CSIRO</td><td><p>Canola</p></td>
<td><p>Abiotic stress tolerance</p></td><td>Hilltops Council</td><td>NSW</td>
<td>0.063</td><td>Post-harvest monitoring</td></tr>
<tr><td>DIR 999</td><td>1</td><td>Nowhere Ltd</td><td><p>Wheat</p></td>
<td><p>None</p></td><td></td><td>Atlantis</td><td>1</td><td>Current</td></tr>
</tbody></table>
<script>
var markers = [{"licence":"DIR 209","sitenumber":"1","lat":-27.55,"lng":152.33},
               {"licence":"DIR 205","sitenumber":"2","lat":-34.22,"lng":148.29}];
var centre = {"lat":0.0,"lng":0.0};
</script></body></html>"""

_BANNED = ("escape", "escapee", "stray", "self-sown", "loss of containment",
           "contaminat", "unauthorised presence")


def _errof(fn):
    try:
        fn()
    except Exception as e:
        return str(e)
    return ""


def selftest():
    fails = []

    def ck(label, cond, got=""):
        print("  %-56s %s%s" % (label, "ok" if cond else "FAIL",
                                "" if cond else "  <- %s" % got))
        if not cond:
            fails.append(label)

    print("table parsing")
    rows = parse_page_table(_FIXTURE)
    ck("layout table ignored, site table chosen by header", len(rows) == 3, len(rows))
    ck("cell text joined across nested elements",
       rows[0].get("trait") == "Asexual seed production", rows[0].get("trait"))
    ck("site number kept under `sitenumber`, not `site`",
       rows[0].get("sitenumber") == "1" and "site" not in rows[0])

    print("\ncoordinates from markup")
    cm = find_inline_coords(_FIXTURE)
    ck("two site pairs found, map centre at 0,0 rejected", len(cm) == 2, len(cm))
    merge_coords(rows, cm)
    ck("coordinates merged onto the right rows",
       rows[0].get("_lat") == -27.55 and rows[1].get("_lat") == -34.22)

    print("\nplacement")
    recs = [r for r in (to_record(x) for x in rows) if r]
    ck("unplaceable state dropped, not guessed", len(recs) == 2, len(recs))
    ck("published coordinate -> grade site, precise true",
       recs[0]["addr_grade"] == "site" and recs[0]["precise"] is True)
    nocoord = [dict(r) for r in rows[:1]]
    nocoord[0].pop("_lat"); nocoord[0].pop("_lng")
    _LGA.clear()
    ck("no coordinate and no resolved council -> DROPPED, not placed",
       to_record(nocoord[0]) is None)
    _LGA["lockyervalley"] = (-27.55, 152.33)
    r2 = to_record(nocoord[0])
    ck("resolved council -> lga grade, precise false",
       r2["addr_grade"] == "lga" and r2["precise"] is False
       and (r2["lat"], r2["lng"]) == (-27.55, 152.33))
    ck("council-grade record names the council", "Lockyer Valley" in r2["name"])
    ck("coarse record does not claim to sit at the trial",
       "sits where the trial is" not in r2["desc"])
    ck("precise record does claim it",
       "sits where the trial is" in recs[0]["desc"])
    ck("no state-level fallback table is defined",
       not [g for g in globals() if g.startswith("STATE_") and g != "STATE_BOX"
            and g != "STATE_NAME"])
    _LGA.clear()

    print("\npick() traps")
    ck("`translation` does not answer a latitude request",
       pick({"revision_translation_affected": True}, "lat") == "")
    ck("`website` does not answer a site request",
       pick({"website": "x", "sitenumber": "7"}, "sitenumber") == "7")

    print("\nstatus column")
    ck("\"Crop status\" read as status, not as a second organism",
       rows[0].get("status") == "Current" and rows[0].get("organism") == "Sorghum",
       (rows[0].get("status"), rows[0].get("organism")))
    ck("status carried through to the record",
       recs[1]["status"] == "Post-harvest monitoring" and recs[1]["phase"] == "post",
       (recs[1]["status"], recs[1]["phase"]))

    print("\nphase and wording")
    ck("'Post-harvest monitoring' -> post", _phase("Post-harvest monitoring") == "post")
    ck("'Current' -> live", _phase("Current") == "live")
    ck("unstated status -> empty, not asserted", _phase("Licensed field trial") == "")
    _LGA["mingenew"] = (-29.19, 115.44)
    ck("a record with no published status asserts no phase",
       to_record({"licence": "DIR 1", "lga": "Shire of Mingenew",
                  "state": "WA"})["phase"] == "")
    _LGA.clear()
    blob = json.dumps(recs + [r2]).lower()
    bad = [w for w in _BANNED if w in blob]
    ck("no banned wording in any record", not bad, bad)

    print("\nrobots handling")
    rp = RobotFileParser()
    rp.parse(["User-agent: *", "Disallow: /views/ajax", "Disallow: /admin/"])
    ck("a rule on /views/ajax does not close the map page",
       rp.can_fetch(UA, PAGE) and not rp.can_fetch(UA, BASE + "/views/ajax"))
    rp2 = RobotFileParser()
    rp2.parse(["User-agent: *", "Disallow: /what-weve-approved/"])
    ck("a rule on the map path does close it", not rp2.can_fetch(UA, PAGE))

    print("\ncircuit breaker")
    LIVE_DEAD[:] = []
    _dead("connected, no HTTP response")
    ck("a second live request is skipped, not retried",
       "skipped" in _errof(lambda: fetch(PAGE, timeout=1)))
    ck("the archive is a different host and is NOT skipped",
       "skipped" not in _errof(lambda: fetch(WB_AVAIL % "x", timeout=1)))
    ck("breaker is set once and names the stage", LIVE_DEAD == ["connected, no HTTP response"])
    LIVE_DEAD[:] = []

    print("\ncouncil validation")
    box = STATE_BOX["QLD"]
    ck("QLD box rejects a NSW point", not (box[0] <= -33.8 <= box[1]))
    ck("QLD box accepts the Lockyer Valley point",
       box[0] <= -27.55 <= box[1] and box[2] <= 152.33 <= box[3])
    ck("every state OGTR can name has a box to check against",
       set(STATE_BOX) == set(STATE_NAME))
    ck("a council resolved into the wrong state would be refused",
       not (STATE_BOX["WA"][2] <= 152.33 <= STATE_BOX["WA"][3]))

    print("\nrelay")
    global RELAY
    RELAY, keep = "https://relay.example.com/f", RELAY
    ck("relay wraps the absolute URL", _relay(PAGE).endswith(urllib.parse.quote(PAGE, safe="")))
    RELAY = ""
    ck("no relay leaves the URL untouched", _relay(PAGE) == PAGE)
    RELAY = keep

    print("\n%s" % ("all checks pass" if not fails
                    else "%d FAILED: %s" % (len(fails), "; ".join(fails))))
    return 1 if fails else 0


if __name__ == "__main__":
    # `sys.exit(main() or 0)` exited 1 ON SUCCESS: main() returned _emit()'s
    # True, bool is a subclass of int, and True exits 1. Inside `bash -e` in
    # releases.yml that aborts the step and every harvester after it - the
    # documented cfia_approvals.py fault, arriving through a different door.
    # Only --selftest is allowed to set a code, and only when a check failed.
    rc = main()
    sys.exit(rc if type(rc) is int else 0)
