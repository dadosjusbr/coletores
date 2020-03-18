# Criando um um coletor de remunerações do sistema justiça

Um esclarecimento importante é que o coletor de remunerações não apenas coleta. Também é responsabilidade do coletor traduzir o conteúdo dos arquivos baixados em um [resultado de coleta](https://github.com/dadosjusbr/storage/blob/master/agency.go#L27). Isso não quer dizer que a pessoa que decidir contribuir precisa criar um único [PR](https://help.github.com/pt/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request) com a coleta e tradução, pelo contrário. Nós recomendamos que a funcionalidade seja enviada para revisão em, pelo menos, duas etapas.

Outro esclarecimento importante é que o DadosJusBR se refere a órgãos do *sistema de justiça* e não apenas do judiciário. Também estamos interessados em órgãos regionais e federais. Isso quer dizer que é do interesse e escopo do projeto libertar remunerações de tribunais (por exemplo, TRF1, TRT13, TREPB e TJPB), Ministérios Públicos (por exemplo, MPF e MPPB), Defensorias e Procuradorias.

Feitos os devidos esclarecimentos preliminares, mãos a obra!

## Design e API

Um coletor é um [processo](https://pt.wikipedia.org/wiki/Processo_(inform%C3%A1tica) com uma [API](https://pt.wikipedia.org/wiki/Interface_de_programa%C3%A7%C3%A3o_de_aplica%C3%A7%C3%B5es) específica:

A invocação do processo coletor recebe via linha de comando dois parâmetros:

- `--mes`: Mês ao qual se refere a coleta
- `--ano`: Ano ao qual se refere a coleta

E são esperadas as seguintes saídas:

- `stdout`: Em caso de sucesso, imprimir um [CrawlingResult](https://github.com/dadosjusbr/storage/blob/master/agency.go#L27) em formato JSON
- `stderr`: Em caso de sucesso, vazio. Em caso de erro, imprimir um relatório que facilite encontrar e procurar o erro
- `status`: Em caso de sucesso 0 (zero), ou diferente de 0 caso contrário

Coletores podem precisar de mais configuração além do mês e do ano da coleta. Como visto [aqui](https://github.com/dadosjusbr/coletores/tree/master/mppb) e [aqui](https://github.com/dadosjusbr/coletores/tree/master/trepb), recomendamos a utilização de [variávias de ambiente](https://pt.wikipedia.org/wiki/Vari%C3%A1vel_de_ambiente) para esse fim.

Para dar liberdade de desenvolvimento e facilitar o gerenciamento de dependências, coletores do DadosJusBR são executados em um [contêiner Docker](https://aws.amazon.com/pt/containers/?nc1=f_ccr). Dentre outras vantagens, isso permite que coletores sejam escritos diferentes linguagens. Sendo assim, você pode esperar que seu coletor será executado da seguinte forma:

```sh
$ git clone https://github.com/dadosjusbr/coletores
$ cd coletores/nomeColetor
$ docker build --build-arg GIT_COMMIT=$(git rev-list -1 HEAD) -t nomeColetor .
$ docker run docker run --mount source=dadosjus,target=/dadojusbr_data/ --env-file=.env nomeColetor --mes=01 --ano=2020 > nomeColetor_2020_01.json
```

## FAQ

- Em que linguagens posso escrever meu coletor?

Apesar da definição da API e da utilização de contêiners Docker permitir a escrita em muitas linguagens, o time DadosJusBR optou por restringir para Python e Go. As razões para isso é que acreditamos que a revisão do código do coletor precisa ser feita por uma pessoa que tenha experiência com coletores/tradutores e também na linguagem. Isso evitará vários.

- Preciso escrever testes para o coletor?

Sim. Testes são uma peça importantíssima para tentar diminuir a quantidade de defeitos e não seria diferente com coletores no DadosJusBR. Somado a isso, prezamos pela sanidade mental e o tempo das pessoas que gentilmente estão tentando manter as coletas executando mensalmente.
