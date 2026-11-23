#!/usr/bin/env python3
"""Prepare a human-reviewed CAOS outreach pilot. This tool never sends email.

Workflow:
  1. export-sample --catalog data/sources.json --output outreach/pilot.csv
  2. Research contacts manually from official site contact pages and fill CSV.
  3. Set contact_verified=yes, approval=approved, and provide a source URL.
  4. Add approved offer terms/version and run build-drafts.
  5. Review every .eml before creating Gmail drafts or sending anything.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from email.message import EmailMessage
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "sources.json"
FIELDS = [
    "record_id", "title", "url", "category", "source", "source_license",
    "contact_name", "contact_email", "contact_role", "contact_source_url",
    "contact_verified", "contact_basis", "approval", "offer_terms_url",
    "offer_terms_version", "status", "notes",
]
EMAIL_RE = re.compile(r"^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+$")


def load_records(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and data.get("_caos_shards") == 1:
        records = []
        for rel in data.get("shards", []):
            shard = json.loads((path.parent / rel).read_text(encoding="utf-8"))
            if not isinstance(shard, list):
                raise ValueError(f"Shard inválido: {rel}")
            records.extend(shard)
        expected = data.get("record_count")
        if expected is not None and len(records) != expected:
            raise ValueError(f"Contagem divergente: esperado {expected}, obtido {len(records)}")
        return records
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("resources"), list):
        return data["resources"]
    raise ValueError("Formato de catálogo não reconhecido")


def sample_records(records: list[dict], count: int) -> list[dict]:
    # Stable, evenly distributed sample: no dependence on shard ordering alone.
    valid = [r for r in records if isinstance(r, dict) and r.get("url")]
    valid.sort(key=lambda r: hashlib.sha256(
        (str(r.get("id", "")) + "|" + str(r.get("url", ""))).encode("utf-8")
    ).digest())
    return valid[:count]


def export_sample(args: argparse.Namespace) -> None:
    records = load_records(args.catalog)
    chosen = sample_records(records, args.count)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for r in chosen:
            writer.writerow({
                "record_id": r.get("id", ""),
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "category": r.get("category", ""),
                "source": r.get("source", ""),
                "source_license": r.get("source_license", ""),
                "contact_verified": "no",
                "approval": "pending",
                "status": "needs_contact_research",
            })
    print(f"Exportados {len(chosen)} registros de {len(records)} para {args.output}")
    print("Nenhum contato foi coletado e nenhuma mensagem foi enviada.")


def valid_http_url(value: str) -> bool:
    try:
        p = urlparse(value)
        return p.scheme in {"http", "https"} and bool(p.netloc)
    except ValueError:
        return False


def build_drafts(args: argparse.Namespace) -> None:
    args.output.mkdir(parents=True, exist_ok=True)
    made = skipped = 0
    with args.contacts.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        email = (row.get("contact_email") or "").strip()
        source = (row.get("contact_source_url") or "").strip()
        terms = (row.get("offer_terms_url") or "").strip()
        verified = (row.get("contact_verified") or "").strip().lower() == "yes"
        approved = (row.get("approval") or "").strip().lower() == "approved"
        basis = (row.get("contact_basis") or "").strip().lower()
        if not (EMAIL_RE.match(email) and verified and approved and
                valid_http_url(source) and valid_http_url(terms) and
                row.get("offer_terms_version", "").strip() and
                basis in {"public_business_contact", "explicit_opt_in"}):
            skipped += 1
            continue

        title = (row.get("title") or "seu site").strip()
        site = (row.get("url") or "").strip()
        if not valid_http_url(site):
            skipped += 1
            continue
        name = (row.get("contact_name") or "").strip()
        greeting = f"Olá, {name}!" if name else "Olá!"
        msg = EmailMessage()
        msg["To"] = email
        msg["Subject"] = f"CAOS — proposta de presença e garantia para {title}"
        msg.set_content(
            f"{greeting}\n\n"
            "Estou entrando em contato em nome do CAOS, um diretório internacional "
            "de links para recursos, instituições e fontes de informação. "
            "Encontramos este endereço em nosso catálogo público:\n"
            f"{site}\n\n"
            "Estamos apresentando uma opção voluntária de garantia vitalícia por "
            "US$ 20 para o registro indicado. A adesão não é necessária para que "
            "o link permaneça listado no catálogo. A cobertura, as condições, "
            "as limitações e a entidade responsável estão descritas nos termos "
            f"da oferta (versão {row['offer_terms_version']}):\n{terms}\n\n"
            "Se esta mensagem não for pertinente, basta responder informando "
            "que não deseja novos contatos; registraremos a oposição.\n\n"
            "Atenciosamente,\nEquipe CAOS\n"
            "https://carlosjuniorcj16-code.github.io/CAOS/\n\n"
            f"Contato comercial público consultado: {source}\n"
        )
        safe_id = re.sub(r"[^A-Za-z0-9_-]+", "-", str(row.get("record_id", "record")))
        path = args.output / f"{safe_id}.eml"
        if path.exists() and not args.overwrite:
            skipped += 1
            continue
        path.write_bytes(msg.as_bytes())
        made += 1
    print(f"Rascunhos .eml preparados: {made}; ignorados por falta de validação/aprovação: {skipped}")
    print("Isto apenas prepara arquivos para revisão; não cria rascunhos no Gmail nem envia mensagens.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(required=True)
    sample = sub.add_parser("export-sample", help="Exporta amostra determinística do catálogo para CSV")
    sample.add_argument("--catalog", type=Path, default=MANIFEST)
    sample.add_argument("--output", type=Path, default=ROOT / "outreach" / "pilot.csv")
    sample.add_argument("--count", type=int, default=100)
    sample.set_defaults(func=export_sample)
    drafts = sub.add_parser("build-drafts", help="Gera arquivos .eml somente para contatos aprovados")
    drafts.add_argument("--contacts", type=Path, default=ROOT / "outreach" / "pilot.csv")
    drafts.add_argument("--output", type=Path, default=ROOT / "outreach" / "drafts")
    drafts.add_argument("--overwrite", action="store_true")
    drafts.set_defaults(func=build_drafts)
    args = parser.parse_args()
    if getattr(args, "count", 1) < 1:
        parser.error("--count deve ser maior que zero")
    args.func(args)


if __name__ == "__main__":
    main()
