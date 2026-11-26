#!/usr/bin/env python3
"""Discover and verify institutional homepages from Wikidata for the CAOS catalog.

Only structured Wikidata metadata (CC0) and official homepage URLs are reused.
The crawler does not copy page text, documents, images, or website content.
Every candidate is checked against robots.txt and its homepage is fetched with
a low request rate before it can enter the catalog.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit, urlunsplit
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser

from catalog_io import load_catalog, save_catalog

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "sources.json"
WIKIDATA_CATALOG = ROOT / "data" / "wikidata-discovery.json"
ENDPOINTS = (
    "https://query.wikidata.org/sparql",
    # Independent public Wikidata SPARQL mirror; used only if WDQS is unavailable.
    "https://qlever.cs.uni-freiburg.de/api/wikidata",
)
QUERY_TIMEOUT_SECONDS = max(15, min(120, int(os.environ.get("WIKIDATA_QUERY_TIMEOUT", "45"))))
USER_AGENT = "CAOS-Directory/1.1 (https://github.com/carlosjuniorcj16-code/CAOS; responsible open-data discovery)"
MAX_QUERY_RESULTS = 1200

# Direct Wikidata instance classes; intentionally limited to institutions and
# public knowledge organizations rather than arbitrary people or businesses.
CLASSES = {
    "Q3918": ("University", "Universidade", "education"),
    "Q31855": ("Research institute", "Instituto de pesquisa", "research"),
    "Q7075": ("Library", "Biblioteca", "libraries"),
    "Q33506": ("Museum", "Museu", "arts"),
    "Q166118": ("Archive", "Arquivo", "history"),
    "Q190107": ("Observatory", "Observatório", "astronomy"),
    "Q167346": ("Botanical garden", "Jardim botânico", "biology"),
    "Q955824": ("Scientific society", "Sociedade científica", "research"),
    "Q327333": ("Government agency", "Órgão público", "public-data"),
    "Q16917": ("Hospital", "Hospital", "medicine"),
    "Q3914": ("School", "Escola", "education"),
}

TOPICS = {
    "education": ("Educação e instituições de ensino", "Education and learning"),
    "research": ("Pesquisa acadêmica e institutos", "Academic research and institutes"),
    "libraries": ("Bibliotecas, arquivos e acervos", "Libraries, archives and collections"),
    "arts": ("Museus, artes e patrimônio", "Museums, arts and heritage"),
    "history": ("História e memória", "History and memory"),
    "astronomy": ("Astronomia e observatórios", "Astronomy and observatories"),
    "biology": ("Biologia e jardins botânicos", "Biology and botanical gardens"),
    "public-data": ("Instituições públicas e dados", "Public institutions and data"),
    "medicine": ("Medicina e instituições de saúde", "Medicine and health institutions"),
}

def normalized_url(value: str) -> str:
    """Normalize a homepage for duplicate detection without changing its URL."""
    try:
        p = urlsplit(value.strip())
        if p.scheme.lower() not in {"http", "https"} or not p.hostname:
            return ""
        host = p.hostname.lower().removeprefix("www.")
        if not re.fullmatch(r"[a-z0-9.-]+", host) or "." not in host:
            return ""
        if p.port and p.port not in {80, 443}:
            host = f"{host}:{p.port}"
        path = p.path.rstrip("/") or "/"
        return urlunsplit((p.scheme.lower(), host, path, "", ""))
    except ValueError:
        return ""

def domain_key(value: str) -> str:
    normalized = normalized_url(value)
    if not normalized:
        return ""
    p = urlsplit(normalized)
    return (p.hostname or "").removeprefix("www.")

def fetch_wikidata(limit: int) -> list[dict]:
    """Query WDQS first, then an independent SPARQL mirror if it is unavailable."""
    values = " ".join("wd:" + qid for qid in CLASSES)
    query = f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT DISTINCT ?item ?itemLabel ?website ?class ?countryLabel WHERE {{
      VALUES ?class {{ {values} }}
      ?item wdt:P31 ?class ;
            wdt:P856 ?website ;
            rdfs:label ?itemLabel .
      FILTER(LANG(?itemLabel) IN ("en", "pt"))
      OPTIONAL {{
        ?item wdt:P17 ?country .
        ?country rdfs:label ?countryLabel .
        FILTER(LANG(?countryLabel) IN ("en", "pt"))
      }}
    }}
    LIMIT {min(MAX_QUERY_RESULTS, max(limit * 8, 300))}
    """
    params = urlencode({"query": query, "format": "json"})
    last_error = None
    for endpoint in ENDPOINTS:
        request = Request(
            endpoint + "?" + params,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/sparql-results+json, application/json",
            },
        )
        for attempt in range(2):
            try:
                with urlopen(request, timeout=QUERY_TIMEOUT_SECONDS) as response:
                    payload = json.loads(response.read().decode("utf-8"))
                bindings = payload.get("results", {}).get("bindings")
                if not isinstance(bindings, list):
                    raise ValueError("Unexpected SPARQL response: results.bindings is missing")
                return bindings
            except (HTTPError, URLError, TimeoutError, OSError, json.JSONDecodeError, ValueError) as exc:
                last_error = exc
                if isinstance(exc, HTTPError) and exc.code not in {429, 500, 502, 503, 504}:
                    break
                if attempt == 0:
                    time.sleep(3)
    raise RuntimeError(f"All Wikidata SPARQL endpoints failed: {last_error}")

def robots_allows(url: str) -> bool:
    p = urlsplit(url)
    robots_url = f"{p.scheme}://{p.netloc}/robots.txt"
    parser = RobotFileParser()
    parser.set_url(robots_url)
    request = Request(robots_url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=8) as response:
            body = response.read(256_000).decode("utf-8", errors="replace")
        parser.parse(body.splitlines())
    except HTTPError as exc:
        # A missing robots.txt means no published crawl restrictions.
        if exc.code == 404:
            parser.parse([])
        else:
            return False
    except (URLError, TimeoutError, OSError):
        # Fail closed when the site's crawl policy cannot be retrieved.
        # Socket resets are OSError subclasses and must not abort the batch.
        return False
    return parser.can_fetch("CAOS-Directory", url)

def homepage_is_live(url: str) -> tuple[bool, str]:
    if not robots_allows(url):
        return False, "robots_denied_or_unavailable"
    for method in ("HEAD", "GET"):
        request = Request(url, headers={"User-Agent": USER_AGENT, "Range": "bytes=0-1023"}, method=method)
        try:
            with urlopen(request, timeout=8) as response:
                status = getattr(response, "status", 200)
                final_url = response.geturl()
                if status < 200 or status >= 400 or not normalized_url(final_url):
                    return False, f"http_{status}"
                # Avoid accepting a Wikidata URL that redirects to an unrelated host.
                if domain_key(final_url) != domain_key(url):
                    return False, "cross_domain_redirect"
                if method == "GET":
                    response.read(1024)
                return True, f"http_{status}"
        except HTTPError as exc:
            if method == "HEAD" and exc.code in {403, 405, 501}:
                continue
            if method == "GET" and exc.code in {403, 404, 410}:
                return False, f"http_{exc.code}"
            if method == "HEAD":
                continue
            return False, f"http_{exc.code}"
        except (URLError, TimeoutError, OSError):
            if method == "HEAD":
                continue
            return False, "network_error"
    return False, "unreachable"

def binding_value(binding: dict, key: str) -> str:
    return str((binding.get(key) or {}).get("value") or "").strip()

def build_record(item: dict, record_id: int) -> dict | None:
    entity_url = binding_value(item, "item")
    match = re.search(r"/(Q[1-9]\d*)$", entity_url)
    if not match:
        return None
    qid = match.group(1)
    website = binding_value(item, "website")
    url = normalized_url(website)
    if not url:
        return None
    class_qid = binding_value(item, "class").rsplit("/", 1)[-1]
    mapped = CLASSES.get(class_qid)
    if not mapped:
        return None
    type_en, type_pt, topic = mapped
    name = binding_value(item, "itemLabel")
    if not name or name.startswith("Q") and name[1:].isdigit():
        return None
    country = binding_value(item, "countryLabel")
    topic_pt, topic_en = TOPICS[topic]
    description_pt = (
        f"Site oficial de {name}. Consulte a instituição diretamente para "
        "informações, serviços, publicações e recursos atualizados."
    )
    description_en = (
        f"Official website of {name}. Consult the institution directly for "
        "current information, services, publications and resources."
    )
    tags = ["Wikidata", type_en, "institutional website"]
    if country:
        tags.append(country)
    return {
        "id": record_id,
        "title": name,
        "category": "cross",
        "subcategory": topic_pt,
        "description": description_en,
        "description_pt": description_pt,
        "url": url,
        "type": "Institutional website",
        "type_pt": "Site institucional",
        "access": "See the official website",
        "access_pt": "Consulte o site oficial",
        "tags": tags,
        "topic": topic,
        "topic_pt": topic_pt,
        "topic_en": topic_en,
        "topic_group": "cross",
        "source": "Wikidata",
        "source_id": qid,
        "source_url": f"https://www.wikidata.org/wiki/{qid}",
        "source_license": "CC0 1.0",
        "source_attribution": "Structured metadata from Wikidata (CC0 1.0); official website URL stated on the entity.",
        "imported_at": datetime.now(timezone.utc).isoformat(),
        "content_license": "Not determined; consult the institution's website.",
        "country": country,
        "discovery_method": "wikidata_official_website_verified",
        "verification_status": "homepage_live_checked",
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=CATALOG)
    parser.add_argument("--limit", type=int, default=300, help="Maximum new records per run (1-500)")
    parser.add_argument("--max-checks", type=int, default=1000, help="Maximum homepages to verify (1-1500)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.limit <= 500 or not 1 <= args.max_checks <= 1500:
        parser.error("--limit deve ficar entre 1 e 500; --max-checks entre 1 e 1500.")

    raw = load_catalog(args.catalog)
    catalog = raw if isinstance(raw, dict) else {"resources": raw}
    resources = catalog.get("resources")
    if not isinstance(resources, list):
        raise SystemExit("Formato inválido: resources deve ser uma lista.")

    # The validator combines the canonical catalog with the legacy Wikidata
    # supplemental catalog. Exclude both here so a rediscovered homepage cannot
    # make the entire ingestion PR fail validation.
    supplemental_records = []
    if WIKIDATA_CATALOG.exists():
        supplemental_raw = json.loads(WIKIDATA_CATALOG.read_text(encoding="utf-8"))
        supplemental_records = supplemental_raw.get("resources", []) if isinstance(supplemental_raw, dict) else []
        if not isinstance(supplemental_records, list):
            raise ValueError("Formato inválido: resources deve ser uma lista em data/wikidata-discovery.json.")

    known_records = [x for x in resources + supplemental_records if isinstance(x, dict)]
    known_urls = {normalized_url(str(x.get("url", ""))) for x in known_records}
    known_domains = {domain_key(str(x.get("url", ""))) for x in known_records}
    next_id = max(
        (int(x.get("id", 0)) for x in known_records if str(x.get("id", "")).isdigit()),
        default=0,
    ) + 1

    bindings = fetch_wikidata(args.max_checks)
    additions, checked, rejected, seen_entities = [], 0, {}, set()
    started = time.monotonic()
    deadline_seconds = 17 * 60
    time_budget_reached = False
    for item in bindings:
        if time.monotonic() - started >= deadline_seconds:
            time_budget_reached = True
            break
        if len(additions) >= args.limit or checked >= args.max_checks:
            break
        entity_url = binding_value(item, "item")
        qid_match = re.search(r"/(Q[1-9]\d*)$", entity_url)
        qid = qid_match.group(1) if qid_match else ""
        if not qid or qid in seen_entities:
            continue
        seen_entities.add(qid)
        record = build_record(item, next_id + len(additions))
        if not record:
            continue
        url = record["url"]
        domain = domain_key(url)
        if url in known_urls or domain in known_domains:
            continue
        checked += 1
        live, reason = homepage_is_live(url)
        if not live:
            rejected[reason] = rejected.get(reason, 0) + 1
            continue
        additions.append(record)
        known_urls.add(url)
        known_domains.add(domain)
        time.sleep(0.1)

    summary = {
        "provider": "Wikidata",
        "metadata_license": "CC0 1.0",
        "records_received": len(bindings),
        "homepages_checked": checked,
        "new_verified_records": len(additions),
        "rejected": rejected,
        "catalog_total_after_run": len(resources) + len(additions),
        "dry_run": args.dry_run,
        "time_budget_reached": time_budget_reached,
        "elapsed_seconds": round(time.monotonic() - started, 1),
        "records": [{"title": x["title"], "url": x["url"], "type": x["type"], "country": x.get("country", "")} for x in additions[:20]],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if args.dry_run or not additions:
        return
    resources.extend(additions)
    catalog["resources"] = resources
    save_catalog(args.catalog, catalog)

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Discovery failed safely: {exc}", file=sys.stderr)
        raise SystemExit(1)
