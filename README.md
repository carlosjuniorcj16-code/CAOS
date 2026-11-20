# CAOS — Cúpula dos Agentes Ordenados e Sensoriais

**An open, decentralized gateway to humanity's public knowledge.**

CAOS is an independent, public knowledge-indexing initiative. Its first implementation is deliberately simple: a curated, searchable directory connecting people and machines to useful public sources across five scientific domains.

> CAOS is a gateway, not an owner of knowledge. The knowledge remains distributed across the people, institutions, repositories and communities that create it.

## Mission

Improve the discoverability, organization, interoperability and reuse of humanity's publicly available knowledge. Lower the friction between curiosity and reliable sources. Help humans and AI systems navigate the information landscape while preserving provenance, context and access conditions.

## Five-domain taxonomy

1. **Natural Sciences** — biology, chemistry, physics, astronomy, Earth and environmental sciences.
2. **Formal Sciences** — mathematics, logic, statistics, theoretical computer science and systems theory.
3. **Social Sciences** — sociology, economics, anthropology, history, political science and related study of human systems.
4. **Health & Medical Sciences** — medicine, public health, neuroscience, epidemiology and health research.
5. **Engineering & Applied Sciences** — engineering disciplines, robotics, materials, applied computing and technology.

Cross-disciplinary resources may be classified as **Cross-disciplinary** when they genuinely span multiple domains.

## Why a directory first?

A reliable index is a smaller, cheaper and more maintainable first step than training or operating a multi-agent system. CAOS can later expose structured data and APIs for search, retrieval, research agents and AI training workflows. No model training is required for the initial portal.

## Repository structure

- `index.html` — static public portal and client-side search/filter interface.
- `data/sources.json` — structured resource directory.
- `CONTRIBUTING.md` — contribution and curation rules.
- `SOURCES.md` — initial source notes and reference guides.

## Run locally

Open `index.html` through a local static server (recommended) so the browser can load `data/sources.json`. For example:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000`.

No API key, backend, database server or AI model is required.

## Public access and deployment

The portal is a static website and can be hosted by GitHub Pages or any static hosting provider. Enable GitHub Pages in the repository settings and select the `main` branch and root folder.

## Principles

- Publicly accessible sources first.
- Open-source software and open contribution.
- Preserve original links and source attribution.
- Record access and licensing caveats; do not imply that every linked item is open-license.
- Distinguish peer-reviewed research, preprints, datasets, institutional guidance and general reference material.
- Inclusion is not endorsement or a guarantee of accuracy.
- Prefer primary sources and established repositories.
- Respect privacy, copyright, terms of service and applicable law.
- Do not collect credentials, bypass access controls, target private individuals or facilitate covert surveillance. CAOS indexes lawful public knowledge; it is not an intrusion or espionage platform.
- AI-generated classifications and summaries, when introduced, must remain traceable and reviewable by humans.

## Current status

**Stage 1 — Static knowledge portal / seed directory.** The initial collection is a starting point, not an exhaustive index of the internet. Links should be periodically checked and reviewed by contributors.

## License

The CAOS source code is intended to be released under the MIT License. The resource metadata is intended to be reusable under CC0 where legally possible. These licenses do not change the licenses or terms of linked third-party content.
