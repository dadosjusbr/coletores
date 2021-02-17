# Ministério Público do Estado do Rio de Janeiro

Este coletor tem como objetivo a recuperação de informações sobre folhas de pagamentos dos funcionários do Ministério Público do Estado do Rio de Janeiro. O site com as informações pode ser acessado [aqui](http://transparencia.mprj.mp.br/contracheque).

O coletor será estruturado como uma CLI. Uma vez passado como argumentos mês e ano, será feito o download de onze planilhas no formato ODS. Cada planilha é referente a uma dessas categorias:

- Tipo I - Folha de remuneração: Membros Ativos, Membros Inativos, Servidores Ativos, Servidores Inativos, Pensionistas, Colaboradores.

- Tipo II - Verbas Indenizatórias e outras remunerações temporárias.

# Coletando usando Docker

Por exemplo, para coletar o mês de novembro de 2020, basta executar o seguinte comando:

```sh
$ sudo docker build -t mprj .
sudo docker run -e MONTH=11 -e YEAR=2020 -e GIT_COMMIT=$(git rev-parse HEAD) -e OUTPUT_FOLDER='/output mprj
```

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
- **Indenizações (Number)**: Auxílio-alimentação, Auxílio-educação, Auxílio-saúde, Conversão de licença especial, Devolução IR-RRA, Indenização de férias não usufruídas, Indenização por licença não gozada. Soma de todas essas remunerações
- **Outras remunerações retroativas/temporárias**: Valores pagos a título de Auxílio-alimentação, Auxílio-educação, Auxílio-Saúde, Devolução fundo de reserva, Diferenças de auxílios, Gratificações eventuais, Indenização de transporte, Parcelas pagas em atraso. Soma desses valores

# Esclarecimentos sobre verbas referentes á exercícios anteriores

O mprj deixa disponível [aqui](http://transparencia.mprj.mp.br/contracheque/verbas-referentes-a-exercicios-anteriores) informações acerca de verbas referentes á exercícios anteriores.

As planilhas referentes ás verbas de exercícios anteriores possuem as seguintes colunas:

- **Matrícula (Number)**: Matŕicula do funcionário
- **Nome (String)**: Nome do funcionário
- **Cargo (String)**: Cargo do funcionário dentro do MP
- **Lotação (String)**: Local (cidade, departamento, promotoria) em que o funcionário trabalha
- **Número do processo (String)**: Identificador do processo
- **Objeto do processo**: Conjunto do material lógico elaborando o mérito a ser julgado
- **Origem do processo**: Natureza do processo definida pelo tipo de direito

Planilhas deste tipo, não serão coletadas pois se tratam de um tratamento especial, gerando significativo custo adicional ao código e foge dos objetivos descritos neste coletor.

# Dificuldades para libertação dos dados

- **Dificuldades na coleta dos arquivos**: A url de download de planilhas sofre muita variação de acordo com o tipo de funcionário e mês.
    Para download de planilhas de verbas indenizatórias referentes aos servidores ativos, é necessário que a url contenha trẽs parâmetros de identificação do tipo de funcionário denominados tipoFunc1, tipoFunc2 e tipoFunc3, respectivamente, além de mês e ano. Seguindo a seguinte estrutura:

    - http://transparencia.mprj.mp.br/contrachequeverbas-indenizatorias-e-outras-remuneracoes-temporarias-de-servidores-ativos&mes=11&ano=2020&tipoFunc1=11&tipoFunc2=21&tipoFunc3=23

- Não há logica aparente na distribuição os parâmetros mencionados acima.
- A matrícula ou registro do funcionário fornecido pelo órgão não segue uma padronização sucinta no que diz respeito á caracteres. Existem funcionários cuja identificação varia entre as planilhas. Abaixo seguem alguns exemplos ilustrativos com matrículas fictícias que demonstram algumas situações reais de formatação.
    - Exemplo:
        - O funcionário X pode ser identificado pela matrícula : 123123 e pela matrícula: 123123.0
        - O funcionário Y é identificado pela matrícula 123123-1

    De modo geral não há problemas em diferenciar os funcionários X e Y, porém é confuso ter 2 formas de identificar o funcionário X. Além de sofrermos certo custo pra lidar com o caso de funcionários como Y que possuem caracteres especiais em sua matrícula '-' .

- **Dificulta o parsing**: Existe variação entre meses na quantidade de disposição de colunas em planilhas referentes á verbas indenizatórias de um mesmo tipo de funcionário. Exemplo:
    - Há 13 colunas na planilha de verbas Indenizatórias referentes á servidores inativos do mês de novembro de 2020.
    - Há 11 colunas na planilha de verbas indenizatórias referentes á servidores inativos do mẽs de outubro de 2020.
    - Existe uma situação de intensa variação nas planilhas referentes a verbas indenizatórias para diversos meses de 2020. A variação toma dois parâmetros e contempla servidores e membros, ativos e inativos:
      - Quantidade de colunas.
      - Ordem que as colunas aparecem nas planilhas.
    - Em termos de código isso representa a criação de uma nova distribuição de colunas e de variáveis no cálculo de total. Desse modo, estão reportadas abaixo algumas dessas variações que acabaram por gerar esta necessidade.
      - Há 2 colunas especificando indenizações de transporte/locomoção na planilha de verbas indenizatórias referentes á membros ativos no mês de janeiro de 2020. Isto entra em detrimento com outros meses, gerando alteração na ordem e quantidade de colunas.
      - Há 2 colunas especificando indenizações referentes á licenças na planilha de verbas indenizatórias referentes á membros ativos do mês de janeiro de 2020. Isto entra em detrimento com outros meses, gerando alteração na ordem e quantidade de colunas.
      - Não há coluna referente á substituição de cargo em comissão / função gratificada na planilha de verbas indenizatórias referente á membros ativos nos meses de janeiro, maio, julho ,junho e agosto de 2020.
      - Não há coluna referente á substituição de cargo em comissão / função gratificada na planilha de verbas indenizatórias referente á membros ativos dos meses de fevereiro e março de 2020.
      - Não há coluna referente á parcelas pagas em atraso na planilha de verbas indenizatórias referente á servidores ativos do mês de abril de 2020.
      - Não há coluna referente á conversão de licença especial na planilha de verbas indenizatórias referente á membros ativos dos mêses de abril, maio, julho, junho, agosto de 2020.
      - Não há coluna referente á devolução de fundos na planilha de verbas indenizatórias referente á membros ativos do meses de abril, maio e julho de 2020.
      - Há uma coluna especificando auxílio moradia na planilha de verbas indenizatórias referente á membros ativos de abril de 2020. Isto entra em detrimento com outros meses, gerando alteração na ordem e quantidade de colunas.
      - Não há coluna referente ao campo devolução IRRRA na planilha de verbas indenizatórias referente á membros inativos dos meses de julho e junho de 2020.
      - Há uma coluna especificando indenizações de transporte / locomoção na planilha de verbas indenizatórias referentes á servidores ativos dos meses de junho, agosto e dezembro de 2020. Isto entra em detrimento com outros meses, gerando alteração na ordem e quantidade de colunas.
      - Não há coluna especificando indenizações de transporte na planilha de verbas indenizatórias referentes á servidores inativos do mês de junho, julho e agosto de 2020.
      - Há uma coluna especificando auxílio alimentação na planilha de verbas indenizatórias referentes á servidores inativos do mês de agosto de 2020. Isto entra em detrimento com outros meses, gerando alteração na ordem e quantidade de colunas.
      - Há uma coluna especificando auxílio educação na planilha de verbas indenizatórias referentes á servidores inativos do mês de julho de 2020.
