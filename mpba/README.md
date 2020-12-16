# Ministério Público do Estado da Bahia (MP-BA)

Este crawler tem como objetivo a recuperação de informações sobre folhas de pagamentos
dos funcionários do Ministério Público do Estado da Bahia (MP-BA). O site com as informações
pode ser acessado [aqui](https://lai.sistemas.mpba.mp.br/).

O crawler está estruturado como uma CLI. Você passa dois argumentos (mês e ano) e é baixado um
arquivo no formato **JSON** representando a folha de pagamento da instituição.

## Legislação

Os dados devem estar de acordo com a [Resolução 102 do CNJ](https://atos.cnj.jus.br/atos/detalhar/69).

## Como usar

## Dicionário de Dados

Nas tabelas abaixo você poderá ver os campos apresentados no payload da API
do MP-BA explicados e mapeados com aos objetos desse projeto.
Os campos com `-` não foram encontrados (em uma ou outra estrutura).

| Campo no MP-BA | Campo no `coletores.Employee` | Descrição | Observações |
| ------------- | ------------- | ------------- | ------------- |
| `nuMatricula` (Number) | `Reg` | Matrícula do funcionário | |
| `nuMesReferencia` (Number) | - | | |
| `nuAnoReferencia` (Number) | - | | |
| `nmServidor` (String) | `Name` | Nome completo do funcionário | |
| `dsCargo` (String) | `Role` | Cargo do funcionário dentro do tribunal |  |
| - | `Type` | Tipo do servidor |  |
| `dsLotacao` (String) | `Workplace` | Local (cidade, departamento, promotoria) em que o funcionário trabalha |  |
| `dsLotacao` (String) | `Active` |  | Se inativo aparece com valor "INATIVO". Caso contrário, apresenta a lotação. |
| tabela abaixo | `Income` |  |  |
| tabela abaixo | `Discounts` |  |  |


| Campo no MP-BA | Campo no `coletores.IncomeDetails` | Descrição | Observações |
| ------------- | ------------- | ------------- | ------------- |
| - | `Total` | Rendimentos após os descontos. |  |
| `vlRendCargoEfetivo` (Number) | `Wage` | Remuneração do cargo efetivo - vencimento básico, subsídio, gratificação de atividade judiciária, vantagem pecuniária individual (VPI), adicionais de qualificação, gratificação de atividade externa (GAE), gratificação de atividade de segurança (GAS), além de outras parcelas desta natureza. |  |
| tabela abaixo | `Perks` |  |  |
| tabela abaixo | `Other` (`Funds`) |  |  |


| Campo no MP-BA | Campo no `coletores.Perks` | Descrição | Observações |
| ------------- | ------------- | ------------- | ------------- |
| `vlIdenizacoes` | `Total` | Auxílio-alimentação, auxílio-transporte, auxílio pré-escolar, auxílio-saúde, auxílio-natalidade, auxílio-moradia, ajuda de custo, além de outras parcelas desta natureza. |  |
| - | `Food` |  | |
| `vlRendFerias` | `Vacations` |  | |
| - | `Transportation` |  | |
| - | `PreSchool` |  | |
| - | `Health` |  | |
| - | `BirthAid` |  | |
| - | `HousingAid` |  | |
| - | `Subsistence` |  | |
| - | `CompensatoryLeave` |  | |
| - | `Pecuniary` |  | |
| - | `VacationPecuniary` |  | |
| - | `FurnitureTransport` |  | |
| - | `PremiumLicensePecuniary` |  | |


| Campo no MP-BA | Campo no `coletores.Funds` | Descrição | Observações |
| ------------- | ------------- | ------------- | ------------- |
| `vlRendTotalLiquido` (Number) | `Total` | Valor após descontos. O rendimento líquido efetivamente recebido por desembargador, juiz de direito ou servidor pode ser inferior ao ora divulgado, por não estarem demonstrados os descontos pessoais, tais como pensões e consignações. | |
| `vlRendAbonoPerman` (Number) | `PersonalBenefits` | Vantagem pessoal nominalmente identificada (VPNI), adicional por tempo de serviço, quintos, décimos e vantagens decorrentes de sentença judicial ou extensão administrativa, abono de permanência. |  |
| `vlIdenizacoes` (Number) | `EventualBenefits` | Abono constitucional de um terço de férias, indenização de férias, antecipação de férias, gratificação natalina, antecipação de gratificação natalina, serviço extraordinário, substituição, pagamentos retroativos, além de outras parcelas desta natureza. |  |
| `vlRendCargoComissao` | `PositionOfTrust` |  | |
| `vlRendGratNatalina` (Number) | `Gratification` | Gratificações de qualquer natureza. | |
| - | `Daily` | Valor de diárias efetivamente pago pelo Tribunal de Justiça do Estado da Bahia no mês de referência, ainda que o período de afastamento se estenda para além deste. | |
| `vlRendTotalBruto` (Number) | `OriginPosition` | Remuneração ou subsídio bruto percebido no órgão de origem por magistrado ou servidor, cedido ou requisitado. | |
| `vlRendVerbas` | `OtherFundsTotal` |  | |
| `vlOutrasRemun` | `Others` |  | |

| Campo no MP-BA | Campo no `coletores.Discount` | Descrição | Observações |
| ------------- | ------------- | ------------- | ------------- |
| `vlDescTotalBruto` | `Total` | Total dos descontos efetuados pelo Tribunal de Justiça da Bahia no mês. |  |
| `vlDescPrevidencia` (Number) | `PrevContribution` | Contribuição Previdenciária Oficial (Plano de Seguridade Social do Servidor Público ou Regime Geral de Previdência Social). | |
| `vlDescTeto` (Number) | `CeilRetention` | Auxílio-alimentação, auxílio-transporte, auxílio pré-escolar, auxílio-saúde, auxílio-natalidade, auxílio-moradia, ajuda de custo, além de outras parcelas desta natureza. | |
| `vlDescIR` (Number) | `IncomeTax` | Imposto de Renda Retido na Fonte. | |
| `valorDescontoDiverso` (Number) | `OtherDiscountsTotal` | Cotas de participação de auxílio pré-escolar e auxílio-transporte e demais descontos extraordinários de caráter não pessoal. | |
| - | `Others` | - | |


## Arquivos
  
### Remunerações

O acesso pode ser feito a partir de uma API:

- **URL Base**: [https://lai-app.sistemas.mpba.mp.br/api/quadroremuneratoriogeral/consultar?mes={mes}&ano={ano}&cargo=0](https://lai-app.sistemas.mpba.mp.br/api/quadroremuneratoriogeral/consultar?mes=10&ano=2020&cargo=0)
- **Formato**: JSON
- **Obs:** os dados estão disponíveis a partir de Setembro de 2012. Para buscar por todos os cargos o valor no parâmetro deve ser `0`.

## Dificuldades para libertação dos dados

* Falta detalhamento com relação a remunerações e gratificações.
