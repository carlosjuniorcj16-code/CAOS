# CAOS Autonomous Discovery

O mecanismo de descoberta roda diariamente pelo GitHub Actions e também pode ser iniciado manualmente em **Actions → CAOS autonomous web discovery**.

## O que ele faz

1. Consulta o Wikidata Query Service para encontrar universidades, institutos de pesquisa, bibliotecas, museus, arquivos, observatórios, jardins botânicos, sociedades científicas, órgãos públicos, hospitais e escolas que declaram um site oficial.
2. Reutiliza somente metadados estruturados do Wikidata (CC0 1.0) e a URL oficial informada pela entidade.
3. Deduplica por URL e domínio em relação ao catálogo atual.
4. Consulta o robots.txt de cada site e não verifica a página inicial quando a política não permite ou não pode ser obtida.
5. Faz uma verificação HTTP leve da página inicial, com limite de requisições e sem baixar o conteúdo integral.
6. Acrescenta até 75 novos registros verificados por execução ao catálogo e abre/atualiza um pull request para revisão.

## Segurança e limites

- O crawler não copia textos, imagens, PDFs, bases de dados ou conteúdo protegido dos sites.
- A licença CC0 cobre os metadados estruturados do Wikidata; não altera os direitos dos sites vinculados.
- Redirecionamentos para outro domínio, URLs inválidas, duplicatas e sites inacessíveis são rejeitados.
- O processo é limitado a 250 verificações por execução e 75 inclusões por lote.
- O catálogo principal só muda depois que o pull request é revisado e mesclado. Isso protege os 13 mil registros existentes e evita publicar automaticamente links de baixa qualidade.
- A rotina diária depende da disponibilidade do GitHub Actions e do Wikidata Query Service; não é um processo 24/7 nem um crawler irrestrito.

## Execução manual

Use primeiro **Run workflow** com `dry_run=true`. O relatório mostra até 20 registros encontrados, contagens e motivos de rejeição. Para gerar um lote revisável, execute com `dry_run=false`.

## Arquivos

- `scripts/discover_wikidata.py`: descoberta, deduplicação e verificação.
- `.github/workflows/autonomous-discovery.yml`: agendamento diário e pull request.
- `data/sources.json`: catálogo canônico; alterado somente pelo lote aprovado.
