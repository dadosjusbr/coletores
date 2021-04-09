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

# Dificuldades na libertação de dados: 

## Dificuldades de coleta:

- Parâmetro do nome do mês na Url varia entre primeira letra maiúscula e todas as letras minúsculas, tornando necessário várias estratégias para o request. Exemplo: Janeiro para jan/2018 , janeiro para jan/2019. Fevereiro para fev/2018, fevereiro para fev/2019. 
- Url sofre variação de acordo com codificação do nome do arquivo. Caractheres especiais, com acentos ou pontuções recebem mapeamento para código. Exemplo: á é mapeado para %C3%A0, já o caracthere a, sem acento, não sofre necessidade de mapeamento.
- Url de verbas indenizátorias precisa de um sufixo associado a membros ativos apenas em 2019. Exemplo: para o ano de 2018 não necessita desse sufixo, em 2019 precisamos que o sufixo "2Dvi" seja adicionado na url.

## Dificuldades de Parsing:

- Antes de 2019 o conjunto de colunas para remunerações simples não conta com as colunas, 'Outras Remunerações Temporarárias' e 'Verbas Indenizatórias', a partir de 2019 essas colunas são adicionadas á planilha de remunerações simples, necessitando de tratamento especial. 
- Gratificação Natalina é nomeada como 13º VENCIMENTO antes de agosto de 2019. 
- Colunas com nomes pouco significativos antes de agosto de 2019. Exemplo: Em jan/2019 as colunas da planilha de verbas indenizatórias são as seguintes: 'VERBAS INDENIZATÓRIAS 1','VERBAS INDENIZATÓRIAS 2', 'REMUNERAÇÃO TEMPORÁRIA 1', 'REMUNERAÇÃO TEMPORÁRIA 2'. 
- Variação na quantidade de colunas para os meses entre abril á junho de 2020, estando ausente a coluna nomeada 'ABONO  FÉR. IND. EX. ANT', nos demais meses esta coluna está presente, exigindo tratamento especial para os meses supracitados. 