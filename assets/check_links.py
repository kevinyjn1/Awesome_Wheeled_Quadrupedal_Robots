#!/usr/bin/env python3
"""Check that every http(s) link in a markdown file resolves.

Usage:  python3 assets/check_links.py README.md
Exit code 1 if any link fails. Writes link_report.txt next to the file.

Only the standard library is used. Some publishers (IEEE, Springer, YouTube)
block bots or rate-limit; a 403/429 there is reported as a warning, not a
failure. Shields.io badge images are skipped.
"""
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

URL_RE = re.compile(r"https?://[^\s)\]\"'>]+")
SKIP_SUBSTR = ("img.shields.io", "cdn.rawgit.com")
SOFT_CODES = {401, 403, 405, 429, 503}
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
}


def fetch(url: str) -> tuple[str, int | str]:
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, headers=HEADERS, method=method)
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return url, r.status
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code in (403, 405, 404):
                continue  # retry with GET
            return url, e.code
        except Exception as e:  # noqa: BLE001
            if method == "HEAD":
                continue
            return url, f"ERR {type(e).__name__}"
    return url, "ERR"


def main() -> None:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "README.md")
    text = path.read_text(encoding="utf-8")
    urls = sorted({u.rstrip(".,;") for u in URL_RE.findall(text) if not any(s in u for s in SKIP_SUBSTR)})
    print(f"Checking {len(urls)} unique links ...")
    bad, soft = [], []
    with ThreadPoolExecutor(max_workers=16) as ex:
        for url, status in ex.map(fetch, urls):
            if status == 200 or (isinstance(status, int) and 300 <= status < 400):
                continue
            if status in SOFT_CODES:
                soft.append((url, status))
            else:
                bad.append((url, status))
    report = path.with_name("link_report.txt")
    with report.open("w", encoding="utf-8") as f:
        f.write(f"Checked {len(urls)} links\n\nFAILED ({len(bad)}):\n")
        f.writelines(f"  {s}  {u}\n" for u, s in bad)
        f.write(f"\nWARN / bot-blocked ({len(soft)}):\n")
        f.writelines(f"  {s}  {u}\n" for u, s in soft)
    print(f"OK: {len(urls) - len(bad) - len(soft)}  WARN: {len(soft)}  FAILED: {len(bad)}  -> {report}")
    for u, s in bad:
        print(f"  FAILED {s}: {u}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
