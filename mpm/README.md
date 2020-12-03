# Ministério Público Militar- Crawler

Este crawler tem como objetivo a recuperação de informações sobre folhas de pagamentos dos funcionários do Ministério Público Militar. O site com as informações pode ser acessado [aqui](https://www.mpm.mp.br/folha-de-pagamento/).

Serão baixadas 12 planilhas no formato xlsx referentes ao mês e ano que foram passados como argurmentos, as mesmas são correpondentes a remuneração mensal e verbas indenizatórias dos seguintes grupo:

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
    sudo docker build -t mpf .  
  ```

  ```sh
  sudo docker run -e MONTH=2 -e YEAR=2020 mpm
  ```

 ### Executando sem Docker

   ```sh
    python main.py 
  ```