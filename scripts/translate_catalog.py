#!/usr/bin/env python3
"""Create and resume stored translations for every CAOS resource and topic.

Configure TRANSLATE_API_URL with a LibreTranslate-compatible /translate endpoint.
Set TRANSLATE_API_KEY if the provider requires one. Never commit API keys.
"""
from __future__ import annotations
import argparse, json, os, time, urllib.parse, urllib.request, urllib.error
from pathlib import Path

LANGUAGES=["pt","en","es","fr","de","it","zh","ja","ru","nl","pl","ko","ar","hi","tr"]
def translate(text, target, endpoint, key, source):
    if not text: return ""
    payload={"q":text,"source":source,"target":target,"format":"text"}
    if key: payload["api_key"]=key
    req=urllib.request.Request(endpoint,data=urllib.parse.urlencode(payload).encode(),headers={"Content-Type":"application/x-www-form-urlencoded","Accept":"application/json"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req,timeout=45) as response:
                data=json.loads(response.read().decode("utf-8"))
            value=data.get("translatedText")
            if not value: raise RuntimeError(f"Resposta sem translatedText: {data}")
            return value
        except (urllib.error.URLError,TimeoutError,RuntimeError) as exc:
            if attempt==4: raise
            time.sleep(2**attempt)
    return text
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--catalog",type=Path,default=Path("data/sources.json"))
    ap.add_argument("--endpoint",default=os.getenv("TRANSLATE_API_URL",""))
    ap.add_argument("--api-key",default=os.getenv("TRANSLATE_API_KEY",""))
    ap.add_argument("--languages",default=",".join(LANGUAGES))
    ap.add_argument("--source-language",default="auto")
    ap.add_argument("--delay",type=float,default=.15)
    ap.add_argument("--limit",type=int,default=0,help="Limita registros por execução; 0 processa todos")
    args=ap.parse_args()
    if not args.endpoint: raise SystemExit("Defina TRANSLATE_API_URL com um endpoint LibreTranslate compatível.")
    data=json.loads(args.catalog.read_text(encoding="utf-8"))
    langs=[x.strip() for x in args.languages.split(",") if x.strip()]
    cache={}
    def tr(text,target):
        key=(text,target)
        if key not in cache:
            cache[key]=translate(text,target,args.endpoint,args.api_key,args.source_language)
            time.sleep(args.delay)
        return cache[key]
    topics={}
    for item in data["resources"]:
        topic=item.get("topic","")
        if topic and topic not in topics:
            base=item.get("topic_pt") or item.get("topic_en") or topic
            topics[topic]={lang:tr(base,lang) for lang in langs}
    processed=0
    for item in data["resources"]:
        topic=item.get("topic","")
        base=item.get("description_pt") or item.get("description") or item.get("title","")
        if not base: continue
        translations=item.setdefault("translations",{})
        needs_work=not all(translations.get(lang,{}).get("description") for lang in langs) or not item.get("topic_i18n")
        if not needs_work: continue
        if args.limit and processed>=args.limit: break
        for lang in langs:
            entry=translations.setdefault(lang,{})
            if not entry.get("description"):
                if lang=="pt" and item.get("description_pt"): entry["description"]=item["description_pt"]
                elif lang=="en" and item.get("description"): entry["description"]=item["description"]
                else: entry["description"]=tr(base,lang)
            if item.get("type") and not entry.get("type"): entry["type"]=tr(item["type"],lang)
            if item.get("access") and not entry.get("access"): entry["access"]=tr(item["access"],lang)
            if item.get("subcategory_pt") or item.get("subcategory"):
                sub=item.get("subcategory_pt") or item.get("subcategory")
                if not entry.get("subcategory"): entry["subcategory"]=tr(sub,lang)
        item["topic_i18n"]=topics.get(topic,{})
        processed+=1
        if processed%25==0:
            args.catalog.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
            print(f"Salvos: {processed}/{len(data['resources'])}")
    args.catalog.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"Traduções atualizadas em {processed} registros para {len(langs)} idiomas.")
if __name__=="__main__": main()
