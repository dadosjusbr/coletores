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

### Executando sem uso do docker:

 - É necessário ter instalado o Python Pip. Clique [aqui] (https://linuxize.com/post/how-to-install-pip-on-ubuntu-20.04/) para saber mais.

 - Após instalado o pip, rode os seguintes comandos:

```sh
pip install -U python-dotenv
pip install pyexcel-xls
pip install json
```
 - Para preencher o env, basta criar uma cópia do arquivo .env.example renomeando para .env. os parãmetros requeridos são year = ano e month, esse último deve ser preenchido de acordo com o número que representa o mês. (Exemplo: Se quero consultas a folha de pagamento referente a janeiro de 2020 devo preencher, year=2020 e month=1).

 - Para executar o script é necessário rodar o seguinte comando no diretório mpm:

  ```sh
    python main.py
  ```