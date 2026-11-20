# CAOS

**Site publicado:** https://carlosjuniorcj16-code.github.io/CAOS/  
**Hospedagem oficial:** GitHub Pages, com build e publicação pelo GitHub Actions.

**Diretório internacional de links para fontes, dados, conhecimento e cultura.**

CAOS é o nome do diretório. O projeto reúne caminhos para bibliotecas, arquivos, museus, universidades, instituições públicas, periódicos, bases de dados, documentos, coleções culturais, ferramentas, serviços de referência e outras fontes de informação em diferentes países e idiomas.

O catálogo é amplo e aberto a novas áreas. A organização por categorias serve para facilitar a navegação; não pretende estabelecer fronteiras para o conhecimento nem limitar os assuntos que podem entrar no diretório.

## Catálogo

A versão atual reúne **13.519 fontes**, distribuídas em **67 categorias temáticas com registros**. O projeto agora inclui pipelines para ampliar o catálogo com conjuntos externos licenciados e para gerar traduções armazenadas para cada idioma. O seletor de categorias é recolhível, apresenta a quantidade de fontes por assunto e permite filtrar o catálogo sem depender de um agrupamento rígido. A busca destaca os termos encontrados nos resultados e ignora diferenças de acentuação. O número cresce por meio de contribuições e curadoria contínua. O catálogo inclui recursos científicos, educacionais, culturais, jurídicos, históricos, geográficos, estatísticos, tecnológicos, ambientais, médicos e de muitos outros campos.

A presença de um link não significa endosso, certificação ou garantia de disponibilidade. Cada fonte define suas próprias condições de acesso, direitos autorais, licenças e termos de reutilização.

## Idiomas

A interface está disponível em 15 idiomas: português brasileiro, inglês, espanhol, francês, alemão, italiano, chinês simplificado, japonês, russo, neerlandês, polonês, coreano, árabe, hindi e turco. O seletor altera também o idioma do documento e a direção de leitura para árabe. O português brasileiro é o idioma inicial. Os nomes oficiais das instituições e serviços são preservados. As traduções das descrições, categorias, tipos e condições de acesso são armazenadas por registro em `translations` e `topic_i18n`. Use `scripts/translate_catalog.py` para preencher ou atualizar os campos ausentes com um endpoint compatível com LibreTranslate. O processo é retomável e não sobrescreve traduções já existentes.

## Expansão do catálogo

O catálogo atual inclui 12.000 registros selecionados do dump oficial do Curlie, que contém aproximadamente 2,9 milhões de entradas; isso não representa a importação integral do diretório. Os registros mantêm a categoria de origem, a licença CC BY 3.0 e a atribuição obrigatória. Novas importações devem ocorrer em lotes revisados, sem copiar o dump completo para o navegador. Consulte [`scripts/CATALOG_PIPELINE.md`](scripts/CATALOG_PIPELINE.md).

As descrições em português e inglês já estão normalizadas em `translations`. Os outros idiomas têm pacotes de interface completos; as descrições e metadados dos registros são preenchidos pelo pipeline de tradução, que requer um endpoint compatível com LibreTranslate.

## Dados para Inteligência Artificial

O portal possui uma área especializada em datasets e fontes primárias para IA em [ai-data.html](ai-data.html), com catálogo próprio em [data/ai_sources.json](data/ai_sources.json). A curadoria contém 32 fontes, entre corpora de texto, rastreamento web, conhecimento estruturado, literatura científica, biomedicina, código, imagens, áudio, dados geoespaciais, hubs e benchmarks, incluindo corpora multilíngues, avaliação de tradução, fala e engenharia de software. Os registros documentam área, tipo, formatos, idiomas, volume aproximado, licença/direitos, acesso, atualização, usos recomendados, ressalvas e links oficiais. A interface oferece busca e filtros em 15 idiomas. As descrições dos registros estão em português e inglês; o campo description_i18n aceita traduções adicionais. Volumes são indicativos e devem ser conferidos na documentação oficial.

A inclusão no catálogo não certifica qualidade nem concede direitos de treinamento: cada licença, versão e conteúdo de origem deve ser auditado antes do uso.

## Como usar

- Pesquise por nome, assunto, instituição, disciplina ou palavra-chave.
- Use as categorias como atalhos de navegação.
- Abra os links para consultar diretamente as fontes originais.
- Confira as condições de acesso e reutilização no próprio site de cada fonte.
- Sugira novos recursos e correções por meio do repositório.

O diretório pode apoiar estudo, ensino, jornalismo, pesquisa, descoberta de dados, preservação da informação, consulta cultural e exploração independente.

## Estrutura

- `index.html`: portal principal multilíngue.
- `ai-data.html`: diretório especializado de datasets e fontes para IA.
- `freeware.html`: curadoria de freeware confiável, servidores cloud e plataformas gratuitas.
- `data/freeware.json`: metadados, limites, licenças, riscos e evidências oficiais da curadoria gratuita.
- `data/ai_sources.json`: metadados estruturados de datasets e fontes para IA.
- `data/sources.json`: catálogo estruturado de fontes e links.
- `CONTRIBUTING.md`: orientações para contribuições.
- `SOURCES.md`: critérios editoriais e referências de curadoria.

## Executar localmente

Na pasta do projeto, inicie um servidor estático:

```bash
python -m http.server 8000
```

Acesse `http://localhost:8000`. O portal não exige chave de API, backend ou banco de dados.

## Princípios editoriais

- Alcance internacional e diversidade geográfica, cultural e linguística.
- Neutralidade política, econômica, religiosa e tecnológica.
- Descrições factuais, claras e acessíveis.
- Preferência por páginas oficiais, fontes primárias e repositórios reconhecidos.
- Distinção entre acesso aberto, acesso gratuito, cadastro e assinatura.
- Respeito a direitos autorais, licenças, privacidade e termos de uso.
- Inclusão informativa, sem endosso institucional.
- Duplicatas devem ser evitadas e links corrigidos quando identificados.
- A disponibilidade dos serviços externos pode mudar sem aviso.

## Licenças

O código-fonte pretende ser distribuído sob MIT. Os metadados do diretório pretendem ser reutilizáveis sob CC0 quando legalmente possível. Essas licenças não alteram as licenças nem os termos dos conteúdos de terceiros vinculados.

