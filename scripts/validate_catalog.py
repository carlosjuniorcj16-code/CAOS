import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "sources.json"
AI_CATALOG = ROOT / "data" / "ai_sources.json"
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
if not CATALOG.exists():
    fail("Catálogo canônico data/sources.json não encontrado.")
if "search-index.json" not in html:
    fail("index.html não referencia o índice compacto search-index.json.")

LANGUAGES = {"pt", "en", "es", "fr", "de", "it", "zh", "ja", "ru", "nl", "pl", "ko", "ar", "hi", "tr"}
html = HTML.read_text(encoding="utf-8")
missing_languages = []
for code in sorted(LANGUAGES):
    if (f"L.{code}=" not in html) and ((code + ":{") not in html):
        missing_languages.append(code)
if missing_languages:
    fail("Idiomas sem pacote de interface: " + ", ".join(missing_languages))
for i, item in enumerate(data, 1):
    translations = item.get("translations", {})
    if not isinstance(translations, dict):
        fail(f"Traduções inválidas no registro {i}.")
    for language, fields in translations.items():
        if language not in LANGUAGES or not isinstance(fields, dict):
            fail(f"Pacote de tradução inválido no registro {i}: {language}")
try:
    ai_data = json.loads(AI_CATALOG.read_text(encoding="utf-8"))
    ai_records = ai_data.get("records") if isinstance(ai_data, dict) else None
except Exception as exc:
    fail(f"JSON inválido em data/ai_sources.json: {exc}")

if not isinstance(ai_records, list) or not ai_records:
    fail("O catálogo de dados para IA precisa conter uma lista não vazia em records.")

AI_AREAS = {"web", "text", "hub", "knowledge", "scientific", "biomedical", "code", "image", "multimodal", "audio", "geospatial", "evaluation"}
AI_REQUIRED = {"id", "name", "area", "kind", "formats", "languages", "volume", "license", "access", "update", "uses", "description_pt", "description_en", "caveat", "url", "docs"}
ai_ids = set()
ai_urls = set()
for i, item in enumerate(ai_records, 1):
    if not isinstance(item, dict):
        fail(f"Registro de IA {i} não é um objeto.")
    missing = AI_REQUIRED - item.keys()
    if missing:
        fail(f"Registro de IA {i} sem campos: {', '.join(sorted(missing))}")
    ident = str(item["id"]).strip()
    if not ident or ident in ai_ids:
        fail(f"ID de dataset vazio ou duplicado: {ident}")
    ai_ids.add(ident)
    if item["area"] not in AI_AREAS:
        fail(f"Área inválida no registro de IA {i}: {item['area']}")
    for field in ("formats", "languages", "uses"):
        if not isinstance(item[field], list) or not item[field] or not all(isinstance(v, str) and v.strip() for v in item[field]):
            fail(f"Campo {field} inválido no registro de IA {i}.")
    for field in ("name", "kind", "volume", "license", "access", "update", "description_pt", "description_en", "caveat"):
        if not isinstance(item[field], str) or not item[field].strip():
            fail(f"Campo {field} vazio no registro de IA {i}.")
    for field in ("url", "docs"):
        parsed = urlparse(str(item[field]))
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            fail(f"URL {field} inválida no registro de IA {i}: {item[field]}")
    normalized = item["url"].strip().rstrip("/").lower()
    if normalized in ai_urls:
        fail(f"URL duplicada no catálogo de IA: {item['url']}")
    ai_urls.add(normalized)

translated = {lang: sum(bool(x.get("translations", {}).get(lang, {}).get("description")) for x in data) for lang in sorted(LANGUAGES)}
print(f"OK: {len(data)} registros principais e {len(ai_records)} fontes de IA; IDs, categorias, campos e URLs estruturais válidos.")
print("Cobertura de descrições traduzidas: " + json.dumps(translated, ensure_ascii=False))
