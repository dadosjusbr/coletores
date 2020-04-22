# Ministério Público da Paraíba - Crawler

Este crawler tem como objetivo a recuperação de informações sobre folhas de pagamentos dos funcionários do Ministério Público da Paraíba. O site com as informações pode ser acessado [aqui](http://pitagoras.mppb.mp.br/PTMP/FolhaListar).

O crawler está estruturado como uma CLI. Você passa dois argumentos (mês e ano) e serão baixadas oito planilhas no formato ODS, cada planilha é referente a uma destas categorias: 

- Tipo I - Folha de remunerações: Membros Ativos, Membros Inativos, Servidores Ativos, Servidores Inativos, Servidores à Disposição,  Aposentados/Pensionistas, Estagiários. 

- Tipo II - Verbas Referentes à exercícios anteriores.

- Tipo III - Verbas Indenizatórias e outras remunerações temporárias.

As planilhas estão de acordo com a resolução [89/2012 do CNMP] (http://www.cnmp.mp.br/portal/atos-e-normas/norma/795/). O formato das planilhas segue o definido no anexo desta resolução, com pequenas diferenças .

## Como usar

### Executando com Docker

- Inicialmente é preciso instalar o [Docker](https://docs.docker.com/install/). 

- Construção da imagem:

```sh
docker build --build-arg GIT_COMMIT=$(git rev-list -1 HEAD) -t mppb .
```

- Execução:
	- Para executar é necessário passar o .env e um volume, caso deseje persistência dos dados. No .env, o campo ```OUTPUT_PATH``` indica o path relativo dentro do container. 
	- OBS: O path dos arquivos retornado no [CrawlingResult](https://github.com/dadosjusbr/storage/blob/master/agency.go) será relativo ao container. Montar o volume de dados no mesmo path para diversos containers pode ser boa prática.
	- Um arquivo .env.example na pasta raíz indica as variáveis de ambiente que precisam ser passadas para o coletor.


```sh
docker volume create dadosjus
docker run \
--mount source=dadosjus,target=/dadojus_crawling_output/ \
--env-file=.env \
mppb --mes=${MES} --ano=${ANO}
```

- ```docker volume create dadosjus``` cria um volume local que pode ser usado pelos containers com o nome "dadosjus".
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

As planilhas possuem as seguintes colunas:

- **Nome (String)**: Nome completo do funcionário
- **Matrícula (String)**: Matrícula do funcionário  
- **Cargo (String)**: Cargo do funcionário dentro do MP
- **Lotação (String)**: Local (cidade, departamento, promotoria) em que o funcionário trabalha
- **Remuneração do cargo efetivo (Number)**: Vencimento, GAMPU, V.P.I, Adicionais de Qualificação, G.A.E e G.A.S, além de outras desta natureza. Soma de todas essas remunerações
- **Outras Verbas Remuneratórias, Legais ou Judiciais (Number)**: V.P.N.I., Adicional por tempo de serviço, quintos, décimos e vantagens decorrentes de sentença judicial ou extensão administrativa
- **Função de Confiança ou Cargo em Comissão (Number)**: Rubricas que representam a retribuição paga pelo exercício de função (servidor efetivo) ou remuneração de cargo em comissão (servidor sem vínculo ou requisitado)
- **Gratificação Natalina (Number)**: Parcelas da Gratificação Natalina (13º) pagas no mês corrente, ou no caso de vacância ou exoneração do servidor
- **Férias - ⅓ Constitucional (Number)**: Adicional correspondente a 1/3 (um terço) da remuneração, pago ao servidor por ocasião das férias
- **Abono de Permanência (Number)**:  Valor equivalente ao da contribuição previdenciária, devido ao funcionário público que esteja em condição de aposentar-se, mas que optou por continuar em atividade (instituído pela Emenda Constitucional nº 41, de 16 de dezembro de 2003
- **Total de Rendimentos Brutos (Number)**: Total dos rendimentos brutos pagos no mês
- **Contribuição Previdenciária (Number)**: Contribuição Previdenciária Oficial (Plano de Seguridade Social do Servidor Público e Regime Geral de Previdência Social)
- **Imposto de Renda (Number)**: Imposto de Renda Retido na Fonte
- **Retenção por Teto Constitucional (Number)**: Valor deduzido da remuneração básica bruta, quando esta ultrapassa o teto constitucional, nos termos da legislação correspondente
- **Total de Descontos (Number)**:  Total dos descontos efetuados no mês
- **Rendimento Líquido Total (Number)**: Rendimento líquido após os descontos referidos nos itens anteriores
- **Indenizações (Number)**: Auxílio-alimentação, Auxílio-transporte, Auxílio-Moradia, Ajuda de Custo e outras dessa natureza, exceto diárias, que serão divulgadas no Portal da Transparência. Soma de todas essas remunerações
- **Outras Remunerações Temporárias (Number)**: Valores pagos a título de Adicional de Insalubridade ou de Periculosidade, Adicional Noturno, Serviço Extraordinário, Substituição de Função, 'Atrasados'. Soma de todas essas remunerações

## Planilhas

- Lista de planilhas: [http://pitagoras.mppb.mp.br/PTMP/FolhaListar](http://pitagoras.mppb.mp.br/PTMP/FolhaListar)
  
### Tipo 1 - Remunerações ###

- **URL Base**: [http://pitagoras.mppb.mp.br/PTMP/FolhaPagamentoExercicioMesNewOds](http://pitagoras.mppb.mp.br/PTMP/FolhaPagamentoExercicioMesNewOds)
- **Parâmetros da url**: exercicio=[ano]&mes=[mes]&tipo=[Membros Ativos (*1*), Membros Inativos (*2*), Servidores Ativos (*3*), Servidores Inativos (*4*), Servidores à Disposição (*5*), Aposentados/Pensionistas (*6*)]
 - [Exemplo](http://pitagoras.mppb.mp.br/PTMP/FolhaPagamentoExercicioMesNewOds?mes=1&exercicio=2019&tipo=1)
- **Formato da tabela:** [Tipo I](http://www.cnmp.mp.br/portal/images/Resolucoes/Anexo-200---RES-89.pdf)

#### Tabela de remuneração de estagiários:  
- **URL Base**: [http://pitagoras.mppb.mp.br/PTMP/FolhaPagamentoEstagiarioExercicioMesOds?](http://pitagoras.mppb.mp.br/PTMP/FolhaPagamentoEstagiarioExercicioMesOds?)
- **Parâmetros da url**: exercicio=[ano]&mes=[mes]
	- [Exemplo](http://pitagoras.mppb.mp.br/PTMP/FolhaPagamentoEstagiarioExercicioMesOds?mes=1&exercicio=2019)
- **Formato da tabela:**  [Tipo I](http://www.cnmp.mp.br/portal/images/Resolucoes/Anexo-200---RES-89.pdf) com algumas diferenças de nomenclatura:
	- Remuneração de cargo efetivo: Remuneração
	- Função de Confiança ou Cargo em Comissão: Função de Confiança
	- Gratificação Natalina: 13º Vencimento 
	- Férias (⅓ constitucional): Adicional de Férias (Constitucional)

### Tipo 2 - Verbas referentes à exercícios anteriores ### 
- **URL Base**:[http://pitagoras.mppb.mp.br/PTMP/FolhaExercicioAnteriorMesNewOds?](http://pitagoras.mppb.mp.br/PTMP/FolhaExercicioAnteriorMesNewOds?)
- **Parâmetros da url:** exercicio=[ano]&mes=[mes]
	- [Exemplo](http://pitagoras.mppb.mp.br/PTMP/FolhaExercicioAnteriorMesNewOds?mes=1&exercicio=2019)
- **Formato da tabela:** [Tipo II](http://www.cnmp.mp.br/portal/images/Resolucoes/Anexo-200---RES-89.pdf) com algumas diferenças:
	- Campos inexistentes:
		- Valor bruto/Líquido
		- Campos referentes a descontos.
		- Cargo e lotação do funcionário.
	- Campos adicionais:
		- Valor recebido (Parcela)
		- Valor total remanescente a receber
		- Número de parcelas restantes a receber

### Tipo 3 - Tabela de Indenizações ### 
- **URL Base**:[https://pitagoras.mppb.mp.br/PTMP/FolhaVerbaIndenizRemTemporariaOds?](https://pitagoras.mppb.mp.br/PTMP/FolhaVerbaIndenizRemTemporariaOds?mes=1&exercicio=2019)
- **Parâmetros da url:** exercicio=[ano]&mes=[mes]
	- [Exemplo](https://pitagoras.mppb.mp.br/PTMP/FolhaVerbaIndenizRemTemporariaOds?mes=1&exercicio=2019)
- **Formato da tabela:** [Tipo III](http://www.cnmp.mp.br/portal/images/Resolucoes/Anexo-200---RES-89.pdf)
- **Obs**: Indenizações disponíveis apenas para o ano de 2019.

## Dificuldades para libertação dos dados

- Não há API para acesso aos dados
