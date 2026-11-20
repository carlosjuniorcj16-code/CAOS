# CAOS — Cúpula dos Agentes Ordenados e Sensoriais

**Um portal aberto, descentralizado e multilíngue para o conhecimento público da humanidade.**

A CAOS é uma iniciativa independente para indexar, organizar e facilitar a descoberta de fontes públicas de conhecimento. Sua primeira implementação é intencionalmente simples: um diretório pesquisável que conecta pessoas e sistemas a fontes relevantes nas cinco grandes áreas científicas.

> A CAOS é um portal, não proprietária do conhecimento. O conhecimento permanece distribuído entre as pessoas, instituições, repositórios e comunidades que o produzem.

## Missão

Melhorar a descoberta, a organização, a interoperabilidade e o reúso do conhecimento publicamente disponível. Reduzir a distância entre curiosidade e fontes confiáveis. Ajudar pessoas e sistemas de IA a navegar pelo universo informacional, preservando procedência, contexto e condições de acesso.

## Cinco áreas do conhecimento

1. **Ciências naturais** — biologia, química, física, astronomia, ciências da Terra e ambientais.
2. **Ciências formais** — matemática, lógica, estatística, ciência da computação teórica e teoria dos sistemas.
3. **Ciências sociais** — sociologia, economia, antropologia, história, ciência política e estudos dos sistemas humanos.
4. **Ciências da saúde e médicas** — medicina, saúde pública, neurociência, epidemiologia e pesquisa em saúde.
5. **Engenharia e ciências aplicadas** — disciplinas de engenharia, robótica, materiais, computação aplicada e tecnologia.

Fontes que realmente abrangem várias disciplinas podem receber a classificação **Multidisciplinares**.

## Por que começar por um diretório?

Um índice confiável é uma primeira etapa menor, mais econômica e mais simples de manter do que treinar ou operar um sistema multiagente. Posteriormente, a CAOS poderá oferecer dados estruturados e APIs para busca, recuperação de informação, agentes de pesquisa e fluxos de treinamento de IA. A versão inicial não exige chaves de API, servidor de banco de dados ou modelo de IA.

## Estrutura do repositório

- `index.html` — portal estático bilíngue (português brasileiro como padrão; inglês como segunda opção), com busca e filtros.
- `data/sources.json` — diretório estruturado de fontes, com descrições em português e inglês.
- `CONTRIBUTING.md` — orientações para contribuições e curadoria.
- `SOURCES.md` — notas sobre a seleção inicial de fontes e referências.

## Executar localmente

Abra `index.html por meio de um servidor estático local (recomendado) para que o navegador carregue `data/sources.json`. Exemplo:

```bash
python -m http.server 8000
```

Acesse `http://localhost:8000`.

Nenhuma chave de API, backend, servidor de banco de dados ou modelo de IA é necessário.

## Publicação

O portal é um site estático e pode ser hospedado pelo GitHub Pages ou por qualquer serviço de hospedagem estática. Ative o GitHub Pages nas configurações do repositório e selecione a branch `main` e a pasta raiz.

## Princípios

- Priorizar fontes legalmente acessíveis ao público.
- Software de código aberto e contribuição aberta.
- Preservar links originais e atribuição das fontes.
- Registrar ressalvas de licença e acesso; não sugerir que todo conteúdo vinculado tenha licença aberta.
- Diferenciar pesquisas revisadas por pares, preprints, conjuntos de dados, orientações institucionais e obras de referência.
- A inclusão de uma fonte não significa endosso nem garantia de exatidão.
- Priorizar fontes primárias e repositórios reconhecidos.
- Respeitar privacidade, direitos autorais, termos de uso e legislação aplicável.
- Não coletar credenciais, contornar controles de acesso, visar indivíduos privados ou facilitar vigilância clandestina. A CAOS indexa conhecimento público obtido legalmente.
- Classificações e resumos gerados por IA, quando introduzidos, devem ser rastreáveis e passíveis de revisão humana.

## Situação atual

**Etapa 1 — Portal estático e diretório inicial.** A coleção atual é um ponto de partida, não um índice exaustivo da internet. Os links devem ser verificados periodicamente e revisados pela comunidade.

## Licenças

O código-fonte da CAOS pretende ser distribuído sob a licença MIT. Os metadados do diretório pretendem ser reutilizáveis sob CC0 quando legalmente possível. Essas licenças não alteram as licenças nem os termos dos conteúdos de terceiros vinculados.
