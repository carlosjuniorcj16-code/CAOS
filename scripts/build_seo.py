#!/usr/bin/env python3
"""Generate crawlable CAOS category/resource pages and XML sitemaps."""
import html
import json
import os
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist"
BASE = os.environ.get("CAOS_SITE_URL", "https://carlosjuniorcj16-code.github.io/CAOS").rstrip("/")
PAGE_SIZE = 60
LANGS = {
    "pt": ("pt-BR", "Português"), "en": ("en", "English"),
    "es": ("es", "Español"), "fr": ("fr", "Français"),
    "de": ("de", "Deutsch"), "it": ("it", "Italiano"),
    "zh": ("zh-CN", "中文"), "ja": ("ja", "日本語"),
    "ru": ("ru", "Русский"), "nl": ("nl", "Nederlands"),
    "pl": ("pl", "Polski"), "ko": ("ko", "한국어"),
    "ar": ("ar", "العربية"), "hi": ("hi", "हिन्दी"),
    "tr": ("tr", "Türkçe")
}

def e(value):
    return html.escape(str(value or ""), quote=True)

def slug(value):
    import unicodedata
    value = unicodedata.normalize("NFKD", str(value or ""))
    value = "".join(c for c in value if not unicodedata.combining(c))
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return (value[:84].strip("-") or "fonte")

def absolute(route):
    return BASE + (route if route.startswith("/") else "/" + route)

def write(route, content):
    target = OUT / route.lstrip("/")
    if route.endswith("/"):
        target = target / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")

def topic_name(topic, lang, topics, resources):
    meta = next((x for x in topics if x.get("id") == topic), {})
    if lang == "pt":
        return meta.get("pt") or next((x.get("topic_pt") for x in resources if x.get("topic") == topic and x.get("topic_pt")), topic)
    if lang == "en":
        return meta.get("en") or next((x.get("topic_en") for x in resources if x.get("topic") == topic and x.get("topic_en")), meta.get("pt", topic))
    for item in resources:
        if item.get("topic") == topic:
            topic_i18n = item.get("topic_i18n") or {}
            value = topic_i18n.get(lang) if isinstance(topic_i18n, dict) else None
            if isinstance(value, str) and value.strip():
                return value
    return meta.get("en") or meta.get("pt") or topic

def description(item, lang):
    translations = item.get("translations") or {}
    translated = translations.get(lang, {}) if isinstance(translations, dict) else {}
    if isinstance(translated, dict) and translated.get("description"):
        return str(translated["description"]).strip()
    if lang == "pt":
        return str(item.get("description_pt") or item.get("description") or "").strip()
    if lang == "en":
        return str(item.get("description") or item.get("description_pt") or "").strip()
    return ""

def route_for_source(item, lang):
    name = slug(item.get("title"))
    ident = slug(item.get("id"))
    if lang == "pt":
        return "/fontes/" + name + "-" + ident + "/"
    return "/" + lang + "/sources/" + name + "-" + ident + "/"

def route_for_category(topic, lang, page=1):
    if lang == "pt":
        root = "/categorias/" + slug(topic) + "/"
        return root if page == 1 else root + "pagina/" + str(page) + "/"
    root = "/" + lang + "/categories/" + slug(topic) + "/"
    return root if page == 1 else root + "page/" + str(page) + "/"

def shell(lang, title, summary, canonical, body, jsonld, alternates=None):
    locale = LANGS.get(lang, LANGS["pt"])[0]
    alternate_html = ""
    for code, url in (alternates or {}).items():
        hreflang = "pt-BR" if code == "pt" else code
        alternate_html += '<link rel="alternate" hreflang="' + e(hreflang) + '" href="' + e(url) + '">\n'
    ld = json.dumps(jsonld, ensure_ascii=False).replace("<", "\\u003c")
    return """<!doctype html>
<html lang="{locale}"{direction}>
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{summary}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{canonical}">
{alternates}
<meta property="og:type" content="website"><meta property="og:site_name" content="CAOS">
<meta property="og:title" content="{title}"><meta property="og:description" content="{summary}">
<meta property="og:url" content="{canonical}"><meta name="twitter:card" content="summary">
<script type="application/ld+json">{ld}</script>
<style>
:root{{--navy:#17254a;--blue:#3158bd;--paper:#fffdf8;--cream:#f5f0e5;--ink:#202a35;--muted:#68727b;--line:#dedbd2}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:16px/1.65 system-ui,-apple-system,"Segoe UI",sans-serif}}
header,footer{{background:var(--navy);color:#fff;padding:17px max(20px,calc((100% - 1120px)/2))}}
header a,footer a{{color:#f0c54b;text-decoration:none}}header strong{{font:700 22px Georgia,serif;letter-spacing:.14em}}
main{{max-width:1120px;margin:0 auto;padding:38px 22px 70px}}nav.crumb{{font-size:12px;color:var(--muted);margin-bottom:20px}}nav.crumb a{{color:var(--blue)}}
h1{{font:400 clamp(32px,5vw,54px)/1.08 Georgia,serif;letter-spacing:-.035em;color:var(--navy);margin:10px 0 14px}}
.lead{{max-width:850px;color:#59636c;font-size:16px}}.meta{{font-size:12px;color:var(--muted);margin:15px 0 25px}}
.list{{border-top:1px solid var(--line);margin-top:25px}}.item{{padding:17px 0;border-bottom:1px solid var(--line)}}
.item h2{{font:400 22px/1.25 Georgia,serif;margin:0 0 5px;color:var(--navy)}}.item p{{font-size:13px;color:#5e6871;margin:0 0 8px}}
a{{color:var(--blue)}}.actions{{display:flex;gap:15px;flex-wrap:wrap;font-size:12px;font-weight:700}}
.pager{{display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin:25px 0}}.pager a{{padding:8px 12px;border:1px solid var(--line);text-decoration:none}}
.notice{{background:var(--cream);padding:14px 16px;border-left:4px solid #e66a3b;font-size:12px;margin:24px 0}}
footer{{font-size:12px;line-height:1.8}}footer a{{margin-right:14px}}
@media(max-width:600px){{main{{padding:27px 17px 50px}}.item h2{{font-size:19px}}}}
</style></head>
<body><header><a href="{home}"><strong>CAOS</strong></a> · Diretório público do conhecimento</header>
<main>{body}</main>
<footer><a href="{home}">Página inicial</a><a href="{categories}">Todas as categorias</a><a href="https://github.com/carlosjuniorcj16-code/CAOS">Código e catálogo</a><p>CAOS organiza caminhos para fontes externas. Consulte os direitos, a disponibilidade e as condições de uso na fonte original.</p></footer>
</body></html>""".format(
        locale=e(locale), direction=' dir="rtl"' if lang == "ar" else "",
        title=e(title), summary=e(summary[:290]), canonical=e(canonical),
        alternates=alternate_html, ld=ld, home=e(absolute("/")),
        categories=e(absolute("/categorias/")), body=body
    )

def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    # Preserve every standalone application page and its runtime data in the
    # published artifact. GitHub Pages serves dist/ only; omitting these files
    # makes valid repository pages appear as 404s after deployment.
    for relative in (
        "index.html", "ai-data.html", "radar.html", "leituras.html", "software.html", "freeware.html", "quantum.html",
        "data/sources.json", "data/global-sources.json", "data/ai_sources.json", "data/languages.json",
        "data/research-radar.json", "data/reading-recommendations.json",
        "data/open-source-software.json", "data/freeware.json", "data/quantum.json", "search-index.json",
    ):
        src = ROOT / relative
        if src.exists():
            dest = OUT / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)

    assets = ROOT / "assets"
    if assets.is_dir():
        shutil.copytree(assets, OUT / "assets", dirs_exist_ok=True)

    index_html = (ROOT / "index.html").read_text(encoding="utf-8")
    match = re.search(r"const TOPICS=(\[.*?\]);", index_html, re.S)
    if not match:
        raise SystemExit("Não foi possível localizar TOPICS em index.html.")
    topics = json.loads(match.group(1))
    data = json.loads((ROOT / "data/sources.json").read_text(encoding="utf-8"))
    resources = data if isinstance(data, list) else data.get("resources", [])
    supplement = json.loads((ROOT / "data/global-sources.json").read_text(encoding="utf-8"))
    resources += supplement.get("records", [])
    if not isinstance(resources, list):
        raise SystemExit("data/sources.json não contém uma lista de recursos.")

    groups = {}
    for item in resources:
        if isinstance(item, dict) and item.get("topic") and item.get("title") and item.get("url"):
            groups.setdefault(str(item["topic"]), []).append(item)

    source_routes = {}
    sitemap_urls = []
    def add_url(route):
        sitemap_urls.append(absolute(route))

    # Build useful individual landing pages. Records without a meaningful
    # description remain discoverable through their category listing.
    source_page_count = 0
    for item in resources:
        if not isinstance(item, dict) or item.get("id") is None or not item.get("title") or not item.get("url"):
            continue
        parsed = urlparse(str(item["url"]))
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            continue
        variants = {}
        preferred = "pt" if item.get("description_pt") else str(item.get("language") or "en").lower().split("-")[0]
        if preferred not in LANGS:
            preferred = "en"
        preferred_desc = description(item, preferred)
        if not preferred_desc:
            preferred, preferred_desc = "en", description(item, "en")
        if not preferred_desc:
            preferred, preferred_desc = "pt", description(item, "pt")
        if len(preferred_desc) >= 35:
            variants[preferred] = preferred_desc
        for code in LANGS:
            translated = description(item, code)
            if len(translated) >= 35 and translated != variants.get(code):
                variants[code] = translated
        if not variants:
            continue

        routes = {code: route_for_source(item, code) for code in variants}
        source_routes[str(item["id"])] = routes
        topic = str(item.get("topic") or "reference")
        for code, desc in variants.items():
            topic_title = topic_name(topic, code, topics, resources)
            title = str(item["title"]) + " | " + topic_title + " | CAOS"
            host = parsed.netloc.lower().removeprefix("www.")
            category_route = route_for_category(topic, "pt")
            crumb_label = "Categorias" if code == "pt" else "Categories"
            body = (
                '<nav class="crumb"><a href="' + e(absolute("/")) + '">CAOS</a> › '
                '<a href="' + e(absolute("/categorias/")) + '">' + crumb_label + '</a> › '
                '<a href="' + e(absolute(category_route)) + '">' + e(topic_title) + '</a></nav>'
                '<h1>' + e(item["title"]) + '</h1><p class="lead">' + e(desc) + '</p>'
                '<div class="meta">' + e(topic_title) + ' · ' + e(item.get("type_pt") or item.get("type") or "Fonte externa")
                + (' · ' + e(item.get("access_pt") or item.get("access")) if item.get("access_pt") or item.get("access") else "")
                + ' · ' + e(host) + '</div><div class="actions">'
                '<a href="' + e(item["url"]) + '" target="_blank" rel="noopener noreferrer">Visitar fonte original ↗</a>'
                '<a href="' + e(absolute(category_route)) + '">Explorar esta categoria</a></div>'
            )
            tags = item.get("tags", [])
            if isinstance(tags, list) and tags:
                body += '<p class="meta">Temas: ' + " · ".join(e(x) for x in tags[:12]) + '</p>'
            if item.get("source") == "Curlie":
                body += '<aside class="notice">Registro adaptado de <a href="https://curlie.org/" rel="noopener">Curlie.org</a>, sob licença <a href="https://www.curlie.org/docs/en/license.html" rel="noopener">CC BY 3.0</a>. A atribuição não implica endosso por Curlie.</aside>'
            body += '<aside class="notice">O CAOS é um diretório independente. A página de destino controla o conteúdo, o acesso, os direitos autorais e as condições de reutilização.</aside>'
            canonical = absolute(routes[code])
            jsonld = {
                "@context": "https://schema.org", "@type": "WebPage",
                "name": str(item["title"]), "description": desc[:290],
                "url": canonical, "inLanguage": LANGS[code][0],
                "isPartOf": {"@type": "WebSite", "name": "CAOS", "url": absolute("/")},
                "about": {"@type": "Thing", "name": str(item["title"])}
            }
            write(routes[code], shell(code, title, desc, canonical, body, jsonld,
                                      {key: absolute(value) for key, value in routes.items()}))
            add_url(routes[code])
            source_page_count += 1

    # Category pages are server-rendered, paginated and linked with ordinary anchors.
    category_page_count = 0
    category_index = []
    for topic, items in groups.items():
        for code in ("pt", "en"):
            name = topic_name(topic, code, topics, resources)
            lead = (
                ("Explore fontes e recursos sobre " if code == "pt" else "Explore sources and resources about ")
                + name + ": " + str(len(items)) + (" links organizados pelo diretório CAOS." if code == "pt" else " links organized by the CAOS directory.")
            )
            pages = max(1, (len(items) + PAGE_SIZE - 1) // PAGE_SIZE)
            alternates = {"pt": absolute(route_for_category(topic, "pt")),
                          "en": absolute(route_for_category(topic, "en"))}
            for page in range(1, pages + 1):
                route = route_for_category(topic, code, page)
                batch = items[(page - 1) * PAGE_SIZE:page * PAGE_SIZE]
                cards = []
                for item in batch:
                    target = source_routes.get(str(item.get("id")), {})
                    target_url = target.get(code) or target.get("pt") or target.get("en")
                    desc = description(item, code) or description(item, "pt") or description(item, "en")
                    heading = '<h2><a href="' + e(absolute(target_url)) + '">' + e(item["title"]) + '</a></h2>' if target_url else '<h2>' + e(item["title"]) + '</h2>'
                    cards.append('<article class="item">' + heading + '<p>' + e(desc[:420]) + '</p><div class="actions"><a href="' + e(item["url"]) + '" target="_blank" rel="noopener noreferrer">' + ("Fonte original ↗" if code == "pt" else "Original source ↗") + '</a></div></article>')
                pager = ""
                if pages > 1:
                    prev_link = '<a href="' + e(absolute(route_for_category(topic, code, page - 1))) + '">← Anterior</a>' if page > 1 else ""
                    next_link = '<a href="' + e(absolute(route_for_category(topic, code, page + 1))) + '">Próxima →</a>' if page < pages else ""
                    pager = '<nav class="pager" aria-label="Paginação">' + prev_link + '<span>' + str(page) + ' / ' + str(pages) + '</span>' + next_link + '</nav>'
                body = (
                    '<nav class="crumb"><a href="' + e(absolute("/")) + '">CAOS</a> › '
                    '<a href="' + e(absolute("/categorias/")) + '">' + ("Categorias" if code == "pt" else "Categories") + '</a></nav>'
                    '<h1>' + e(name) + '</h1><p class="lead">' + e(lead) + '</p>'
                    '<div class="meta">' + str(len(items)) + (' fontes catalogadas · Página ' if code == "pt" else ' cataloged sources · Page ')
                    + str(page) + ' / ' + str(pages) + '</div><section class="list">' + "".join(cards) + '</section>' + pager
                )
                jsonld = {
                    "@context": "https://schema.org", "@type": "CollectionPage",
                    "name": name, "description": lead, "url": absolute(route),
                    "inLanguage": LANGS[code][0],
                    "isPartOf": {"@type": "WebSite", "name": "CAOS", "url": absolute("/")},
                    "mainEntity": {"@type": "ItemList", "numberOfItems": len(items),
                        "itemListElement": [{"@type": "ListItem", "position": (page - 1) * PAGE_SIZE + i + 1,
                            "name": item["title"],
                            "url": absolute(target.get(code) or target.get("pt") or target.get("en")) if (target := source_routes.get(str(item.get("id")), {})) else item["url"]}
                            for i, item in enumerate(batch)]}
                }
                shell_alternates = alternates if page == 1 else {}
                write(route, shell(code, name + " | CAOS", lead, absolute(route), body, jsonld, shell_alternates))
                add_url(route)
                category_page_count += 1
            if code == "pt":
                category_index.append((name, len(items), route_for_category(topic, "pt")))

    category_index.sort(key=lambda row: row[0].casefold())
    category_items = "".join(
        '<article class="item"><h2><a href="' + e(absolute(route)) + '">' + e(name) + '</a></h2><p>' + str(count) + ' fontes catalogadas</p></article>'
        for name, count, route in category_index
    )
    index_body = (
        '<nav class="crumb"><a href="' + e(absolute("/")) + '">CAOS</a> › Categorias</nav>'
        '<h1>Mapa do conhecimento</h1><p class="lead">Explore o catálogo público do CAOS por área temática. Cada categoria reúne fontes externas, bibliotecas, instituições, bases de dados, periódicos e outros caminhos de pesquisa.</p>'
        '<section class="list">' + category_items + '</section><p class="meta">Interface disponível em 15 idiomas. Consulte as condições de uso na fonte original.</p>'
    )
    index_ld = {"@context": "https://schema.org", "@type": "CollectionPage",
        "name": "Mapa do conhecimento | CAOS",
        "description": "Índice de categorias e fontes públicas de conhecimento do diretório CAOS.",
        "url": absolute("/categorias/"), "inLanguage": "pt-BR",
        "mainEntity": {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "url": absolute(route)}
            for i, (name, count, route) in enumerate(category_index)]}}
    write("/categorias/", shell("pt", "Mapa do conhecimento | CAOS",
        "Explore as categorias e fontes do diretório público CAOS.", absolute("/categorias/"), index_body, index_ld))
    add_url("/categorias/")

    # Enrich the original client-side homepage without changing its catalogue behavior.
    root_meta = (
        '<link rel="canonical" href="' + e(absolute("/")) + '">'
        '<meta name="robots" content="index,follow,max-image-preview:large">'
        '<meta property="og:type" content="website"><meta property="og:site_name" content="CAOS">'
        '<meta property="og:title" content="CAOS: Diretório público do conhecimento">'
        '<meta property="og:description" content="Descubra bibliotecas, arquivos, instituições, pesquisas, bases de dados e fontes de conhecimento em todo o mundo.">'
        '<meta property="og:url" content="' + e(absolute("/")) + '"><meta name="twitter:card" content="summary">'
        '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@type": "WebSite", "name": "CAOS",
            "url": absolute("/"), "inLanguage": "pt-BR",
            "description": "Diretório público e multilíngue de fontes de conhecimento."
        }, ensure_ascii=False).replace("<", "\\u003c") + '</script>'
    )
    homepage = (OUT / "index.html").read_text(encoding="utf-8")
    homepage = homepage.replace("</head>", root_meta + "\n</head>")
    homepage = homepage.replace('<select class="lang" id="language"',
        '<a href="' + e(absolute("/categorias/")) + '" style="font-size:12px;color:#f0c54b;text-decoration:none">Mapa de categorias</a><select class="lang" id="language"')
    (OUT / "index.html").write_text(homepage, encoding="utf-8")

    ai_page = OUT / "ai-data.html"
    if ai_page.exists():
        ai = ai_page.read_text(encoding="utf-8")
        ai = ai.replace("</head>", '<link rel="canonical" href="' + e(absolute("/ai-data.html")) + '"><meta name="robots" content="index,follow"></head>')
        ai_page.write_text(ai, encoding="utf-8")
    add_url("/")
    for standalone in ("/ai-data.html", "/radar.html", "/leituras.html", "/software.html", "/freeware.html", "/quantum.html"):
        add_url(standalone)

    chunks = [sitemap_urls[i:i + 40000] for i in range(0, len(sitemap_urls), 40000)]
    sitemap_names = []
    for index, chunk in enumerate(chunks, 1):
        name = "sitemap-" + str(index) + ".xml"
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        xml += "\n".join("<url><loc>" + e(url) + "</loc></url>" for url in chunk)
        xml += "\n</urlset>\n"
        write("/" + name, xml)
        sitemap_names.append(name)
    sitemap_index = '<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap_index += "\n".join("<sitemap><loc>" + e(absolute("/" + name)) + "</loc></sitemap>" for name in sitemap_names)
    sitemap_index += "\n</sitemapindex>\n"
    write("/sitemap.xml", sitemap_index)
    write("/robots.txt", "User-agent: *\nAllow: /\nSitemap: " + absolute("/sitemap.xml") + "\n")
    write("/.nojekyll", "")

    print(json.dumps({
        "site": BASE, "resources_in_catalog": len(resources),
        "source_pages": source_page_count, "category_pages": category_page_count,
        "categories": len(groups), "sitemap_files": len(sitemap_names),
        "urls_in_sitemaps": len(sitemap_urls), "output": "dist/"
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
