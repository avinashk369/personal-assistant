"""Normalize Firecrawl Markdown before it reaches retrieval."""

from __future__ import annotations

import re

_HEADING_LINK = re.compile(r"^(#{1,6})\s+(.+?)\s+\[¶\]\([^)]*\)\s*$")
_NOISE_LINE = re.compile(
    r"^(Copy to clipboard|Toggle (Light|Dark|table of contents).*|ContentsMenu.*|\[Back to top\].*|\[View this page\].*|\[Edit this page\].*)$",
    re.IGNORECASE,
)
_FOOTER_HEADING = re.compile(r"^#{1,6}\s+(\[?(Table of Contents|This page|Navigation)\]?).*$", re.IGNORECASE)
_READTHEDOCS_FLYOUT = re.compile(r"On Read the Docs", re.IGNORECASE)


def clean_markdown(markdown: str) -> str:
    """Remove known page chrome while preserving prose, headings, and code examples."""
    lines = markdown.splitlines()
    # Firecrawl commonly places browser navigation before the document's first H1.
    first_h1 = next((index for index, line in enumerate(lines) if line.startswith("# ")), 0)
    cleaned: list[str] = []
    for line in lines[first_h1:]:
        if _FOOTER_HEADING.match(line) or _READTHEDOCS_FLYOUT.search(line):
            # Read the Docs sites append a language/version flyout menu after the
            # last "* * *" separator; it is not a heading, so it needs its own check.
            break
        if _NOISE_LINE.match(line.strip()):
            continue
        heading = _HEADING_LINK.match(line)
        cleaned.append(f"{heading.group(1)} {heading.group(2)}" if heading else line)
    text = "\n".join(cleaned)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"
