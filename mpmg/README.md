# Ministério Público Militar- Crawler

Este crawler tem como objetivo a recuperação de informações sobre folhas de pagamentos dos membros ativos do Ministério Público de Minas Gerais, a partir de 2018. O site com as informações pode ser acessado [aqui](https://transparencia.mpmg.mp.br/nav/contracheque).

O crawler está estruturado como uma CLI. É necessário passar os argumentos mês e ano via variáveis de ambiente (`MONTH`e `YEAR`). E então, serão baixadas as planilhas, no formato xlsx. As mesmas são correpondentes a remuneração mensal e verbas indenizatórias dos Membros Ativos.

De 2018 até abril de 2020 as planilhas seguem o formato Resolução [CNMP 89/2012](https://www.cnmp.mp.br/portal/images/Resolucoes/Resolu%C3%A7%C3%A3o-0891.pdf). A partir de maio de 2020 seguem o Pós Resolução CNMP 200/2019, que altera o Anexo I da Resolução nº 89/2012 para incluir nessa norma informações sobre remunerações temporárias e verbas indenizatórias, de modo que o total de rendimentos brutos passe a contabilizar os valores efetivamente recebidos pelos membros do Ministério Público.

# Dicionário de dados

As planilhas referentes á remunerações possuem as seguintes colunas:

- **Matrícula (Number)**: Matrícula do funcionário
- **Nome (String)**: Nome completo do funcionário
- **Cargo Efetivo (String)**: Cargo do funcionário dentro do MP
- **Situação (String)**: Funcionário ativo ou inativo
- **Unidade Administrativa (String)**: Local (cidade, departamento, promotoria) em que o funcionário trabalha
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


As planilhas referentes á verbas indenizatórias e outras remunerações possuem as seguintes colunas:

- **Vale Alimentação (Number)**
- **Auxílio Alimentação (Number)**
-	**Auxílio Creche (Number)**
-	**Auxílio Transporte (Number)**
- **Auxílio Saúde	Auxílio Moradia (Number)**

A partir da Resolução CNMP 200/2019 é acrescido as seguintes colunas às tabelas referentes a verbas indenizatórias e outras remunerações:
- **Indenizações (Number)** 
- **Indenizações e Diligênias (Number)**
-	**Periculosidade e Insalubridade (Number)**
- **Gratificações (Number)**
- **Outras Remunerações (Number)**
