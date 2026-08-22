#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply a table of row edits to harvest/resources.json.

WHY THIS EXISTS. Sixteen rounds of link work averaged 1.8 rows per round, and a
new ~75-line script was written each time to apply them. The script was never
the interesting part: every one did the same four things and re-implemented the
same three checks. This does them once, so a round can spend its budget on
research instead.

A round now writes a TABLE and nothing else:

    EDITS = [
      {"country": "Kenya", "row": "KEPHIS laboratories",
       "expect": "regional detection",        # must appear in the CURRENT text
       "rename": "KEPHIS - Plant Health Inspectorate",
       "desc":   "...",
       "url":    "https://kephis.go.ke/"},
    ]
    python3 harvest/apply_rows.py edits.json

THE CHECKS, which are the reason this is a script and not a text editor:

  - `expect` is REQUIRED whenever `desc` is given. It is a fragment that must
    already appear in the row's description. If it does not, nothing is written
    and the run fails loudly. This exists because I overwrote a country-specific
    fact - "the Dominican Republic is not a CARICOM member" - with better-sourced
    but wrongly-framed text, and only caught it by chance. A rewrite planned
    against a description I have read must refuse to run against a different one.

  - A row is matched on (COUNTRY, NAME) together, never on name alone. Several
    real bodies share a name across countries: Agence Nationale de Biosecurite
    exists in both Burkina Faso and Cote d'Ivoire, Service de la Protection des
    Vegetaux in four countries, Ministry of Climate Change and Environment in
    both the Maldives and the UAE. A name-only match would have broken four
    correct rows to fix one.

  - `url` never overwrites a link that is already there.

  - Every edit must match exactly one row. Zero matches or several are both
    reported and abort the whole run before anything is written.

  - Nothing is written until every edit has been checked. A partial application
    is worse than none, because the report would then describe a file that does
    not exist.

    python3 harvest/apply_rows.py --selftest
"""
import json, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
RESOURCES = HERE / "resources.json"


def find(doc, country, name):
    cats = doc.get("countries", {}).get(country)
    if cats is None:
        return None, "no such country: %r" % country
    hits = [r for rows in cats.values() if isinstance(rows, list)
            for r in rows if r.get("n") == name]
    if len(hits) == 1:
        return hits[0], None
    return None, ("no row named %r in %s" % (name, country) if not hits
                  else "%d rows named %r in %s" % (len(hits), name, country))


def check(doc, edits):
    """Every problem found, not just the first: fix them in one pass."""
    problems, targets = [], []
    for i, e in enumerate(edits):
        row, err = find(doc, e.get("country", ""), e.get("row", ""))
        if err:
            problems.append("edit %d: %s" % (i, err)); continue
        if e.get("desc") and not e.get("expect"):
            problems.append("edit %d: desc given with no expect fragment" % i); continue
        if e.get("expect") and e["expect"] not in (row.get("d") or ""):
            problems.append("edit %d (%s / %s): expect %r is not in the current "
                            "description, which reads %r"
                            % (i, e["country"], e["row"], e["expect"],
                               (row.get("d") or "")[:90]))
            continue
        targets.append((e, row))
    return targets, problems


def apply(targets):
    applied = {"renamed": 0, "redescribed": 0, "linked": 0, "link_kept": 0}
    for e, row in targets:
        if e.get("rename"):
            row["n"] = e["rename"]; applied["renamed"] += 1
        if e.get("desc") and row.get("d") != e["desc"]:
            row["d"] = e["desc"]; applied["redescribed"] += 1
        if e.get("url"):
            if row.get("u"):
                applied["link_kept"] += 1
            else:
                row["u"] = e["url"]; applied["linked"] += 1
    return applied


def verify(path, edits):
    """Read the file back off disk and confirm each edit landed on its row."""
    doc = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    bad = []
    for e in edits:
        name = e.get("rename") or e.get("row")
        row, err = find(doc, e["country"], name)
        if err:
            bad.append("%s / %s: %s" % (e["country"], name, err)); continue
        if e.get("url") and not row.get("u"):
            bad.append("%s / %s: no link on the row" % (e["country"], name))
        if e.get("desc") and row.get("d") != e["desc"]:
            bad.append("%s / %s: description not the one written" % (e["country"], name))
    return bad


def totals(path):
    doc = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    rows = [r for cats in doc["countries"].values() for rr in cats.values()
            if isinstance(rr, list) for r in rr]
    return (len(rows), len(doc["countries"]),
            sum(1 for r in rows if r.get("u")), sum(1 for r in rows if not r.get("u")))


def run(edits, path=RESOURCES):
    path = pathlib.Path(path)
    doc = json.loads(path.read_text(encoding="utf-8"))
    targets, problems = check(doc, edits)
    if problems:
        print("REFUSED - nothing written:")
        for p in problems:
            print("   " + p)
        return 1
    applied = apply(targets)
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    bad = verify(path, edits)
    for e, _ in targets:
        print("   %-24s %s" % (e["country"][:24], (e.get("rename") or e["row"])[:60]))
    print("\n   renamed %(renamed)d, redescribed %(redescribed)d, linked %(linked)d, "
          "existing links kept %(link_kept)d" % applied)
    if bad:
        print("   VERIFY FAILED:")
        for b in bad:
            print("      " + b)
    print("   entries %d, countries %d, linked %d, unlinked %d" % totals(path))
    return 1 if bad else 0


def selftest():
    ok = True

    def t(label, got, want):
        nonlocal ok
        good = got == want
        ok = ok and good
        print("  %-56s %s" % (label, "pass" if good else "FAIL got %r" % (got,)))

    doc = {"countries": {
        "Alpha": {"complain": [{"n": "Food Agency", "lens": "COMPLAINT", "d": "Inspects imports."}],
                  "decides": [{"n": "Shared Name", "lens": "REGULATOR", "d": "x",
                               "u": "https://typed.example/"}]},
        "Beta": {"decides": [{"n": "Shared Name", "lens": "REGULATOR", "d": "y"}]},
        "Gamma": {"test": [{"n": "Dup", "d": "a"}, {"n": "Dup", "d": "b"}]},
    }}
    e_ok = [{"country": "Alpha", "row": "Food Agency", "expect": "Inspects imports",
             "rename": "Food Agency of Alpha", "desc": "New text.", "url": "https://a.example/"}]
    targets, problems = check(doc, e_ok)
    t("a clean edit passes the check", problems, [])
    apply(targets)
    t("renamed", doc["countries"]["Alpha"]["complain"][0]["n"], "Food Agency of Alpha")
    t("linked", doc["countries"]["Alpha"]["complain"][0]["u"], "https://a.example/")

    _, p = check(doc, [{"country": "Alpha", "row": "Food Agency of Alpha",
                        "expect": "text that is not there", "desc": "z"}])
    t("a wrong expect fragment is refused", len(p), 1)
    t("and the refusal quotes the real text", "New text." in p[0], True)

    _, p = check(doc, [{"country": "Alpha", "row": "Food Agency of Alpha", "desc": "z"}])
    t("desc with no expect is refused", len(p), 1)

    _, p = check(doc, [{"country": "Gamma", "row": "Dup", "expect": "a", "desc": "z"}])
    t("an ambiguous row name is refused", "2 rows named" in p[0], True)

    _, p = check(doc, [{"country": "Nowhere", "row": "X"}])
    t("an unknown country is refused", "no such country" in p[0], True)

    # The shared-name trap: editing Beta must not touch Alpha.
    tg, p = check(doc, [{"country": "Beta", "row": "Shared Name",
                         "expect": "y", "desc": "beta only", "url": "https://b.example/"}])
    t("shared name resolves per country", p, [])
    apply(tg)
    t("only Beta changed", doc["countries"]["Beta"]["decides"][0]["d"], "beta only")
    t("Alpha's same-named row untouched", doc["countries"]["Alpha"]["decides"][0]["d"], "x")
    t("and its existing link was not overwritten",
      doc["countries"]["Alpha"]["decides"][0]["u"], "https://typed.example/")

    # One bad edit in a batch must stop the whole batch.
    _, p = check(doc, [{"country": "Beta", "row": "Shared Name", "expect": "beta only",
                        "desc": "fine"},
                       {"country": "Nowhere", "row": "X"}])
    t("one bad edit reports without applying the good one", len(p), 1)

    print("\n%s" % ("all pass" if ok else "FAILURES ABOVE"))
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not args:
        sys.exit("usage: apply_rows.py edits.json [resources.json]")
    edits = json.loads(pathlib.Path(args[0]).read_text(encoding="utf-8"))
    sys.exit(run(edits, args[1] if len(args) > 1 else RESOURCES))
