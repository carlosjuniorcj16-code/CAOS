# CAOS — triagem automática do catálogo

O workflow **CAOS automated catalog triage** classifica os metadados dos registros do catálogo inteiro e gera `outreach/triage.csv` como artefato privado da execução do GitHub Actions (retenção de 14 dias).

## O que faz
- Lê os shards do catálogo e valida a contagem declarada no manifesto.
- Usa regras transparentes sobre título, descrição, categoria, tags, tipo e URL.
- Marca candidatos por tipo: governo, educação/cultura, comercial, organização, pessoal ou incerto.
- Exporta pontuação, sinais encontrados e status para priorização.

## O que não faz
- Não visita os sites nem procura endereços de e-mail.
- Não infere consentimento ou base legal.
- Não aprova contatos, cria mensagens ou envia e-mails.
- Uma classificação positiva é apenas uma hipótese para priorizar pesquisa; deve ser validada antes de qualquer contato.

## Execução
GitHub → Actions → **CAOS automated catalog triage** → Run workflow.
O CSV será anexado à execução como artefato, sem ser publicado no GitHub Pages ou commitado no repositório.
