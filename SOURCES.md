# Curadoria de fontes

O catálogo reúne **mais de 13,5 mil fontes e recursos**, navegáveis por **205 categorias temáticas** de diferentes países, idiomas e áreas. CAOS funciona como um diretório amplo: as categorias ajudam a navegar, mas não limitam os assuntos que podem ser incluídos.

## Escopo

O diretório abrange, entre outros, ciência, tecnologia, educação, artes, cultura, literatura, história, direito, governo, saúde, meio ambiente, geografia, economia, estatística, linguística, arquivos, bibliotecas, museus, dados e ferramentas de referência.

A coleção combina fontes primárias, instituições públicas, bibliotecas, arquivos, repositórios, periódicos, índices, bases estatísticas, conjuntos de dados, coleções culturais, ferramentas de pesquisa e portais institucionais.

## Critérios de inclusão

- Priorizar páginas oficiais, fontes primárias, instituições públicas, bibliotecas, arquivos e repositórios reconhecidos.
- Buscar diversidade geográfica, cultural e linguística.
- Descrever a função de cada recurso de forma factual e compreensível.
- Informar quando o acesso pode exigir cadastro, vínculo institucional ou pagamento.
- Evitar duplicatas e preferir a página oficial ou mais útil do serviço.
- Conferir o endereço e a relevância do recurso antes de incluí-lo.
- Diferenciar periódicos revisados por pares, preprints, bases de dados, documentos e materiais educativos.
- Respeitar direitos autorais, licenças, privacidade e condições de reutilização.
- A inclusão não representa endosso institucional nem garantia de qualidade de cada conteúdo externo.

## Curadoria especializada de física quântica

O atlas `quantum.html` e seu catálogo `data/quantum.json` reúnem fontes oficiais de universidades, laboratórios, institutos metrológicos, agências científicas, periódicos, repositórios e projetos de software. A seleção cobre fundamentos, informação quântica, computação, materiais, óptica, sensores, redes, teoria de campos, simulação e literatura.

Referências institucionais de partida incluem NIST, NSF, Berkeley Lab, RIKEN, CERN, Oxford, Sandia, Quantum Frontiers, ICFO, QuTech e os periódicos PRX Quantum e Quantum. A seleção de destaques recentes aponta para as páginas originais do Nobel, RIKEN, Sandia, Oxford e Quantum Frontiers. Preprints devem ser identificados como tal e não descritos como artigos revisados por pares. Anúncios de programas ou instituições não substituem artigos, dados experimentais ou documentação técnica.

## Categorias

O seletor apresenta uma lista temática ampla e plana, com categorias específicas e contagem de fontes em cada uma. A lista pode ser aberta e recolhida, e não depende do agrupamento anterior em seis áreas gerais. Recursos que atravessam diferentes campos podem ser encontrados também pela busca textual.

## Idiomas

A interface está disponível em 15 idiomas: português brasileiro, inglês, espanhol, francês, alemão, italiano, chinês simplificado, japonês, russo, neerlandês, polonês, coreano, árabe, hindi e turco. O português brasileiro é o idioma inicial. As traduções dos registros são armazenadas por idioma; nomes oficiais e títulos próprios devem ser preservados.

## Fontes externas em grande escala

O projeto pode incorporar o dump público do Curlie em lotes controlados. O diretório declara aproximadamente 2,9 milhões de entradas estruturadas, distribuídas por categorias e acompanhadas de URL, título e descrição editorial. O dump é atualizado periodicamente e distribuído em TSV compactado. O conteúdo está sob CC BY 3.0 Unported, com atribuição obrigatória em páginas públicas que o utilizem. O CAOS mantém a procedência por registro e exibe a atribuição no rodapé quando houver conteúdo importado.

- Download oficial: https://www.curlie.org/docs/en/rdf.html
- Licença e atribuição: https://www.curlie.org/docs/en/license.html

A versão atual do CAOS contém 12.000 registros selecionados do dump Curlie, dentro de um catálogo de 13.519 registros. Trata-se de uma amostra importada em lote, não do dump completo. Os registros preservam `source`, `source_license`, `source_attribution` e o caminho original de categoria; novas importações devem manter a atribuição CC BY 3.0 e passar por revisão antes da publicação.

## Referências para a curadoria

- UNESCO: Open Science: https://www.unesco.org/en/open-science
- IBICT: Repositórios e Ciência Aberta: https://www.gov.br/ibict/pt-br/atuacao/pesquisa-servicos-e-iniciativas/repositorios-e-ciencia-aberta
- Europeana: https://www.europeana.eu/
- OpenDOAR: https://v2.sherpa.ac.uk/opendoar/
- re3data: https://www.re3data.org/
- WorldCat: https://www.worldcat.org/
- Library of Congress: https://www.loc.gov/
- UNESCO Digital Library: https://unesdoc.unesco.org/

Os registros completos estão em `data/sources.json`. Para ampliar o catálogo com o diretório Curlie, consulte `scripts/import_curlie.py`. O conteúdo Curlie é licenciado sob CC BY 3.0 Unported e exige atribuição pública; os registros importados mantêm `source`, `source_license`, `source_attribution` e o caminho de categoria original.


## Catálogo especializado de dados para IA

O subdiretório **Dados para Inteligência Artificial** (`ai-data.html`) reúne 32 registros e cataloga corpora de texto, rastreamentos web, bases de conhecimento, literatura científica, biomedicina, código-fonte, imagens, áudio, dados geoespaciais, hubs de datasets e benchmarks de avaliação.

Cada registro em `data/ai_sources.json` documenta área, tipo, formatos, idiomas, volume aproximado, licença e direitos, acesso, atualização, usos recomendados, ressalvas e links oficiais. A expansão inclui MADLAD-400, FLORES-200, FLEURS, MMLU e SWE-bench, com atenção às licenças e às condições próprias dos conteúdos de origem. Os volumes são aproximações, não garantias de tamanho atual. Licenças e direitos podem variar por versão, arquivo e conteúdo de origem. Plataformas agregadoras não concedem uma licença única a todos os recursos hospedados. A curadoria deve privilegiar documentação oficial, proveniência, deduplicação, privacidade, qualidade e revisão de direitos.

### Referências oficiais dos novos benchmarks e corpora

- MADLAD-400: https://huggingface.co/datasets/allenai/MADLAD-400
- FLORES-200: https://huggingface.co/datasets/facebook/flores
- FLEURS: https://huggingface.co/datasets/google/fleurs
- MMLU: https://huggingface.co/datasets/cais/mmlu
- SWE-bench: https://github.com/SWE-bench/SWE-bench
- Mozilla Common Voice: https://commonvoice.mozilla.org/terms/en.html

As descrições de licença no catálogo são resumos de orientação, não pareceres jurídicos. Confirme a licença da versão, dos arquivos e dos materiais de origem antes de baixar, redistribuir ou usar em treinamento.


## Atlas de sistemas operacionais e software open source

A página **Atlas de Software Livre** ([software.html](./software.html)) reúne uma curadoria inicial de 177 recursos em nove ecossistemas: distribuições GNU/Linux; BSD e illumos; sistemas alternativos e de pesquisa; plataformas móveis; sistemas embarcados e RTOS; ambientes gráficos e distribuição de aplicações; forjas, fundações e registries; segurança da cadeia de software; linguagens, toolchains, frameworks, bancos de dados e infraestrutura de aplicações.

Os links priorizam páginas oficiais de projetos, documentação, repositórios e índices de pacotes. A presença no atlas não é endosso, certificação de segurança, garantia de manutenção ou confirmação de que todos os componentes são livres. Projetos experimentais são identificados como tais; firmware, drivers, serviços, licenças mistas e dependências precisam de verificação própria.

O arquivo data/open-source-software.json contém as sementes de descoberta e um esquema versionado de metadados para enriquecimento futuro: identificadores, URL canônica, plataformas, arquiteturas, versões, licenças SPDX e escopo, componentes proprietários, dependências, governança, mantenedores, SBOM, vulnerabilidades, proveniência de build, assinatura, atualizações seguras e evidências datadas. As entradas iniciais não têm todos esses campos preenchidos; ausência significa desconhecido, não que o recurso não possua a característica.

## Freeware, cloud gratuito e infraestrutura de desenvolvimento

- Oracle Cloud Free Tier e Always Free: https://www.oracle.com/cloud/free/ e https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm
- Google Cloud Free Program: https://docs.cloud.google.com/free/docs/free-cloud-features?hl=pt-BR
- AWS Free Tier e FAQs: https://aws.amazon.com/free/ e https://aws.amazon.com/free/free-tier-faqs/
- Microsoft Azure Free Account: https://azure.microsoft.com/en-us/free/ e https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/create-free-services
- Cloudflare Workers limits: https://developers.cloudflare.com/workers/platform/limits/
- Render Free: https://render.com/docs/free
- Koyeb instances and pricing: https://www.koyeb.com/docs/reference/instances e https://www.koyeb.com/docs/faqs/pricing
- Vercel Hobby: https://vercel.com/docs/plans/hobby
- GitHub Pages limits e GitHub Actions billing: https://docs.github.com/pt/pages/getting-started-with-github-pages/github-pages-limits e https://docs.github.com/en/actions/concepts/billing-and-usage
- LibreOffice, VideoLAN VLC, 7-Zip, KeePassXC, GIMP, Blender e OBS Studio: páginas oficiais listadas em data/freeware.json.
- Microsoft PowerToys: https://learn.microsoft.com/en-us/windows/powertoys e https://github.com/microsoft/PowerToys
- Bitwarden: https://bitwarden.com/pt-br/open-source/ e https://bitwarden.com/pt-br/help/password-manager-plans/
- Microsoft Sysinternals: https://learn.microsoft.com/en-us/sysinternals/

A curadoria distingue cotas gratuitas recorrentes, créditos temporários, planos gratuitos limitados, serviços serverless e software livre. Nenhuma oferta cloud é tratada como capacidade ilimitada ou SLA de produção. Limites e elegibilidade devem ser revalidados nas fontes oficiais antes do uso.


## Expansão global de fontes

O arquivo `data/global-sources.json` contém um lote complementar de portais nacionais de dados, institutos estatísticos, infraestruturas de pesquisa, repositórios e catálogos internacionais. O lote inicial amplia a cobertura para América Latina, África, Sul, Leste e Sudeste da Ásia, Europa e Oceania, além de infraestruturas globais. Cada registro aponta para o domínio institucional ou serviço de origem. A inclusão não certifica a qualidade de cada conjunto nem concede direitos de reutilização; confirme a licença e a proveniência no registro original.

A navegação temática mantém categorias transversais e específicas. Categorias sem registros no momento permanecem disponíveis como taxonomia de descoberta e podem receber contribuições futuras. Não são apresentadas como se já contivessem fontes.


## Lote complementar de alcance internacional

O arquivo `data/global-sources.json` acrescenta 75 registros candidatos de portais nacionais de dados, institutos de estatística, infraestruturas de pesquisa e repositórios em diferentes regiões. Para evitar falsa impressão de auditoria, cada registro começa com `verification_status: candidate_unverified` e `checked_at: null`. Esses links precisam de verificação individual de destino, entidade responsável, escopo, idioma, licença e disponibilidade antes de serem classificados como verificados. A interface elimina URLs repetidas ao combinar os catálogos.


O índice compacto `search-index.json` é gerado no processo de build a partir do catálogo principal. A página inicial também carrega o catálogo canônico como fallback quando o índice servido está vazio e combina os registros complementares de `data/global-sources.json`; URLs repetidas são removidas na interface. A validação automatizada verifica separadamente o índice principal e o lote complementar.


## Contagem global de URLs

`python scripts/build_site_stats.py` gera `site-stats.json` com a contagem deduplicada de destinos HTTP(S) externos nos catálogos e links de referência das páginas especializadas. O build de publicação gera esse arquivo novamente em cada execução; a homepage lê o total em vez de manter um número estático.

## Descoberta institucional ROR

O workflow `.github/workflows/ingest-ror.yml` consulta mensalmente o registro ROR por meio do DOI conceitual do dump, que sempre aponta para a versão mais recente. O arquivo ZIP é verificado pelo checksum publicado no Zenodo antes da leitura. Cada lote seleciona até 1.000 sites oficiais listados em registros ativos, com distribuição por país e deduplicação por ROR ID e URL. Os metadados ROR são CC0 1.0; a licença do conteúdo dos sites vinculados não é presumida. Os lotes passam por pull request, validação e build antes da integração automática autorizada.
