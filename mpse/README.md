# Ministério Público de Sergipe

Este coletor tem como objetivo a recuperação de informações sobre folhas de pagamentos dos membros ativos do Ministério Público de Sergipe nos anos 2018, 2019, 2020 e 2021. O site com as informações pode ser acessado [aqui](https://sistemas.mpse.mp.br/2.0/PublicDoc//PublicacaoDocumento/Contracheque_Tr.html).

O coletor será estruturado como uma CLI. Uma vez passado como argumentos mês e ano, será feito o download de planilhas, no formato ODS e ODT, sendo cada uma referente a uma dessas categorias:

- Folha de remuneração: Membros Ativos - As planilhas deste tipo, com exceção das dos colaboradores, seguem o formato seguinte:

- **Matrícula (String)**: Matrícula do funcionário.
- **Nome (String)**: Nome completo do funcionário.
- **Cargo (String)**: Cargo do funcionário dentro do MP.
- **Lotação (String)**: Local (cidade, departamento, promotoria) em que o funcionário trabalha.
- **Remuneração do Cargo Efetivo (Number)**: Subsídio dos membros do Ministério Público, proventos de membros e servidores do Ministério Público, vencimento básico, gratificação por exercício de atividades perigosas dos secretários de diligências, parcela de readaptação e outras verbas de mesma natureza.
- **Outras Verbas Remuneratórias, Legais ou Judiciais (Number)**: Adicional por tempo de serviço, avanços trienais, FG incorporada, AS incorporada, gratificações incorporadas e outras verbas de mesma natureza.
- **Função de Confiança ou Cargo em Comissão (Number)**: Gratificações de direção, chefe de gabinete, procurador-assessor, promotor-assessor, promotor-corregedor e coordenador de centro de apoio operacional. Função Gratificada (servidor efetivo) ou remuneração de cargo em comissão e outras verbas de mesma natureza.
- **Gratificação Natalina (Number)**: Parcelas da gratificação natalina (13º) pagas no mês corrente.
- **Férias Constitucionais (Number)**: Adicional correspondente a 1/3 (um terço) da remuneração, pago a membros e servidores por ocasião das férias.
- **Abono de Permanência (Number)**: Valor equivalente ao da contribuição previdenciária, devido ao membro ou servidor que esteja em condição de aposentar-se, mas que optou por continuar em atividade, em conformidade com o Art. 40, § 19, da Constituição Federal.

- **Outras Remunerações Temporárias (Number)**: GEO, Dif. GEO, Insalubridade, Dif. Insalubridade, Peruculosidade, Dif. periculosidade, Adicional Trabalho Técnico, Dif. Adicional Trabalho Técnico, Grat. Atividade Ensino, Substituições, Dif. Substituições, Cumulação, Dif. Cumulação, Dif. Cumulação, Representação de Direção, Dif. Representação de Direção, Grat. Turma Recursal, Dif Grat. Turma Recursal, Grat. Dificil Provimento, Dif. Grat. Dificil Provimento, Grat. Assessor, Dif. Grat. Assessor, Representação GAECO, Dif. Representação GAECO, Dif. Representação GAECO.

- **Verbas Indenizatórias (Number)**: Auxílio-Saúde, Dif. Auxílio-Saúde, Auxílio-Alimentação, Dif. Auxílio-Alimentação,  Auxílio-Interiorização, Dif. Auxílio-Interiorização, Dif. Auxílio Lei 8.625/93, Indenizações Férias/Licença-Prêmio, Abono Pecuniário,Dif. Abono Pecuniário, Ressarcimentos.

- **Total de Rendimentos Brutos (Number)**: Total dos rendimentos brutos pagos no mês.
- **Contribuição Previdenciária (Number)**: Contribuição Previdenciária Oficial (IPERGS ou INSS) e IPERGS-Saúde.
- **Imposto de Renda (Number)**: Imposto de Renda Retido na Fonte.
- **Retenção por Teto Constitucional (Number)**: Valor deduzido da remuneração bruta, quando esta ultrapassa o teto constitucional, de acordo com a Resolução nº 09/2006 do CNMP.
- **Total de Descontos (Number)**: Soma dos descontos referidos nos itens 8, 9 e 10.
- **Rendimento Líquido Total (Number)**: Rendimento líquido após os descontos referidos nos itens anteriores.


- Verbas Indenizatórias e outras remunerações temporárias. Seguem o formato seguinte:

- **Matrícula (String)**: Matrícula do funcionário.
- **Nome (String)**: Nome completo do funcionário.
- **Cargo (String)**: Cargo do funcionário dentro do MP.
- **Lotação (String)**: Local (cidade, departamento, promotoria) em que o funcionário trabalha.
- **Verbas Indenizatórias**: Auxílio-Saúde, Dif. Auxílio-Saúde, Auxílio-Alimentação, Dif. Auxílio-Alimentação,  Auxílio-Interiorização, Dif. Auxílio-Interiorização, Dif. Auxílio Lei 8.625/93, Indenizações Férias/Licença-Prêmio, Abono Pecuniário,Dif. Abono Pecuniário, Ressarcimentos.

- **Outras Remunerações Temporárias**: GEO, Dif. GEO, Insalubridade, Dif. Insalubridade, Periculosidade, Dif. periculosidade, Adicional Trabalho Técnico, Dif. Adicional Trabalho Técnico, Grat. Atividade Ensino, Substituições, Dif. Substituições, Cumulação, Dif. Cumulação, Dif. Cumulação, Representação de Direção, Dif. Representação de Direção, Grat. Turma Recursal, Dif Grat. Turma Recursal, Grat. Dificil Provimento, Dif. Grat. Dificil Provimento, Grat. Assessor, Dif. Grat. Assessor, Representação GAECO, Dif. Representação GAECO.


## Dificuldades 

- Cada planilha de dados, liberada mensalmente, possui um ID único de acesso, dificultando assim uma automação mais eficiente da coleta.

- Durante todo o período monitorado, 2018 até o momento, a maneira de disponibilazação dos dados foi alterada três vezes. Alterações na maneira que o arquivo é formatado e no conteúdo das colunas obrigaram a necessidade da criação de diferentes arquivos parser que se adéquem a cada um deles.

Exemplos:
    - Durante o ano de 2018, os dados são expostos com subdivisões por páginas, o que gera linhas de dados excepcionais que não são previstas no parser padrão, por exemplo, numeração de páginas e duplicação de cabeçalhos.
    - Durante todo o ano de 2018 e Junho, Julho e Agosto de 2019 ocorrem alterações em quais colunas temos disponíveis nas planilhas de verbas indenizatórias, com a saída do dado sobre verbas recisórias.

## Como usar

 ### Executando com Docker

 - Inicialmente é preciso instalar o [Docker](https://docs.docker.com/install/). 

 - Construção da imagem:

  ```sh
    $ cd coletores/mpse
    $ sudo docker build -t mpse .
  ```
 - Execução:
 
  ```sh
    $ sudo docker run -e MONTH=02 -e YEAR=2020 -e GIT_COMMIT=$(git rev-list -1 HEAD) mpse
  ```

 ### Executando sem Docker

 - É necessário ter instalado o [Python](https://www.python.org/downloads/release/python-385/) versão 3.8.5;
 
No Linux, distribuições Ubuntu/Mint:

```
sudo apt install python3 python3-pip
```

 - Utilize o PiP (foi utilizada a versão 20.3.3) para instalar as dependências que estão listadas no arquivo requirements.txt.
  
    ```sh
      $ cd coletores/mpse
      $ pip3 install -r requirements.txt
    ```

  - Após concluida a instalação das dependências utilize os seguintes comandos:  

   ```sh
      $ cd src
      $ MONTH=01 YEAR=2020 GIT_COMMIT=$(git rev-list -1 HEAD) python3 main.py
  ```