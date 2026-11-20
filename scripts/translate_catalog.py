#!/usr/bin/env python3
"""Build resumable, stored translations for CAOS resource descriptions and metadata.

Requires a LibreTranslate-compatible /translate endpoint. Configure:
  TRANSLATE_API_URL=https://your-translation-service/translate
  TRANSLATE_API_KEY=...   (only when required by the provider)

The script preserves official source titles and URLs. It stores translated descriptions,
category labels, resource types, access labels and subcategories in the catalog JSON.
"""
from __future__ import annotations
import argparse
import json
import os
import time
import urllib.parse
import urllib.request
import urllib.error
from pathlib import Path

LANGUAGES = ["pt", "en", "es", "fr", "de", "it", "zh", "ja", "ru", "nl", "pl", "ko", "ar", "hi", "tr"]

def request_translation(text, target, endpoint, api_key, source):
    if not text:
        return ""
    payload = {"q": text, "source": source, "target": target, "format": "text"}
    if api_key:
        payload["api_key"] = api_key
    request = urllib.request.Request(
        endpoint,
        data=urllib.parse.urlencode(payload).encode("utf-8"),
        headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"}
    )
    for attempt in range(5):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                result = json.loads(response.read().decode("utf-8"))
            translated = result.get("translatedText")
            if not translated:
                raise RuntimeError(f"Resposta sem translatedText: {result}")
            return translated
        except (urllib.error.URLError, TimeoutError, RuntimeError):
            if attempt == 4:
                raise
            time.sleep(2 ** attempt)
    return text

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, default=Path("data/sources.json"))
    parser.add_argument("--endpoint", default=os.getenv("TRANSLATE_API_URL", ""))
    parser.add_argument("--api-key", default=os.getenv("TRANSLATE_API_KEY", ""))
    parser.add_argument("--languages", default=",".join(LANGUAGES))
    parser.add_argument("--source-language", default="auto")
    parser.add_argument("--delay", type=float, default=0.2)
    parser.add_argument("--limit", type=int, default=0, help="Maximum number of incomplete records in this run; 0 means all")
    args = parser.parse_args()
    if not args.endpoint:
        raise SystemExit("Defina TRANSLATE_API_URL com um endpoint compatível com LibreTranslate.")
    data = json.loads(args.catalog.read_text(encoding="utf-8"))
    languages = [code.strip() for code in args.languages.split(",") if code.strip()]
    cache = {}

    def translate(text, target):
        key = (text, target)
        if key not in cache:
            cache[key] = request_translation(text, target, args.endpoint, args.api_key, args.source_language)
            time.sleep(args.delay)
        return cache[key]

    topic_sources = {}
    for item in data["resources"]:
        topic = item.get("topic", "")
        if topic and topic not in topic_sources:
            topic_sources[topic] = item.get("topic_pt") or item.get("topic_en") or topic

    topic_translations = {}
    for topic, source_label in topic_sources.items():
        topic_translations[topic] = {}
        for language in languages:
            if language == "pt":
                topic_translations[topic][language] = source_label
            elif language == "en":
                matching = next((x.get("topic_en") for x in data["resources"] if x.get("topic") == topic and x.get("topic_en")), "")
                topic_translations[topic][language] = matching or translate(source_label, language)
            else:
                topic_translations[topic][language] = translate(source_label, language)

    processed = 0
    for item in data["resources"]:
        base = item.get("description_pt") or item.get("description") or item.get("title", "")
        if not base:
            continue
        existing = item.setdefault("translations", {})
        complete = all(existing.get(language, {}).get("description") for language in languages)
        topic = item.get("topic", "")
        if complete and item.get("topic_i18n"):
            continue
        if args.limit and processed >= args.limit:
            break
        for language in languages:
            fields = existing.setdefault(language, {})
            if not fields.get("description"):
                if language == "pt" and item.get("description_pt"):
                    fields["description"] = item["description_pt"]
                elif language == "en" and item.get("description"):
                    fields["description"] = item["description"]
                else:
                    fields["description"] = translate(base, language)
            if item.get("type") and not fields.get("type"):
                fields["type"] = translate(item["type"], language)
            if item.get("access") and not fields.get("access"):
                fields["access"] = translate(item["access"], language)
            subcategory = item.get("subcategory_pt") or item.get("subcategory")
            if subcategory and not fields.get("subcategory"):
                fields["subcategory"] = translate(subcategory, language)
        item["topic_i18n"] = topic_translations.get(topic, {})
        processed += 1
        if processed % 10 == 0:
            args.catalog.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"Salvos: {processed} registros incompletos processados")

    args.catalog.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    coverage = {
        language: sum(bool(x.get("translations", {}).get(language, {}).get("description")) for x in data["resources"])
        for language in languages
    }
    print(json.dumps({"processed": processed, "total": len(data["resources"]), "coverage": coverage}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
