#!/usr/bin/env python3
"""Import journal homepages from the public DOAJ journal metadata API.

Only journal-level metadata (CC0) and publisher-supplied homepage URLs are
stored. The importer does not crawl or copy journal website content.
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
from urllib.parse import quote, urlencode, urlsplit, urlunsplit
from urllib.request import Request, urlopen

from catalog_io import load_catalog, save_catalog

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "sources.json"
API = "https://doaj.org/api/v4/search/journals"
# DOAJ disables wildcard queries. This broad OR query uses ordinary indexed terms
# so the public search endpoint can be paginated without the rejected "*" pattern.
# It is a discovery slice, not a claim that every possible title language is covered.
SEARCH_QUERY = "a OR e OR i OR o OR u OR y"
USER_AGENT = "CAOS-Directory/1.2 (responsible metadata discovery; https://github.com/carlosjuniorcj16-code/CAOS)"
TOPICS = {
    "natural": ("Ciências naturais", "Natural sciences"),
    "formal": ("Ciências formais", "Formal sciences"),
    "social": ("Ciências sociais", "Social sciences"),
    "health": ("Saúde e medicina", "Health and medicine"),
    "engineering": ("Engenharia e tecnologia", "Engineering and technology"),
    "cross": ("Pesquisa multidisciplinar", "Multidisciplinary research"),
}

def normalized_url(value: str) -> str:
    try:
        p = urlsplit(value.strip())
        if p.scheme.lower() not in {"http", "https"} or not p.hostname:
            return ""
        host = p.hostname.lower().removeprefix("www.")
        if not re.fullmatch(r"[a-z0-9.-]+", host) or "." not in host:
            return ""
        if p.username or p.password:
            return ""
        path = p.path.rstrip("/") or "/"
        return urlunsplit((p.scheme.lower(), host, path, "", ""))
    except ValueError:
        return ""

def domain_key(value: str) -> str:
    normalized = normalized_url(value)
    return (urlsplit(normalized).hostname or "").removeprefix("www.") if normalized else ""

def request_page(page: int, page_size: int) -> dict:
    url = API + "/" + quote(SEARCH_QUERY, safe="") + "?" + urlencode({"page": page, "pageSize": page_size})
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    for attempt in range(5):
        try:
            with urlopen(request, timeout=45) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            if exc.code not in {429, 500, 502, 503, 504} or attempt == 4:
                raise
            time.sleep(min(30, 2 ** attempt * 2))
        except (URLError, TimeoutError, OSError, json.JSONDecodeError):
            if attempt == 4:
                raise
            time.sleep(min(30, 2 ** attempt * 2))
    raise RuntimeError("DOAJ request failed after retries")

def homepage_from(record: dict) -> str:
    bib = record.get("bibjson") or {}
    # DOAJ's canonical journal homepage is bibjson.ref.journal.
    ref = bib.get("ref") or {}
    candidate = normalized_url(str(ref.get("journal") or ""))
    if candidate:
        return candidate
    links = bib.get("link") or []
    if isinstance(links, dict):
        links = [links]
    preferred = [x for x in links if isinstance(x, dict) and str(x.get("type", "")).lower() in {"homepage", "journal"}]
    for link in preferred:
        candidate = normalized_url(str(link.get("url") or ""))
        if candidate:
            return candidate
    return ""

def topic_for(record: dict) -> str:
    bib = record.get("bibjson") or {}
    terms = " ".join(
        str(x.get("term", "")) for x in (bib.get("subject") or [])
        if isinstance(x, dict)
    ).lower()
    title = str(bib.get("title") or "").lower()
    text = terms + " " + title
    rules = [
        ("health", ("medicine", "medical", "health", "nursing", "clinical", "dentistry", "pharmacy", "veterinary")),
        ("engineering", ("engineering", "technology", "computer", "information systems", "robotics")),
        ("social", ("social science", "economics", "sociology", "political", "education", "law", "psychology")),
        ("formal", ("mathematics", "statistics", "logic", "theoretical computer")),
        ("natural", ("biology", "chemistry", "physics", "ecology", "geology", "environment", "astronomy")),
    ]
    for topic, needles in rules:
        if any(term in text for term in needles):
            return topic
    return "cross"

def build_record(item: dict, record_id: int) -> dict | None:
    bib = item.get("bibjson") or {}
    title = str(bib.get("title") or "").strip()
    url = homepage_from(item)
    if not title or not url:
        return None
    publisher = bib.get("publisher") or {}
    if isinstance(publisher, str):
        publisher_name, country = publisher, ""
    else:
        publisher_name = str(publisher.get("name") or "").strip()
        country = str(publisher.get("country") or "").strip()
    topic = topic_for(item)
    topic_pt, topic_en = TOPICS[topic]
    issns = [str(value).strip() for value in (bib.get("pissn"), bib.get("eissn")) if value]
    if not issns:
        issns = [str(x).strip() for x in (bib.get("identifier") or []) if isinstance(x, dict) and str(x.get("type", "")).lower() in {"pissn", "eissn", "issn"} and x.get("id")]
    if not issns:
        issns = [str(x).strip() for x in (bib.get("issn") or []) if x]
    source_id = str(item.get("id") or (issns[0] if issns else url))
    languages = [str(x).upper() for x in (bib.get("language") or []) if x]
    subjects = [str(x.get("term", "")).strip() for x in (bib.get("subject") or []) if isinstance(x, dict) and x.get("term")]
    tags = ["DOAJ", "Open access journal"] + subjects[:8]
    if publisher_name:
        tags.append(publisher_name)
    if country:
        tags.append(country)
    if languages:
        tags.extend(languages[:3])
    return {
        "id": record_id,
        "title": title,
        "category": topic,
        "subcategory": topic_pt,
        "description": f"Periódico científico de acesso aberto indexado no DOAJ. Consulte o site oficial para escopo, edições e políticas editoriais.",
        "description_pt": f"Periódico científico de acesso aberto indexado no DOAJ. Consulte o site oficial para escopo, edições e políticas editoriais.",
        "url": url,
        "type": "Open access academic journal",
        "type_pt": "Periódico acadêmico de acesso aberto",
        "access": "Open access journal website",
        "access_pt": "Site de periódico de acesso aberto",
        "tags": tags,
        "topic": topic,
        "topic_pt": topic_pt,
        "topic_en": topic_en,
        "topic_group": topic,
        "source": "DOAJ",
        "source_id": source_id,
        "source_url": "https://doaj.org/toc/" + (issns[0] if issns else source_id),
        "source_license": "CC0 1.0 (journal-level metadata)",
        "source_attribution": "Journal-level metadata from the Directory of Open Access Journals (DOAJ), available under CC0 1.0.",
        "imported_at": datetime.now(timezone.utc).isoformat(),
        "content_license": "See the journal website; DOAJ metadata license does not determine website content rights.",
        "publisher": publisher_name,
        "country": country,
        "issn": issns,
        "languages": languages,
        "discovery_method": "doaj_public_journal_metadata",
        "verification_status": "publisher_metadata_not_live_checked",
        "checked_at": None,
    }

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=CATALOG)
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--page-size", type=int, default=100)
    parser.add_argument("--max-pages", type=int, default=1)
    parser.add_argument("--state-file", type=Path, default=ROOT / "data" / "discovery_state.json")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.limit <= 1000 or not 1 <= args.page_size <= 100 or not 1 <= args.max_pages <= 10:
        parser.error("--limit: 1-1000; --page-size: 1-100; --max-pages: 1-10")

    raw = load_catalog(args.catalog)
    catalog = raw if isinstance(raw, dict) else {"resources": raw}
    resources = catalog.get("resources")
    if not isinstance(resources, list):
        raise SystemExit("Invalid catalog: resources must be a list.")
    known_urls = {normalized_url(str(x.get("url", ""))) for x in resources if isinstance(x, dict)}
    known_domains = {domain_key(str(x.get("url", ""))) for x in resources if isinstance(x, dict)}
    next_id = max((int(x.get("id", 0)) for x in resources if isinstance(x, dict) and str(x.get("id", "")).isdigit()), default=0) + 1

    state = json.loads(args.state_file.read_text(encoding="utf-8")) if args.state_file.exists() else {}
    start_page = max(1, int(state.get("doaj_next_page", 1)))
    additions, scanned, pages, rejected = [], 0, 0, 0
    next_page = start_page
    for page in range(start_page, start_page + args.max_pages):
        payload = request_page(page, args.page_size)
        pages += 1
        results = payload.get("results") or payload.get("records") or []
        for item in results:
            scanned += 1
            record = build_record(item, next_id + len(additions))
            if not record:
                rejected += 1
                continue
            key, domain = normalized_url(record["url"]), domain_key(record["url"])
            if not key or key in known_urls or domain in known_domains:
                rejected += 1
                continue
            additions.append(record)
            known_urls.add(key)
            known_domains.add(domain)
            if len(additions) >= args.limit:
                break
        total = payload.get("total")
        if isinstance(total, int) and total > 0:
            total_pages = (total + args.page_size - 1) // args.page_size
            next_page = page + 1 if page < total_pages else 1
        else:
            next_page = page + 1 if len(results) >= args.page_size else 1
        if len(additions) >= args.limit or not results:
            if not results:
                next_page = 1
            break
        time.sleep(0.6)  # Stay below the public service's documented request rate.

    summary = {
        "provider": "DOAJ journal metadata API",
        "metadata_license": "CC0 1.0",
        "pages_read": pages,
        "next_page": next_page,
        "records_scanned": scanned,
        "new_journal_sites": len(additions),
        "skipped_or_invalid": rejected,
        "catalog_total_after_import": len(resources) + len(additions),
        "dry_run": args.dry_run,
        "sample": [{"title": x["title"], "url": x["url"], "topic": x["topic"], "country": x.get("country", "")} for x in additions[:15]],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if args.dry_run:
        return
    state["doaj_next_page"] = next_page
    args.state_file.parent.mkdir(parents=True, exist_ok=True)
    args.state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if additions:
        resources.extend(additions)
        catalog["resources"] = resources
        save_catalog(args.catalog, catalog)

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"DOAJ import failed safely: {exc}", file=sys.stderr)
        raise SystemExit(1)
