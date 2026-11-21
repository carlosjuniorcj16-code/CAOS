#!/usr/bin/env python3
"""Build an exact, deduplicated count of external source URLs across CAOS."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "site-stats.json"
DATASETS = {
    "main_directory": ("data/sources.json", {"url"}),
    "international_sources": ("data/global-sources.json", {"url"}),
    "ai_data_sources": ("data/ai_sources.json", {"url", "docs"}),
    "open_source_software": ("data/open-source-software.json", {"url"}),
    "freeware_resources": ("data/freeware.json", {"url", "docs"}),
    "quantum_references": ("data/quantum.json", {"url"}),
    "research_radar": ("data/research-radar.json", {"url"}),
}
HTML_PAGES = (
    "index.html", "ai-data.html", "freeware.html", "quantum.html",
    "radar.html", "leituras.html", "software.html",
)
HREF_RE = re.compile(r"""\bhref\s*=\s*["'](https?://[^"'<>]+)["']""", re.I)
SITE_HOSTS = {"carlosjuniorcj16-code.github.io", "localhost", "127.0.0.1"}


def normalize_url(value: str) -> str:
    try:
        parsed = urlsplit(value.strip())
        if parsed.scheme.lower() not in {"http", "https"} or not parsed.hostname:
            return ""
        if parsed.username or parsed.password:
            return ""
        host = parsed.hostname.lower().removeprefix("www.")
        if host in SITE_HOSTS or "." not in host:
            return ""
        port = parsed.port
        netloc = host
        if port and not ((parsed.scheme.lower() == "http" and port == 80) or
                         (parsed.scheme.lower() == "https" and port == 443)):
            netloc = f"{host}:{port}"
        path = parsed.path.rstrip("/") or "/"
        return urlunsplit((parsed.scheme.lower(), netloc, path, parsed.query, ""))
    except (TypeError, ValueError):
        return ""


def collect_urls(value, allowed_fields: set[str], found: set[str]) -> None:
    if isinstance(value, list):
        for item in value:
            collect_urls(item, allowed_fields, found)
    elif isinstance(value, dict):
        for key, item in value.items():
            if key in allowed_fields and isinstance(item, str):
                normalized = normalize_url(item)
                if normalized:
                    found.add(normalized)
            elif isinstance(item, (dict, list)):
                collect_urls(item, allowed_fields, found)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"Cannot read {path.relative_to(ROOT)}: {exc}") from exc


def main() -> None:
    all_urls: set[str] = set()
    per_catalog: dict[str, int] = {}
    record_counts: dict[str, int] = {}

    for name, (relative, fields) in DATASETS.items():
        path = ROOT / relative
        if not path.exists():
            if name in {"main_directory", "international_sources"}:
                raise SystemExit(f"Required catalogue is missing: {relative}")
            per_catalog[name] = 0
            record_counts[name] = 0
            continue
        data = load_json(path)
        found: set[str] = set()
        collect_urls(data, fields, found)
        if name in {"open_source_software", "quantum_references"} and isinstance(data, dict):
            for category in data.get("categories", []):
                rows = category.get("resources", []) if name == "open_source_software" else category.get("items", [])
                for row in rows:
                    if isinstance(row, list) and len(row) > 1 and isinstance(row[1], str):
                        normalized = normalize_url(row[1])
                        if normalized:
                            found.add(normalized)
                    elif isinstance(row, dict) and isinstance(row.get("url"), str):
                        normalized = normalize_url(row["url"])
                        if normalized:
                            found.add(normalized)
        per_catalog[name] = len(found)
        all_urls.update(found)
        if isinstance(data, list):
            record_counts[name] = len(data)
        elif isinstance(data, dict):
            rows = data.get("resources") or data.get("records") or data.get("items") or []
            record_counts[name] = len(rows) if isinstance(rows, list) else 0
        else:
            record_counts[name] = 0

    static_links: set[str] = set()
    for relative in HTML_PAGES:
        path = ROOT / relative
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        for match in HREF_RE.findall(content):
            normalized = normalize_url(match)
            if normalized:
                static_links.add(normalized)
    per_catalog["static_page_links"] = len(static_links)
    all_urls.update(static_links)

    payload = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_unique_urls": len(all_urls),
        "catalogue_record_counts": record_counts,
        "unique_urls_by_catalogue": per_catalog,
        "counting_policy": (
            "Unique external HTTP(S) destinations found in the CAOS source catalogues "
            "and static reference links. Host names are normalized, www and trailing "
            "slashes are removed, fragments are ignored, and duplicate destinations "
            "are counted once. Linked-site content is not copied."
        ),
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
