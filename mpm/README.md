# Ministério Público Militar- Crawler

Este crawler tem como objetivo a recuperação de informações sobre folhas de pagamentos dos funcionários do Ministério Público Militar. O site com as informações pode ser acessado [aqui](https://www.mpm.mp.br/folha-de-pagamento/).

O crawler está estruturado como uma CLI. É necessário passar os argumentos mês e ano. E então, serão baixadas 12 planilhas no formato xlsx referentes ao mês e ano que foram passados como argurmentos, as mesmas são correpondentes a remuneração mensal e verbas indenizatórias dos seguintes grupo:

- Grupo 1: Membros ativos;
- Grupo 2: Membros inativos;
- Grupo 3: Servidores ativos;
- Grupo 4: Servidore inativos;
- Grupo 5: Pensionistas;
- Grupo 6: Colaboradores.

## Como usar

 - E necessário preencher o arquivo .env de acordo com o .env.example

 ### Executando com Docker

 - Inicialmente é preciso instalar o [Docker](https://docs.docker.com/install/). 

 - Construção da imagem:

  ```sh
    sudo docker build -t mpm .
  ```
 - Execução:
 
  ```sh
    sudo docker run -e MONTH=2 -e YEAR=2020 -e GIT_COMMIT=$(git rev-list -1 HEAD) mpm 
  ```

 ### Executando sem Docker

 - É necessário ter instalado o [Python] (https://www.python.org/downloads/release/python-385/) versão 3.8.5;
 - Utilize o PiP para instalar as dependências que estão listadas no arquivo requirements.txt.
  
    ```sh
      cd coletores/mpm
      pip3 install -r requirements.txt
    ```

  - Após concluida a instalação das dependências utilize os seguintes comandos:  

   ```sh
      cd src
      MONTH=1 YEAR=2020 GIT_COMMIT=$(git rev-list -1 HEAD) python3 main.py
  ```

  - Para gerar um arquivo json com o resultado do parser, rode o seguinte comando:

  ```sh
    MONTH=2 YEAR=2020 GIT_COMMIT=$(git rev-list -1 HEAD) python3 main.py > result.json
  ```