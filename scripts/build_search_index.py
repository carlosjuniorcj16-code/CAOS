#!/usr/bin/env python3
"""Build a compact browser search payload from the canonical CAOS catalogue.

Fail closed: a malformed or partially indexed catalogue must never silently
replace a working search index with an empty or incomplete one.
"""
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

from catalog_io import load_catalog

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "sources.json"
OUTPUT = ROOT / "search-index.json"
FIELDS = (
    "id", "title", "url", "category", "topic", "topic_pt", "topic_en",
    "topic_i18n", "topic_group", "subcategory", "subcategory_pt", "tags",
    "description", "description_pt", "type", "type_pt", "access",
    "access_pt", "translations", "source",
)
REQUIRED = ("id", "title", "url", "topic")


def fail(message):
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main():
    try:
        raw = load_catalog(SOURCE)
    except Exception as exc:
        fail(f"Cannot read canonical catalogue: {exc}")

    records = raw if isinstance(raw, list) else raw.get("resources") if isinstance(raw, dict) else None
    if not isinstance(records, list) or not records:
        fail("Canonical catalogue must contain a non-empty resources list.")

    compact = []
    seen = set()
    for number, item in enumerate(records, 1):
        if not isinstance(item, dict):
            fail(f"Record {number} is not an object.")
        missing = [key for key in REQUIRED if item.get(key) in (None, "")]
        if missing:
            fail(f"Record {number} is missing required search fields: {', '.join(missing)}")
        ident = str(item["id"])
        if ident in seen:
            fail(f"Duplicate catalogue ID: {ident}")
        seen.add(ident)
        parsed = urlparse(str(item["url"]))
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            fail(f"Invalid URL in record {number}: {item['url']}")
        compact.append({
            key: item[key]
            for key in FIELDS
            if key in item and item[key] not in (None, "", [], {})
        })

    if len(compact) != len(records):
        fail(f"Index is incomplete: {len(compact)} of {len(records)} records.")

    payload = {"version": 1, "total": len(compact), "resources": compact}
    temporary = OUTPUT.with_suffix(".json.tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    temporary.replace(OUTPUT)
    print(f"Compact search index: {len(compact):,} records, {OUTPUT.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
