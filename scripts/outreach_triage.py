#!/usr/bin/env python3
"""Classify CAOS catalog records for human-supervised outreach research.

This is metadata-only triage. It does not visit websites, discover addresses,
infer consent, approve recipients, create messages, or send email.
"""
from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "sources.json"
OUT = ROOT / "outreach" / "triage.csv"
FIELDS = ["record_id", "title", "url", "category", "source", "candidate_type",
          "score", "confidence", "signals", "triage_status"]

RULES = {
    "government_public": [
        "government", "gov.br", ".gov", "ministry", "municipality", "prefeitura",
        "municipal", "federal", "state department", "public agency", "parliament",
        "senate", "congress", "tribunal", "court", "biblioteca nacional"
    ],
    "educational_cultural": [
        "university", "universidade", "college", "school", "escola", "institute",
        "instituto", "museum", "museu", "library", "biblioteca", "archive",
        "arquivo", "research center", "centro de pesquisa", "academy", "academia"
    ],
    "commercial_candidate": [
        "company", "empresa", "corporation", "corporate", "business", "commercial",
        "shop", "store", "loja", "marketplace", "บริการ", "consulting", "consultoria",
        "agency", "agência", "studio", "estúdio", "services", "serviços", "pricing",
        "plans", "subscription", "preços", "produtos"
    ],
    "organization_candidate": [
        "foundation", "fundação", "nonprofit", "non-profit", "ngo", "association",
        "associação", "organization", "organização", "consortium", "consórcio",
        "society", "sociedade", "network", "rede", "community", "comunidade"
    ],
    "individual_or_personal": [
        "personal blog", "my blog", "portfolio", "personal website", "about me",
        "meu blog", "portfólio pessoal", "personal page"
    ],
}
WEIGHTS = {"government_public": 3, "educational_cultural": 3,
           "commercial_candidate": 3, "organization_candidate": 3,
           "individual_or_personal": 4}

def records_from(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and data.get("_caos_shards") == 1:
        rows = []
        for rel in data.get("shards", []):
            shard = json.loads((path.parent / rel).read_text(encoding="utf-8"))
            if not isinstance(shard, list):
                raise ValueError(f"Shard inválido: {rel}")
            rows.extend(shard)
        expected = data.get("record_count")
        if expected is not None and len(rows) != expected:
            raise ValueError(f"Contagem divergente: esperado {expected}, obtido {len(rows)}")
        return rows
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("resources"), list):
        return data["resources"]
    raise ValueError("Formato de catálogo não reconhecido")

def flat(value):
    if isinstance(value, list):
        return " ".join(str(x) for x in value)
    if isinstance(value, dict):
        return " ".join(str(x) for x in value.values())
    return str(value or "")

def classify(record):
    fields = ["title", "description", "category", "tags", "type", "url"]
    corpus = " ".join(flat(record.get(k)) for k in fields).lower()
    scores, hits = {}, {}
    for kind, words in RULES.items():
        found = [w for w in words if w in corpus]
        if found:
            scores[kind] = min(10, len(found) * WEIGHTS[kind])
            hits[kind] = found[:8]
    if not scores:
        return "unclear", 0, "low", "", "needs_review"
    ranked = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    best, score = ranked[0]
    second = ranked[1][1] if len(ranked) > 1 else 0
    if best == "individual_or_personal" and score >= 4:
        status, confidence = "likely_personal", "medium"
    elif score >= 6 and score - second >= 3:
        status, confidence = "candidate", "medium"
    else:
        status, confidence = "needs_review", "low"
    signals = "; ".join(hits[best])
    return best, score, confidence, signals, status

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--catalog", type=Path, default=MANIFEST)
    p.add_argument("--output", type=Path, default=OUT)
    args = p.parse_args()
    rows = records_from(args.catalog)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    counts = {}
    with args.output.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for r in rows:
            if not isinstance(r, dict):
                continue
            kind, score, confidence, signals, status = classify(r)
            counts[status] = counts.get(status, 0) + 1
            writer.writerow({
                "record_id": r.get("id", ""), "title": r.get("title", ""),
                "url": r.get("url", ""), "category": flat(r.get("category")),
                "source": r.get("source", ""), "candidate_type": kind,
                "score": score, "confidence": confidence, "signals": signals,
                "triage_status": status,
            })
    print(f"Registros classificados: {sum(counts.values())}")
    for key in sorted(counts):
        print(f"{key}: {counts[key]}")
    print(f"CSV: {args.output}")
    print("Classificação heurística de metadados; não confirma contato, consentimento ou elegibilidade legal.")

if __name__ == "__main__":
    main()
