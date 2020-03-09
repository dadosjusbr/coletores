# Ministério Público de Pernambuco - Crawler

Este crawler tem como objetivo a recuperação de informações sobre folhas de pagamentos dos funcionários do Ministério Público de Pernambuco. O site com as informações pode ser acessado [aqui](https://transparencia.mppe.mp.br/contracheque).

O crawler está estruturado como uma CLI. Você passa dois argumentos (mês e ano) e serão baixadas oito planilhas no formato XLSX, 

## Como usar

### Executando com Docker

- Inicialmente é preciso instalar o [Docker](https://docs.docker.com/install/). 

- Construção da imagem:

```sh
docker build -t mppe .
```

- Execução:
	- Para executar é necessário passar o .env e um volume, caso deseje persistência dos dados. No .env, o campo ```OUTPUT_PATH``` indica o path relativo dentro do container. 
	- OBS: O path dos arquivos retornado no [CrawlingResult](https://github.com/dadosjusbr/storage/blob/master/agency.go) será relativo ao container. Montar o volume de dados no mesmo path para diversos containers pode ser boa prática.
	- Um arquivo .env.example na pasta raíz indica as variáveis de ambiente que precisam ser passadas para o coletor.


```sh
docker volume create dadosjus

docker run \
--mount type=bind,source="$(pwd)"/DIRETORIO_DE_SAIDA,target=/OUTPUT_DIR \
--env-file=.env \
mppe --mes=${MES} --ano=${ANO}
```

- No comando de run:
	- ```--mount source=dadosjus,target=/dadojus_crawling_output/``` monta o volume que criamos anteriormente no path "/dadojus_crawling_output/", dessa forma, qualquer coisa que salvarmos dentro desse path será persistida após  o container ser derrubado.
	- ```--env-file=.env``` especifica o path para o env-file.
	- ```mppb --mes=${MES} --ano=${ANO}``` é o nome do container que queremos executar e os argumentos que serão passados para a função de entrada.

  
### Executando sem uso do docker:

- É preciso ter o compilador de Go instalado em sua máquina. Mais informações [aqui](https://golang.org/dl/).

- Um arquivo .env.example na pasta raíz indica as variáveis de ambiente que precisam ser passadas para o coletor.
- O resultado do coletor, [CrawlingResult](https://github.com/dadosjusbr/storage/blob/master/agency.go), possui um campo que indica o commit do git usado para dar o build. Para que ele seja setado adequadamente, é precisso passar o commit como argumento do build.
 

```sh
go get
go build -ldflags "-X main.gitCommit=$(git rev-parse -1 HEAD)"
./mppb --mes=${MES} --ano=${ANO}
```


## Dicionário de Dados
