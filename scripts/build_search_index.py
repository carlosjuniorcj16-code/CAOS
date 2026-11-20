#!/usr/bin/env python3
"""Build a compact browser search payload from the canonical CAOS catalogue."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "sources.json"
OUTPUT = ROOT / "search-index.json"
FIELDS = ("id","title","url","topic","topic_pt","topic_en","topic_i18n","subcategory","subcategory_pt","tags","description","description_pt","type","type_pt","access","access_pt","translations","source")
def main():
    raw = json.loads(SOURCE.read_text(encoding="utf-8"))
    records = raw if isinstance(raw, list) else raw.get("resources", [])
    compact, seen = [], set()
    for item in records:
        if not isinstance(item, dict) or not all(item.get(k) for k in ("id","title","url","topic")):
            continue
        ident = str(item["id"])
        if ident in seen:
            continue
        seen.add(ident)
        compact.append({key:item[key] for key in FIELDS if key in item and item[key] not in (None,"",[],{})})
    OUTPUT.write_text(json.dumps({"version":1,"total":len(compact),"resources":compact},ensure_ascii=False,separators=(",",":")),encoding="utf-8")
    print(f"Compact search index: {len(compact)} records, {OUTPUT.stat().st_size:,} bytes")
if __name__ == "__main__":
    main()
