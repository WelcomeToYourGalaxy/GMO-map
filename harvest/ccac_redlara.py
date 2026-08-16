#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Two accreditation bodies: CCAC in Canada, REDLARA across Latin America.

Both are voluntary accreditation rather than state registers, and both are the
only facility-level source for their region, so they are kept together and
labelled the same way: an organisation appears because it applied and passed.
Absence means not accredited. It never means no work.

CCAC certifies Canadian institutions that use animals in science - 178 of them,
including federal departments broken out site by site. Names only, no addresses.

REDLARA accredits assisted-reproduction centres in 16 Latin American countries -
209 of them, and unlike the registry paper (which lists names and nothing else)
each centre has a page carrying a street address, city, phone and website. That
makes Latin America the one region outside the US, UK and China where this map
can put a fertility clinic at its own door.

    python3 harvest/ccac_redlara.py
    python3 harvest/ccac_redlara.py --dry-run
    python3 harvest/ccac_redlara.py --ccac-file page.htm --redlara-file list.htm
"""

import json, re, sys, time, pathlib
from urllib.request import Request, urlopen
from urllib.parse import quote, urljoin

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "ccac_redlara.json"
CACHE = HERE / "_geocache.json"

CCAC = "https://ccac.ca/en/certification/certified-institutions.html"
# The list is reached from quem_somos.asp; the guessed filename 404s. Both
# are tried, newest guess first, because a site that renames one page
# usually keeps the other.
# acreditacao.asp is the page that actually holds the list; every earlier guess
# 404'd or returned the wrong page, and the run reported "0 accredited centres"
# without saying it had never found the list at all.
REDLARA_LIST = "https://redlara.com/acreditacao.asp"
REDLARA_ALT = ["https://redlara.com/quem_somos.asp",
               "https://redlara.com/centros.asp"]

# The detail pages are numbered, not linked from one index in a form this
# harvester can rely on. If the list page ever moves again, the centres are
# still reachable by walking the numbers - centro.asp?USIM5=1 upward - and a
# gap in the numbering is a centre that has left the network, not a failure.
REDLARA_CENTRE = "https://redlara.com/centro.asp?USIM5=%d"
REDLARA_MAX_ID = 400
PHOTON = "https://photon.komoot.io/api/?limit=1&q="

COUNTRY_PT = {
    "Argentina": (-38.42, -63.62), "Bolivia": (-16.29, -63.59),
    "Brasil": (-14.24, -51.93), "Chile": (-35.68, -71.54),
    "Colombia": (4.57, -74.30), "Costa Rica": (9.75, -83.75),
    "Ecuador": (-1.83, -78.18), "El Salvador": (13.79, -88.90),
    "Guatemala": (15.78, -90.23), "M\u00e9xico": (23.63, -102.55),
    "Nicaragua": (12.87, -85.21), "Panama": (8.54, -80.78),
    "Paraguay": (-23.44, -58.44), "Peru": (-9.19, -75.02),
    "Republica Dominicana": (18.74, -70.16), "Uruguay": (-32.52, -55.77),
    "Venezuela": (6.42, -66.59),
}
CANADA = (56.13, -106.35)


def get(url, tries=3, encoding=None):
    for i in range(tries):
        try:
            r = Request(url, headers={"User-Agent":
                                      "GMO-map/1.0 (public research map)"})
            raw = urlopen(r, timeout=90).read()
            if encoding:
                return raw.decode(encoding, "replace")
            return raw.decode("utf-8", "replace")
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(3 * (i + 1))


def _text(s):
    import html as _h
    return re.sub(r"\s+", " ", _h.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


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


# ---------------------------------------------------------------------------
# CCAC
# ---------------------------------------------------------------------------
def parse_ccac(html):
    """Each institution is a <p> name followed by a <ul class="cert-status">.

    Federal departments hold several research centres inside one block, and
    those sub-sites are kept: Agriculture and Agri-Food Canada is five separate
    places doing the work, not one entry in Ottawa.
    """
    i = html.find('<div id="cert-inst">')
    body = html[i:] if i >= 0 else html
    # Two shapes, not one. A single-site institution is <p>name</p> followed by
    # <ul class="cert-status">. A parent with several sites uses
    # <ul class="cert-list">, each <li> naming a site and holding its own nested
    # cert-status. Reading only the first shape lost every federal research
    # centre - the five Agriculture and Agri-Food Canada sites arrived as one
    # dot on the department.
    out = []
    # Two shapes, not one. A single-site institution is <p>name</p> followed by
    # <ul class="cert-status">. A parent with several sites uses
    # <ul class="cert-list">, each <li> naming a site and holding its own nested
    # cert-status. Reading only the first shape lost every federal research
    # centre - the five Agriculture and Agri-Food Canada sites arrived as one
    # dot on the department.
    #
    # The name capture is [^<]* rather than .*?: a lazy dot still matches across
    # earlier blocks when the anchor it is looking for is further down the page,
    # and it produced sites attached to whichever institution happened to
    # precede them.
    seen = set()
    for m in re.finditer(r"<p>([^<]+)</p>\s*<ul class=\"cert-list\">", body):
        nm = _text(m.group(1))
        nxt = body.find("<p>", m.end())
        block = body[m.end():nxt if nxt > 0 else len(body)]
        for li in re.finditer(r"<li>(.*?)<ul class=\"cert-status\">(.*?)</ul>",
                              block, re.S):
            site = _text(re.split(r"<ul", li.group(1))[0])
            st = _text(li.group(2))
            if not site:
                continue
            out.append({"name": site, "parent": nm, "status": st})
            seen.add(site.lower())
        seen.add(nm.lower())

    for name, ul in re.findall(r"<p>([^<]+)</p>\s*<ul class=\"cert-status\">(.*?)</ul>",
                               body, re.S):
        nm = _text(name)
        if not nm or nm.lower() in seen:
            continue
        seen.add(nm.lower())
        out.append({"name": nm, "parent": "", "status": _text(ul)})
    return out


# ---------------------------------------------------------------------------
# REDLARA
# ---------------------------------------------------------------------------
def parse_redlara_list(html):
    out = []
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.S):
        cells = [_text(c) for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", row, re.S)]
        link = re.findall(r'href="([^"]*centro\.asp[^"]*)"', row)
        if len(cells) >= 2 and link and cells[0] and cells[1]:
            out.append({"country": cells[0], "name": cells[1],
                        "url": urljoin(REDLARA_LIST, link[0])})
    return out


def _centre_name(html):
    """The centre's own name.

    Walking backwards from Localiza\u00e7\u00e3o looked reasonable and returned
    the laboratory director - the page puts Diretores/Administradores between
    the name and the address, so the nearest line above is a person. The <title>
    holds the name followed by country and city, which is unambiguous, so that
    is used and the trailing place words are cut off.
    """
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    if not m:
        return ""
    t = _text(m.group(1))
    tail = re.search(r"\s+(Argentina|Bolivia|Brasil|Brazil|Chile|Colombia|Costa Rica|"
                     r"Ecuador|El Salvador|Guatemala|M\u00e9xico|Mexico|Nicaragua|Panama|"
                     r"Paraguay|Peru|Republica Dominicana|Uruguay|Venezuela)\b", t)
    return (t[:tail.start()] if tail else t).strip()


def parse_redlara_centre(html):
    """The detail page prints a Localiza\u00e7\u00e3o block: street, then
    'Country - City', then contact lines."""
    body = re.sub(r"<script.*?</script>", " ", html, flags=re.S)
    body = re.sub(r"<style.*?</style>", " ", body, flags=re.S)
    lines = [_text(x) for x in re.split(r"<[^>]+>", body)]
    lines = [x for x in lines if x and len(x) > 1]
    out = {"street": "", "city": "", "country": "", "email": "",
           "phone": "", "website": "", "accredited": False}
    # Every page carries REDLARA's own contact details in its header, so
    # scanning the whole page for the first email and phone gave every one of
    # the 209 centres the same address in Mexico. The centre's own block starts
    # at Localiza\u00e7\u00e3o, and nothing before it is read.
    start = next((i for i, x in enumerate(lines) if x.startswith("Localiza")), None)
    if start is None:
        return out
    for x in lines[max(0, start - 6):start]:
        if x.lower().startswith("acreditado"):
            out["accredited"] = True
    if start + 2 < len(lines):
        out["street"] = lines[start + 1]
        loc = lines[start + 2]
        if " - " in loc:
            out["country"], out["city"] = [p.strip() for p in loc.split(" - ", 1)]
        else:
            out["city"] = loc
    for i in range(start, min(start + 14, len(lines))):
        x = lines[i]
        if x.startswith("Contato"):
            for j in range(i + 1, min(i + 5, len(lines))):
                v = lines[j]
                if v.startswith("Website"):
                    break
                if "@" in v and not out["email"]:
                    out["email"] = v
                elif re.match(r"^[\(\+\d][\d\s\-\(\)\.]{6,}$", v) and not out["phone"]:
                    out["phone"] = v
        if x.startswith("Website") and i + 1 < len(lines) and not out["website"]:
            out["website"] = lines[i + 1]
    return out


def main():
    dry = "--dry-run" in sys.argv
    def arg(flag):
        return (sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else None)

    cache = load_cache()
    out = []

    # ---- CCAC --------------------------------------------------------------
    f = arg("--ccac-file")
    try:
        html = (pathlib.Path(f).read_text(encoding="utf-8", errors="replace")
                if f else get(CCAC))
        recs = parse_ccac(html)
        print("  CCAC: %d certified institutions" % len(recs))
        for r in recs:
            place = r["name"] + ", Canada"
            latlng = geocode(place, cache) or CANADA
            bits = ["An institution certified by the Canadian Council on Animal "
                    "Care for its use of animals in science."]
            if r["parent"]:
                bits.append("A site of %s." % r["parent"])
            if r["status"]:
                bits.append(r["status"] + ".")
            bits.append("CCAC certification is a condition of federal research "
                        "funding rather than a licence, so an institution outside "
                        "it is not necessarily outside the work \u2014 it may "
                        "simply not take federal money.")
            bits.append("The CCAC publishes names and certificate status and no "
                        "addresses, so this point marks the institution rather "
                        "than the building where animals are held.")
            out.append({
                "name": r["name"][:150], "source": "industry:animals",
                "type": "CCAC certified institution",
                "lat": latlng[0], "lng": latlng[1],
                "state": "Canada", "precise": False,
                "addr_grade": "administrative",
                "impact": 2, "company": r["parent"], "size": "",
                "status": r["status"][:80] or "CCAC certified",
                "phase": "post", "date": "", "otype": "institute",
                "tags": ["animals:services"], "species": ["lab_animals"],
                "url": CCAC, "desc": " ".join(bits), "checked": "",
            })
            if len(out) % 40 == 0:
                time.sleep(0.6)
    except Exception as e:
        print("  CCAC failed (%s)" % e, file=sys.stderr)

    # ---- REDLARA -----------------------------------------------------------
    f = arg("--redlara-file")
    try:
        # The site is windows-1252, not UTF-8. Decoded as UTF-8 it throws;
        # decoded as UTF-8 with errors ignored it silently turns Ginecolog\u00eda
        # into mojibake on every Spanish-language centre name.
        centres = []
        if f:
            centres = parse_redlara_list(
                pathlib.Path(f).read_bytes().decode("cp1252", "replace"))
        else:
            for u in [REDLARA_LIST] + REDLARA_ALT:
                try:
                    got = parse_redlara_list(get(u, encoding="cp1252"))
                except Exception as e:
                    print("  %s: %s" % (u.split("/")[-1], e))
                    continue
                if len(got) > 20:
                    print("  centre list found at %s" % u)
                    centres = got
                    break
            if not centres:
                # Walking the ids rather than reporting nothing. A list page
                # that moves should cost us the country labels, not 209 clinics.
                print("  no list page answered; walking centro.asp ids instead")
                for i in range(1, REDLARA_MAX_ID + 1):
                    u = REDLARA_CENTRE % i
                    try:
                        page = get(u, tries=1, encoding="cp1252")
                    except Exception:
                        continue
                    d = parse_redlara_centre(page)
                    if d.get("street") or d.get("city"):
                        centres.append({"country": d.get("country", ""),
                                        "name": _centre_name(page) or ("centre %d" % i),
                                        "url": u, "_page": page})
                    time.sleep(0.4)
                print("  %d centres found by walking ids" % len(centres))
        print("  REDLARA: %d accredited centres" % len(centres))
        exact_n = 0
        for c in centres:
            d = {}
            if c.get("_page"):
                d = parse_redlara_centre(c["_page"])
            else:
                try:
                    page = get(c["url"], tries=2, encoding="cp1252")
                    d = parse_redlara_centre(page)
                    time.sleep(1)
                except Exception:
                    pass
            street, city = d.get("street", ""), d.get("city", "")
            latlng, exact = None, False
            if street and city:
                latlng = geocode("%s, %s, %s" % (street, city, c["country"]), cache)
                exact = latlng is not None
            if latlng is None and city:
                latlng = geocode("%s, %s" % (city, c["country"]), cache)
            if latlng is None:
                latlng = COUNTRY_PT.get(c["country"])
            if latlng is None:
                continue
            exact_n += 1 if exact else 0

            bits = ["A centre accredited by REDLARA, the Latin American Network of "
                    "Assisted Reproduction."]
            if d.get("website"):
                bits.append("Website: %s." % d["website"])
            bits.append("A fertility clinic is where human embryos are made, selected and "
                "stored, and where assisted reproduction happens, like IVF, "
                "ICSI, egg and sperm donation, freezing embryos and eggs for "
                "later.")
            bits.append("REDLARA accreditation is voluntary and its members report "
                        "to a shared registry, which is why Latin America can be "
                        "read at all \u2014 most countries in the region have no "
                        "national register of clinics. What it is not is a "
                        "complete list: a clinic outside REDLARA appears nowhere.")
            if not exact:
                bits.append("No street address resolved, so this point is the city "
                            "or the country rather than the centre.")

            out.append({
                "name": c["name"][:150], "source": "industry:repro",
                "type": "Fertility clinic",
                "lat": latlng[0], "lng": latlng[1],
                "state": ", ".join([x for x in (city, c["country"]) if x]),
                "precise": bool(exact),
                "addr_grade": ("operational" if exact else "centroid"),
                "impact": 2, "company": "", "size": "",
                "status": "REDLARA accredited",
                "phase": "post", "date": "", "otype": "company",
                "tags": ["repro:clinics"], "species": ["human"],
                "url": c["url"], "desc": " ".join(bits), "checked": "",
            })
        print("  REDLARA: %d placed at a street address" % exact_n)
    except Exception as e:
        print("  REDLARA failed (%s)" % e, file=sys.stderr)

    if not out:
        print("Nothing usable. The previous file, if any, is left alone.",
              file=sys.stderr)
        return
    print("  %d records total" % len(out))
    if dry:
        print("dry run \u2014 nothing written")
        return
    CACHE.write_text(json.dumps(cache, indent=0), encoding="utf-8")
    OUT.write_text(json.dumps({
        "generated": time.strftime("%Y-%m-%d"),
        "note": ("CCAC certified institutions (Canada) and REDLARA accredited "
                 "centres (Latin America). Both voluntary accreditation, not "
                 "state registers."),
        "projects": out}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote %s" % OUT.name)


if __name__ == "__main__":
    main()
