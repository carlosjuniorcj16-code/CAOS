#!/usr/bin/env python3
"""Build a small, diverse radar of recent research from the public arXiv API."""
import json
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "research-radar.json"
API = "https://export.arxiv.org/api/query"
TOPICS = [
    ("Inteligência artificial", "cat:cs.AI OR cat:cs.LG"),
    ("Linguagem e comunicação", "cat:cs.CL"),
    ("Robótica", "cat:cs.RO"),
    ("Biociências", "cat:q-bio.GN OR cat:q-bio.QM OR cat:q-bio.NC"),
    ("Terra, clima e espaço", "cat:physics.ao-ph OR cat:astro-ph.CO OR cat:astro-ph.EP OR cat:astro-ph.GA"),
]
NS = {"a": "http://www.w3.org/2005/Atom"}

def clean(value):
    return re.sub(r"\s+", " ", value or "").strip()

def fetch_topic(area, query):
    params = urllib.parse.urlencode({
        "search_query": query,
        "start": 0,
        "max_results": 12,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    })
    request = urllib.request.Request(
        API + "?" + params,
        headers={"User-Agent": "CAOS-Research-Radar/1.0 (public research discovery; contact via GitHub repository)"},
    )
    with urllib.request.urlopen(request, timeout=35) as response:
        root = ET.fromstring(response.read())
    found = []
    for entry in root.findall("a:entry", NS):
        title = clean(entry.findtext("a:title", default="", namespaces=NS))
        summary = clean(entry.findtext("a:summary", default="", namespaces=NS))
        published = clean(entry.findtext("a:published", default="", namespaces=NS))
        links = entry.findall("a:link", NS)
        url = next((x.attrib.get("href") for x in links if x.attrib.get("rel") == "alternate"), None)
        if not url:
            id_url = clean(entry.findtext("a:id", default="", namespaces=NS))
            url = id_url
        authors = [clean(x.findtext("a:name", default="", namespaces=NS)) for x in entry.findall("a:author", NS)]
        if title and url and url.startswith("https://arxiv.org/abs/"):
            found.append({
                "area": area, "title": title, "summary": summary[:520],
                "published": published, "authors": authors[:8],
                "url": url, "source": "arXiv",
            })
    return found

def main():
    items = []
    for index, (area, query) in enumerate(TOPICS):
        try:
            items.extend(fetch_topic(area, query))
        except Exception as exc:
            print(f"WARNING: {area}: {exc}")
        if index < len(TOPICS) - 1:
            time.sleep(3)
    # Pick the newest result from each distinct area first, then fill by date.
    items.sort(key=lambda x: x.get("published", ""), reverse=True)
    selected, used = [], set()
    for item in items:
        if item["area"] not in used:
            selected.append(item)
            used.add(item["area"])
        if len(selected) == 5:
            break
    if len(selected) < 5:
        for item in items:
            if item not in selected:
                selected.append(item)
            if len(selected) == 5:
                break
    payload = {
        "schema_version": 1,
        "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "arXiv API",
        "items": selected,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Radar updated: {len(selected)} records from {len(items)} candidates.")

if __name__ == "__main__":
    main()
