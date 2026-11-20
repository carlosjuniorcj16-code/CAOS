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


## Atlas de sistemas operacionais e software open source

A página [Atlas de Software Livre](software.html) e o arquivo [data/open-source-software.json](data/open-source-software.json) reúnem **271 recursos em 11 ecossistemas**. A coleção preserva os 177 registros iniciais e adiciona recursos oficiais de sistemas operacionais, mobile/embedded, diretórios e forjas, linguagens, pacotes, ferramentas, frameworks, infraestrutura, segurança e comunidades.

Os links do JSON apontam preferencialmente para a página oficial, documentação, repositório upstream ou registro canônico. A lista abaixo destaca fontes primárias e diretórios institucionais que orientam a descoberta; ela não substitui a revisão do registro individual.

### Sistemas operacionais — Linux, GNU e distribuições

- Linux kernel: https://kernel.org/ e https://docs.kernel.org/
- Debian: https://www.debian.org/ e https://www.debian.org/doc/
- Fedora: https://fedoraproject.org/ e https://docs.fedoraproject.org/
- Arch Linux: https://archlinux.org/ e https://wiki.archlinux.org/
- Gentoo: https://www.gentoo.org/ e https://wiki.gentoo.org/
- NixOS: https://nixos.org/ e https://search.nixos.org/
- Alpine Linux: https://alpinelinux.org/ e https://wiki.alpinelinux.org/
- openSUSE: https://www.opensuse.org/ e https://doc.opensuse.org/
- Void Linux: https://voidlinux.org/ e https://docs.voidlinux.org/
- GNU Guix: https://guix.gnu.org/ e https://guix.gnu.org/manual/
- Devuan: https://www.devuan.org/
- Slackware: https://www.slackware.com/
- Ubuntu: https://ubuntu.com/ e https://help.ubuntu.com/
- Linux Mint: https://linuxmint.com/
- Qubes OS: https://www.qubes-os.org/
- Tails: https://tails.net/
- Kali Linux: https://www.kali.org/
- Rocky Linux: https://rockylinux.org/
- AlmaLinux: https://almalinux.org/
- Linux From Scratch: https://www.linuxfromscratch.org/

### Sistemas operacionais — BSD, illumos e alternativas

- FreeBSD: https://www.freebsd.org/ e https://docs.freebsd.org/
- OpenBSD: https://www.openbsd.org/
- NetBSD: https://www.netbsd.org/ e https://www.netbsd.org/ports/
- DragonFly BSD: https://www.dragonflybsd.org/
- MidnightBSD: https://www.midnightbsd.org/
- GhostBSD: https://ghostbsd.org/
- HardenedBSD: https://hardenedbsd.org/
- OPNsense: https://opnsense.org/ e https://docs.opnsense.org/
- pfSense CE: https://www.pfsense.org/
- illumos: https://illumos.org/ e https://illumos.github.io/docs/
- OpenIndiana: https://www.openindiana.org/
- OmniOS: https://omnios.org/
- SmartOS: https://smartos.org/
- Haiku: https://www.haiku-os.org/
- Redox OS: https://www.redox-os.org/
- SerenityOS: https://serenityos.org/
- ReactOS: https://reactos.org/
- FreeDOS: https://www.freedos.org/
- GNU Hurd: https://www.gnu.org/software/hurd/
- Genode: https://genode.org/
- HelenOS: https://www.helenos.org/
- MINIX 3: https://www.minix3.org/
- 9front: https://9front.org/
- AROS: https://aros.sourceforge.io/
- KolibriOS: https://kolibrios.org/
- RISC OS Open: https://www.riscosopen.org/
- Fuchsia: https://fuchsia.dev/

### Mobile, embarcados e tempo real

- Android Open Source Project: https://source.android.com/
- LineageOS: https://lineageos.org/ e https://wiki.lineageos.org/
- GrapheneOS: https://grapheneos.org/
- postmarketOS: https://postmarketos.org/
- Mobian: https://mobian.org/
- Ubuntu Touch / UBports: https://ubuntu-touch.io/ e https://docs.ubports.com/
- Zephyr Project: https://www.zephyrproject.org/ e https://docs.zephyrproject.org/
- FreeRTOS: https://www.freertos.org/
- Apache NuttX: https://nuttx.apache.org/
- RIOT OS: https://www.riot-os.org/
- RTEMS: https://www.rtems.org/
- Tock OS: https://www.tockos.org/
- seL4: https://sel4.systems/
- OpenWrt: https://openwrt.org/
- Buildroot: https://buildroot.org/
- Yocto Project: https://www.yoctoproject.org/

### Diretórios, fundações e forjas

- Free Software Directory / FSF: https://directory.fsf.org/
- GNU Software: https://www.gnu.org/software/
- Open Source Initiative: https://opensource.org/
- Apache Software Foundation: https://www.apache.org/projects/
- Eclipse Foundation: https://projects.eclipse.org/
- OW2: https://www.ow2.org/
- OpenSSF Landscape: https://landscape.openssf.org/
- CNCF Landscape: https://landscape.cncf.io/
- Open Hub: https://openhub.net/
- Repology: https://repology.org/
- Libraries.io: https://libraries.io/
- GitHub: https://github.com/
- GitLab: https://gitlab.com/
- Codeberg: https://codeberg.org/
- Forgejo: https://forgejo.org/
- Gitea: https://about.gitea.com/
- SourceHut: https://sourcehut.org/
- GNU Savannah: https://savannah.gnu.org/
- KDE Invent: https://invent.kde.org/
- GNOME GitLab: https://gitlab.gnome.org/
- freedesktop.org: https://gitlab.freedesktop.org/
- Linux kernel Git: https://git.kernel.org/

### Linguagens, runtimes e registros de pacotes

- Python: https://www.python.org/ e https://docs.python.org/3/
- Rust: https://www.rust-lang.org/ e https://doc.rust-lang.org/
- Go: https://go.dev/ e https://go.dev/doc/
- OpenJDK: https://openjdk.org/
- C / GCC: https://gcc.gnu.org/
- C++: https://isocpp.org/ e https://en.cppreference.com/w/
- Julia: https://julialang.org/
- Ruby: https://www.ruby-lang.org/
- PHP: https://www.php.net/
- Perl: https://www.perl.org/
- Haskell: https://www.haskell.org/
- OCaml: https://ocaml.org/
- Elixir: https://elixir-lang.org/
- Erlang/OTP: https://www.erlang.org/
- Lua: https://www.lua.org/
- R: https://www.r-project.org/
- Zig: https://ziglang.org/
- Nim: https://nim-lang.org/
- Swift: https://www.swift.org/
- Kotlin: https://kotlinlang.org/
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
- Go Packages: https://pkg.go.dev/
- pub.dev: https://pub.dev/
- CRAN: https://cran.r-project.org/
- Conda-forge: https://conda-forge.org/
- Homebrew: https://brew.sh/
- Flathub: https://flathub.org/
- AUR: https://aur.archlinux.org/
- Nixpkgs: https://github.com/NixOS/nixpkgs
- vcpkg: https://vcpkg.io/
- Conan Center: https://conan.io/center

### Toolchains, frameworks e infraestrutura

- GCC: https://gcc.gnu.org/
- LLVM/Clang: https://llvm.org/ e https://clang.llvm.org/
- Eclipse Temurin: https://adoptium.net/temurin/
- .NET: https://dotnet.microsoft.com/
- CMake: https://cmake.org/
- Meson: https://mesonbuild.com/
- Ninja: https://ninja-build.org/
- Bazel: https://bazel.build/
- GNU Make: https://www.gnu.org/software/make/
- Gradle: https://gradle.org/
- Apache Maven: https://maven.apache.org/
- Qt: https://www.qt.io/
- GTK: https://www.gtk.org/
- wxWidgets: https://www.wxwidgets.org/
- React: https://react.dev/
- Vue: https://vuejs.org/
- Angular: https://angular.dev/
- Svelte: https://svelte.dev/
- Electron: https://www.electronjs.org/
- Tauri: https://tauri.app/
- Flutter: https://flutter.dev/
- Django: https://www.djangoproject.com/
- Flask: https://flask.palletsprojects.com/
- FastAPI: https://fastapi.tiangolo.com/
- Ruby on Rails: https://rubyonrails.org/
- Laravel: https://laravel.com/
- Symfony: https://symfony.com/
- Spring: https://spring.io/projects/spring-framework
- Quarkus: https://quarkus.io/
- ASP.NET Core: https://dotnet.microsoft.com/apps/aspnet
- Node.js: https://nodejs.org/
- Deno: https://deno.com/
- Bun: https://bun.sh/
- PostgreSQL: https://www.postgresql.org/
- MariaDB: https://mariadb.org/
- SQLite: https://sqlite.org/
- Valkey: https://valkey.io/
- ClickHouse: https://clickhouse.com/
- DuckDB: https://duckdb.org/
- Apache Cassandra: https://cassandra.apache.org/
- Apache CouchDB: https://couchdb.apache.org/
- OpenSearch: https://opensearch.org/
- Ceph: https://ceph.io/
- OpenZFS: https://openzfs.org/
- Kubernetes: https://kubernetes.io/
- containerd: https://containerd.io/
- Podman: https://podman.io/
- Buildah: https://buildah.io/
- Moby: https://mobyproject.org/
- QEMU: https://www.qemu.org/
- KVM: https://www.linux-kvm.org/
- Xen: https://xenproject.org/
- Incus: https://linuxcontainers.org/incus/
- OpenTofu: https://opentofu.org/
- Ansible: https://www.ansible.com/
- OpenStack: https://www.openstack.org/
- Apache HTTP Server: https://httpd.apache.org/
- nginx: https://nginx.org/
- HAProxy: https://www.haproxy.org/
- Caddy: https://caddyserver.com/
- Traefik: https://traefik.io/traefik/
- Prometheus: https://prometheus.io/
- Grafana OSS: https://grafana.com/oss/
- OpenTelemetry: https://opentelemetry.io/
- Zabbix: https://www.zabbix.com/

### Segurança, SBOM, integridade e licenças

- OpenSSF Scorecard: https://scorecard.dev/
- OSV.dev: https://osv.dev/
- OSV-Scanner: https://google.github.io/osv-scanner/
- Trivy: https://trivy.dev/
- Syft: https://github.com/anchore/syft
- Grype: https://github.com/anchore/grype
- Sigstore: https://www.sigstore.dev/
- SLSA: https://slsa.dev/
- SPDX: https://spdx.dev/
- CycloneDX: https://cyclonedx.org/
- REUSE: https://reuse.software/
- The Update Framework (TUF): https://theupdateframework.io/
- in-toto: https://in-toto.io/
- OpenChain: https://openchainproject.org/
- FOSSology: https://www.fossology.org/
- GNU Licenses: https://www.gnu.org/licenses/
- Choose a License: https://choosealicense.com/

O esquema `record_schema` do JSON define os campos necessários para enriquecimento futuro: licença SPDX e escopo, estado de manutenção, plataformas e arquiteturas suportadas, componentes proprietários, dependências, SBOM, vulnerabilidades, proveniência de build, assinatura, atualização segura, governança, mantenedores e evidências. A coleção atual ainda contém sementes de descoberta; ausência de um campo significa desconhecido, não que o projeto não tenha aquela propriedade.

A licença do projeto não necessariamente cobre plugins, dependências, dados, assets, marcas, firmware, drivers, codecs, documentação ou todos os componentes de uma distribuição. Para análise de conformidade, use os arquivos de licença e avisos da versão exata, além dos metadados de dependências e SBOM. O atlas não é uma lista exaustiva de todos os sistemas operacionais nem de todos os projetos open source existentes; é uma base ampla, estruturada para expansão contínua.
