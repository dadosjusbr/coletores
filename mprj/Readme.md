# Ministério Público do Estado do Rio de Janeiro

Este coletor tem como objetivo a recuperação de informações sobre folhas de pagamentos dos funcionários do Ministério Público do Estado do Rio de Janeiro. O site com as informações pode ser acessado [aqui](http://transparencia.mprj.mp.br/contracheque).

O coletor será estruturado como uma CLI. Uma vez passado como argumentos mês e ano, será feito o download de dezesseis planilhas, onze no formato ODS, e cinco no formato xlsx. Cada planilha é referente a uma dessas categorias: 

- Tipo I - Folha de remuneração: Membros Ativos, Membros Inativos, Servidores Ativos, Servidores Inativos, Pensionistas, Colaboradores. 

- Tipo II - Verbas Referentes á exercícios anteriores.

- Tipo III - Verbas Indenizatórias e outras remunerações temporárias.

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
- **Indenizações (Number)**: Auxílio-alimentação, Auxílio-educação, Auxílio-saúde, Conversão de licença especial, Devolução IR-RRA, Indenização de férias nao usufruídas, Indenização por licença não gozada. Soma de todas essas remunerações
- **Outras remunerações retroativas/temporárias**: Valores pagos a título de Auxílio-alimentação, Auxílio-educação, Auxílio-Saúde, Devolução fundo de reserva, Diferenças de auxílios, Gratificações eventuais, Indenização de transporte, Parcelas pagas em atraso. Soma desses valores