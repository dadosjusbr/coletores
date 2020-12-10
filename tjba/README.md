# Tribunal de Justiça do Estado da Bahia (TJ-BA)

Este crawler tem como objetivo a recuperação de informações sobre folhas de pagamentos
dos funcionários do Tribunal de Justiça do Estado da Bahia (TJ-BA). O site com as informações
pode ser acessado [aqui](https://transparencia.tjba.jus.br/transparencia/home#).
A página conta com uma pequena seção de orientações a respeito dos campos.

O crawler está estruturado como uma CLI. Você passa dois argumentos (mês e ano) e é baixado um
arquivo no formato **JSON** representando a folha de pagamento da instituição.

## Legislação

Os dados devem estar de acordo com a [Resolução 102 do CNJ](https://atos.cnj.jus.br/atos/detalhar/69).
O site com a resolução pode não funcionar caso você esteja acessando de fora do Brasil.

## Como usar

## Dicionário de Dados

Nas tabelas abaixo você poderá ver os campos apresentados no payload da API
do TJ-BA explicados e mapeados com aos objetos desse projeto.
Os campos com `-` não foram encontrados (em uma ou outra estrutura).

| Campo no TJ-BA | Campo no `coletores.Employee` | Descrição | Observações |
| ------------- | ------------- | ------------- | ------------- |
| `matricula` (Number) | `Reg` | Matrícula do funcionário | |
| `dataReferencia` (Timestamp) | - | | |
| `nome` (String) | `Name` | Nome completo do funcionário | |
| `cargo` (String) | `Role` | Cargo do funcionário dentro do tribunal |  |
| `tipoServidor` (String) | `Type` | | Servidor (`S`), Juiz (`J`), Desembargador (`D`) |
| `lotacao` (String) | `Workplace` | Local (cidade, departamento, promotoria) em que o funcionário trabalha |  |
| `status` (String) | `Active` | Se ativo ou inativo | Valores `A` ou `I` |
| tabela abaixo | `Income` |  |  |
| tabela abaixo | `Discounts` |  |  |
| `ano` | - |  | Geralmente esse campo vem com valor `null` |
| `mes` | - |  | Geralmente esse campo vem com valor `null` |
| `id` | - |  | Mesmo valor da `matricula` |


| Campo no TJ-BA | Campo no `coletores.IncomeDetails` | Descrição | Observações |
| ------------- | ------------- | ------------- | ------------- |
| `totalCredito` | `Total` | Rendimentos após os descontos. |  |
| `valorParadigma` (Number) | `Wage` | Remuneração do cargo efetivo - vencimento básico, subsídio, gratificação de atividade judiciária, vantagem pecuniária individual (VPI), adicionais de qualificação, gratificação de atividade externa (GAE), gratificação de atividade de segurança (GAS), além de outras parcelas desta natureza. |  |
| tabela abaixo | `Perks` |  |  |
| tabela abaixo | `Other` (`Funds`) |  |  |


| Campo no TJ-BA | Campo no `coletores.Perks` | Descrição | Observações |
| ------------- | ------------- | ------------- | ------------- |
| `valorIndenizacao` | `Total` | Auxílio-alimentação, auxílio-transporte, auxílio pré-escolar, auxílio-saúde, auxílio-natalidade, auxílio-moradia, ajuda de custo, além de outras parcelas desta natureza. |  |
| - | `Food` |  | |
| - | `Vacations` |  | |
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


| Campo no TJ-BA | Campo no `coletores.Funds` | Descrição | Observações |
| ------------- | ------------- | ------------- | ------------- |
| `valorLiquido` (Number) | `Total` | Valor após descontos. O rendimento líquido efetivamente recebido por desembargador, juiz de direito ou servidor pode ser inferior ao ora divulgado, por não estarem demonstrados os descontos pessoais, tais como pensões e consignações. | |
| `valorVantagemPessoal` (Number) | `PersonalBenefits` | Vantagem pessoal nominalmente identificada (VPNI), adicional por tempo de serviço, quintos, décimos e vantagens decorrentes de sentença judicial ou extensão administrativa, abono de permanência. | No payload existe o campo `vantagensPessoais`, uma lista, que até agora só aparece vazia. |
| `valorVantagemEventual` (Number) | `EventualBenefits` | Abono constitucional de um terço de férias, indenização de férias, antecipação de férias, gratificação natalina, antecipação de gratificação natalina, serviço extraordinário, substituição, pagamentos retroativos, além de outras parcelas desta natureza. | No payload existe o campo `vantagensEventuais`, uma lista, que até agora só aparece vazia. |
| `valorComissao` | `PositionOfTrust` |  | |
| `valorGratificacao` (Number) | `Gratification` | Gratificações de qualquer natureza. | |
| `valorDiaria` (Number) | `Daily` | Valor de diárias efetivamente pago pelo Tribunal de Justiça do Estado da Bahia no mês de referência, ainda que o período de afastamento se estenda para além deste. | |
| `valorRemuneracaoOrigem` (Number) | `OriginPosition` | Remuneração ou subsídio bruto percebido no órgão de origem por magistrado ou servidor, cedido ou requisitado. | |
| - | `OtherFundsTotal` |  | |
| - | `Others` |  | |

| Campo no TJ-BA | Campo no `coletores.Discount` | Descrição | Observações |
| ------------- | ------------- | ------------- | ------------- |
| `totalDebito` | `Total` | Total dos descontos efetuados pelo Tribunal de Justiça da Bahia no mês. |  |
| `valorPrevidencia` (Number) | `PrevContribution` | Contribuição Previdenciária Oficial (Plano de Seguridade Social do Servidor Público ou Regime Geral de Previdência Social). | |
| `valorRetencaoTeto` (Number) | `CeilRetention` | Auxílio-alimentação, auxílio-transporte, auxílio pré-escolar, auxílio-saúde, auxílio-natalidade, auxílio-moradia, ajuda de custo, além de outras parcelas desta natureza. | |
| `valorIR` (Number) | `IncomeTax` | Imposto de Renda Retido na Fonte. | |
| `valorDescontoDiverso` (Number) | `OtherDiscountsTotal` | Cotas de participação de auxílio pré-escolar e auxílio-transporte e demais descontos extraordinários de caráter não pessoal. | |
| - | `Others` | - | |


## Arquivos
  
### Remunerações

O acesso pode ser feito a partir de uma API:

- **URL Base**: [https://transparencia.tjba.jus.br/transparencia/api/v1/remuneracao/ano/{ano}/mes/{mes}](https://transparencia.tjba.jus.br/transparencia/api/v1/remuneracao/ano/2020/mes/1)
- **Formato**: JSON
- **Obs:** os dados estão disponíveis a partir de Junho de 2012.

## Dificuldades para libertação dos dados

* Apesar de haver uma pequena seção sobre os campos na página,
falta detalhamento com relação a remunerações e gratificações.
