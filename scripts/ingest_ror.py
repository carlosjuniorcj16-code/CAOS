#!/usr/bin/env python3
"""Import a diverse, bounded batch of official organization sites from ROR's CC0 dump.

The importer stores ROR metadata and the website URL listed by ROR. It does not
crawl linked sites or copy their text, files, images, or other content.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
import time
import zipfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit, urlunsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "sources.json"
ZENODO_CONCEPT_API = "https://zenodo.org/api/records/6347574"
USER_AGENT = "CAOS-ROR-Importer/1.0 (https://github.com/carlosjuniorcj16-code/CAOS; responsible open-data discovery)"
TOPIC_META = {
    "education": ("Educação e instituições de ensino", "Education & learning", "culture"),
    "medicine": ("Medicina e instituições de saúde", "Medicine & health institutions", "health"),
    "public-data": ("Governo, políticas públicas e dados", "Government & public data", "society"),
    "research": ("Pesquisa e organizações científicas", "Research & scientific organizations", "research"),
    "archival-science": ("Arquivologia e ciência arquivística", "Archival science", "research"),
    "research-funding": ("Financiamento e fomento à pesquisa", "Research funding & funders", "research"),
    "research-infrastructure": ("Infraestruturas de pesquisa", "Research infrastructure", "research"),
    "nonprofit-sector": ("Organizações sem fins lucrativos", "Nonprofit organizations", "society"),
    "industry-research": ("Pesquisa industrial e inovação", "Industrial research & innovation", "technology"),
}
CATEGORY_BY_GROUP = {
    "nature": "natural", "formal": "formal", "society": "social",
    "health": "health", "technology": "engineering", "culture": "cross",
    "research": "cross",
}


def request_json(url: str) -> dict:
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    last_error = None
    for attempt in range(5):
        try:
            with urlopen(request, timeout=90) as response:
                return json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = exc
            if isinstance(exc, HTTPError) and exc.code not in {429, 500, 502, 503, 504}:
                break
            time.sleep(min(45, 2 ** attempt * 3))
    raise RuntimeError(f"Zenodo metadata request failed: {last_error}")


def normalize_url(value: str) -> str:
    try:
        parsed = urlsplit(value.strip())
        if parsed.scheme.lower() not in {"http", "https"} or not parsed.hostname:
            return ""
        if parsed.username or parsed.password:
            return ""
        host = parsed.hostname.lower().removeprefix("www.")
        if "." not in host:
            return ""
        port = parsed.port
        netloc = host
        if port and not ((parsed.scheme.lower() == "http" and port == 80) or
                         (parsed.scheme.lower() == "https" and port == 443)):
            netloc = f"{host}:{port}"
        path = parsed.path.rstrip("/") or "/"
        return urlunsplit((parsed.scheme.lower(), netloc, path, "", ""))
    except (TypeError, ValueError):
        return ""


def download_and_verify(file_info: dict, target: Path) -> None:
    url = file_info.get("links", {}).get("self")
    checksum = str(file_info.get("checksum") or "")
    if not url or ":" not in checksum:
        raise RuntimeError("Zenodo file metadata is missing a download URL or checksum.")
    algorithm, expected = checksum.split(":", 1)
    if algorithm not in {"md5", "sha256"}:
        raise RuntimeError(f"Unsupported Zenodo checksum algorithm: {algorithm}")
    digest = hashlib.new(algorithm)
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=180) as response, target.open("wb") as output:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            output.write(chunk)
            digest.update(chunk)
    actual = digest.hexdigest()
    if actual.lower() != expected.lower():
        target.unlink(missing_ok=True)
        raise RuntimeError(f"ROR dump checksum mismatch: expected {expected}, got {actual}")


def display_name(record: dict) -> str:
    names = record.get("names") or []
    for preferred in ("ror_display", "label"):
        for item in names:
            if preferred in (item.get("types") or []) and item.get("value"):
                return str(item["value"]).strip()
    for item in names:
        if item.get("value"):
            return str(item["value"]).strip()
    return ""


def website_url(record: dict) -> str:
    for link in record.get("links") or []:
        if isinstance(link, dict) and link.get("type") == "website":
            value = str(link.get("value") or "").strip()
            if normalize_url(value):
                return value
    return ""


def country_details(record: dict) -> tuple[str, str]:
    for location in record.get("locations") or []:
        details = location.get("geonames_details") or {}
        code = str(details.get("country_code") or "").upper()
        name = str(details.get("country_name") or "").strip()
        if code or name:
            return code, name
    return "", ""


def topic_for(types: list[str], name: str) -> str:
    values = set(types)
    if "archive" in values:
        return "archival-science"
    if "funder" in values:
        return "research-funding"
    if "facility" in values:
        return "research-infrastructure"
    if "healthcare" in values:
        return "medicine"
    if "education" in values:
        return "education"
    if "government" in values:
        return "public-data"
    if "nonprofit" in values:
        return "nonprofit-sector"
    if "company" in values:
        return "industry-research"
    return "research"


def build_record(source: dict, record_id: int) -> dict | None:
    name = display_name(source)
    homepage = website_url(source)
    ror_id = str(source.get("id") or "").strip()
    if not name or not homepage or not ror_id:
        return None
    types = [str(value) for value in (source.get("types") or []) if value]
    topic = topic_for(types, name)
    topic_pt, topic_en, group = TOPIC_META[topic]
    country_code, country = country_details(source)
    tags = ["ROR", "Research Organization Registry", *types]
    if country_code:
        tags.append(country_code)
    description_en = (
        f"Official website listed in the Research Organization Registry (ROR) "
        f"record for {name}. Consult the destination for current institutional "
        f"information, research, services and access conditions."
    )
    description_pt = (
        f"Site indicado no registro da Research Organization Registry (ROR) "
        f"para {name}. Consulte o destino para informações institucionais, "
        f"pesquisas, serviços e condições de acesso atualizadas."
    )
    return {
        "id": record_id,
        "title": name,
        "category": CATEGORY_BY_GROUP[group],
        "subcategory": topic_pt,
        "description": description_en,
        "description_pt": description_pt,
        "url": homepage,
        "type": "Research organization website",
        "type_pt": "Site de organização de pesquisa",
        "access": "Website listed in ROR; check current access at destination",
        "access_pt": "Site listado no ROR; confirme as condições de acesso no destino",
        "tags": tags,
        "topic": topic,
        "topic_pt": topic_pt,
        "topic_en": topic_en,
        "topic_group": group,
        "source": "Research Organization Registry (ROR)",
        "source_id": ror_id,
        "source_url": ror_id,
        "source_license": "CC0 1.0",
        "source_attribution": "ROR organization metadata (CC0 1.0); homepage URL as listed in the ROR record.",
        "imported_at": datetime.now(timezone.utc).isoformat(),
        "content_license": "Not determined; consult the linked organization's website.",
        "country": country,
        "country_code": country_code,
        "organization_types": types,
        "verification_status": "ror_registry_listed_not_live_checked",
        "discovery_method": "ror_cc0_data_dump",
    }


def stable_order(value: str, seed: str) -> str:
    return hashlib.sha256((seed + ":" + value).encode("utf-8")).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=CATALOG)
    parser.add_argument("--limit", type=int, default=1000)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.limit <= 5000:
        parser.error("--limit must be between 1 and 5000")

    raw = json.loads(args.catalog.read_text(encoding="utf-8"))
    catalog = raw if isinstance(raw, dict) else {"resources": raw}
    resources = catalog.get("resources")
    if not isinstance(resources, list) or not resources:
        raise SystemExit("Invalid catalog: resources must be a non-empty list.")

    known_urls = {normalize_url(str(item.get("url", ""))) for item in resources if isinstance(item, dict)}
    known_ids = {str(item.get("source_id", "")) for item in resources if isinstance(item, dict)}
    next_id = max(
        (int(item.get("id", 0)) for item in resources
         if isinstance(item, dict) and str(item.get("id", "")).isdigit()),
        default=0,
    ) + 1

    metadata = request_json(ZENODO_CONCEPT_API)
    files = metadata.get("files") or []
    zip_info = next((item for item in files if str(item.get("key", "")).lower().endswith(".zip")), None)
    if not zip_info:
        raise RuntimeError("Latest ROR Zenodo record contains no ZIP data dump.")
    release = str(metadata.get("doi") or metadata.get("id") or "latest")
    publication_date = str((metadata.get("metadata") or {}).get("publication_date") or "")
    print(f"ROR release: {release} ({publication_date})")

    with tempfile.TemporaryDirectory(prefix="caos-ror-") as temporary:
        archive = Path(temporary) / str(zip_info["key"])
        download_and_verify(zip_info, archive)
        with zipfile.ZipFile(archive) as zipped:
            json_files = [
                name for name in zipped.namelist()
                if name.lower().endswith(".json") and "ror-data" in name.lower()
                and "schema_v" not in name.lower()
            ]
            if not json_files:
                raise RuntimeError("No current ROR v2 JSON data file found in the verified archive.")
            json_name = sorted(json_files)[-1]
            with zipped.open(json_name) as stream:
                records = json.load(stream)

    if not isinstance(records, list) or not records:
        raise RuntimeError("ROR dump JSON is empty or has an unexpected structure.")

    buckets: dict[str, list[tuple[str, str, dict]]] = defaultdict(list)
    candidate_urls: set[str] = set()
    skipped = {"inactive": 0, "no_website_or_name": 0, "duplicate": 0}
    for source in records:
        if str(source.get("status") or "active").lower() != "active":
            skipped["inactive"] += 1
            continue
        ror_id = str(source.get("id") or "").strip()
        if not ror_id or ror_id in known_ids:
            skipped["duplicate"] += 1
            continue
        homepage = website_url(source)
        key = normalize_url(homepage)
        name = display_name(source)
        if not key or not name:
            skipped["no_website_or_name"] += 1
            continue
        if key in known_urls or key in candidate_urls:
            skipped["duplicate"] += 1
            continue
        candidate_urls.add(key)
        country_code, _ = country_details(source)
        country_key = country_code or "ZZ"
        built = build_record(source, 0)
        if built:
            buckets[country_key].append((stable_order(ror_id, release), ror_id, built))

    for bucket in buckets.values():
        bucket.sort(key=lambda item: item[0])
    country_order = sorted(buckets, key=lambda country: stable_order(country, release))
    additions = []
    while len(additions) < args.limit and any(buckets[country] for country in country_order):
        for country in country_order:
            if not buckets[country] or len(additions) >= args.limit:
                continue
            _, ror_id, record = buckets[country].pop(0)
            record["id"] = next_id + len(additions)
            additions.append(record)
            known_ids.add(ror_id)
            known_urls.add(normalize_url(record["url"]))

    summary = {
        "provider": "Research Organization Registry (ROR)",
        "release_doi": release,
        "publication_date": publication_date,
        "metadata_license": "CC0 1.0",
        "records_in_dump": len(records),
        "countries_with_candidates": len(buckets),
        "new_official_websites": len(additions),
        "catalog_total_after_import": len(resources) + len(additions),
        "skipped": skipped,
        "dry_run": args.dry_run,
        "sample": [
            {"title": item["title"], "url": item["url"], "country": item.get("country", ""),
             "topic": item["topic"]}
            for item in additions[:20]
        ],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if args.dry_run or not additions:
        return
    resources.extend(additions)
    catalog["resources"] = resources
    args.catalog.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ROR import failed safely: {exc}", file=sys.stderr)
        raise SystemExit(1)
