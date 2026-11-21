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
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit, urlunsplit
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "sources.json"
ENDPOINT = "https://query.wikidata.org/sparql"
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
    values = " ".join("wd:" + qid for qid in CLASSES)
    query = f"""
    SELECT DISTINCT ?item ?itemLabel ?website ?class ?classLabel ?countryLabel WHERE {{
      VALUES ?class {{ {values} }}
      ?item wdt:P31 ?class ;
            wdt:P856 ?website .
      OPTIONAL {{ ?item wdt:P17 ?country . }}
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en,pt". }}
    }}
    LIMIT {min(MAX_QUERY_RESULTS, max(limit * 8, 300))}
    """
    request = Request(
        ENDPOINT + "?" + urlencode({"query": query, "format": "json"}),
        headers={"User-Agent": USER_AGENT, "Accept": "application/sparql-results+json"},
    )
    last_error = None
    for attempt in range(4):
        try:
            with urlopen(request, timeout=60) as response:
                payload = json.loads(response.read().decode("utf-8"))
            return payload.get("results", {}).get("bindings", [])
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = exc
            if isinstance(exc, HTTPError) and exc.code not in {429, 500, 502, 503, 504}:
                break
            time.sleep(min(30, 2 ** attempt * 3))
    raise RuntimeError(f"Wikidata query failed: {last_error}")

def robots_allows(url: str) -> bool:
    p = urlsplit(url)
    robots_url = f"{p.scheme}://{p.netloc}/robots.txt"
    parser = RobotFileParser()
    parser.set_url(robots_url)
    request = Request(robots_url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=12) as response:
            body = response.read(256_000).decode("utf-8", errors="replace")
        parser.parse(body.splitlines())
    except HTTPError as exc:
        # A missing robots.txt means no published crawl restrictions.
        if exc.code == 404:
            parser.parse([])
        else:
            return False
    except (URLError, TimeoutError):
        # Fail closed when the site's crawl policy cannot be retrieved.
        return False
    return parser.can_fetch("CAOS-Directory", url)

def homepage_is_live(url: str) -> tuple[bool, str]:
    if not robots_allows(url):
        return False, "robots_denied_or_unavailable"
    for method in ("HEAD", "GET"):
        request = Request(url, headers={"User-Agent": USER_AGENT, "Range": "bytes=0-1023"}, method=method)
        try:
            with urlopen(request, timeout=15) as response:
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
        except (URLError, TimeoutError):
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
    parser.add_argument("--limit", type=int, default=150, help="Maximum new records per run (1-500)")
    parser.add_argument("--max-checks", type=int, default=500, help="Maximum homepages to verify (1-1500)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.limit <= 500 or not 1 <= args.max_checks <= 1500:
        parser.error("--limit deve ficar entre 1 e 500; --max-checks entre 1 e 1500.")

    raw = json.loads(args.catalog.read_text(encoding="utf-8"))
    catalog = raw if isinstance(raw, dict) else {"resources": raw}
    resources = catalog.get("resources")
    if not isinstance(resources, list):
        raise SystemExit("Formato inválido: resources deve ser uma lista.")

    known_urls = {normalized_url(str(x.get("url", ""))) for x in resources if isinstance(x, dict)}
    known_domains = {domain_key(str(x.get("url", ""))) for x in resources if isinstance(x, dict)}
    next_id = max(
        (int(x.get("id", 0)) for x in resources if isinstance(x, dict) and str(x.get("id", "")).isdigit()),
        default=0,
    ) + 1

    bindings = fetch_wikidata(args.max_checks)
    additions, checked, rejected, seen_entities = [], 0, {}, set()
    for item in bindings:
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
        time.sleep(0.25)

    summary = {
        "provider": "Wikidata",
        "metadata_license": "CC0 1.0",
        "records_received": len(bindings),
        "homepages_checked": checked,
        "new_verified_records": len(additions),
        "rejected": rejected,
        "catalog_total_after_run": len(resources) + len(additions),
        "dry_run": args.dry_run,
        "records": [{"title": x["title"], "url": x["url"], "type": x["type"], "country": x.get("country", "")} for x in additions[:20]],
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
        print(f"Discovery failed safely: {exc}", file=sys.stderr)
        raise SystemExit(1)
