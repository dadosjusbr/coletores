# Ministério Público do Estado do Rio Grande do Norte

Este coletor tem como objetivo a recuperação de informações sobre folhas de pagamentos dos membros ativos do Ministério Público do Estado do Rio Grande do Norte nos anos 2018, 2019 e 2020. O site com as informações pode ser acessado [aqui](http://transparencia.mprn.mp.br/).

O coletor será estruturado como uma CLI. Uma vez passado como argumentos mês e ano, será feito o download de planilhas, no formato ODS, sendo cada uma referente a uma dessas categorias:

- Tipo I - Folha de remuneração: Membros Ativos - As planilhas deste tipo, com exceção das dos colaboradores, seguem o formato seguinte:

- **Nome (String)**: Nome completo do funcionário.
- **Matrícula (String)**: Matrícula do funcionário.
- **Cargo (String)**: Cargo do funcionário dentro do MP.
- **Remuneração do Cargo Efetivo (Number)**: Subsídio dos membros do Ministério Público, proventos de membros e servidores do Ministério Público, vencimento básico, gratificação por exercício de atividades perigosas dos secretários de diligências, parcela de readaptação e outras verbas de mesma natureza.
- **Outras Verbas Remuneratórias, Legais ou Judiciais (Number)**: Adicional por tempo de serviço, avanços trienais, FG incorporada, AS incorporada, gratificações incorporadas e outras verbas de mesma natureza.
- **Função de Confiança ou Cargo em Comissão (Number)**: Gratificações de direção, chefe de gabinete, procurador-assessor, promotor-assessor, promotor-corregedor e coordenador de centro de apoio operacional. Função Gratificada (servidor efetivo) ou remuneração de cargo em comissão e outras verbas de mesma natureza.
- **Gratificação Natalina (Number)**: Parcelas da gratificação natalina (13º) pagas no mês corrente.
- **Férias (1/3 constitucional) (Number)**: Adicional correspondente a 1/3 (um terço) da remuneração, pago a membros e servidores por ocasião das férias.
- **Abono de Permanência (Number)**: Valor equivalente ao da contribuição previdenciária, devido ao membro ou servidor que esteja em condição de aposentar-se, mas que optou por continuar em atividade, em conformidade com o Art. 40, § 19, da Constituição Federal.
- **Outras remunerações retroativas/Temporárias (Number)**: Valores pagos a título de adicional de insalubridade ou de periculosidade, adicional noturno, serviço extraordinário, substituição de função, gratificação de diretor de promotoria de justiça, gratificação de difícil provimento e gratificação por participação em órgãos colegiados.
- **Indenizações (Number)**: Auxílio-alimentação, auxílio-moradia, auxílio-transporte, auxílio-creche, abono-família, férias não usufruídas e outras verbas de mesma natureza.
- **Total de Rendimentos Brutos (Number)**: Total dos rendimentos brutos pagos no mês.
- **Contribuição Previdenciária (Number)**: Contribuição Previdenciária Oficial (IPERGS ou INSS) e IPERGS-Saúde.
- **Imposto de Renda (Number)**: Imposto de Renda Retido na Fonte.
- **Retenção por Teto Constitucional (Number)**: Valor deduzido da remuneração bruta, quando esta ultrapassa o teto constitucional, de acordo com a Resolução nº 09/2006 do CNMP.
- **Total de Descontos (Number)**: Soma dos descontos referidos nos itens 8, 9 e 10.
- **Total Líquido (Number)**: Rendimento obtido após o abatimento dos descontos referidos no item 11. O valor líquido efetivamente recebido pelo membro ou servidor pode ser inferior ao ora divulgado, porque não são considerados os descontos de caráter pessoal.


- Tipo III - Verbas Indenizatórias e outras remunerações temporárias. Seguem o formato seguinte:

- **Matrícula (String)**: Matrícula do funcionário.
- **Nome (String)**: Nome completo do funcionário.
- **Cargo (String)**: Cargo do funcionário dentro do MP.
- **Lotação (String)**: Local (cidade, departamento, promotoria) em que o funcionário trabalha.
- **Verbas Indenizatórias**: Auxílio Saúde, Auxílio Alimentação, Auxílio Moradia.
- **Outras Remunerações Temporárias**: Substituição Cargo C. Função GAE, Adicional Periculosidade, Licença Compensatória.

## Dificuldades 

- URLs:

    - A URL para download dos dados possui um código que é corresponde ao mês. No entanto, esse código não aparenta seguir padrão referenciando o mês correspondente. 
 
    - A cada mês lançado no porta de transparência do MPRN é necessário verificar o link para download do mês desejado (referente a remuneração mensal e a verbas indenizatórias) e acrescentar no crawler os códigos para acesso.

    Exemplo:
     - O link abaixo é refetente a remuneração mensal (R0082) de novembro de 2020 e o código correspondente a esse mês é 45874.
    http://transparencia.mprn.mp.br/Arquivos/C0007/2020/R0082/45874.ods

     - O mesmo ocorre nas planilhas de Verbas indenizatórias e Remunerações tempórarias (R2167). O link abaixo é do mês de novembro de 2020, o código 46826 corresponde ao mês 
     http://transparencia.mprn.mp.br/Arquivos/C0007/2020/R2167/46826.ods?dt=05042021145100

## Como usar

 ### Executando com Docker

 - Inicialmente é preciso instalar o [Docker](https://docs.docker.com/install/). 

 - Construção da imagem:

  ```sh
    $ cd coletores/mprn
    $ sudo docker build -t mprn .
  ```
 - Execução:
 
  ```sh
    $ sudo docker run -e MONTH=02 -e YEAR=2020 -e GIT_COMMIT=$(git rev-list -1 HEAD) mprn
  ```

 ### Executando sem Docker

 - É necessário ter instalado o [Python](https://www.python.org/downloads/release/python-385/) versão 3.8.5;
 
No Linux, distribuições Ubuntu/Mint:

```
sudo apt install python3 python3-pip
```

 - Utilize o PiP (foi utilizada a versão 20.3.3) para instalar as dependências que estão listadas no arquivo requirements.txt.
  
    ```sh
      $ cd coletores/mprn
      $ pip3 install -r requirements.txt
    ```

  - Após concluida a instalação das dependências utilize os seguintes comandos:  

   ```sh
      $ cd src
      $ MONTH=01 YEAR=2020 GIT_COMMIT=$(git rev-list -1 HEAD) python3 main.py
  ```