# Ministério Público de Rondônia (MPRO)

Este coletor tem como objetivo a recuperação de informações sobre folhas de pagamentos de funcionários a partir do Ministério Público de Rondônia. O site com as informações pode ser acessado [aqui](https://servicos-portal.mpro.mp.br/web/mp-transparente/contracheque).

O crawler está estruturado como uma CLI. Você deve passar dois argumentos: O órgão e o caminho para o diretório do chromedriver, e serão baixadas duas planilhas no formato csv, cada planilha é referente a uma destas categorias:
-   1. Contracheque - Membros Ativos
-   2. Contracheque - Verbas Indenizatórias

Estas planilhas contém as informações de pagamento de todos os meses disponíveis, a fim de gerar os crawling results de cada mês.

## Como usar
### Execução com Python:

- Para executar o script é necessário rodar o seguinte comando, a partir do diretório mpro, adicionando às variáveis seus respectivos valores, a depender da consulta desejada. É válido lembrar que faz-se necessario ter o [Python 3.6.9](https://www.python.org/downloads/) instalado, bem como o chromedriver compatível com a versão do seu Google Chrome. Ele pode ser baixado [aqui](https://chromedriver.chromium.org/downloads).

    ```sh
    COURT=MPRO YEAR=2018 DRIVER_PATH=/chromedriver GIT_COMMIT=$(git rev-list -1 HEAD) python3 src/main.py
    ```
- Para que a execução do script possa ser corretamente executada é necessário que todos os requirements sejam devidamente instalados. Para isso, executar o [PIP](https://pip.pypa.io/en/stable/installing/) passando o arquivo requiments.txt, por meio do seguinte comando:

   ```sh
      pip install -r requirements.txt
   ```