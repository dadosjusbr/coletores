# Ministério Público do Distrito Federal e Territórios. - Crawler

Este crawler tem como objetivo a recuperação de informações sobre folhas de pagamentos dos membros ativos do Ministério Público do Distrito Federal e territórios, a partir de 2018. O site com as informações pode ser acessado [aqui](https://www.mpdft.mp.br/transparencia/index.php?item=remuneracao&tipo=membrosAtivos&resp=REMUNERACAO&titulo=Remunera%C3%A7%C3%A3o%20de%20todos%20os%20membros%20ativos).

O crawler está estruturado como uma CLI. É necessário passar os argumentos mês, ano e caminho para armazenar os arquivos via variáveis de ambiente (`MONTH`, `YEAR`, `OUTPUT_FOLDER`). E então, serão baixadas as planilhas, no formato xlsx. As mesmas são correpondentes a remuneração mensal e verbas indenizatórias dos Membros Ativos.


# Dicionário de dados

As planilhas referentes á remunerações possuem as seguintes colunas:

- **Matrícula (Number)**: Matrícula do funcionário
- **Nome (String)**: Nome completo do funcionário
- **Cargo (String)**: Cargo do funcionário dentro do MP
- **Lotação (String)**: Local (cidade, departamento, promotoria) em que o funcionário trabalha
- **Remuneração do cargo efetivo (Number)**: Vencimento, GAMPU, V.P.I, Adicionais de Qualificação, G.A.E e G.A.S, além de outras desta natureza. Soma de todas essas remunerações
- **Outras Verbas Remuneratórias, Legais ou  Judiciais (Number)**: V.P.N.I., Adicional por tempo de serviço, quintos, décimos e vantagens decorrentes de sentença judicial ou extensão administrativa
- **Função de confiança ou cargo em comissão (Number)**: Rubricas que representam a retribuição paga pelo exercício de função (servidor efetivo) ou remuneração de cargo em comissão (servidor sem vínculo ou requisitado)
- **Gratificação natalina (Number)**: Parcelas da Gratificação Natalina (13º) pagas no mês corrente, ou no caso de vacância ou exoneração do servidor
- **Férias - ⅓ Constitucional (Number)**: Adicional correspondente a 1/3 (um terço) da remuneração, pago ao servidor por ocasião das férias
- **Abono de permanência (Number)**: Valor equivalente ao da contribuição previdenciária, devido ao funcionário público que esteja em condição de aposentar-se, mas que optou por continuar em atividade (instituído pela Emenda Constitucional nº 41, de 16 de dezembro de 2003)
- **Total de Rendimentos Brutos (Number)**: Total dos rendimentos brutos pagos no mês.
- **Contribuição Previdenciária (Number)**: Contribuição Previdenciária.
- **Imposto de Renda (Number)**: Imposto de Renda Retido na Fonte.
- **Retenção por Teto Constitucional (Number)**: Valor deduzido da remuneração bruta, quando esta ultrapassa o teto constitucional, de acordo com a Resolução nº 09/2006 do CNMP.
- **Total de Descontos (Number)**: Soma dos descontos referidos nos itens 8, 9 e 10.
- **Total Líquido (Number)**: Rendimento obtido após o abatimento dos descontos referidos no item 11. O valor líquido efetivamente recebido pelo membro ou servidor pode ser inferior ao ora divulgado, porque não são considerados os descontos de caráter pessoal.


As planilhas referentes á verbas indenizatórias possuem as seguintes colunas:
									
- **Abono Pecuniário (Number)**: Troca de alguns dias do período de férias pelo recebimento de um valor extra.
- **Auxílio pré-escolar (Number)**: Benefício concedido ao servidor para auxiliar nas despesas pré-escolares de filhos ou dependentes com idade até 5 (cinco) anos de idade.
-	**Ajuda de Custo (Number)**: Valor pago ao empregado com a finalidade de cobrir despesas por conta da mudança de local de trabalho ou circunstâncias especiais definidas pelo empregador.
-	**Auxílio natalidade (Number)**: O Auxílio Natalidade é o benefício devido à servidora efetiva – ou ao pai servidor, quando a parturiente não for servidora – por motivo de nascimento de filho.
- **Auxílio alimentação (Number)**
- **Auxílio transporte (Number)**
- **Férias indenizada (Number)**
- **Banco de horas indenizado (Number)**
- **Auxílio moradia (Number)**
- **Licença prêmio pecúnia (Number)**

As planilhas referentes á remunerações temporárias possuem as seguintes colunas:

-**Substituição de Membros (Number)**
-**Função de Substituição (Number)**
-**Gratificação por Encargo de Curso (Number)**
-**Adicional de Insalubridade (Number)**
-**Gratificação por Encargo de Concurso (Number)**
-**Adicional de Periculosidade (Number)**
-**Gratificação de Exercício Cumulativo com Ofício Sem Psss (Number)**
-**Gratificação Exercício Cumulativo com Ofício Com Psss (Number)**
-**Membros Substituição (Number)**	
-**Hora Extra Sem Psss (Number)**
-**Adicional Noturno Sem Psss**
-**Substituição Membros MS2013 (Number)**
-**Adicional Penosidade (Number)**

