"""Read and write the CAOS canonical catalogue in legacy or sharded form.

The manifest remains at data/sources.json. Resource records are stored in
bounded JSON-array files under data/sources/. Readers always receive the
original in-memory list/dict shape, so callers do not need to know the layout.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

MANIFEST_KEY = "_caos_shards"
DEFAULT_SHARD_BYTES = 18 * 1024 * 1024


def _records_and_metadata(data: Any):
    if isinstance(data, list):
        return data, {}, True
    if isinstance(data, dict):
        records = data.get("resources")
        if not isinstance(records, list):
            raise ValueError("Catalogue object must contain a resources list")
        return records, {k: v for k, v in data.items() if k != "resources"}, False
    raise ValueError("Catalogue must be a JSON object or array")


def load_catalog(path: str | Path):
    path = Path(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get(MANIFEST_KEY) != 1:
        return data
    records = []
    for relative in data.get("shards", []):
        shard_path = path.parent / relative
        shard = json.loads(shard_path.read_text(encoding="utf-8"))
        if not isinstance(shard, list):
            raise ValueError(f"Invalid catalogue shard: {shard_path}")
        records.extend(shard)
    expected = data.get("record_count")
    if expected is not None and len(records) != expected:
        raise ValueError(f"Catalogue shard count mismatch: expected {expected}, got {len(records)}")
    metadata = data.get("catalog_metadata") or {}
    if data.get("catalog_is_list"):
        return records
    return {**metadata, "resources": records}


def _write_json(path: Path, value: Any):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def save_catalog(path: str | Path, data: Any):
    path = Path(path)
    current = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    if not isinstance(current, dict) or current.get(MANIFEST_KEY) != 1:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return
    records, metadata, is_list = _records_and_metadata(data)
    shard_dir = path.parent / "sources"
    shard_dir.mkdir(parents=True, exist_ok=True)
    max_bytes = int(current.get("max_shard_bytes") or DEFAULT_SHARD_BYTES)
    shards, batch, batch_bytes = [], [], 2
    for record in records:
        encoded = json.dumps(record, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        if len(encoded) + 2 > max_bytes:
            raise ValueError("A single catalogue record exceeds the configured shard size")
        if batch and batch_bytes + len(encoded) + 1 > max_bytes:
            shards.append(batch)
            batch, batch_bytes = [], 2
        batch.append(record)
        batch_bytes += len(encoded) + 1
    if batch or not shards:
        shards.append(batch)
    names = []
    for number, chunk in enumerate(shards, 1):
        name = f"part-{number:05d}.json"
        _write_json(shard_dir / name, chunk)
        names.append(f"sources/{name}")
    for old in shard_dir.glob("part-*.json"):
        if f"sources/{old.name}" not in names:
            old.unlink()
    manifest = {
        MANIFEST_KEY: 1,
        "format": "caos-json-shards-v1",
        "max_shard_bytes": max_bytes,
        "record_count": len(records),
        "catalog_is_list": is_list,
        "catalog_metadata": metadata,
        "shards": names,
    }
    _write_json(path, manifest)


def migrate_to_shards(path: str | Path, max_shard_bytes: int = DEFAULT_SHARD_BYTES):
    path = Path(path)
    data = load_catalog(path)
    records, _, _ = _records_and_metadata(data)
    manifest = {
        MANIFEST_KEY: 1,
        "format": "caos-json-shards-v1",
        "max_shard_bytes": max_shard_bytes,
        "record_count": len(records),
        "catalog_is_list": isinstance(data, list),
        "catalog_metadata": {},
        "shards": [],
    }
    # Seed the manifest so save_catalog writes the initial shard set.
    _write_json(path, manifest)
    save_catalog(path, data)
    return len(records), len(json.loads(path.read_text(encoding="utf-8"))["shards"])
