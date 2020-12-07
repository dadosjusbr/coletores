# Tribunal de Justiça do Estado da Bahia (TJ-BA)

Este crawler tem como objetivo a recuperação de informações sobre folhas de pagamentos
dos funcionários do Tribunal de Justiça do Estado da Bahia (TJ-BA). O site com as informações
pode ser acessado [aqui](https://transparencia.tjba.jus.br/transparencia/home#).

O crawler está estruturado como uma CLI. Você passa dois argumentos (mês e ano) e é baixado um
arquivo no formato **JSON** representando a folha de pagamento da instituição.

## Legislação

Os dados devem estar de acordo com a [Resolução 102 do CNJ](https://atos.cnj.jus.br/atos/detalhar/69).
O site com a resolução pode não funcionar caso você esteja acessando de fora do Brasil.

## Como usar

### Executando com Docker

- Inicialmente é preciso instalar o [Docker](https://docs.docker.com/install/). 

- Construção da imagem:

```sh
docker build --build-arg GIT_COMMIT=$(git rev-list -1 HEAD) -t tjba .
```

- Execução:
	- Para executar é necessário passar o `.env` e um volume, caso deseje persistência dos dados.
	No .env, o campo `OUTPUT_PATH` indica o path relativo dentro do container. 
	- OBS: O path dos arquivos retornado no [CrawlingResult](https://github.com/dadosjusbr/storage/blob/master/agency.go)
	será relativo ao container. Montar o volume de dados no mesmo path para diversos containers pode ser boa prática.
	- Um arquivo `.env.example` na pasta raiz indica as variáveis de ambiente que precisam ser passadas para o coletor.


```sh
docker volume create dadosjus

docker run \
--mount source=dadosjus,target=/dadojus_crawling_output/ \
--env-file=.env \
tjba --mes=${MES} --ano=${ANO}
```

- `docker volume create dadosjus` cria um volume local que pode ser usado pelos containers com o nome "dadosjus".
- No comando de run:
	- `--mount source=dadosjus,target=/dadojus_crawling_output/` monta o volume que criamos anteriormente
	no path `/dadojus_crawling_output/`, dessa forma, qualquer coisa que salvarmos dentro desse path será persistida
	após o container ser derrubado.
	- `--env-file=.env` especifica o path para o env-file.
	- `tjba --mes=${MES} --ano=${ANO}` é o nome do container que queremos executar e os argumentos que serão
	passados para a função de entrada.
  
### Executando sem uso do Docker

É preciso ter o compilador de Go instalado em sua máquina. Mais informações [aqui](https://golang.org/dl/).

- Um arquivo ``.env.example` na pasta raiz indica as variáveis de ambiente que precisam ser passadas para o coletor.
- O resultado do coletor, [CrawlingResult](https://github.com/dadosjusbr/storage/blob/master/agency.go), possui um
campo que indica o commit do git usado para dar o build. Para que ele seja setado adequadamente, é preciso passar o
commit como argumento do build.

```sh
go get
go build -ldflags "-X main.gitCommit=$(git rev-parse -1 HEAD)"
./tjba --mes=${MES} --ano=${ANO}
```

## Dicionário de Dados

Para cada funcionário, o JSON possui os seguintes campos:

- **Id (Number)**: Matrícula do funcionário
- **Nome (String)**: Nome completo do funcionário
- **Lotação (String)**: Local (cidade, departamento, promotoria) em que o funcionário trabalha (Capítulo 2 - § 2º - I)
- **Cargo (String)**: Cargo do funcionário dentro do tribunal (Capítulo 2 - § 2º - I)
- **Rendimentos:**
	- **Remuneração Paradigma (Number)**: Remuneração do cargo efetivo - Vencimento, G.A.J., V.P.I, Adicionais de Qualificação, G.A.E e G.A.S, além de outras desta natureza. (Capítulo 2 - § 2º - II)
	- **Vantagens Pessoais (Number)**: V.P.N.I., Adicional por tempo de serviço, quintos, décimos e vantagens decorrentes de sentença judicial ou extensão administrativa, abono de permanência. (Capítulo 2 - § 2º - III)
	- **Subsídio (Number)**: Rubricas que representam a retribuição paga pelo exercício de função (servidor efetivo) ou remuneração de cargo em comissão (servidor sem vínculo ou requisitado). (Capítulo 2 - § 2º - IV)
	- **Indenizações (Number)**: Auxílio-alimentação, Auxílio-transporte, Auxílio Pré-escolar, Auxílio Saúde, Auxílio Natalidade, Auxílio Moradia, Ajuda de Custo, além de outras desta natureza. (Capítulo 2 - § 2º - V)
	- **Vantagens Eventuais (Number)**: Abono constitucional de 1/3 de férias, indenização de férias, antecipação de férias, gratificação natalina, antecipação de gratificação natalina, serviço extraordinário, substituição, pagamentos retroativos, além de outras desta natureza. (Capítulo 2 - § 2º - VI)
	- **Gratificações (Number)**
	- **Total de Créditos (Number)**: Total dos rendimentos pagos no mês. (Capítulo 2 - § 2º - VIII)
- **Descontos:**
	- **Contribuição Previdenciária (Number)**: Contribuição Previdenciária Oficial (Plano de Seguridade Social do Servidor Público e Regime Geral de Previdência Social).
	- **Imposto de Renda (Number)**: Imposto de Renda Retido na Fonte.
	- **Descontos Diversos**: Cotas de participação de auxílio pré-escolar, auxílio transporte e demais descontos extraordinários de caráter não pessoal.
	- **Retenção por Teto Constitucional (Number)**: Valores retidos por excederem ao teto remuneratório constitucional conforme Resoluções nº 13 e 14, do CNJ. (Capítulo 2 - § 2º - IX)
	- **Total de Debitos (Number)**:  Total dos descontos efetuados no mês.
- **Rendimento Líquido (Number)**: Rendimento líquido após os descontos referidos nos itens anteriores.
- **Remuneração do órgão de origem (Number)**: Remuneração percebida no órgão de origem por magistrados e servidores, cedidos ou requisitados, optantes por aquela remuneração. (Capítulo 2 - § 2º - VII)
- **Diárias**:  Valor de diárias efetivamente pago no mês de referência, ainda que o período de afastamento se estenda para além deste. (Capítulo 2 - § 2º - X)

## Arquivos
  
### Remunerações

O acesso pode ser feito a partir de uma API:

- **URL Base**: [https://transparencia.tjba.jus.br/transparencia/api/v1/remuneracao/ano/<ano>/mes/<mes>](https://transparencia.tjba.jus.br/transparencia/api/v1/remuneracao/ano/2020/mes/1)
- **Formato**: JSON

## Dificuldades para libertação dos dados

* Embora os campos `vantagensPessoais` e `vantagensEventuais` apareçam como listas no _payload_
não foi encontrado nenhum valor na amostra investigada.
