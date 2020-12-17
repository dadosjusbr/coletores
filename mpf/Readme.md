# Ministério Público Federal

Este crawler tem como objetivo a recuperação de informações sobre folhas de pagamentos dos funcionários do Ministério Público Federal. O site com as informações pode ser acessado [aqui](http://www.transparencia.mpf.mp.br/conteudo/contracheque).

O crawler está estruturado de modo que serão passadas via cli os quatro parâmetros descritos abaixo:

```sh
MONTH = (Inteiro entre 1 - 12 responsável por indicar o mês)
YEAR = (Inteiro entre 2015 - 2020 responsável por indicar o ano)
OUTPUT_FOLDER = (Parâmetro no formato ./nomeDaPastaDestino responsável por indicar em qual diretório filho de src o download dos arquivos deve ser realizado, caso o diretório não exista ele será criado)
GIT_COMMIT = (Parâmetro contendo um hashcode de modo a representar a versão mais recente desse coletor. Obtêm-se pelo comando: $(git rev-list -1 HEAD))
```
O número de arquivos baixados e seus respectivos formatos variam de acordo com o mês e ano solicitado na consulta.

Será realizado o download de 6 arquivos no formato xlsx referentes ao mês e ano definidos na variável de ambiente para consultas anteriores á Julho de 2019, cujos arquivos pertencem aos seguintes grupos : 

 -Grupo 1: Membros Ativos;  
 -Grupo 2: Membros Inativos;  
 -Grupo 3: Servidores Ativos;  
 -Grupo 4: Servidores Inativos;  
 -Grupo 5: Pensionistas;  
 -Grupo 6: Colaboradores;  

Para consultas que se referem á meses iguais ou posteriores á Julho de 2019, será realizado o download de 12 arquivos no formato ods referentes ao mês e ano definidos na variável de ambiente, cujos arquivos pertecem aos seguintes grupos:

 -Grupo 1: Membros Ativos;  
 -Grupo 2: Membros Inativos;  
 -Grupo 3: Servidores Ativos;  
 -Grupo 4: Servidores Inativos;  
 -Grupo 5: Pensionistas;  
 -Grupo 6: Colaboradores;  
 -Grupo 7: Verbas indenizatórias e outras remunerações temporárias membros ativos;  
 -Grupo 8: Verbas indenizatórias e outras remunerações temporárias membros inativos;  
 -Grupo 9: Verbas indenizatórias e outras remunerações temporárias servidores ativos;  
 -Grupo 10: Verbas indenizatórias e outras remunerações temporárias servidores inativos;  
 -Grupo 11: Verbas indenizatórias e outras remunerações temporárias pensionistas;  
 -Grupo 12: Verbas indenizatórias e outras remunerações temporárias colaboradores;  

É importante verificar que os arquivos nomeados como verbas indenizatórias são responsáveis por detalhar com maior precisão a natureza de algumas remunerações associadas aos grupos 1 á 6.

## Como utilizar 

### Executando com Docker

- Inicialmente é preciso instalar o [Docker](https://docs.docker.com/install/).

- Construção da imagem:

```sh
cd coletores/mpf
sudo docker build -t mpf .
``` 
- Execução:  
    - Para executar será necessário utilizar-se  do seguinte comando:   

```sh
sudo docker run --env-file=./src/.env mpf
```
### Execução sem uso de Docker 

- Inicialmente é preciso ter instalado o [Python](https://www.python.org/downloads/) versão 3.8.5 na sua máquina.
  - Utilize o gerenciador de pacotes do python [PiP](https://pypi.org/) para instalar as dependências contidas no arquivo requirements.txt .
  - Para instalar as dependências execute o seguinte comando:

    ```sh
    cd coletores/mpf 
    pip3 install -r requirements.txt
    ```
  - Finalmente execute :

    ```sh
    cd coletores/mpf/src
    python3 main.py
    ```











