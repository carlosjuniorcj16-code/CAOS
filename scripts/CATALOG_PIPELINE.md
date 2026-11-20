# Expansão e tradução do catálogo CAOS

## Escopo atual

O diretório contém 13.022 registros próprios e 67 categorias com fontes. O fluxo de importação foi preparado para incorporar até 10.000 registros por execução a partir do dump oficial do Curlie, mantendo URL, título, descrição editorial, categoria de origem, idioma e atribuição.

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
