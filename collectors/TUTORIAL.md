# Criando um um coletor de remunerações do sistema justiça

Na nomenclatura do DadosJusBR, um coletor (_crawler_) de remunerações é responsável por duas tarefas: baixar os dados do site oficial do órgão e convertê-los para o formato padronizado de [resultado de coleta](https://github.com/dadosjusbr/storage/blob/master/agency.go#L27) (_crawling result_). Para facilitar o processo de revisão, aconselhamos que separe a automação do download dos arquivos (*Craw*) e da tradução (*parsing*) em dois [PRs](https://help.github.com/pt/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request), sendo o segundo aberto depois do primeiro ter sido aprovado. Assim, acreditamos que o processo de revisão fica mais simples e rápido.

Outro esclarecimento importante é que buscamos todos os órgãos do *sistema de justiça* e não apenas do Judiciário. Também estamos interessados em órgãos regionais e federais. Isso quer dizer que é do interesse e escopo do projeto libertar remunerações de tribunais (por exemplo, TRF1, TRT13, TREPB e TJPB), Ministérios Públicos (por exemplo, MPF e MPPB), Defensorias e Procuradorias.

Feitos os devidos esclarecimentos preliminares, mãos a obra!

## Design e API

Um coletor é um [processo](https://pt.wikipedia.org/wiki/Processo_%28inform%C3%A1tica%29) com uma [API](https://pt.wikipedia.org/wiki/Interface_de_programa%C3%A7%C3%A3o_de_aplica%C3%A7%C3%B5es) específica:

A invocação do processo coletor recebe via linha de comando dois parâmetros:

- `--mes`: Mês ao qual se refere a coleta
- `--ano`: Ano ao qual se refere a coleta

E são esperadas as seguintes saídas:

- `stdout`: Em caso de sucesso, imprimir um [CrawlingResult](https://github.com/dadosjusbr/storage/blob/master/agency.go#L27) em formato JSON
- `stderr`: Em caso de sucesso, vazio. Em caso de erro, imprimir um relatório que facilite encontrar e procurar o erro
- `status`: Em caso de sucesso 0 (zero), ou diferente de 0 caso contrário

Coletores podem precisar de mais configuração além do mês e do ano da coleta. Como visto [aqui](https://github.com/dadosjusbr/coletores/tree/master/mppb) e [aqui](https://github.com/dadosjusbr/coletores/tree/master/trepb), recomendamos a utilização de [variáveis de ambiente](https://pt.wikipedia.org/wiki/Vari%C3%A1vel_de_ambiente) para esse fim, com isso deve-se ser adicionado também um arquivo .env-sample que indica quais váriaveis de ambiente devemos preencher antes de executar o coletor.

Para dar liberdade de desenvolvimento e facilitar o gerenciamento de dependências, coletores do DadosJusBR são executados em um [contêiner Docker](https://aws.amazon.com/pt/containers/?nc1=f_ccr). Um arquivo .Dockerfile deve existir em cada coletor, esse [arquivo](https://github.com/dadosjusbr/coletores/blob/master/trepb/Dockerfile) pode ser utilizado como modelo. Dentre outras vantagens, isso permite que coletores sejam escritos em diferentes linguagens, para o dadosjusbr, aceitamos contribuições em Golang e Python. Sendo assim, você pode esperar que seu coletor será executado da seguinte forma:

```sh
$ git clone https://github.com/dadosjusbr/coletores
$ cd coletores/nomeColetor
$ docker build --build-arg GIT_COMMIT=$(git rev-list -1 HEAD) -t nomeColetor .
$ docker run docker run --mount source=dadosjusbr,target=/dadosjusbr_data/ --env-file=.env nomeColetor --mes=01 --ano=2020 > nomeColetor_2020_01.json
```

Na construção da imagem `docker build`:

- `--build-arg GIT_COMMIT=$(git rev-list -1 HEAD)`: esse comando passa variáveis de ambiente que serã visíveis apenas durante a etapa de construção da imagem docker. Mais informações sobre parâmetros e variáveis de ambiente para construção de imagens docker [aqui](https://docs.docker.com/engine/reference/commandline/build/). No caso, a variável `GIT_COMMIT` conterá o hash do commit mais atual (`HEAD`).

Na execução do coletor `docker run`:

- `--mount source=dadosjus,target=/dadosjusbr_data`: monta um volume dentro do contêiner onde será executado o coletor. O objetivo desse volume é prover acesso aos arquivos baixados na coleta de fora do contêiner. Mais informações sobre volumes docker [aqui](https://docker-unleashed.readthedocs.io/aula2.html).

- `--env-file=.env`: instrui o comando `docker run` a carregar esse arquivo com variáveis de ambiente.

- `nomeColetor`: é o nome do coletor construído no comando `docker build`. Por exemplo, `trepb`.

As pessoas desenvolvedoras de coletores devem sempre ter o cuidado de setar o campo [Crawler](https://github.com/dadosjusbr/storage/blob/master/agency.go#L31). Esse campo possui atributos que identificam unicamente o coletor e a coleta. Essas informações são muito importantes pois além de facilitar a depuração/detecção de problemas, elas tornam as informações publicadas pelo DadosJusBR completamente auditáveis. A variável de ambiente `GIT_COMMIT` deve ser utilizada para setar a versão do coletor executado para extrair os dados ([Crawler.CrawlerID](https://github.com/dadosjusbr/storage/blob/master/agency.go#L22)).

Após a execução do coletor, os dados serão validados e armazenados num banco de dados do DadosJusBR. Esse banco de dados é utilizado para servir a página do [dadosjusbr](https://dadosjusbr.org/).

## FAQ

- Em que linguagens posso escrever meu coletor?

Apesar da definição da API e da utilização de contêiners Docker permitir a escrita em muitas linguagens, o time DadosJusBR optou por restringir para Python e Go. A principal razão para isso é que acreditamos que a revisão do código do coletor precisa ser feita por pessoas que tenham experiência com coletores/tradutores e também na linguagem. Isso evitará que vários problemas cheguem em produção, bem como contribuirá bastante para disseminar conhecimento.

- Preciso escrever testes para o coletor?

Sim. Testes são uma peça importantíssima para tentar diminuir a quantidade de defeitos e não seria diferente com coletores no DadosJusBR. Somado a isso, prezamos pela sanidade mental e o tempo das pessoas que gentilmente estão tentando manter as coletas executando mensalmente.
