# CAOS — Diretório Público do Conhecimento

**Um diretório público, independente, científico e internacional de links para fontes de conhecimento e informação.**

A CAOS é um índice aberto que aproxima o público das fontes originais: bibliotecas, arquivos, instituições de pesquisa, periódicos, bases de dados, documentos, coleções culturais, estatísticas e ferramentas de referência. O catálogo organiza caminhos de acesso; não substitui, hospeda ou certifica os conteúdos externos.

## Um catálogo em expansão

A versão atual reúne **575 fontes**, organizadas em seis áreas:

| Área | Fontes |
|---|---:|
| Ciências naturais | 134 |
| Ciências formais | 35 |
| Ciências sociais | 131 |
| Ciências da saúde e médicas | 49 |
| Engenharia e ciências aplicadas | 69 |
| Multidisciplinares | 157 |
| **Total** | **575** |

A coleção inclui fontes brasileiras e internacionais, com atenção a diferentes regiões, idiomas, tradições científicas e tipos de instituição. Não é uma lista exaustiva nem um ranking.

## Áreas do conhecimento

1. **Ciências naturais** — biologia, química, física, astronomia, ciências da Terra, ambiente e biodiversidade.
2. **Ciências formais** — matemática, lógica, estatística, computação teórica e fundamentos.
3. **Ciências sociais** — sociologia, economia, antropologia, história, ciência política, educação e estudos das sociedades.
4. **Ciências da saúde e médicas** — medicina, saúde pública, neurociência, epidemiologia e pesquisa em saúde.
5. **Engenharia e ciências aplicadas** — engenharia, robótica, materiais, infraestrutura, energia e tecnologias.
6. **Multidisciplinares** — bibliotecas, catálogos, índices, arquivos e recursos que abrangem diferentes campos.

## Idiomas

A interface está disponível em **português brasileiro, inglês, espanhol, francês, alemão, italiano, chinês simplificado, japonês e russo**. O português brasileiro é o idioma inicial. Os nomes oficiais das instituições e serviços são preservados. As descrições do catálogo estão disponíveis prioritariamente em português e inglês e passam por tradução progressiva; em outros idiomas, os títulos originais permanecem para facilitar a identificação das fontes.

## Para que serve

O diretório pode apoiar estudo, ensino, jornalismo, pesquisa independente, descoberta de dados, preservação da informação e desenvolvimento de ferramentas de consulta. Os registros estruturados também podem servir como ponto de partida para mecanismos de busca, recuperação de informação e treinamento de sistemas de inteligência artificial. Essa é uma possibilidade entre várias, não o propósito exclusivo da CAOS.

Qualquer consulta, cópia ou reutilização deve respeitar direitos autorais, licenças, privacidade, termos de uso e condições de acesso definidas por cada fonte. A inclusão no catálogo é informativa e não significa endosso.

## Estrutura do repositório

- `index.html` — portal editorial multilíngue, com português brasileiro como padrão, busca, filtros e carregamento progressivo.
- `data/sources.json` — catálogo estruturado de fontes e links.
- `CONTRIBUTING.md` — orientações para contribuições e curadoria.
- `SOURCES.md` — critérios, distribuição e referências de curadoria.

## Executar localmente

Na pasta do projeto, inicie um servidor estático:

```bash
python -m http.server 8000
```

Acesse `http://localhost:8000`. O portal não exige chave de API, backend, banco de dados ou modelo de IA.

## Publicação

O site pode ser hospedado pelo GitHub Pages ou por qualquer serviço de hospedagem estática. Para GitHub Pages, selecione a branch `main` e a pasta raiz nas configurações do repositório.

## Princípios editoriais

- Neutralidade política, econômica, religiosa e tecnológica.
- Acesso público, pluralidade de perspectivas e alcance internacional.
- Curadoria baseada em relevância, procedência e descrição factual.
- Preferência por fontes primárias, instituições reconhecidas e repositórios estabelecidos.
- Diversidade geográfica, linguística e institucional.
- Informação clara sobre acesso, cadastro, restrições e licenças.
- Diferenciação entre artigos revisados por pares, preprints, conjuntos de dados e documentos institucionais.
- Inclusão não significa endosso nem garantia de exatidão.
- Respeito à privacidade, aos direitos autorais, aos termos de uso e à legislação aplicável.
- Não coletar credenciais, contornar controles de acesso, visar indivíduos privados ou facilitar vigilância clandestina.
- Correções e classificações transparentes e passíveis de revisão pública.

## Estado do projeto

**Etapa 1 — Portal público e diretório de fontes.** O catálogo está em expansão. Links, descrições, traduções e classificações devem ser verificados e aperfeiçoados continuamente. A disponibilidade dos serviços externos pode mudar sem aviso.

## Licenças

O código-fonte pretende ser distribuído sob MIT. Os metadados do diretório pretendem ser reutilizáveis sob CC0 quando legalmente possível. Essas licenças não alteram as licenças nem os termos dos conteúdos de terceiros vinculados.
