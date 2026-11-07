#!/usr/bin/env python3
"""Check that cited URLs exist and, optionally, mention expected terms. Standard library only.

Usage:
  python tools/verify_sources.py URL [URL ...]
  python tools/verify_sources.py --file report.md          # extracts every http(s) URL
  python tools/verify_sources.py URL --expect "rust,memory safety"
Exit code 0 = all URLs reachable (and terms found); 1 = at least one problem.
"""
import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser

URL_RE = re.compile(r"https?://[^\s<>\"')\]]+")
UA = "Mozilla/5.0 (compatible; DebateArenaVerifier/0.1)"


class _Title(HTMLParser):
    def __init__(self):
        super().__init__()
        self._in = False
        self.title = ""

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self._in = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in = False

    def handle_data(self, data):
        if self._in:
            self.title += data


def extract_urls(text):
    seen, out = set(), []
    for u in URL_RE.findall(text):
        u = u.rstrip(".,;:!?")
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def check_url(url, expect=None, timeout=10, max_bytes=300_000):
    res = {"url": url, "ok": False, "status": None, "final_url": None,
           "title": "", "missing_terms": [], "error": None}
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            res["status"] = r.status
            res["final_url"] = r.geturl()
            body = r.read(max_bytes).decode("utf-8", errors="replace")
        p = _Title()
        p.feed(body)
        res["title"] = " ".join(p.title.split())
        res["ok"] = 200 <= res["status"] < 300
        low = body.lower()
        res["missing_terms"] = [t for t in (expect or []) if t.lower() not in low]
    except urllib.error.HTTPError as e:
        res["status"], res["error"] = e.code, f"HTTP {e.code}"
    except Exception as e:  # DNS failure, timeout, TLS, etc.
        res["error"] = f"{type(e).__name__}: {e}"
    if res["missing_terms"]:
        res["ok"] = False
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("urls", nargs="*")
    ap.add_argument("--file", help="text/markdown file to extract URLs from")
    ap.add_argument("--expect", default="", help="comma-separated terms that must appear on every page")
    ap.add_argument("--timeout", type=int, default=10)
    ap.add_argument("--json", action="store_true", help="print JSON instead of a table")
    a = ap.parse_args(argv)

    urls = list(a.urls)
    if a.file:
        with open(a.file, encoding="utf-8") as f:
            urls += extract_urls(f.read())
    urls = list(dict.fromkeys(urls))
    if not urls:
        print("No URLs given.", file=sys.stderr)
        return 2
    terms = [t.strip() for t in a.expect.split(",") if t.strip()]
    results = [check_url(u, terms, a.timeout) for u in urls]

    if a.json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            mark = "OK  " if r["ok"] else "FAIL"
            note = r["error"] or (f"missing terms: {r['missing_terms']}" if r["missing_terms"] else r["title"][:60])
            print(f"{mark} {r['status'] or '---'} {r['url']}  {note}")
        bad = sum(not r["ok"] for r in results)
        print(f"\nChecked {len(results)} | OK {len(results) - bad} | Problems {bad}")
    return 0 if all(r["ok"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
