#!/usr/bin/env python3
"""Refresh CAOS research radar and subject-based reading recommendations.

Sources: arXiv Atom API, Europe PMC REST API, PubMed E-utilities, Crossref REST API.
Only bibliographic metadata and source links are stored. Linked full text is never copied.
"""
import json
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RADAR_OUT = ROOT / "data" / "research-radar.json"
READING_OUT = ROOT / "data" / "reading-recommendations.json"
ARXIV = "https://export.arxiv.org/api/query"
EUROPE_PMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
CROSSREF = "https://api.crossref.org/works"
USER_AGENT = "CAOS-Research-Discovery/1.1 (https://github.com/carlosjuniorcj16-code/CAOS)"
NS = {"a": "http://www.w3.org/2005/Atom"}
TODAY = datetime.now(timezone.utc).date()
FROM_DATE = TODAY - timedelta(days=45)

TOPICS = [
    {"id": "ai", "name": "Inteligência artificial", "terms": "machine learning OR artificial intelligence", "arxiv": "cat:cs.AI OR cat:cs.LG", "europe": 'TITLE_ABS:("machine learning" OR "artificial intelligence")', "pubmed": '"machine learning"[Title/Abstract] OR "artificial intelligence"[Title/Abstract]', "crossref": "machine learning artificial intelligence"},
    {"id": "language", "name": "Linguagem e comunicação", "terms": "language linguistics communication", "arxiv": "cat:cs.CL", "europe": 'TITLE_ABS:(language OR linguistics OR communication)', "pubmed": "language[Title/Abstract] OR linguistics[Title/Abstract] OR communication[Title/Abstract]", "crossref": "language linguistics communication"},
    {"id": "robotics", "name": "Robótica e sistemas autônomos", "terms": "robotics autonomous systems", "arxiv": "cat:cs.RO", "europe": 'TITLE_ABS:(robotics OR "autonomous systems")', "pubmed": 'robotics[Title/Abstract] OR "autonomous systems"[Title/Abstract]', "crossref": "robotics autonomous systems"},
    {"id": "biosciences", "name": "Biociências e saúde", "terms": "biology genomics neuroscience", "arxiv": "cat:q-bio.GN OR cat:q-bio.QM OR cat:q-bio.NC", "europe": 'TITLE_ABS:(biology OR genomics OR neuroscience)', "pubmed": "biology[Title/Abstract] OR genomics[Title/Abstract] OR neuroscience[Title/Abstract]", "crossref": "biology genomics neuroscience"},
    {"id": "earth-space", "name": "Terra, clima e espaço", "terms": "climate earth sciences astronomy", "arxiv": "cat:physics.ao-ph OR cat:astro-ph.CO OR cat:astro-ph.EP OR cat:astro-ph.GA", "europe": 'TITLE_ABS:(climate OR "earth science" OR astronomy)', "pubmed": 'climate[Title/Abstract] OR "earth science"[Title/Abstract] OR astronomy[Title/Abstract]', "crossref": "climate earth science astronomy"},
    {"id": "datacenters", "name": "Data centers e infraestrutura computacional", "terms": "data centers cloud computing high performance computing", "arxiv": "cat:cs.DC OR cat:cs.NI OR cat:cs.PF", "europe": 'TITLE_ABS:("data center" OR "cloud computing" OR "high-performance computing")', "pubmed": '"data center"[Title/Abstract] OR "cloud computing"[Title/Abstract] OR "high performance computing"[Title/Abstract]', "crossref": "data centers cloud computing high performance computing"},
    {"id": "quantum", "name": "Computação e informação quânticas", "terms": "quantum computing quantum information quantum algorithms", "arxiv": "cat:quant-ph OR cat:cs.ET", "europe": 'TITLE_ABS:("quantum computing" OR "quantum information" OR "quantum algorithms")', "pubmed": '"quantum computing"[Title/Abstract] OR "quantum information"[Title/Abstract] OR "quantum algorithms"[Title/Abstract]', "crossref": "quantum computing quantum information quantum algorithms"},
    {"id": "energy-thermo", "name": "Energia, termodinâmica e sistemas complexos", "terms": "thermodynamics energy systems entropy statistical mechanics", "arxiv": "cat:physics.class-ph OR cat:physics.app-ph OR cat:cond-mat.stat-mech", "europe": 'TITLE_ABS:(thermodynamics OR entropy OR "energy systems" OR "energy conversion")', "pubmed": 'thermodynamics[Title/Abstract] OR entropy[Title/Abstract] OR "energy systems"[Title/Abstract] OR "energy conversion"[Title/Abstract]', "crossref": "thermodynamics energy systems entropy energy conversion"},
]

def clean(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()

def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=35) as response:
        return json.loads(response.read().decode("utf-8"))

def get_xml(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/atom+xml, application/xml"})
    with urllib.request.urlopen(req, timeout=35) as response:
        return ET.fromstring(response.read())

def normalize_date(value):
    value = clean(value)
    if not value:
        return ""
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        parts = value.split()
        for count, fmt in ((3, "%Y %b %d"), (2, "%Y %b"), (1, "%Y")):
            try:
                return datetime.strptime(" ".join(parts[:count]), fmt).date().isoformat()
            except (ValueError, TypeError):
                pass
        match = re.search(r"\d{4}-\d{2}-\d{2}", value)
        return match.group(0) if match else ""

def record(area, title, published, url, source, authors=None, doi=""):
    title = clean(title)
    url = clean(url)
    if not title or not url.startswith("https://"):
        return None
    return {
        "area": area,
        "title": title,
        "published": normalize_date(published),
        "authors": [clean(x) for x in (authors or []) if clean(x)][:6],
        "url": url,
        "source": source,
        "doi": clean(doi).lower(),
    }

def fetch_arxiv(topic):
    params = urllib.parse.urlencode({
        "search_query": topic["arxiv"], "start": 0, "max_results": 12,
        "sortBy": "submittedDate", "sortOrder": "descending",
    })
    root = get_xml(ARXIV + "?" + params)
    found = []
    for entry in root.findall("a:entry", NS):
        links = entry.findall("a:link", NS)
        url = next((x.attrib.get("href") for x in links if x.attrib.get("rel") == "alternate"), "")
        if not url:
            url = clean(entry.findtext("a:id", default="", namespaces=NS))
        authors = [x.findtext("a:name", default="", namespaces=NS) for x in entry.findall("a:author", NS)]
        item = record(topic["name"], entry.findtext("a:title", default="", namespaces=NS),
                      entry.findtext("a:published", default="", namespaces=NS), url, "arXiv", authors)
        if item:
            item["summary"] = clean(entry.findtext("a:summary", default="", namespaces=NS))[:420]
            found.append(item)
    return found

def fetch_europe_pmc(topic):
    query = f'{topic["europe"]} AND FIRST_PDATE:[{FROM_DATE.isoformat()} TO {TODAY.isoformat()}]'
    params = urllib.parse.urlencode({
        "query": query, "format": "json", "resultType": "core", "pageSize": 12,
        "sort_date": "y",
    })
    data = get_json(EUROPE_PMC + "?" + params)
    found = []
    for hit in data.get("resultList", {}).get("result", []):
        pmid = clean(hit.get("pmid"))
        doi = clean(hit.get("doi"))
        if doi:
            url = "https://doi.org/" + doi
        elif pmid:
            url = "https://pubmed.ncbi.nlm.nih.gov/" + pmid + "/"
        else:
            continue
        authors = [a.get("fullName", "") for a in hit.get("authorList", {}).get("author", [])]
        item = record(topic["name"], hit.get("title"), hit.get("firstPublicationDate") or hit.get("firstIndexDate"),
                      url, "Europe PMC", authors, doi)
        if item:
            found.append(item)
    return found


def fetch_pubmed(topic):
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    search_params = urllib.parse.urlencode({
        "db": "pubmed", "term": topic["pubmed"],
        "datetype": "pdat", "mindate": FROM_DATE.strftime("%Y/%m/%d"),
        "maxdate": TODAY.strftime("%Y/%m/%d"), "retmode": "json",
        "retmax": 12, "sort": "pub+date",
    })
    search = get_json(base + "esearch.fcgi?" + search_params)
    ids = search.get("esearchresult", {}).get("idlist", [])
    if not ids:
        return []
    time.sleep(0.45)
    summary_params = urllib.parse.urlencode({"db": "pubmed", "id": ",".join(ids), "retmode": "json"})
    summary = get_json(base + "esummary.fcgi?" + summary_params).get("result", {})
    found = []
    for pmid in ids:
        hit = summary.get(pmid, {})
        if not hit:
            continue
        authors = [a.get("name", "") for a in hit.get("authors", [])]
        doi = ""
        for article_id in hit.get("articleids", []):
            if article_id.get("idtype") == "doi":
                doi = article_id.get("value", "")
                break
        item = record(topic["name"], hit.get("title"), hit.get("pubdate"),
                      "https://pubmed.ncbi.nlm.nih.gov/" + pmid + "/",
                      "PubMed", authors, doi)
        if item:
            item["venue"] = clean(hit.get("fulljournalname"))
            found.append(item)
    return found

def fetch_crossref(topic):
    params = urllib.parse.urlencode({
        "query.bibliographic": topic["crossref"],
        "filter": f"from-pub-date:{FROM_DATE.isoformat()},until-pub-date:{TODAY.isoformat()},type:journal-article",
        "rows": 12, "sort": "published", "order": "desc",
        "select": "DOI,title,author,published,URL,publisher,container-title,type",
    })
    data = get_json(CROSSREF + "?" + params)
    found = []
    for hit in data.get("message", {}).get("items", []):
        parts = hit.get("published", {}).get("date-parts", [[]])
        date = "-".join(str(x).zfill(2) for x in parts[0]) if parts and parts[0] else ""
        authors = [(" ".join(x for x in [a.get("given"), a.get("family")] if x)) for a in hit.get("author", [])]
        doi = clean(hit.get("DOI"))
        url = "https://doi.org/" + doi if doi else clean(hit.get("URL"))
        item = record(topic["name"], (hit.get("title") or [""])[0], date, url, "Crossref", authors, doi)
        if item:
            item["venue"] = clean((hit.get("container-title") or [""])[0])
            found.append(item)
    return found

def key(item):
    return item.get("doi") or re.sub(r"[^a-z0-9]+", "", item["title"].lower())[:150]

def collect():
    all_items = []
    health = {}
    for topic in TOPICS:
        topic_items = []
        for provider, fetcher in (("arXiv", fetch_arxiv), ("Europe PMC", fetch_europe_pmc), ("PubMed", fetch_pubmed), ("Crossref", fetch_crossref)):
            try:
                topic_items.extend(fetcher(topic))
                health[topic["id"] + ":" + provider] = "ok"
            except Exception as exc:
                health[topic["id"] + ":" + provider] = "error: " + clean(exc)[:180]
            time.sleep(1.2)
        unique = {}
        for item in topic_items:
            k = key(item)
            if k and k not in unique:
                unique[k] = item
        ranked = sorted(unique.values(), key=lambda x: x.get("published", ""), reverse=True)
        for item in ranked[:5]:
            all_items.append(item)

    if not all_items:
        raise SystemExit("No source returned records; previous feeds preserved.")

    # One compact radar record per topic, preferring arXiv's primary preprint record.
    radar = []
    for topic in TOPICS:
        candidates = [x for x in all_items if x["area"] == topic["name"]]
        if candidates:
            radar.append(sorted(candidates, key=lambda x: (x["source"] == "arXiv", x.get("published", "")), reverse=True)[0])
    radar = sorted(radar, key=lambda x: x.get("published", ""), reverse=True)[:5]
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return {
        "schema_version": 2,
        "updated_at": now,
        "window_days": 45,
        "sources": ["arXiv", "Europe PMC", "PubMed", "Crossref"],
        "items": radar,
        "source_health": health,
    }, {
        "schema_version": 1,
        "updated_at": now,
        "window_days": 45,
        "method": "Recent bibliographic metadata from primary or scholarly index APIs; newest-first within each subject; no quality or popularity ranking.",
        "sources": ["arXiv", "Europe PMC", "PubMed", "Crossref"],
        "topics": [{"id": t["id"], "name": t["name"],
                    "items": sorted([x for x in all_items if x["area"] == t["name"]],
                                    key=lambda x: x.get("published", ""), reverse=True)[:5]}
                   for t in TOPICS],
        "source_health": health,
    }

def write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def main():
    radar, readings = collect()
    assert 1 <= len(radar["items"]) <= 5
    assert len(readings["topics"]) == 8\n    assert sum(len(t["items"]) for t in readings["topics"]) <= 40
    for item in radar["items"] + [x for t in readings["topics"] for x in t["items"]]:
        assert item["url"].startswith("https://") and item["title"] and item["published"]
    write_json(RADAR_OUT, radar)
    write_json(READING_OUT, readings)
    total = sum(len(t["items"]) for t in readings["topics"])
    print(f"Updated radar: {len(radar['items'])}; reading suggestions: {total}; sources: {', '.join(readings['sources'])}")
    for provider, status in sorted(readings["source_health"].items()):
        print(f"{provider}: {status}")

if __name__ == "__main__":
    main()
