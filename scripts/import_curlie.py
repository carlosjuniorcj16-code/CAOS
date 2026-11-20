#!/usr/bin/env python3
"""Import a curated, deduplicated subset of the official Curlie TSV dump.

Download: https://www.curlie.org/docs/en/rdf.html
License: CC BY 3.0 Unported. Keep the attribution fields and site credit.
The dump is intentionally not committed to this repository.
"""
from __future__ import annotations
import argparse, csv, json, re, sys, tarfile, tempfile
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

TOPIC_RULES = [
    ("science", "research"), ("computers", "computing"), ("business", "business"),
    ("health", "medicine"), ("arts", "arts"), ("society", "society"),
    ("sports", "sports"), ("news", "communication"), ("reference", "reference"),
    ("shopping", "business"), ("recreation", "sports"), ("games", "computing"),
    ("home", "society"), ("kids", "education"), ("regional", "geography"),
]
KEYWORDS = [
    (("astronomy","space"),"astronomy"), (("physics","particle"),"physics"),
    (("chemistry","chemical"),"chemistry"), (("biology","life science"),"biology"),
    (("medicine","medical","clinical"),"medicine"), (("health","public health"),"public-health"),
    (("neuroscience","brain"),"neuroscience"), (("mathematics","math","logic"),"mathematics"),
    (("statistics","data science"),"statistics"), (("computer","software","internet"),"computing"),
    (("cybersecurity","security"),"cybersecurity"), (("robot","automation"),"robotics"),
    (("engineering",),"engineering"), (("energy","sustainability"),"energy"),
    (("transport","logistics"),"transport"), (("education","school","university"),"education"),
    (("library","book","catalog"),"libraries"), (("journal","publishing"),"journals"),
    (("research","science","academic"),"research"), (("history",),"history"),
    (("philosophy",),"philosophy"), (("art","museum","heritage"),"arts"),
    (("literature","humanities"),"literature"), (("language","linguistic"),"languages"),
    (("law","legal","justice"),"law"), (("politic","election","democracy"),"politics"),
    (("econom","finance"),"economics"), (("sociology","society","demograph"),"society"),
    (("geography","cartography","regional"),"geography"), (("government","public data"),"public-data"),
    (("journalism","media","communication","news"),"communication"),
    (("patent","intellectual property"),"patents"), (("standard","metrology"),"standards"),
    (("reference","encyclopedia","directory"),"reference"), (("agriculture","farming"),"agriculture"),
    (("environment","conservation","ecology"),"environment"), (("anthropology",),"anthropology"),
    (("architecture","urban planning"),"architecture"), (("archaeology",),"archaeology"),
    (("film","cinema","audiovisual"),"cinema"), (("commerce","business","management"),"business"),
    (("human rights","civil rights"),"human-rights"), (("religion","mythology"),"religion"),
    (("photography","photojournalism"),"photography"), (("music","musicology"),"music"),
    (("psychology","behavior"),"psychology"), (("international relations","diplomacy"),"international-relations"),
    (("labor","employment","work"),"labor"), (("tourism","travel","heritage tourism"),"tourism"),
    (("veterinary","animal health"),"veterinary"), (("ocean","marine"),"oceanography"),
    (("water","sanitation","hydrology"),"water"), (("criminal","criminology"),"criminal-justice"),
    (("disaster","emergency","civil protection"),"disaster-risk"),
    (("food science","nutrition"),"food-science"), (("fashion","textile","clothing"),"fashion"),
    (("migration","refugee","diaspora"),"migration"), (("open source","free software"),"opensource"),
    (("peace","conflict","security studies"),"peace"), (("science communication",),"science-communication"),
    (("education research","education policy"),"education-research"), (("materials science","metallurgy"),"materials"),
]
TOPIC_NAMES = {
    "research":"Pesquisa acadêmica e repositórios","computing":"Computação e ciência da computação",
    "business":"Comércio, negócios e gestão","medicine":"Medicina e pesquisa clínica",
    "arts":"Artes, museus e patrimônio","society":"Sociedade, sociologia e demografia",
    "sports":"Esportes e ciências do movimento","communication":"Comunicação, jornalismo e mídia",
    "reference":"Enciclopédias, índices e referências","education":"Educação e ensino",
    "geography":"Geografia e cartografia","astronomy":"Astronomia e espaço","physics":"Física e partículas",
    "chemistry":"Química e materiais químicos","biology":"Biologia e ciências da vida",
    "public-health":"Saúde pública e epidemiologia","neuroscience":"Neurociência","mathematics":"Matemática e lógica",
    "statistics":"Estatística e análise de dados","cybersecurity":"Cibersegurança e segurança digital",
    "robotics":"Robótica e sistemas autônomos","engineering":"Engenharia e tecnologias aplicadas",
    "energy":"Energia e sustentabilidade","transport":"Transportes e logística","libraries":"Bibliotecas, livros e catálogos",
    "journals":"Periódicos e publicação científica","history":"História e arqueologia","philosophy":"Filosofia e pensamento",
    "literature":"Literatura e humanidades","languages":"Línguas e linguística","law":"Direito, legislação e justiça",
    "politics":"Política, eleições e democracia","economics":"Economia e finanças","public-data":"Dados públicos e administração",
    "patents":"Patentes, propriedade intelectual e inovação","standards":"Normas técnicas e metrologia",
    "agriculture":"Agricultura e alimentação","environment":"Meio ambiente e conservação",
    "anthropology":"Antropologia e etnografia","architecture":"Arquitetura e urbanismo","archaeology":"Arqueologia",
    "cinema":"Cinema e audiovisual","human-rights":"Direitos humanos e cidadania","religion":"Estudos religiosos e mitologia",
    "photography":"Fotografia e imagem","music":"Música e musicologia","psychology":"Psicologia e comportamento",
    "international-relations":"Relações internacionais e diplomacia","labor":"Trabalho e relações laborais",
    "tourism":"Turismo e patrimônio cultural","veterinary":"Veterinária e ciências animais",
    "oceanography":"Oceanografia e ciências marinhas","water":"Recursos hídricos e saneamento",
    "criminal-justice":"Criminologia e justiça criminal","disaster-risk":"Desastres, riscos e proteção civil",
    "food-science":"Ciência dos alimentos e nutrição","fashion":"Moda, têxteis e vestuário","migration":"Migração, refúgio e diásporas",
    "opensource":"Software livre e código aberto","peace":"Paz, conflitos e segurança internacional",
    "science-communication":"Comunicação pública da ciência","education-research":"Pesquisa em educação e políticas educacionais",
    "materials":"Ciência dos materiais",
}
TOPIC_EN = {
    "research":"Academic research & repositories","computing":"Computing & computer science","business":"Business, commerce & management",
    "medicine":"Medicine & clinical research","arts":"Arts, museums & heritage","society":"Society, sociology & demography",
    "sports":"Sports & movement science","communication":"Communication, journalism & media","reference":"Encyclopedias, indexes & reference",
    "education":"Education & learning","geography":"Geography & cartography"
}
def norm_url(value: str) -> str:
    value=value.strip()
    if not value.startswith(("http://","https://")): return ""
    p=urlsplit(value)
    if not p.netloc or "." not in p.netloc: return ""
    return urlunsplit((p.scheme.lower(),p.netloc.lower(),p.path.rstrip("/") or "/",p.query,""))
def topic_for(path: str) -> str:
    p=path.casefold().replace("_"," ").replace("&"," and ")
    for words,topic in KEYWORDS:
        if any(w in p for w in words): return topic
    top=p.split("/")[0].strip()
    return dict(TOPIC_RULES).get(top,"reference")
def locate(root: Path, suffix: str) -> Path:
    hits=sorted(root.rglob("*"+suffix))
    if not hits: raise SystemExit(f"Arquivo *{suffix} não encontrado em {root}")
    return hits[0]
def rows(path: Path):
    with path.open(encoding="utf-8",newline="") as f:
        sample=f.read(8192); f.seek(0)
        dialect=csv.excel_tab
        reader=csv.reader(f,dialect)
        first=next(reader,None)
        if not first: return
        known={"url","title","description","catid","category","path","name","id","site"}
        header=any(str(v).strip().casefold() in known for v in first)
        if header:
            names=[str(v).strip().casefold() for v in first]
            for row in reader:
                if row: yield dict(zip(names,row))
        else:
            raise SystemExit(f"{path.name} parece não ter cabeçalho. Consulte o README do dump e adapte o parser antes de importar. Primeira linha: {first[:8]}")
def pick(row, *keys):
    for k in keys:
        v=row.get(k.casefold())
        if v and v.strip(): return v.strip()
    return ""
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--dump",required=True,type=Path,help="Diretório extraído do arquivo oficial Curlie .tar.gz")
    ap.add_argument("--catalog",default=Path("data/sources.json"),type=Path)
    ap.add_argument("--limit",type=int,default=10000,help="Máximo de registros novos (padrão: 10.000)")
    ap.add_argument("--per-topic",type=int,default=500)
    ap.add_argument("--dry-run",action="store_true")
    args=ap.parse_args()
    root=args.dump
    if root.is_file() and tarfile.is_tarfile(root):
        target=Path(tempfile.mkdtemp(prefix="curlie-"))
        with tarfile.open(root,"r:gz") as tf:
            for member in tf.getmembers():
                if member.isfile() and not Path(member.name).is_absolute() and ".." not in Path(member.name).parts: tf.extract(member,target)
        root=target
    sites=locate(root,"-c.tsv")
    cats=locate(root,"-s.tsv")
    category_map={}
    for row in rows(cats):
        cid=pick(row,"catid","id","category_id")
        path=pick(row,"path","fullpath","category_path","name","title")
        if cid and path: category_map[cid]=path
    catalog=json.loads(args.catalog.read_text(encoding="utf-8"))
    existing={norm_url(x.get("url","")) for x in catalog.get("resources",[])}
    counts=defaultdict(int); additions=[]
    for row in rows(sites):
        url=norm_url(pick(row,"url","site","link"))
        if not url or url in existing: continue
        title=pick(row,"title","name") or urlsplit(url).netloc
        desc=pick(row,"description","desc","editorial_description")
        cid=pick(row,"catid","category_id","category")
        path=category_map.get(cid,pick(row,"category_path","path","category_name"))
        if not desc or len(desc)<20: continue
        topic=topic_for(path)
        if counts[topic]>=args.per_topic: continue
        counts[topic]+=1
        additions.append({
            "id":0,"title":title,"category":"cross","subcategory":TOPIC_NAMES.get(topic,"Referências"),
            "description":desc,"description_pt":"","url":url,"type":"Website","access":"See source",
            "tags":[path] if path else [],"topic":topic,"topic_pt":TOPIC_NAMES.get(topic,"Referências"),
            "topic_en":TOPIC_EN.get(topic,topic.replace("-"," ").title()),"topic_group":"cross",
            "source":"Curlie","source_id":pick(row,"id","uid","site_id"),
            "source_category_path":path,"source_language":pick(row,"lang","language") or "en",
            "source_license":"CC BY 3.0","source_attribution":"Content from Curlie.org"
        })
        existing.add(url)
        if len(additions)>=args.limit: break
    if args.dry_run:
        print(json.dumps({"new_records":len(additions),"by_topic":dict(counts),"source_file":str(sites),"category_file":str(cats)},ensure_ascii=False,indent=2)); return
    next_id=max((int(x.get("id",0)) for x in catalog["resources"]),default=0)+1
    for item in additions: item["id"]=next_id; next_id+=1
    catalog["resources"].extend(additions)
    args.catalog.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"Importados {len(additions)} registros Curlie. Total: {len(catalog['resources'])}.")
if __name__=="__main__": main()
