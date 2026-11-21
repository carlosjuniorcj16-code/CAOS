#!/usr/bin/env python3
"""Convert data/sources.json into bounded JSON shards without dropping records."""
import argparse
import hashlib
import json
from pathlib import Path

from catalog_io import load_catalog, migrate_to_shards


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, default=Path("data/sources.json"))
    parser.add_argument("--max-shard-mb", type=int, default=18)
    args = parser.parse_args()
    before = load_catalog(args.catalog)
    records_before = before if isinstance(before, list) else before.get("resources", [])
    before_count = len(records_before)
    before_hash = hashlib.sha256(json.dumps(before, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    count, shard_count = migrate_to_shards(args.catalog, args.max_shard_mb * 1024 * 1024)
    after = load_catalog(args.catalog)
    records_after = after if isinstance(after, list) else after.get("resources", [])
    after_hash = hashlib.sha256(json.dumps(after, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    if before_count != count or count != len(records_after) or before_hash != after_hash:
        raise SystemExit("Migration integrity check failed: records or content changed.")
    sizes = [(args.catalog.parent / "sources" / f"part-{i:05d}.json").stat().st_size for i in range(1, shard_count + 1)]
    if any(size > args.max_shard_mb * 1024 * 1024 for size in sizes):
        raise SystemExit("A generated shard exceeds the configured size limit.")
    print(json.dumps({
        "status": "verified",
        "records": count,
        "shards": shard_count,
        "max_shard_bytes": max(sizes, default=0),
        "sha256_before_after_match": True,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
