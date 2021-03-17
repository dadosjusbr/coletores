# Ministério Público do Estado de Goiás

Este coletor tem como objetivo a recuperação de informações sobre folhas de pagamentos dos funcionários do Ministério Público do Estado de Goiás. O site com as informações pode ser acessado [aqui](https://www.mpgo.mp.br/transparencia/contracheque/detalhamento_folha?tipo=r_membro_ativo).

O coletor será estruturado como uma CLI. Uma vez passado como argumentos mês e ano, será feito o download de duas planilhas em formato CSV. Cada planilha é referente a uma dessas categorias:

- Tipo I - Folha de remuneração: Membros Ativos

- Tipo II - Verbas Indenizatórias e outras remunerações temporárias referentes há membros ativos.

# Coletando usando Docker

Por exemplo, para coletar o mês de novembro de 2020, basta executar os seguintes comandos:

```sh
$ sudo docker build -t mppr .
sudo docker run -e MONTH=11 -e YEAR=2020 -e GIT_COMMIT=$(git rev-parse HEAD) -e OUTPUT_FOLDER='/output' mppr
```
# Dicionário de dados

As planilhas referentes á remunerações possuem as seguintes colunas:

- **Nome (String)**: Nome completo do funcionário
- **Nome do Cargo (String)**: Cargo do funcionário dentro do MP
- **Nome da Lotação (String)**: Local (cidade, departamento, promotoria) em que o funcionário trabalha
- **Remuneração do cargo efetivo (Number)**: Vencimento, GAMPU, V.P.I, Adicionais de Qualificação, G.A.E e G.A.S, além de outras desta natureza. Soma de todas essas remunerações
- **Outras Verbas Remuneratórias Legais/Judiciais (Number)**: V.P.N.I., Adicional por tempo de serviço, quintos, décimos e vantagens decorrentes de sentença judicial ou extensão administrativa
- **Função de Confiança ou Cargo em Comissão  (Number)**: Rubricas que representam a retribuição paga pelo exercício de função (servidor efetivo) ou remuneração de cargo em comissão (servidor sem vínculo ou requisitado)
- **Gratificação Natalina (Number)**: Parcelas da Gratificação Natalina (13º) pagas no mês corrente, ou no caso de vacância ou exoneração do servidor
- **Férias (1/3 constitucional) (Number)**: Adicional correspondente a remuneração paga ao servidor por ocasião das férias
- **Abono de Permanência (Number)**: Valor equivalente ao da contribuição previdenciária, devido ao funcionário público que esteja em condição de aposentar-se, mas que optou por continuar em atividade (instituído pela Emenda Constitucional nº 41, de 16 de dezembro de 2003)
- **Outras Remunerações Temporárias (Number)**: Valores pagos a título de Auxílio-alimentação, Auxílio-cursos,Auxílio-Saúde, Auxílio-creche, Auxílio-moradia.
- **Verbas Indenizatórias  (Number)**: Verbas referentes á indenizações recebidas pelo funcionario á titulo de Adicional noturno, Cumulações, Serviços extraordinários e substituição de função.

# Dificuldades na libertação de dados: 

## Dificuldades de coleta 
- A pagina do ministério oferece as planilhas referentes á verbas indenizatórias e remunerações simples em seções diferentes, sendo necessário selecionar o periodo de tempo referente a cada uma delas para esclarecimento e compreensão dos dados.
- A pagina apresenta diversas planilhas em formato XLS tipico formato para excel, com planilhas corrompidas, tornando necessário que o usuário opte por formatos alternativos. 

## Dificuldades de Parsing 
- Há uma situação problematica na qual as planilhas que contém informações acerca de membros, contém entre elas informações que dizem respeito á colaboradores, fazendo-se necessário usar de critérios de seleção para que os valores correspondentes á colaboradores não interfiram nos calculos referentes á membros.