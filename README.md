# CAOS — Diretório Público do Conhecimento

**Um diretório público, independente, científico e internacional de links para fontes de conhecimento e informação.**

A CAOS organiza referências para facilitar a descoberta de fontes originais: bibliotecas, arquivos, instituições de pesquisa, periódicos, bases de dados, documentos, catálogos e ferramentas. Não é proprietária dessas fontes, não certifica todo o conteúdo indicado e não representa uma orientação política, econômica ou tecnológica.

## Objetivo

Facilitar a descoberta de informação pública para estudo, ensino, pesquisa, jornalismo, consulta e investigação independente. A curadoria busca reunir recursos de diferentes países, idiomas e tradições acadêmicas, com critérios transparentes e participação aberta.

## Áreas do conhecimento

1. **Ciências naturais** — biologia, química, física, astronomia, ciências da Terra e ambientais.
2. **Ciências formais** — matemática, lógica, estatística, computação teórica e teoria dos sistemas.
3. **Ciências sociais** — sociologia, economia, antropologia, história, ciência política e estudos das sociedades.
4. **Ciências da saúde e médicas** — medicina, saúde pública, neurociência, epidemiologia e pesquisa em saúde.
5. **Engenharia e ciências aplicadas** — engenharia, robótica, materiais, infraestrutura e tecnologias.
6. **Multidisciplinares** — bibliotecas, catálogos, índices e recursos que abrangem diferentes campos.

O catálogo contém **173 fontes e recursos**: 35 em ciências naturais, 16 em ciências formais, 28 em ciências sociais, 25 em saúde e medicina, 27 em engenharia e ciências aplicadas e 42 multidisciplinares. É uma coleção em expansão, não uma lista exaustiva nem um ranking.

## Diretório de links e idiomas

A primeira versão é um site estático e pesquisável. Cada registro aponta para o endereço da fonte original. A CAOS não hospeda os materiais externos e não controla suas políticas de acesso, disponibilidade, licenciamento ou atualização.

A interface está disponível em **português brasileiro, inglês, espanhol, francês, alemão e italiano**. O português brasileiro é o idioma inicial. Os nomes oficiais das fontes são preservados; as descrições do catálogo estão sendo traduzidas progressivamente, portanto nem todo registro está disponível em todos os idiomas.

## Possíveis usos

O diretório pode apoiar pesquisa, educação, jornalismo, descoberta de dados, preservação da informação e desenvolvimento de ferramentas de consulta. Os registros estruturados também podem servir como ponto de partida para sistemas de busca, recuperação de informação e treinamento de inteligência artificial. Qualquer reutilização deve respeitar licenças, direitos autorais, privacidade, termos de uso e condições de acesso de cada fonte. Essa é uma possibilidade entre várias, não o propósito exclusivo do projeto.

## Estrutura do repositório

- `index.html` — portal estático multilíngue, com português brasileiro como padrão, busca e filtros.
- `data/sources.json` — diretório estruturado de fontes e links.
- `CONTRIBUTING.md` — orientações para contribuições e curadoria.
- `SOURCES.md` — critérios, distribuição e referências de curadoria.

## Executar localmente

```bash
python -m http.server 8000
```

Acesse `http://localhost:8000`. A versão atual não exige chave de API, backend, banco de dados ou modelo de IA.

## Publicação

O portal pode ser hospedado pelo GitHub Pages ou por qualquer serviço de hospedagem estática. Para GitHub Pages, selecione a branch `main` e a pasta raiz nas configurações do repositório.

## Princípios editoriais

- Neutralidade política, econômica, religiosa e tecnológica.
- Acesso público, pluralidade de perspectivas e alcance internacional.
- Curadoria baseada em relevância, procedência e descrição factual.
- Preferência por fontes primárias, instituições reconhecidas e repositórios estabelecidos.
- Preservação dos links originais e atribuição adequada.
- Informação clara sobre acesso, cadastro, restrições e licenças.
- Diferenciação entre artigos revisados por pares, preprints, conjuntos de dados e documentos institucionais.
- Inclusão não significa endosso nem garantia de exatidão.
- Respeito à privacidade, aos direitos autorais, aos termos de uso e à legislação aplicável.
- Não coletar credenciais, contornar controles de acesso, visar indivíduos privados ou facilitar vigilância clandestina.
- Critérios e classificações transparentes e passíveis de revisão pública.

## Situação atual

**Etapa 1 — Portal público e diretório inicial.** A coleção é um ponto de partida. Os links devem ser verificados periodicamente, e as descrições, traduções e classificações podem ser aperfeiçoadas pela comunidade.

## Licenças

O código-fonte pretende ser distribuído sob MIT. Os metadados do diretório pretendem ser reutilizáveis sob CC0 quando legalmente possível. Essas licenças não alteram as licenças nem os termos dos conteúdos de terceiros vinculados.
