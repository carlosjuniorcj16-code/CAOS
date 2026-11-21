#!/usr/bin/env python3
"""Import official institution homepages from OpenAlex into the CAOS directory.

Only OpenAlex metadata is reused (CC0). Website content and licenses are not
copied; every imported record links to the institution's own homepage.
"""
from __future__ import annotations
import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit, urlunsplit
from urllib.request import Request, urlopen

from catalog_io import load_catalog, save_catalog

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / "data" / "sources.json"
API = "https://api.openalex.org/institutions"
FIELDS = "id,display_name,homepage_url,type,country_code,updated_date,ids"
TOPIC_META = {
    "education": ("Instituições de ensino e universidades", "Education and universities"),
    "research": ("Pesquisa acadêmica e institutos", "Academic research and institutes"),
    "medicine": ("Medicina e instituições de saúde", "Medicine and health institutions"),
}

def normalized_url(value: str) -> str:
    parsed = urlsplit(value.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return ""
    host = parsed.netloc.lower()
    path = parsed.path.rstrip("/")
    return urlunsplit((parsed.scheme.lower(), host, path, "", "")).lower()

def fetch_page(cursor: str, api_key: str | None, per_page: int) -> dict:
    params = {"per_page": per_page, "cursor": cursor, "select": FIELDS}
    if api_key:
        params["api_key"] = api_key
    request = Request(
        API + "?" + urlencode(params),
        headers={"User-Agent": "CAOS-Directory/1.0 (open data curation; https://github.com/carlosjuniorcj16-code/CAOS)",
                 "Accept": "application/json"},
    )
    for attempt in range(6):
        try:
            with urlopen(request, timeout=45) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            if exc.code not in {429, 500, 502, 503, 504} or attempt == 5:
                raise
            time.sleep(min(60, 2 ** attempt))
        except URLError:
            if attempt == 5:
                raise
            time.sleep(min(60, 2 ** attempt))
    raise RuntimeError("OpenAlex request failed after retries")

def topic_for(kind: str, name: str) -> str:
    value = (kind + " " + name).lower()
    if "healthcare" in value or "hospital" in value or "medical" in value:
        return "medicine"
    if "university" in value or "education" in value or "college" in value:
        return "education"
    return "research"

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--limit", type=int, default=500)
    parser.add_argument("--per-page", type=int, default=100)
    parser.add_argument("--max-pages", type=int, default=5)
    parser.add_argument("--state-file", type=Path, default=ROOT / "data" / "discovery_state.json")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.limit < 1 or args.limit > 5000 or not 1 <= args.per_page <= 100 or args.max_pages < 1 or args.max_pages > 50:
        parser.error("--limit deve ficar entre 1 e 5000; --per-page entre 1 e 100; --max-pages entre 1 e 50.")
    api_key = os.environ.get("OPENALEX_API_KEY")
    if args.max_pages > 1 and not api_key:
        parser.error("Defina OPENALEX_API_KEY para paginação além da primeira página (cursor).")

    raw = load_catalog(args.catalog)
    catalog = raw if isinstance(raw, dict) else {"resources": raw}
    resources = catalog.get("resources", [])
    if not isinstance(resources, list):
        raise SystemExit("Formato inválido: resources deve ser uma lista.")
    known_urls = {normalized_url(str(x.get("url", ""))) for x in resources if isinstance(x, dict)}
    next_id = max((int(x.get("id", 0)) for x in resources if isinstance(x, dict) and str(x.get("id", "")).isdigit()), default=0) + 1
    state = json.loads(args.state_file.read_text(encoding="utf-8")) if args.state_file.exists() else {}
    cursor = str(state.get("openalex_next_cursor") or "*")
    if cursor != "*" and not api_key:
        parser.error("Defina OPENALEX_API_KEY para continuar a paginação OpenAlex salva no estado.")
    additions, pages, scanned = [], 0, 0
    while cursor and pages < args.max_pages and len(additions) < args.limit:
        page_cursor = cursor
        payload = fetch_page(page_cursor, api_key, args.per_page)
        pages += 1
        for item in payload.get("results", []):
            scanned += 1
            name = str(item.get("display_name") or "").strip()
            homepage = str(item.get("homepage_url") or "").strip()
            url_key = normalized_url(homepage)
            if not name or not url_key or url_key in known_urls:
                continue
            kind = str(item.get("type") or "research institution")
            topic = topic_for(kind, name)
            topic_pt, topic_en = TOPIC_META[topic]
            country = str(item.get("country_code") or "").upper()
            description = f"Official website of {name}. Consult the institution's own pages for current information, research and services."
            additions.append({
                "id": next_id + len(additions),
                "title": name,
                "category": "cross",
                "subcategory": topic_pt,
                "description": description,
                "description_pt": "",
                "url": homepage,
                "type": "Research institution",
                "type_pt": "Instituição de pesquisa",
                "access": "See official website",
                "access_pt": "Consulte o site oficial",
                "tags": [tag for tag in (kind, country, "OpenAlex institution") if tag],
                "topic": topic,
                "topic_pt": topic_pt,
                "topic_en": topic_en,
                "topic_group": "cross",
                "source": "OpenAlex",
                "source_id": item.get("id"),
                "source_url": "https://api.openalex.org/institutions/" + str(item.get("id", "")).rsplit("/", 1)[-1],
                "source_license": "CC0 1.0",
                "source_attribution": "Metadata from OpenAlex (CC0 1.0); homepage URL supplied by OpenAlex.",
                "source_updated_at": item.get("updated_date"),
                "imported_at": datetime.now(timezone.utc).isoformat(),
                "content_license": "Not determined; consult the institution's website.",
                "verification_status": "openalex_metadata_not_live_checked",
                "checked_at": None,
                "discovery_method": "openalex_institution_metadata",
                "country_code": country,
            })
            known_urls.add(url_key)
            if len(additions) >= args.limit:
                break
        next_cursor = (payload.get("meta") or {}).get("next_cursor")
        # If the batch limit is reached mid-page, revisit this page next time;
        # already imported URLs will be deduplicated and the remaining rows kept.
        cursor = page_cursor if len(additions) >= args.limit else (next_cursor or "*")

    summary = {
        "provider": "OpenAlex Institutions API",
        "pages_read": pages,
        "next_cursor_saved": bool(cursor and cursor != "*"),
        "records_scanned": scanned,
        "new_records": len(additions),
        "catalog_total_after_import": len(resources) + len(additions),
        "by_topic": {topic: sum(x["topic"] == topic for x in additions) for topic in TOPIC_META},
        "dry_run": args.dry_run,
    }
    if args.dry_run:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return
    state["openalex_next_cursor"] = cursor or "*"
    args.state_file.parent.mkdir(parents=True, exist_ok=True)
    args.state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if additions:
        resources.extend(additions)
        catalog["resources"] = resources
        save_catalog(args.catalog, catalog)
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
