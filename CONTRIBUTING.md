# Como contribuir com a CAOS

A CAOS é um diretório público e internacional de links para fontes de conhecimento e informação. Contribuições ajudam a ampliar a cobertura, corrigir registros e tornar a descoberta de fontes mais acessível.

## Fluxo de contribuição

1. Abra uma issue para propor mudanças editoriais ou discutir alterações amplas.
2. Faça suas alterações em uma branch própria.
3. Envie um Pull Request para `main`, explicando o que mudou e por quê.
4. Aguarde a revisão e a aprovação do mantenedor. Não há inclusão automática de contribuições.

Não solicite nem espere acesso de escrita ao repositório. Alterações enviadas por forks e Pull Requests são preferidas.

## Sugerir uma fonte

Cada registro em `data/sources.json` deve conter:

- `id`: número inteiro único.
- `title`: nome oficial da fonte.
- `category`: `natural`, `formal`, `social`, `health`, `engineering` ou `cross`.
- `subcategory`: campo ou finalidade específica.
- `description`: descrição factual, preferencialmente em inglês.
- `description_pt`: descrição factual em português brasileiro.
- `url`: endereço oficial ou canônico.
- `type`: tipo de recurso.
- `access`: condições de acesso conhecidas.
- `tags`: termos úteis para busca.

## Critérios de inclusão

1. Priorize fontes primárias, universidades, instituições públicas de pesquisa, bibliotecas, arquivos, periódicos e repositórios reconhecidos.
2. Verifique se o destino é relevante e se o endereço corresponde à fonte indicada.
3. Descreva o conteúdo com clareza e sem linguagem promocional.
4. Não classifique uma fonte como acesso aberto apenas porque sua página inicial é gratuita.
5. Diferencie publicações revisadas por pares de preprints e materiais não revisados.
6. Informe restrições de acesso e licenças quando conhecidas.
7. Busque diversidade geográfica, linguística e institucional.
8. Evite duplicatas, malware, downloads enganosos e fontes que facilitem atividades ilegais ou violações de privacidade.
9. Não envie dados pessoais, credenciais vazadas, registros privados ou materiais obtidos sem autorização.
10. Não use o diretório para visar, perfilar ou vigiar indivíduos privados.

## Revisão e validação

Toda alteração está sujeita à revisão. O fluxo automatizado verifica estrutura JSON, campos obrigatórios, IDs, categorias e duplicatas de URL, além da sintaxe dos scripts JavaScript embutidos em `index.html`. A aprovação automatizada não substitui a revisão humana da qualidade, legitimidade ou segurança de uma fonte.

## Idiomas

A interface está disponível em português brasileiro, inglês, espanhol, francês, alemão, italiano, chinês simplificado, japonês, russo, neerlandês, polonês, coreano, árabe, hindi e turco. As descrições do catálogo estão em português e inglês quando disponíveis. Traduções adicionais devem preservar o nome oficial e o sentido da descrição original.

A CAOS é um índice informativo, não um endosso. Cada pessoa deve avaliar as fontes em seu contexto.