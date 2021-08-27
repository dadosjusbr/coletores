# Ministerio publico do Mato Grosso do Sul

Este coletor tem como objetivo a recuperação de informações sobre folhas de pagamentos dos membros ativos do Ministério Público do Mato Grosso do Sul nos anos 2018, 2019, 2020 e 2021. O site com as informações pode ser acessado **[aqui](https://transparencia.mpms.mp.br/QvAJAXZfc/opendoc.htm?document=portaltransparencia%5Cportaltransparencia.qvw&lang=pt-BR&host=QVS%40srv-1645&anonymous=true)**.

O coletor será estruturado como uma CLI. Uma vez passado como argumentos mês e ano, será feito o download de planilhas, nos formato ODS, sendo cada uma referente a uma dessas categorias:

Folha de remuneração: Membros Ativos - As planilhas deste tipo, seguem o seguinte formato:

- **Matrícula (String)**: Matrícula do funcionário.
- **Nome (String)**: Nome completo do funcionário.
- **Cargo (String)**: Cargo do funcionário dentro do MP.
- **Lotação (String)**: Local (cidade, departamento, promotoria) em que o funcionário trabalha.
- **Remuneração Básica do Cargo Efetivo (Number)**: Vencimento, GAMPU, V.P.I, Adicionais de Qualificação, G.A.E e G.A.S, além de outras desta natureza.
- **Outras Verbas Remuneratórias, Legais ou Judiciais (Number)**:  V.P.N.I., Adicional por tempo de serviço, quintos, décimos e vantagens decorrentes de sentença judicial ou extensão administrativa.
- **Função de Confiança ou Cargo em Comissão (Number)**: Rubricas que representam a retribuição paga pelo exercício de função (servidor efetivo) ou remuneração de cargo em comissão (servidor sem vínculo ou requisitado).
- **Gratificação Natalina (Number)**:  Parcelas da Gratificação Natalina (13º) pagas no mês corrente, ou no caso de vacância ou exoneração do servidor.
- **Férias Constitucionais (Number)**: Adicional correspondente a 1/3 (um terço) da remuneração, pago a membros e servidores por ocasião das férias.
- **Abono de Permanência (Number)**: Valor equivalente ao da contribuição previdenciária, devido ao Membro/Servidor que esteja em condição de aposentar-se, mas que optou por continuar em atividade (instituído pela Emenda Constitucional nº 41, de 16 de dezembro de 2003).
- **Outras Remunerações Temporárias (Number)**: Valor total (somatório) das Remunerações Temporárias.

- **Verbas Indenizatórias (Number)**:  Valor total (somatório) das Verbas Indenizatórias.

- **Total de Rendimentos Brutos (Number)**: Total dos rendimentos brutos pagos no mês.
- **Contribuição Previdenciária (Number)**: Contribuição Previdenciária Oficial (Plano de Seguridade Social do Servidor Público e Regime Geral de Previdência Social).
- **Imposto de Renda (Number)**: Imposto de Renda Retido na Fonte.
- **Retenção por Teto Constitucional (Number)**: Valor deduzido da remuneração básica bruta, quando esta ultrapassa o teto constitucional, nos termos da legislação correspondente.
- **Total de Descontos (Number)**: Total dos descontos efetuados no mês.
- **Rendimento Líquido Total (Number)**: Rendimento líquido após os descontos referidos nos itens anteriores.

Planilha de verbas indenizatórias e outras remunerações temporárias (disponiveis a partir do mês 7 de 2019). Seguem o seguinte formato:

- **Matrícula (String)**: Matrícula do funcionário.
- **Nome (String)**: Nome completo do funcionário.
- **Cargo (String)**: Cargo do funcionário dentro do MP.
- **Lotação (String)**: Local (cidade, departamento, promotoria) em que o funcionário trabalha.

- **Verbas Indenizatórias (Number)**: Auxílio-alimentação, Auxílio-transporte, Auxílio-Moradia, Ajuda de Custo e outras dessa natureza.

- **Outras Remunerações Temporárias (Number)**: Valores pagos a título de Adicional de Insalubridade ou de Periculosidade, Adicional Noturno, Serviço Extraordinário, Substituição de Função, Cumulações.

## Como usar

<!-- ### Executando com Docker

 - Inicialmente é preciso instalar o [Docker](https://docs.docker.com/install/). 

 - Construção da imagem:

    ```sh
    $ cd coletores/mpms
    $ sudo docker build -t mpms .
    ```
 - Execução:
 
    ```sh
    $ sudo docker run -e YEAR=2020 -e MONTH=2 -e DRIVER_PATH=/chromedriver -e GIT_COMMIT=$(git rev-list -1 HEAD) mpms
    ``` -->

### Execução sem Docker:

- Para executar o script é necessário rodar o seguinte comando, a partir do diretório mpms, adicionando às variáveis seus respectivos valores, a depender da consulta desejada. É válido lembrar que faz-se necessario ter o [Python 3.8+](https://www.python.org/downloads/) instalado, bem como o chromedriver compatível com a versão do seu Google Chrome. Ele pode ser baixado [aqui](https://chromedriver.chromium.org/downloads).
 
    ```sh
    $ YEAR=2018 MONTH=03 DRIVER_PATH=/chromedriver GIT_COMMIT=$(git rev-list -1 HEAD) python3 src/main.py
    ```
- Para que a execução do script possa ser corretamente executada é necessário que todos os requirements sejam devidamente instalados. Para isso, executar o [PIP](https://pip.pypa.io/en/stable/installing/) passando o arquivo requiments.txt, por meio do seguinte comando:
   
   ```sh
    $ pip install -r requirements.txt
   ```