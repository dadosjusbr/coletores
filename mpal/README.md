# Ministério Público do Estado de Alagoas

Este coletor tem como objetivo a recuperação de informações sobre folhas de pagamentos dos membros ativos do Ministério Público do Estado de Alagoas nos anos 201, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020 e 2021. O site com as informações pode ser acessado [aqui](https://sistemas.mpal.mp.br/).

O coletor será estruturado como uma CLI. Uma vez passado como argumentos mês e ano, será feito o download de um arquivo, no formato JSON.

## Dicionário de dados

As planilhas referentes á remunerações possuem as seguintes colunas:

- **Tipo de Folha (String)**: Descrição do tipo de processamento de Folha
- **Nome (String)**: Nome completo do funcionário.
- **Cargo (String)**: Cargo do funcionário.
- **Lotação (String)**
- **Remuneração do Cargo Efetivo (Number)**: Subsídio dos membros do Ministério Público, proventos de membros e servidores do Ministério Público, vencimento básico, gratificação por exercício de atividades perigosas dos secretários de diligências, parcela de readaptação e outras verbas de mesma natureza.
- **Outras Verbas Remuneratórias, Legais ou Judiciais (Number)**: Adicional por tempo de serviço, avanços trienais, FG incorporada, AS incorporada, gratificações incorporadas e outras verbas de mesma natureza.
- **Função de Confiança ou Cargo em Comissão (Number)**: Gratificações de direção, chefe de gabinete, procurador-assessor, promotor-assessor, promotor-corregedor e coordenador de centro de apoio operacional. Função Gratificada (servidor efetivo) ou remuneração de cargo em comissão e outras verbas de mesma natureza.
- **Gratificação Natalina (Number)**: Parcelas da gratificação natalina (13º) pagas no mês corrente.
- **Férias (1/3 constitucional) (Number)**: Adicional correspondente a 1/3 (um terço) da remuneração, pago a membros e servidores por ocasião das férias.
- **Abono de Permanência (Number)**: Valor equivalente ao da contribuição previdenciária, devido ao membro ou servidor que esteja em condição de aposentar-se, mas que optou por continuar em atividade, em conformidade com o Art. 40, § 19, da Constituição Federal.
- **Total de Rendimentos Brutos(Number)**: Total dos rendimentos brutos pagos no mês.
- **Contribuição Previdenciária (Number)**: Contribuição Previdenciária Oficial (IPERGS ou INSS) e IPERGS-Saúde.
- **Imposto de Renda (Number)**: Imposto de Renda Retido na Fonte.
- **Retenção por Teto Constitucional (Number)**: Valor deduzido da remuneração bruta, quando esta ultrapassa o teto constitucional, de acordo com a Resolução nº 09/2006 do CNMP.
- **Total de Descontos (Number)**: Soma dos descontos referidos nos itens 8, 9 e 10.
- **Rendimento Líquido Total(Number)**: Rendimento obtido após o abatimento dos descontos referidos no item 11. O valor líquido efetivamente recebido pelo membro ou servidor pode ser inferior ao ora divulgado, porque não são considerados os descontos de caráter pessoal.
- **Indenizações (Number)**: Auxílio-alimentação, Auxílio-transporte, Auxílio-moradia, Ajuda de Custo e outras dessa natureza, exceto diárias, divulgadas neste Portal da Transparência.
- **Outras remunerações retroativas/Temporárias (Number)**: Valores pagos a título de Adicional de Insalubridade ou de Periculosidade, Adicional Noturno, Serviço Extraordinário, Substituição de Função, Cumulações.

## Como usar

 ### Executando com Docker

 - Inicialmente é preciso instalar o [Docker](https://docs.docker.com/install/). 

 - Construção da imagem:

  ```sh
    $ cd coletores/mpal
    $ sudo docker build -t mpal .
  ```
 - Execução:
 
  ```sh
    $ sudo docker run -e MONTH=2 -e YEAR=2020 -e GIT_COMMIT=$(git rev-list -1 HEAD) mpal
  ```

 ### Executando sem Docker

 - É necessário ter instalado o [Python](https://www.python.org/downloads/release/python-385/) versão 3.8.5;
 
No Linux, distribuições Ubuntu/Mint:

```
sudo apt install python3 python3-pip
```

 - Utilize o PiP (foi utilizada a versão 20.3.3) para instalar as dependências que estão listadas no arquivo requirements.txt.
  
    ```sh
      $ cd coletores/mpal
      $ pip3 install -r requirements.txt
    ```

  - Após concluida a instalação das dependências utilize os seguintes comandos:  

   ```sh
      $ cd src
      $ MONTH=1 YEAR=2020 GIT_COMMIT=$(git rev-list -1 HEAD) python3 main.py
  ```