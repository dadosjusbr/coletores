# Conselho Nacional de Justiça (CNJ)

Este coletor tem como objetivo a recuperação de informações sobre folhas de pagamentos dos funcionários dos tribunais brasileiros, a partir do Conselho Nacional de Justiça. O site com as informações pode ser acessado [aqui](https://paineis.cnj.jus.br/QvAJAXZfc/opendoc.htm?document=qvw_l%2FPainelCNJ.qvw&host=QVS%40neodimio03&anonymous=true&sheet=shPORT63Relatorios).

O crawler está estruturado como uma CLI. Você deve passar dois argumentos: O órgão e o caminho para o diretório do chromedriver, e serão baixadas quatro planilhas no formato xlsx, cada planilha é referente a uma destas categorias:
-   1. Contracheque
-   2. Direitos Pessoais
-   3. Indenizações
-   4. Direitos Eventuais

Estas planilhas contém as informações de pagamento de todos os meses disponíveis, a fim de gerar os crawling results de cada mês.

## Como usar

### Executando com Docker

 - Inicialmente é preciso instalar o [Docker](https://docs.docker.com/install/). 

 - Construção da imagem:

  ```sh
    $ cd coletores/cnj
    $ sudo docker build -t cnj .
  ```
 - Execução:
 
  ```sh
    $ sudo docker run -e COURT=TJRJ -e YEAR=2020 -e MONTH=2 -e DRIVER_PATH=/chromedriver -e GIT_COMMIT=$(git rev-list -1 HEAD) cnj
  ```

### Execução sem Docker:

- Para executar o script é necessário rodar o seguinte comando, a partir do diretório cnj, adicionando às variáveis seus respectivos valores, a depender da consulta desejada. É válido lembrar que faz-se necessario ter o [Python 3.6.9](https://www.python.org/downloads/) instalado, bem como o chromedriver compatível com a versão do seu Google Chrome. Ele pode ser baixado [aqui](https://chromedriver.chromium.org/downloads).
 
    ```sh
    COURT=TJRJ YEAR=2018 MONTH=03 DRIVER_PATH=/chromedriver GIT_COMMIT=$(git rev-list -1 HEAD) python3 main.py
    ```
- Para que a execução do script possa ser corretamente executada é necessário que todos os requirements sejam devidamente instalados. Para isso, executar o [PIP](https://pip.pypa.io/en/stable/installing/) passando o arquivo requiments.txt, por meio do seguinte comando:
   
   ```sh
      pip install -r requirements.txt
   ```
