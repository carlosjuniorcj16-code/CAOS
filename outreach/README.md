# CAOS — piloto de prospecção por e-mail

## Princípios

- O catálogo é uma lista de links; estar listado **não** significa que o proprietário autorizou marketing por e-mail.
- Não coletar e-mails pessoais em massa, não adivinhar endereços e não usar bases compradas.
- Pesquisar somente contatos comerciais/institucionais publicados pelo próprio site ou contatos que deram opt-in explícito.
- Registrar a URL da página oficial onde o contato foi encontrado e a base do contato.
- Respeitar imediatamente pedidos de não contato e manter uma lista de supressão antes de qualquer nova campanha.
- A adesão de US$ 20 é opcional. A permanência do link no catálogo não depende de pagamento.
- Não enviar nada automaticamente. O modo do piloto é aprovação humana individual.

## Fluxo

1. Exportar uma amostra determinística de 100 registros, distribuída pelo catálogo:
   `python scripts/outreach_pilot.py export-sample --count 100`
2. Pesquisar manualmente a página oficial de contato de cada organização/site.
3. Preencher `contact_email`, `contact_name`, `contact_role`, `contact_source_url`, `contact_verified=yes` e `contact_basis`.
4. Usar `contact_basis=public_business_contact` somente para endereço profissional publicado para contato comercial; ou `explicit_opt_in` para consentimento documentado. Não usar contato pessoal encontrado por enriquecimento automatizado.
5. Definir `approval=approved` somente depois da revisão humana daquele destinatário.
6. Antes de gerar mensagens, publicar e revisar os termos da oferta e preencher `offer_terms_url` e `offer_terms_version` em cada linha aprovada.
7. Gerar arquivos para revisão:
   `python scripts/outreach_pilot.py build-drafts`
8. Revisar cada arquivo .eml. A ferramenta não envia e não cria rascunhos no Gmail. O envio, se autorizado depois, deve ocorrer individualmente ou em lotes pequenos, com monitoramento de respostas e descadastros.

## Campos de controle

- `contact_verified`: yes/no — confirmação manual do endereço e da sua publicação.
- `contact_source_url`: URL exata da página oficial de contato.
- `contact_basis`: `public_business_contact` ou `explicit_opt_in`.
- `approval`: pending/approved/rejected.
- `offer_terms_url` e `offer_terms_version`: termos publicados e versão aprovada.
- `status`: estado operacional; não substitui a lista de supressão.

## Limites desta primeira versão

- Não faz scraping de sites, descoberta automática de e-mails ou disparo em massa.
- Não presume que um endereço de e-mail no site autorize qualquer finalidade de marketing. A legitimidade do contato deve ser avaliada caso a caso, conforme a LGPD e as regras aplicáveis ao destinatário.
- Não promete cobertura jurídica ou técnica além do que estiver definido nos termos publicados.
- O Gmail conectado ao ChatGPT pode ser usado posteriormente para criar rascunhos, depois que os contatos forem pesquisados, validados e aprovados. Esta ferramenta local exporta .eml para inspeção; não contém credenciais nem tokens.
