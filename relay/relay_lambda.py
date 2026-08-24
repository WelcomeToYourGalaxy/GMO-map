# -*- coding: utf-8 -*-
"""A fetch relay in ap-southeast-2, for OGTR_RELAY.

Only needed if --diagnose shows the host answering some networks and not this
one. It changes where the request leaves from and nothing else: the harvester
still reads robots.txt and still stops on a stated rule, and this file will not
fetch a path that robots.txt disallows either.

# Deploy (AWS Lambda, Sydney) -----------------------------------------------
#   1. Lambda console, region ap-southeast-2 (Sydney), Create function,
#      Python 3.12, name ogtr-relay.
#   2. Paste this file as lambda_function.py. Deploy.
#   3. Configuration -> Function URL -> Create, auth type NONE, then add the
#      shared secret below so the URL is not an open proxy.
#   4. Configuration -> General -> Timeout 60s.
#   5. Set OGTR_SECRET on the function, and in GitHub set the repo secret
#      OGTR_RELAY to  https://<id>.lambda-url.ap-southeast-2.on.aws/?k=<secret>
#
# A weekly cron is a few dozen requests a month against a free-tier allowance
# of a million, so this costs nothing. Oracle Cloud's always-free Sydney VM
# running the same logic behind any web server works identically.
#
# In releases.yml, on the ogtr step only:
#     env:
#       OGTR_RELAY: ${{ secrets.OGTR_RELAY }}
# The harvester reads it if present and goes direct if not, so the step keeps
# working whether or not the secret exists.
"""
import json
import os
import urllib.parse
import urllib.request
from urllib.robotparser import RobotFileParser

ALLOW_HOSTS = {"www.ogtr.gov.au", "ogtr.gov.au"}
UA = "GMO-map-harvest/1.0 (+https://github.com/WelcomeToYourGalaxy/GMO-map)"
SECRET = os.environ.get("OGTR_SECRET", "")
_ROBOTS = {}


def _robots_ok(url):
    """The relay honours robots.txt too.

    Without this the relay is a way around the check the harvester exists to
    make - and it is the component most likely to be reused by something with
    no check of its own.
    """
    parts = urllib.parse.urlsplit(url)
    root = "%s://%s" % (parts.scheme, parts.netloc)
    rp = _ROBOTS.get(root)
    if rp is None:
        rp = RobotFileParser()
        rp.set_url(root + "/robots.txt")
        try:
            body = urllib.request.urlopen(
                urllib.request.Request(root + "/robots.txt",
                                       headers={"User-Agent": UA}),
                timeout=20).read().decode("utf-8", "replace")
            rp.parse(body.splitlines())
        except Exception:
            return None                 # unknown, not permitted
        _ROBOTS[root] = rp
    return rp.can_fetch(UA, url)


def _reply(code, body, ctype="text/plain; charset=utf-8"):
    return {"statusCode": code, "headers": {"content-type": ctype}, "body": body}


def lambda_handler(event, context):
    q = (event.get("queryStringParameters") or {})
    if SECRET and q.get("k") != SECRET:
        return _reply(403, "no")
    url = q.get("url") or ""
    parts = urllib.parse.urlsplit(url)
    if parts.scheme != "https" or parts.hostname not in ALLOW_HOSTS:
        # An allowlist, not a filter. An open relay is a thing other people
        # find and use, and it would be running under this account.
        return _reply(400, "only https to %s" % ", ".join(sorted(ALLOW_HOSTS)))
    ok = _robots_ok(url)
    if ok is not True:
        return _reply(403, "robots.txt %s this path"
                      % ("disallows" if ok is False else "could not be read for"))
    try:
        r = urllib.request.urlopen(
            urllib.request.Request(url, headers={
                "User-Agent": UA,
                "Accept": "text/html,application/json;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-AU,en;q=0.9"}),
            timeout=45)
        body = r.read()
        code = r.getcode()
    except Exception as e:
        # The status and the reason, not a bare 502. The whole point of the
        # relay is to find out what the origin says to a client in its own
        # region, and swallowing that answer defeats it.
        return _reply(502, json.dumps({"error": type(e).__name__,
                                       "detail": str(e)[:200]}),
                      "application/json")
    return {"statusCode": code,
            "headers": {"content-type": r.headers.get("content-type",
                                                      "text/plain")},
            "body": body.decode("utf-8", "replace")}
