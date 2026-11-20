# Expansão e tradução do catálogo CAOS

## Escopo atual

O diretório contém 13.519 registros, distribuídos em 67 categorias com fontes. Desses, 12.000 são registros selecionados do dump Curlie — não a totalidade das aproximadamente 2,9 milhões de entradas disponíveis. Novos lotes devem preservar URL, título, descrição, categoria de origem, idioma, licença e atribuição, com deduplicação e revisão antes da publicação.

O dump Curlie é distribuído em TSV, contém aproximadamente 2,9 milhões de entradas e é atualizado periodicamente. A licença do conteúdo é CC BY 3.0 Unported; a atribuição pública é obrigatória. Fontes:
- https://www.curlie.org/docs/en/rdf.html
- https://www.curlie.org/docs/en/license.html

## Importar um lote Curlie

Baixe o dump oficial:

\`\`\`bash
curl -L -o curlie-rdf-all.tar.gz https://curlie.org/directory-dl
\`\`\`

Faça primeiro uma simulação:

\`\`\`bash
python scripts/import_curlie.py --dump curlie-rdf-all.tar.gz --limit 10000 --per-topic 500 --dry-run
\`\`\`

Se a distribuição estiver adequada, remova \`--dry-run\` para importar. O importador lê todos os arquivos \`*-c.tsv\` e \`*-s.tsv\`, relaciona IDs de categoria, evita URLs duplicadas e preserva o caminho e o idioma de origem. O formato oficial sem cabeçalho é lido como: sites \`url,title,description,category_id\`; categorias \`category_id,category_path,site_count,description,geo1,geo2\`.

O dump completo não deve ser colocado diretamente no repositório nem carregado inteiro no navegador. CAOS importa lotes selecionados e mantém a experiência web leve.

## Gerar traduções armazenadas

A interface oferece 15 idiomas. As descrições, nomes de categorias, tipos e rótulos de acesso são armazenados por idioma em \`translations\` e \`topic_i18n\`.

Configure um serviço compatível com a API LibreTranslate. Não grave chaves no repositório:

\`\`\`bash
export TRANSLATE_API_URL="https://seu-servidor/translate"
export TRANSLATE_API_KEY="SUA_CHAVE_SE_HOUVER"
python scripts/translate_catalog.py --limit 100
\`\`\`

Repita o comando para processar lotes adicionais. O script preserva traduções existentes e avança para registros incompletos. Para traduzir todos, omita \`--limit\`. A tradução em massa pode consumir tempo e cota do provedor; revise amostras antes de publicar.

## Validar

\`\`\`bash
python -m py_compile scripts/*.py
python scripts/validate_catalog.py
\`\`\`

O validador informa a cobertura de descrições por idioma. A interface preserva nomes oficiais e títulos próprios; não traduz URLs nem nomes institucionais arbitrariamente.

## Importar instituições pelo OpenAlex

O importador `scripts/ingest_openalex_institutions.py` adiciona somente metadados institucionais e URLs oficiais. Ele não copia conteúdo dos sites. A licença CC0 se aplica aos metadados do OpenAlex; a licença do conteúdo de cada instituição permanece independente e não é presumida.

1. Crie uma chave gratuita no OpenAlex, conforme a [documentação de autenticação](https://help.openalex.org/api/authentication/).
2. No GitHub, abra Settings → Secrets and variables → Actions e crie o secret `OPENALEX_API_KEY`. Nunca coloque a chave no código ou em arquivos do repositório.
3. Abra Actions → Import OpenAlex institution directory → Run workflow. Mantenha `dry_run=true` primeiro.
4. Revise o resumo do lote. Se estiver adequado, execute novamente com `dry_run=false` e um limite controlado.
5. O workflow só permite importação na branch `main`, deduplica por URL e cria um commit do catálogo se houver novos registros.

O OpenAlex exige uma chave gratuita para paginação por cursor além da primeira página. Respeite os limites atuais da API e faça lotes pequenos no começo. Consulte `data/source_registry.json` para a política de proveniência e reutilização.

## Descoberta acadêmica multi-fonte

O workflow `.github/workflows/multi-source-discovery.yml` executa diariamente às 06:37 UTC (03:37 em Brasília) e pode ser iniciado manualmente em Actions. Cada execução percorre até três páginas de 100 registros por provedor (limite de até 300 novos registros por provedor), mantendo cursores para avançar gradualmente. O workflow de Wikidata também executa diariamente, com até 100 novos registros e 350 verificações de homepage por execução. As rotinas de ingestão compartilham um grupo de concorrência para evitar que importadores simultâneos atribuam IDs sobrepostos ao catálogo. Os limites são tetos, não garantias de novos registros; deduplicação, disponibilidade e limites dos provedores reduzem os resultados reais. Ele consulta:

- **DOAJ:** metadados de periódicos de acesso aberto e URLs de homepage fornecidas pelos periódicos. O metadado de nível de periódico é CC0 1.0. A API pública é consultada com intervalo conservador.
- **OpenAlex:** instituições de pesquisa e URLs oficiais. Metadados CC0 1.0. A paginação contínua exige o secret `OPENALEX_API_KEY`; sem ele, a etapa OpenAlex é ignorada em vez de repetir indefinidamente a primeira página.

Os cursores de DOAJ e OpenAlex são persistidos em `data/discovery_state.json`, permitindo avançar pelas páginas sem recomeçar sempre do primeiro lote. As execuções manuais começam em modo `dry_run=true`. Execuções agendadas geram um pull request de revisão; não publicam alterações diretamente em `main`. Os importadores não baixam nem copiam textos, PDFs, imagens ou outros conteúdos dos sites listados. A licença de cada site permanece independente da licença do metadado de descoberta.

O Crossref permanece cadastrado como fonte bibliográfica, mas não é usado para fabricar links de homepage: seus endpoints de periódicos e membros oferecem metadados bibliográficos e de organizações, não um campo confiável e universal de site oficial. CORE também não é ingerido até que haja autorização/licença adequada. Veja `data/source_registry.json`.

## Validação do catálogo especializado de IA

`python scripts/validate_catalog.py` também verifica `data/ai_sources.json`: IDs únicos, áreas permitidas, campos obrigatórios, listas de formatos/idiomas/usos e URLs HTTP(S) válidas. A validação do workflow de CI extrai e verifica a sintaxe JavaScript tanto de `index.html` quanto de `ai-data.html`.


## Radar de pesquisa recente

A página `radar.html` apresenta cinco publicações recentes em áreas distintas: inteligência artificial, linguagem, robótica, biociências e ciências da Terra/espaço. O coletor `scripts/update_research_radar.py` consulta os metadados públicos Atom da API do arXiv, respeitando intervalo de três segundos entre consultas e mantendo apenas títulos, autores, datas, resumos curtos e links de origem.

O workflow `.github/workflows/live-research-radar.yml` atualiza `data/research-radar.json` duas vezes ao dia (07:20 e 19:20 UTC). Essa rotina altera somente o arquivo de dados gerado do Radar; não altera `data/sources.json` nem publica novos registros no diretório principal. Se a fonte não retornar registros, o coletor falha sem sobrescrever a última versão válida.

O Radar é uma janela de recência e diversidade temática, não um ranking de qualidade, popularidade, revisão por pares ou consenso. Cada item direciona o leitor à publicação original. Documentação da API: https://info.arxiv.org/help/api/user-manual.html


## Radar científico e sugestões de leitura

O workflow \`.github/workflows/live-research-radar.yml\` consulta duas vezes ao dia (07:20 e 19:20 UTC) quatro APIs acadêmicas: arXiv, PubMed, Europe PMC e Crossref. O coletor \`scripts/update_research_radar.py\` constrói:

- \`data/research-radar.json\`: até cinco registros multidisciplinares recentes para o Radar.
- \`data/reading-recommendations.json\`: até cinco leituras por eixo temático em cinco áreas, dentro de uma janela móvel de 45 dias.

A página \`radar.html\` resume sinais recentes; \`leituras.html\` apresenta as sugestões segmentadas. A ordenação é por data e diversidade, não por qualidade, citações, popularidade ou consenso. Preprints não devem ser descritos como artigos revisados por pares.

O workflow gera um PR automático com apenas os dois arquivos JSON. A revisão humana permanece necessária para publicar as atualizações. A execução automática depende da permissão do repositório para que GitHub Actions crie pull requests (Settings → Actions → General → Workflow permissions → Allow GitHub Actions to create and approve pull requests). Se uma execução falhar, consulte os logs da etapa correspondente em Actions.

Política de conteúdo: guardar metadados bibliográficos mínimos e links diretos; não copiar PDFs, textos integrais ou imagens. Resumos e abstracts podem ter direitos próprios, portanto não são reproduzidos na página de sugestões. Consulte \`data/source_registry.json\` para a proveniência e os limites de reutilização por provedor.
