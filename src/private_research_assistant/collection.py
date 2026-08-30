"""Explicit, small-scale Firecrawl collection into local Markdown files."""

from __future__ import annotations

import json

from firecrawl import FirecrawlApp

from private_research_assistant.config import Settings

DEFAULT_URLS = (
    "https://packaging.python.org/en/latest/tutorials/installing-packages/",
    "https://packaging.python.org/en/latest/tutorials/packaging-projects/",
    "https://pip.pypa.io/en/stable/user_guide/",
    "https://docs.python.org/3/tutorial/modules.html",
)


def collect_pages(settings: Settings, urls: tuple[str, ...] = DEFAULT_URLS) -> list[dict[str, str]]:
    """Scrape an allowlisted corpus and write a source manifest alongside it."""
    if not settings.firecrawl_api_key:
        raise RuntimeError("FIRECRAWL_API_KEY is missing. Add it to .env before collecting.")
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    app = FirecrawlApp(api_key=settings.firecrawl_api_key)
    manifest: list[dict[str, str]] = []
    for number, url in enumerate(urls, start=1):
        result = app.scrape_url(url, formats=["markdown"])
        markdown = result.markdown if hasattr(result, "markdown") else result["markdown"]
        filename = f"page_{number}.md"
        (settings.data_dir / filename).write_text(markdown, encoding="utf-8")
        manifest.append({"file": filename, "url": url})
    (settings.data_dir / "sources.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest
