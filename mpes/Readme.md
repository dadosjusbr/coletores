# Ministério Público do Estado do Espírito Santo

Este coletor tem como objetivo a recuperação de informações sobre folhas de pagamentos dos funcionários do Ministério Público do Estado do Espírito Santo. O site com as informações pode ser acessado [aqui](https://www.mpes.mp.br/transparencia/informacoes/Contracheque/Remuneracao_de_Todos_os_Membros_Ativos.asp).

O coletor será estruturado como uma CLI. Uma vez passado como argumentos mês e ano, será feito o download de duas planilhas no formato XLSX. Cada planilha é referente a uma dessas categorias:

- Tipo I - Folha de remuneração: Membros Ativos

- Tipo II - Verbas Indenizatórias e outras remunerações temporárias referentes há membros ativos.

# Coletando usando Docker

Por exemplo, para coletar o mês de novembro de 2020, basta executar os seguintes comandos:

```sh
$ sudo docker build -t mpes .
sudo docker run -e MONTH=11 -e YEAR=2020 -e GIT_COMMIT=$(git rev-parse HEAD) -e OUTPUT_FOLDER='/output' mpes
```
# Dicionário de dados

As planilhas referentes á remunerações possuem as seguintes colunas:

- **Nome (String)**: Nome completo do funcionário
- **Cargo (String)**: Cargo do funcionário dentro do MP
- **Lotação (String)**: Local (cidade, departamento, promotoria) em que o funcionário trabalha
- **Sit. * (String)**: Descrição situacional do funcionário, encontra-se em licença, férias ...
- **Remuneração do cargo efetivo (Number)**: Vencimento, GAMPU, V.P.I, Adicionais de Qualificação, G.A.E e G.A.S, além de outras desta natureza. Soma de todas essas remunerações
- **Outras Verbas Remuneratórias Legais/Judiciais (Number)**: V.P.N.I., Adicional por tempo de serviço, quintos, décimos e vantagens decorrentes de sentença judicial ou extensão administrativa
- **Função de Confiança ou Cargo em Comissão  (Number)**: Rubricas que representam a retribuição paga pelo exercício de função (servidor efetivo) ou remuneração de cargo em comissão (servidor sem vínculo ou requisitado)
- **Gratificação Natalina (Number)**: Parcelas da Gratificação Natalina (13º) pagas no mês corrente, ou no caso de vacância ou exoneração do servidor
- **Adicional de Férias (Number)**: Adicional correspondente a remuneração paga ao servidor por ocasião das férias
- **Abono de Permanência (Number)**: Valor equivalente ao da contribuição previdenciária, devido ao funcionário público que esteja em condição de aposentar-se, mas que optou por continuar em atividade (instituído pela Emenda Constitucional nº 41, de 16 de dezembro de 2003)
- **Outras Remunerações Temporárias (Number)**: Valores pagos a título de Auxílio-alimentação, Auxílio-cursos,Auxílio-Saúde, Auxílio-creche, Auxílio-moradia.
- **Verbas Indenizatórias  (Number)**: Verbas referentes á indenizações recebidas pelo funcionario á titulo de Adicional noturno, Cumulações, Serviços extraordinários e substituição de função.

##Obs: Meses anteriores á agosto de 2019 não possuem os campos referentes á Outras Remunerações Temporárias e Verbas Indenizatórias. 

# Dificuldades na libertação de dados: 

## Dificuldades de coleta 
- A pagina do ministério oferece as planilhas referentes á verbas indenizatórias e remunerações simples em seções diferentes, sendo necessário selecionar o periodo de tempo referente a cada uma delas para esclarecimento e compreensão dos dados.
- Existe uma dificuldade relativa ao envio de requisições, para realizar o download de planilhas de anos anteriores ou iguais á 2018, existe a necessidade do envio do parâmetro relativo ao nome do mês em questão com a primeira letra em maiúsculo e as demais letras em minusculo. Para meses posteriores é preciso que este parâmetro seja enviado com todas as letras em minúsculo.
- A url é suscetível á variação de codificação, palavras que contém caractheres especiais no nome dos arquivos disponibilizados pelo site, são convertidas na url com códigos, por exemplo 'á' é codificado em %C3%A0, acredito que isto ocorra devido á alguma ferramenta que mapeia á planilha de um determinado diretório á um endpoint.  

## Dificuldades de Parsing 
- Existem dois formatos de planilha, um associado á meses posteriores á agosto de 2019 e outro associado a meses anteriores. Este fato acaba por exigir duas abordagens diferentes.
- Ausência de detalhes sobre verbas indenizatórias para meses anteriores á agosto de 2019. Aqui temos a completa ausência de detalhamento acerca do que se trata a verba, vemos apenas quatro colunas associadas á valores, nomeadas VERBAS INDENIZATÓRIAS 1, VERBAS INDENIZATÓRIAS 2, REMUNERAÇÃO TEMPORÁRIA 1, REMUNERAÇÃO TEMPORÁRIA 2.  