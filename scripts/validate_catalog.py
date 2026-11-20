import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "sources.json"
HTML = ROOT / "index.html"
ALLOWED = {"natural", "formal", "social", "health", "engineering", "cross"}
REQUIRED = {"id", "title", "category", "url", "type", "access", "tags"}

def fail(message):
    print(f"ERRO: {message}", file=sys.stderr)
    raise SystemExit(1)

try:
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("resources")
except Exception as exc:
    fail(f"JSON inválido em data/sources.json: {exc}")

if not isinstance(data, list) or not data:
    fail("O catálogo precisa ser uma lista não vazia.")

ids, urls = set(), set()
for i, item in enumerate(data, 1):
    if not isinstance(item, dict):
        fail(f"Registro {i} não é um objeto.")
    missing = REQUIRED - item.keys()
    if missing:
        fail(f"Registro {i} sem campos: {', '.join(sorted(missing))}")
    if not isinstance(item["id"], int) or isinstance(item["id"], bool):
        fail(f"ID inválido no registro {i}.")
    if item["id"] in ids:
        fail(f"ID duplicado: {item['id']}")
    ids.add(item["id"])
    if item["category"] not in ALLOWED:
        fail(f"Categoria inválida no registro {i}: {item['category']}")
    if not isinstance(item["title"], str) or not item["title"].strip():
        fail(f"Título vazio no registro {i}.")
    if not isinstance(item["tags"], list):
        fail(f"Tags devem ser uma lista no registro {i}.")
    parsed = urlparse(item["url"])
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        fail(f"URL inválida no registro {i}: {item['url']}")
    normalized = item["url"].strip().rstrip("/").lower()
    if normalized in urls:
        fail(f"URL duplicada: {item['url']}")
    urls.add(normalized)

html = HTML.read_text(encoding="utf-8")
if not re.search(r'<script\b', html, re.I):
    fail("Nenhum script encontrado em index.html.")
if "data/sources.json" not in html:
    fail("index.html não referencia data/sources.json.")

print(f"OK: {len(data)} registros; IDs, categorias, campos e URLs estruturais válidos.")
