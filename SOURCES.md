# Curadoria de fontes

O catálogo reúne **13.519 fontes e recursos**, distribuídos em **67 categorias temáticas com registros** de diferentes países, idiomas e áreas. CAOS funciona como um diretório amplo: as categorias ajudam a navegar, mas não limitam os assuntos que podem ser incluídos.

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

- UNESCO — Open Science: https://www.unesco.org/en/open-science
- IBICT — Repositórios e Ciência Aberta: https://www.gov.br/ibict/pt-br/atuacao/pesquisa-servicos-e-iniciativas/repositorios-e-ciencia-aberta
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

- MADLAD-400 — https://huggingface.co/datasets/allenai/MADLAD-400
- FLORES-200 — https://huggingface.co/datasets/facebook/flores
- FLEURS — https://huggingface.co/datasets/google/fleurs
- MMLU — https://huggingface.co/datasets/cais/mmlu
- SWE-bench — https://github.com/SWE-bench/SWE-bench
- Mozilla Common Voice — https://commonvoice.mozilla.org/terms/en.html

As descrições de licença no catálogo são resumos de orientação, não pareceres jurídicos. Confirme a licença da versão, dos arquivos e dos materiais de origem antes de baixar, redistribuir ou usar em treinamento.


## Atlas de Software Livre e Open Source

O atlas em `software.html` e os registros de `data/open-source-software.json` são uma curadoria de descoberta, não uma certificação. A primeira versão contém 226 referências em oito frentes: sistemas operacionais, diretórios e forjas, linguagens e registros de pacotes, ferramentas de desenvolvimento, frameworks, infraestrutura, segurança/licenças e comunidades/documentação.

### Sistemas operacionais e plataformas

- Linux kernel e documentação: https://kernel.org/ e https://docs.kernel.org/
- Debian: https://www.debian.org/ e https://www.debian.org/doc/
- Fedora: https://fedoraproject.org/ e https://docs.fedoraproject.org/
- Arch Linux: https://archlinux.org/ e https://wiki.archlinux.org/
- Gentoo: https://www.gentoo.org/ e https://wiki.gentoo.org/
- NixOS: https://nixos.org/
- Alpine Linux: https://alpinelinux.org/
- openSUSE: https://www.opensuse.org/
- GNU Guix: https://guix.gnu.org/
- FreeBSD: https://www.freebsd.org/
- OpenBSD: https://www.openbsd.org/
- NetBSD: https://www.netbsd.org/
- DragonFly BSD: https://www.dragonflybsd.org/
- illumos e documentação: https://illumos.org/ e https://illumos.github.io/docs/
- OpenIndiana: https://www.openindiana.org/
- Haiku: https://www.haiku-os.org/
- Redox OS: https://www.redox-os.org/
- ReactOS: https://reactos.org/
- GNU Hurd: https://www.gnu.org/software/hurd/
- Genode: https://genode.org/
- 9front: https://9front.org/
- Android Open Source Project: https://source.android.com/
- LineageOS: https://lineageos.org/
- GrapheneOS: https://grapheneos.org/
- postmarketOS: https://postmarketos.org/
- Zephyr: https://www.zephyrproject.org/
- FreeRTOS: https://www.freertos.org/
- Apache NuttX: https://nuttx.apache.org/
- RIOT OS: https://www.riot-os.org/
- RTEMS: https://www.rtems.org/
- seL4: https://sel4.systems/
- OpenWrt: https://openwrt.org/
- Buildroot: https://buildroot.org/
- Yocto Project: https://www.yoctoproject.org/

### Diretórios, forjas e governança de projetos

- Free Software Directory (FSF): https://directory.fsf.org/
- GNU Software: https://www.gnu.org/software/
- Open Source Initiative: https://opensource.org/
- OpenSSF Landscape: https://landscape.openssf.org/
- CNCF Landscape: https://landscape.cncf.io/
- Apache Software Foundation Projects: https://www.apache.org/projects/
- Eclipse Projects: https://projects.eclipse.org/
- OW2: https://www.ow2.org/
- Codeberg / Forgejo: https://codeberg.org/ e https://forgejo.org/
- SourceHut: https://sourcehut.org/
- GNU Savannah: https://savannah.gnu.org/
- KDE Invent: https://invent.kde.org/
- GNOME GitLab: https://gitlab.gnome.org/
- freedesktop.org: https://gitlab.freedesktop.org/

### Linguagens, bibliotecas e distribuição

- Python: https://www.python.org/
- Rust: https://www.rust-lang.org/
- Go: https://go.dev/
- OpenJDK: https://openjdk.org/
- GCC: https://gcc.gnu.org/
- LLVM/Clang: https://llvm.org/
- Julia: https://julialang.org/
- Ruby: https://www.ruby-lang.org/
- PHP: https://www.php.net/
- Haskell: https://www.haskell.org/
- OCaml: https://ocaml.org/
- Elixir: https://elixir-lang.org/
- Zig: https://ziglang.org/
- PyPI: https://pypi.org/
- npm: https://www.npmjs.com/
- crates.io: https://crates.io/
- Maven Central: https://central.sonatype.com/
- NuGet: https://www.nuget.org/
- RubyGems: https://rubygems.org/
- Packagist: https://packagist.org/
- CPAN: https://www.cpan.org/
- Hackage: https://hackage.haskell.org/
- Hex: https://hex.pm/
- pub.dev: https://pub.dev/
- CRAN: https://cran.r-project.org/
- Conda-forge: https://conda-forge.org/
- Repology: https://repology.org/
- Libraries.io: https://libraries.io/

### Toolchains, frameworks e infraestrutura

- CMake: https://cmake.org/
- Meson: https://mesonbuild.com/
- Ninja: https://ninja-build.org/
- Bazel: https://bazel.build/
- Qt: https://www.qt.io/
- GTK: https://www.gtk.org/
- React: https://react.dev/
- Vue: https://vuejs.org/
- Angular: https://angular.dev/
- Svelte: https://svelte.dev/
- Django: https://www.djangoproject.com/
- FastAPI: https://fastapi.tiangolo.com/
- Ruby on Rails: https://rubyonrails.org/
- Laravel: https://laravel.com/
- Spring: https://spring.io/projects/spring-framework
- PostgreSQL: https://www.postgresql.org/
- MariaDB: https://mariadb.org/
- SQLite: https://sqlite.org/
- DuckDB: https://duckdb.org/
- Valkey: https://valkey.io/
- OpenSearch: https://opensearch.org/
- Ceph: https://ceph.io/
- OpenZFS: https://openzfs.org/
- Kubernetes: https://kubernetes.io/
- Podman: https://podman.io/
- QEMU: https://www.qemu.org/
- OpenStack: https://www.openstack.org/
- OpenTofu: https://opentofu.org/
- Ansible: https://www.ansible.com/
- Prometheus: https://prometheus.io/
- Grafana OSS: https://grafana.com/oss/
- OpenTelemetry: https://opentelemetry.io/

### Segurança, SBOM e licenças

- OpenSSF Scorecard: https://scorecard.dev/
- OSV.dev: https://osv.dev/
- Trivy: https://trivy.dev/
- Syft: https://github.com/anchore/syft
- Grype: https://github.com/anchore/grype
- Sigstore: https://www.sigstore.dev/
- SLSA: https://slsa.dev/
- SPDX: https://spdx.dev/
- CycloneDX: https://cyclonedx.org/
- REUSE: https://reuse.software/
- Licenças GNU: https://www.gnu.org/licenses/
- Choose a License: https://choosealicense.com/

Os links apontam para projetos e documentação oficial sempre que possível. A licença do projeto não necessariamente cobre plugins, dependências, dados, assets, marcas, firmware ou todos os componentes de uma distribuição. Para análise de conformidade, use os arquivos de licença e avisos da versão exata, além dos metadados de dependências e SBOM. O atlas não é uma lista exaustiva de todos os sistemas operacionais nem de todos os projetos open source existentes; é uma base inicial ampla, estruturada para expansão contínua.
