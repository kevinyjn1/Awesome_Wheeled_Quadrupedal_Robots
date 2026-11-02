#!/usr/bin/env python3
"""Alphabetically sort bullet lists in README.md.

Sorts every contiguous run of top-level ``- `` bullets (a run ends at a blank
line, a heading, an HTML tag, or any non-bullet line). Nested sub-bullets stay
attached to their parent. Sorting is case-insensitive and ignores markdown
link / badge syntax, so ``- [Foo](url)`` and ``- [![](badge)](url)`` sort by
their visible text.

Usage:  python3 assets/ordering.py [README.md]
"""
import re
import sys
from pathlib import Path

BADGE_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)")          # ![](...)
LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")           # [text](url)
HTML_RE = re.compile(r"<[^>]+>")
BADGE_TEXT_RE = re.compile(r"img\.shields\.io/badge/([^?)]+)")


def sort_key(block: list[str]) -> str:
    first = block[0]
    # Repo badges: use "OWNER-REPO" text from the shields URL.
    m = BADGE_TEXT_RE.search(first)
    if m:
        return m.group(1).replace("--", "-").lower()
    text = BADGE_RE.sub("", first)
    text = LINK_RE.sub(r"\1", text)
    text = HTML_RE.sub("", text)
    text = text.lstrip("- ").strip().lower()
    return text


def sort_runs(lines: list[str]) -> list[str]:
    out: list[str] = []
    i = 0
    n = len(lines)
    in_code = False
    while i < n:
        line = lines[i]
        if line.strip().startswith("```"):
            in_code = not in_code
        if in_code or not line.startswith("- "):
            out.append(line)
            i += 1
            continue
        # Collect a run of top-level bullets with their nested children.
        blocks: list[list[str]] = []
        while i < n and lines[i].startswith("- "):
            block = [lines[i]]
            i += 1
            while i < n and (lines[i].startswith("  ") or lines[i].startswith("\t")) and lines[i].strip():
                block.append(lines[i])
                i += 1
            blocks.append(block)
        blocks.sort(key=sort_key)
        for b in blocks:
            out.extend(b)
    return out


def main() -> None:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "README.md")
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    sorted_lines = sort_runs(lines)
    if sorted_lines != lines:
        path.write_text("\n".join(sorted_lines), encoding="utf-8")
        print(f"Sorted bullet lists in {path}")
    else:
        print("Already sorted.")


if __name__ == "__main__":
    main()
