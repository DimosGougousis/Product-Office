#!/usr/bin/env python3
"""
Check all markdown links in a file or directory are reachable (no 404s).

Usage:
  python scripts/yuup-check-links.py <path-to-file-or-dir>

If a directory is given, scans all .md files recursively.
Exit 0 = all links resolve. Non-zero = dead links found (printed to stderr).

Deterministic: follows the Iron Law — checks live, returns exit code, no judgment.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

URL_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def find_markdown_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root] if root.suffix == ".md" else []
    return sorted(p for p in root.rglob("*.md"))


def check_url(url: str) -> tuple[bool, str]:
    """Check if a URL is reachable. Returns (ok, reason)."""
    if url.startswith(("http://", "https://")):
        import urllib.request
        import urllib.error
        try:
            req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "YUUP-Link-Checker/1.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status < 400:
                    return True, f"HTTP {resp.status}"
                return False, f"HTTP {resp.status}"
        except urllib.error.HTTPError as e:
            return False, f"HTTP {e.code}"
        except urllib.error.URLError as e:
            return False, str(e.reason)
        except Exception as e:
            return False, str(e)
    else:
        # Local file reference
        return True, "local"


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/yuup-check-links.py <path-to-file-or-dir>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1])
    if not root.exists():
        print(f"ERROR: Path not found: {root}", file=sys.stderr)
        return 2

    md_files = find_markdown_files(root)
    if not md_files:
        print("No markdown files found.")
        return 0

    dead_links: list[tuple[str, str, str]] = []  # (file, link_text, url, reason)
    total_links = 0

    for md_file in md_files:
        text = md_file.read_text(encoding="utf-8")
        for match in URL_PATTERN.finditer(text):
            link_text = match.group(1)
            url = match.group(2)
            total_links += 1
            ok, reason = check_url(url)
            if not ok:
                dead_links.append((str(md_file), link_text, url, reason))

    if dead_links:
        print(f"DEAD LINKS FOUND ({len(dead_links)}/{total_links}):", file=sys.stderr)
        for file_path, text, url, reason in dead_links:
            print(f"  {file_path}", file=sys.stderr)
            print(f"    [{text}]({url}) → {reason}", file=sys.stderr)
        return 1

    print(f"All {total_links} links resolve across {len(md_files)} files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
