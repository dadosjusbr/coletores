# Tribunal de Justiça da Paraíba

Este crawler tem como objetivo a recuperação de informações sobre folhas de pagamentos dos funcionários do Tribunal de Justiça da Paraíba. O site com as informações pode ser acessado [aqui](https://www.tjpb.jus.br/transparencia/gestao-de-pessoas/folha-de-pagamento-de-pessoal).

O crawler está estruturado como uma CLI. Você passa dois argumentos (mês e ano) e serão baixados dois arquivo no formato **PDF** representando a folha de pagamento da instituição, sendo um referente a magistrados e outro referente a servidores.

## Legislação
Os dados devem estar de acordo com a [Resolução 102 do CNJ](https://atos.cnj.jus.br/atos/detalhar/69).

## Como usar

- É preciso ter o compilador de Go instalado em sua máquina. Mais informações [aqui](https://golang.org/dl/).
- Rode o comando abaixo, com mês e ano que você quer ter acesso as informações

```sh
cd crawler/tjpb
go run crawler-tjpb.go --mes=${MES} --ano=${ANO}
```

## Dicionário de Dados

As planilhas apresentadas nos pdfs contém as seguintes colunas:

### Magistrados: 

- **Magistrado(a) (String)**: Nome completo do funcionário
- **Lotação (String)**: Local (cidade, departamento, promotoria) em que o funcionário trabalha
- **Cargo (String)**: Cargo do funcionário dentro do MP
- **Rendimentos:**
	- **Subsídio (Number)**: Rubricas que representam a retribuição paga pelo exercício de função (servidor efetivo) ou remuneração de cargo em comissão (servidor sem vínculo ou requisitado)
	- **Abono Permanência Previdenciário**: Reembolso da contribuição previdenciária, devido ao Servidor público em regime contratual estatutário que esteja em condição de aposentar-se, mas que optou por continuar em atividade.
	- **Vantagens Pessoais (Number)**: V.P.N.I., Adicional por tempo de serviço, quintos, décimos e vantagens decorrentes de sentença judicial ou extensão administrativa, abono de permanência.
	- **Grat. Exercício Mesa Diretora,ESMA e Diretoria Fórum**: Gratificações.
	- **Indenizações (Number)**: Auxílio-alimentação, Auxílio-transporte, Auxílio Pré-escolar, Auxílio Saúde, Auxílio Natalidade, Auxílio Moradia, Ajuda de Custo, além de outras desta natureza.
	- **Vantagens Eventuais (Number)**: Abono constitucional de 1/3 de férias, indenização de férias, antecipação de férias, gratificação natalina, antecipação de gratificação natalina, serviço extraordinário, substituição, pagamentos retroativos, além de outras desta natureza.
- **Descontos:**
	- **Previdência Pública (Number)**: Contribuição Previdenciária Oficial (Plano de Seguridade Social do Servidor Público e Regime Geral de Previdência Social).
	- **Imposto de Renda (Number)**: Imposto de Renda Retido na Fonte
	- **Descontos Diversos**: Cotas de participação de auxílio pré-escolar, auxílio transporte e demais descontos extraordinários de caráter não pessoal. 
	- **Retenção por Teto Constitucional (Number)**: Valores retidos por excederem ao teto remuneratório constitucional conforme Resoluções nº 13 e 14, do CNJ.
- **Total de Debitos (Number)**:  Total dos descontos efetuados no mês
- **Total de Créditos (Number)**: Total dos rendimentos pagos no mês.
- **Total de Créditos Líquidos (Number)**: Rendimento líquido após os descontos referidos nos itens anteriores.
- **Diárias**:  Valor de diárias efetivamente pago no mês de referência, ainda que o período de afastamento se estenda para além deste.”

### Servidores:

- **Nome do Servidor (String)**: Nome completo do funcionário
- **Lotação (String)**: Local (cidade, departamento, promotoria) em que o funcionário trabalha
- **Cargo (String)**: Cargo do funcionário dentro do MP
- **Rendimentos:**
	- **Remuneração Paradigma (Number)**: Remuneração do cargo efetivo - Vencimento, G.A.J., V.P.I, Adicionais de Qualificação, G.A.E e G.A.S, além de outras desta natureza.
	- **Vantagens Pessoais (Number)**: V.P.N.I., Adicional por tempo de serviço, quintos, décimos e vantagens decorrentes de sentença judicial ou extensão administrativa, abono de permanência.
	- **Função de Confiança ou Cargo em Comissão**: Remuneração de cargo em comissão ou confiança (servidor sem vínculo ou requisitado)
	- **Indenizações (Number)**: Auxílio-alimentação, Auxílio-transporte, Auxílio Pré-escolar, Auxílio Saúde, Auxílio Natalidade, Auxílio Moradia, Ajuda de Custo, além de outras desta natureza.
	- **Vantagens Eventuais (Number)**: Abono constitucional de 1/3 de férias, indenização de férias, antecipação de férias, gratificação natalina, antecipação de gratificação natalina, serviço extraordinário, substituição, pagamentos retroativos, além de outras desta natureza.
	- **Total de Créditos (Number)**: Total dos rendimentos pagos no mês.
- **Descontos:**
	- **Previdência Pública (Number)**: Contribuição Previdenciária Oficial (Plano de Seguridade Social do Servidor Público e Regime Geral de Previdência Social).
	- **Imposto de Renda (Number)**: Imposto de Renda Retido na Fonte
	- **Descontos Diversos**: Cotas de participação de auxílio pré-escolar, auxílio transporte e demais descontos extraordinários de caráter não pessoal. 
	- **Retenção por Teto Constitucional (Number)**: Valores retidos por excederem ao teto remuneratório constitucional conforme Resoluções nº 13 e 14, do CNJ.
	- **Total de Debitos (Number)**:  Total dos descontos efetuados no mês
- **Rendimento Líquido (Number)**: Rendimento líquido após os descontos referidos nos itens anteriores.
- **Diárias**:  Valor de diárias efetivamente pago no mês de referência, ainda que o período de afastamento se estenda para além deste.”

## Arquivos
  
### Remunerações ###

- **URL Base**: [https://www.tjpb.jus.br/transparencia/gestao-de-pessoas/folha-de-pagamento-de-pessoal](https://www.tjpb.jus.br/transparencia/gestao-de-pessoas/folha-de-pagamento-de-pessoal)
- **Formato**: PDF, XLS*
- **Tipos**: Existe um arquivo referente aos servidores e um referente aos magistrados.
- **Obs**: 
	- Antes de outubro de 2012 pode-se ter apenas o arquivo de magistrados ou um arquivo geral que não discrimina por funcionário. Esses são nomeados apenas como "remuneracoes-tjpb-mes-ano.pdf" quando baixados.
	- Apenas o mês de outubro/2019 é disponibilizado em '.xls'.


## Dificuldades para libertação dos dados

- Não há API
- A partir de jan/2018 até maio/2020, todos os meses foram disponibilizados em PDF,  exceto de out/2019 que foi disponibilizado em .xls.
- A partir de 2018, foram verificados que há 5 padrões diferentes nos templates dos pdf e não há um padrão na distribuição dos meses nesses padrões. Esses padrões possuem se referem ao tamanho da tabela e/ou a quantidade de colunas existentes em cada uma. Agrupamos os meses nesses 5 tipos e os nomeamos de 'A', 'B', 'C','D' e 'E'. O template 'E' é o único que difere em quantidade de colunas em relação aos demais que embora possuam a mesma quantidade de colunas entre si, as tabelas tem largura e/ou altura diferentes. Abaixo ilustramos como os meses estão distribuídos nos templates com uma tabela:
    
    |  Ano  |  A  |  B | C |  D   |  E |
    |:----------:|:-------------:|:------:|:----------|:-------------:|:------:|
    | 2018 |  Fev-Abr-Mai-Jun-Ago-Set-Out-Nov-Dez | Mar-Jul | Jan |   | 
    | 2019 |    Jan-Fev-Mar-Abr-Mai-Jun-Jul-Ago-Set-Nov  |   Dez |
    | 2020 | Abr |    Jan-Fev | | Mar | Mai |

- Logo do órgão do TJPB no formato é adicionado no arquivo .xls como uma imagem e dificulta a libertação dos dados.
- Precisamos desenvolver uma forma de testar a qualidade dos dados e, em caso de problemas, avaliar a forma de resolução.
- Na figura abaixo,podemos comparar a diferença no layout dos templates com cores, onde: 'A' = Azul ([Abril/2020](https://www.tjpb.jus.br/sites/default/files/anexos/2020/05/transparencia_202004_servidores_0_0.pdf)), 'B' = Amarelo ([fev/2020](https://www.tjpb.jus.br/sites/default/files/anexos/2020/03/transparencia_202002_servidores_0.pdf)), 'C' = Laranja ([Mar/2018](https://www.tjpb.jus.br/sites/default/files/anexos/2018/06/transparencia_201803_servidores.pdf)), 'D' = Vermelho ([Mai/2020](https://www.tjpb.jus.br/sites/default/files/anexos/2020/04/transparencia_202003_servidores_0.pdf)), 'E' = Verde ([Mai/2020](https://www.tjpb.jus.br/sites/default/files/anexos/2020/06/transparencia_202005_servidores2_0.pdf)). 

   ![](https://imagizer.imageshack.com/img923/8154/Qa7qTV.jpg)


- Antes de outubro de 2012 pode-se ter apenas o arquivo de magistrados ou um arquivo geral que não discrimina por funcionário. Esses são nomeados apenas como "remuneracoes-tjpb-mes-ano.pdf" quando baixados.
