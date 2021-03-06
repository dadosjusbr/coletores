# Ministério Público de São Paulo

Este crawler tem como objetivo a recuperação de informações sobre folhas de pagamentos dos funcionários do Ministério Público de São Paulo, nos anos 2018, 2019 e 2020. O site com as informações pode ser acessado [aqui](http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque).

O coletor será estruturado como uma CLI. Uma vez passado como argumentos mês e ano, será feito o download de planilhas no formato ODS e XLSX. Cada planilha é referente a uma dessas categorias:

    Tipo I - Folha de remuneração: Membros Ativos, Membros Inativos, Servidores Ativos, Servidores Inativos, Pensionistas, Colaboradores.

    Tipo II - Verbas Referentes á exercícios anteriores.

    Tipo III - Verbas Indenizatórias e outras remunerações temporárias.

## Como usar

 ### Executando com Docker

 - Inicialmente é preciso instalar o [Docker](https://docs.docker.com/install/). 

 - Construção da imagem:

  ```sh
    $ cd coletores/mpsp
    $ sudo docker build -t mpsp .
  ```
 - Execução:
 
  ```sh
    $ sudo docker run -e MONTH=02 -e YEAR=2020 -e GIT_COMMIT=$(git rev-list -1 HEAD) mpsp 
  ```

 ### Executando sem Docker

 - É necessário ter instalado o [Python](https://www.python.org/downloads/release/python-385/) versão 3.8.5;
 
No Linux, distribuições Ubuntu/Mint:

```
sudo apt install python3 python3-pip
```

 - Utilize o PiP (foi utilizada a versão 20.3.3) para instalar as dependências que estão listadas no arquivo requirements.txt.
  
    ```sh
      $ cd coletores/mpsp
      $ pip3 install -r requirements.txt
    ```

  - Após concluida a instalação das dependências utilize os seguintes comandos:  

   ```sh
      $ cd src
      $ MONTH=01 YEAR=2020 GIT_COMMIT=$(git rev-list -1 HEAD) python3 main.py
  ```

## Dicionário de Dados

As planilhas com a remuneração de membros e servidores possuem as seguintes colunas:   


- **Nome (String)**: Nome completo do funcionário
- **Matrícula (String)**: Matrícula do funcionário  
- **Cargo (String)**: Cargo do funcionário dentro do MP
- **Lotação (String)**: Local (cidade, departamento, promotoria) em que o funcionário trabalha
- **Remuneração do cargo efetivo (Number)**: Vencimento, GAMPU, V.P.I, Adicionais de Qualificação, G.A.E e G.A.S, além de outras desta natureza. Soma de todas essas remunerações
- **Outras Verbas Remuneratórias, Legais ou Judiciais (Number)**: V.P.N.I., Adicional por tempo de serviço, quintos, décimos e vantagens decorrentes de sentença judicial ou extensão administrativa
- **Função de Confiança ou Cargo em Comissão (Number)**: Rubricas que representam a retribuição paga pelo exercício de função (servidor efetivo) ou remuneração de cargo em comissão (servidor sem vínculo ou requisitado)
- **Gratificação Natalina (Number)**: Parcelas da Gratificação Natalina (13º) pagas no mês corrente, ou no caso de vacância ou exoneração do servidor
- **Férias - ⅓ Constitucional (Number)**: Adicional correspondente a 1/3 (um terço) da remuneração, pago ao servidor por ocasião das férias
- **Abono de Permanência (Number)**:  Valor equivalente ao da contribuição previdenciária, devido ao funcionário público que esteja em condição de aposentar-se, mas que optou por continuar em atividade (instituído pela Emenda Constitucional nº 41, de 16 de dezembro de 2003
- **Outras Remunerações Temporárias (Number)**: Valor total (somatório) das remunerações temporárias ou eventuais discriminadas na Tabela de Idenizações temporárias.
- **Verbas Indenizatórias**: Valor total (somatório) das verbas indenizatórias discriminadas na Tabela III.
- **Total de Rendimentos Brutos (Number)**: Total dos rendimentos brutos pagos no mês
- **Contribuição Previdenciária (Number)**: Contribuição Previdenciária Oficial (Plano de Seguridade Social do Servidor Público e Regime Geral de Previdência Social)
- **Imposto de Renda (Number)**: Contribuição Previdenciária Oficial (Plano de Seguridade Social do Servidor Público e Regime Geral de Previdência Social).
- **Retenção por Teto Constitucional (Number)**: Valor deduzido da remuneração básica bruta, quando esta ultrapassa o teto constitucional, nos termos da legislação correspondente
- **Total de Descontos (Number)**:  Total dos descontos efetuados no mês
- **Rendimento Líquido Total (Number)**: Rendimento líquido após os descontos referidos nos itens anteriores


As planilhas com os valores recebidos por pensionistas possuem as seguintes colunas:

- **Cod_Beneficio (String)**: Código do Benefício.
- **Nom_Servidor (String)**: Nome do servidor.
- **Cod_Cargo_Servidor (String)**: Código do cargo do servidor dentro do MP
- **Cargo_Servidor (String)**: Cargo do servidor dentro do MP
- **Nom_Beneficiario (String)**: Nome do beneficiario
- **Situação_beneficiario (String)** Situação do beneficio recebido (vigente, suspenso)
- **Dat_Ini_Ben (Date)**: Data de inicio do pagamento do benefício
- **Num_portaria (String)**: Número da portaria que permite o recebimento do benefício
- **Dat_Publ (Date)**: Não foi possível identificar a qual publicação se refere essa data
- **Val_Bruto (Number)**: Total dos rendimentos brutos pagos no mês
- **Val_Liq (Number)**: Total após os descontos
- **Periodo_Folha (Date)**: Período referente ao contra-cheque

As planilhas com os valores das verbas idenizatórias e outras remunerações temporárias possuem as seguintes colunas:

- **Nome (String)**: Nome completo do funcionário
- **Matrícula (String)**: Matrícula do funcionário  
- **Cargo (String)**: Cargo do funcionário dentro do MP
- **Lotação (String)**: Local (cidade, departamento, promotoria) em que o funcionário trabalha
- **Aux Alimentação (Number)**: Auxílio Alimentação pago por mês
- **Licença Compensatória ato 1124/18 (Number)**: Valor correspondente a compensação ao  servidor por qualquer direito adquirido.
- **Férias em pecúnia (Number)**: Valor correspondente a ⅓ das férias que o trabalhador pode vender 
- **LP em pecúnia (Number)**: Valor correspondente a licensa prêmio pago ao trabalhador
- **Gratificação Cumulativa (Number)**: quantia paga pelo Ministério Público a membro da Instituição quando este for designado para, sem prejuízo das atribuições de seu cargo, acumular ou auxiliar em cargo ou funções de execução da própria sede ou localidade;
- **Gratificação de Natureza Especial (Number)**: quantia paga pelo Ministério Público ao membro da Instituição que, mediante designação das autoridades competentes, executar funções atinentes ao seu cargo fora dos períodos normais de expediente;
- **Gratificação de Grupo de Atuação Especial (Number)**: Gratificação Especial aos servidores e inativos do Quadro do Ministério Público.

## Planilhas

- Para obter as planilhas que não estão presentes em nosso coletor, é necessário consultar o [site](http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque)  e verificar de acordo com o tipos de pagamento, mês e ano desejados; 

- Nos anos analisados (2018, 2019 e 2020) não houve declaração de pagamentos de remunerações, proventos, indenizações ou outros valores pagos a qualquer título, a Colaboradores;

- Planilhas que não conseguimos obter:

    Mês | Ano |  Tipo Funcionario | Tipo planilha | Motivo
    :------:|:------:|:-------------:|:-------------:|:--------------:
    09     | 2019  | Servidores Ativos | Remuneração Mensal | No lugar está disponibilizada a planilha referente a Verbas indenizatórias desse mesmo mês.

- Analisamos as planilhas de dois tipos: Remunerações Mensais e Indenizações/Outras verbas temporárias:

### Tipo 1 - Remunerações Mensais ###

    As planilhas são referentes a:
        - Membros Ativos;
        - Membros Inativos;
        - Servidores Ativos;
        - Servidores Inativos;
        - Pensionistas Membros;
        - Pensionistas Servidores

    - O formato das tabelas listadas a cima, exceto as de pensionistas, seguem o modelo [Tipo I](http://www.cnmp.mp.br/portal/images/Resolucoes/Anexo-200---RES-89.pdf)
    
### Tipo 3 - Tabela de Indenizações ### 
    As planilhas são referentes a:
            - Membros Ativos;
            - Membros Inativos;
            - Servidores Ativos;
            - Servidores Inativos;


    - Formato das tabelas: [Tipo III](http://www.cnmp.mp.br/portal/images/Resolucoes/Anexo-200---RES-89.pdf)

    - Obs: Indenizações disponíveis apenas para alguns meses dos anos de 2018, 2019 e 2020.

## Dificuldades no entendimento dos dados


- Existem funcionários que estão nas planilhas de verbas indenizatórias e remuneração temporárias, porém não estão nas planilhas de remuneração mensal. Não ficou claro o porquê disso ter ocorrido;

- Em algumas planilhas o valor correspondente ao Adicional Insalubridade está declarado como verbas indenizatórias e em outras como remunerações temporárias. Também não ficou claro o porquê disso ter ocorrido;

- A planilha referente a pensionistas não apresenta explicações sobre o significado das variáveis. Houve dúvidas no entendimento da Dat_Publ, uma vez que foi indentificado que essa data não é referente a publicação da portaria que estabelece o recebimento do beneficio, já que tem outro atributo que é referente a data do inicio do recebimento. E em alguns casos, o inicio do beneficio começou antes dessa dat_publ;


- Existem alguns valores negativos relacionados indenizações, como é o caso do funcionario que possuí matrícula 2720, na [tabela](http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membros%20inativos%20ref0519.ods) referente a servidores inativos do mês de maio de 2019. A dúvida é: esses valores realmente deveriam ser negativos?

- Existem pensionistas com valores líquido maiores que os valores bruto. Houve dificuldade para entender o porquê disso ocorrer. Pode ser visto um exemplo na planilha referente a pensionistas membros do mês de maio de 2019. No beneficiário correspondente ao código 60601181. [Link](http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20Membros%20do%20Minist%C3%A9rio%20P%C3%BAblico%20052019.ods)


## Dificuldades para trabalhar com os dados

- Problema para automatizar a coleta dos dados devido a URL para baixar as planilhas variarem bastante de acordo com o grupo, mês e anos. Sendo necessário testar todos os links.

    Abaixo, temos alguns exemplos das urls para downloads das planilhas referentes aos meses outubro, novembro e dezembro, respectivamente. No mês outubro o campo que seria referente ao mês se encontra com o dígito 09, além de também conter  "_1" que não está presente nos demais links.
        
    - http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20memb092019_1.ods
    
    - http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20memb112019A.ods

    - http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20memb122019.ods

    Essa variação na formação do link está presente em diversos meses, em todos os anos analisados (2018, 2019 e 2020)

    Alguns links com diferenças entre letras minúsculas e maiúsculas também dificultam a coleta, visto quê por ser uma pequena diferença é necessário testar todos os links.

    - http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20membros%20ativos%20ref0519.ods
    
    - http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20Membros%20Ativos%20ref0619.ods



- Problemas para automatizar o parser das planilhas de Remuneraões Mensais por possuirem formatos diferentes, algunas incluem algumas verbas indenizatórias outras não, além disso algumas informações estão presentes em algumas planilhas e em outras não. Como exemplo, as planilhas dos Servidores Inativos dos meses de [abril](http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servidores%20inativos%20ref0419.ods), [maio](http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servidores%20inativos%20ref0519.ods), [junho](http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20Servidores%20Inativos%20ref0619.ods) e [julho](http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Servidores%20Inativos%20-%20Tabela%20I%20ref%20072019.ods) de 2019,  existem diferenças em quais valores são informados e nem sempre aparecem na mesma ordem em todas as tabelas.
    



