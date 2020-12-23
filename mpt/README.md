# Ministério Público do Trabalho - Crawler

Este crawler tem como objetivo a recuperação de informações sobre folhas de pagamentos dos funcionários do Ministério Público do Trabalho. O site com as informações pode ser acessado [aqui](https://mpt.mp.br/MPTransparencia/pages/index.xhtml).

O crawler está estruturado como uma CLI. Você deve passar quatro argumentos (mês, ano, diretório de download e diretório do chromedriver) e serão baixadas seis planilhas no formato ODS, cada planilha é referente a uma destas categorias:

- Categoria 1: Membros ativos.
- Categoria 2: Membros inativos.
- Categoria 3: Servidores ativos.
- Categoria 4: Servidores inativos.
- Categoria 5: Colaboradores.
- Categoria 6: Pensionistas.

## Como usar

### Execução com Python:

 - Para executar o script é necessário rodar o seguinte comando, a partir do diretório mpt, adicionando às variáveis seus respectivos valores, a depender da consulta desejada. É válido lembrar que faz-se necessario ter o [Python](https://www.python.org/downloads/) instalado.
 
    ```sh
    MONTH=1 YEAR=2020 OUTPUT_FOLDER=/output DRIVER_PATH=/chromedriver GIT_COMMIT=$(git rev-list -1 HEAD) python3 main.py
    ```
 - Para que a execução do script possa ser corretamente executada é necessário que todos os requirements sejam devidamente instalados. Para isso, executar o [PIP](https://pypi.org/project/pip/) passando o arquivo requiments.txt, por meio do seguinte comando:
   
   ```sh
      pip install -r requirements.txt
   ```
