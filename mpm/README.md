# Ministério Público Militar- Crawler

Este crawler tem como objetivo a recuperação de informações sobre folhas de pagamentos dos funcionários do Ministério Público Militar. O site com as informações pode ser acessado [aqui](https://www.mpm.mp.br/folha-de-pagamento/).

Serão baixadas 6 planilhas no formato xlsx referentes ao mês e ano que foram passados como argurmentos, as mesmas são correpondentes aos seguintes grupo:

- Grupo 1: Membros ativos;
- Grupo 2: Membros inativos;
- Grupo 3: Servidores ativos;
- Grupo 4: Servidore inativos;
- Grupo 5: Pensionistas;
- Grupo 6: Colaboradores.

## Como usar

 - Para executar o script é necessário rodar o seguinte comando no diretório mpm, substituindo month pelo número correspondete ao mês. Como por exemplo para janeiro de 2020: python main.py 1 2020

  ```sh
    python main.py --month --year
  ```