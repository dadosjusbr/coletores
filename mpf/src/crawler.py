import requests
import pathlib 
import os
import sys

_REMU_MEMBROS_ATIVOS ='remuneracao-membros-ativos'
_REMU_SERVIDORES_ATIVOS ='remuneracao-servidores-ativos'
_PROV_SERVIDORES_INATIVOS = 'provento-servidores-inativos'
_PROV_MEMBROS_INATIVOS ='provento-membros-inativos'
_VALORES_PERCEBIDOS_PENSIONISTAS ='valores-percebidos-pensionistas'
_VALORES_PERCEBIDOS_COLABORADORES ='valores-percebidos-colaboradores'
_VERBAS_INDENIZATORIAS_REMU_TEMPORARIAS = 'verbas-indenizatorias-e-outras-remuneracoes-temporarias'

#Url base para os metodos GET.
_BASE_URL = 'http://www.transparencia.mpf.mp.br/conteudo/contracheque/'

#Escrita em disco de uma resposta HTTP
def write_file(response, file_name, output_path):

    #Cria o diretório de download (caso nao exista)
    pathlib.Path('./src/' + output_path).mkdir(exist_ok=True) 

    #Transcrição da resposta HTTP para o disco
    try:
        with open("./src/" + file_name,  "wb") as file :
            file.write(response.content)
        file.close()
    except Exception as excep:
        sys.stderr.write('Não foi possivel armazenar em disco o seguinte arquivo: ' + file_name + 'e o seguinte error foi gerado: ' + excep)
        os._exit(1)

#Processo de download Especifico para Verbas Indenizatórias e remunerações Temporarias
def specific_query(year, month, output_path):
    url = _BASE_URL + _VERBAS_INDENIZATORIAS_REMU_TEMPORARIAS
    query_type = ['membros-ativos', 'membros-inativos', 'servidores-ativos', 'servidores-inativos', 'pensionistas', 'colaboradores']
    extension = '.ods'

    #Não trabalha com determinados caracteres
    if(month == 'Março'):
        month = 'Marco'
    
    #Só são validas consultas a partir de Julho de 2019
    valid_months2019 = ['Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

    if(int(year) < 2019):
        raise ValueError('This kind of consult can be only done between now and July 2019')
    if((int(year) == 2019) and (month not in valid_months2019)):
        raise ValueError('This kind of consult can be only done between now and July 2019')
    else:

        file_names = []
        #Download dos dados para cada Tipo
        for kind in query_type:
            final_url = url +'/'+ kind + '/' + year +'/' + _VERBAS_INDENIZATORIAS_REMU_TEMPORARIAS + '_' + year + '_' + month + extension 
    
            try:
                response  = requests.get(final_url,  allow_redirects=True)
                response.raise_for_status()
            except  requests.exceptions.Timeout:
                sys.stderr.write('A requisição para a url { ' + final_url + ' } excedeu o tempo limite.')
                os._exit(1)
            except requests.exceptions.TooManyRedirects:
                sys.stderr.write('A requisição para a url { ' + final_url + ' } não pôde acessar a pagina requisitada por ter sido redicionada muitas vezes.')
                os._exit(1)
            except requests.exceptions.HTTPError as error:
                sys.stderr.write('A requisição para a url { ' + final_url + ' } falhou retornando erro HTTP: ' + error) 
                os.exit(1) 

            file_name = output_path + '/' + _VERBAS_INDENIZATORIAS_REMU_TEMPORARIAS + '_' + year + '_' + month + '_' + kind + extension 

            #Escreve em disco conteudo da resposta HTTP 
            write_file(response, file_name, output_path)
            file_names.append(file_name)
            
    return file_names

#Processo de download Generico dos dados do MPF
def query(year, month, data_type, output_path):

    if(data_type == _VERBAS_INDENIZATORIAS_REMU_TEMPORARIAS):
        return specific_query(year, month, output_path)

    url = _BASE_URL + data_type +'/'
   
    #Não trabalha com determinados caracteres
    if(month == 'Março'):
        month = 'Marco'

    #O formato dos arquivos (extension) muda para .ods a partir de Junho de 2019 
    months = ['Junho', "Julho", "Agosto", "Setembro", "Outubro", "Novembro", 'Dezembro']
    extension = '.xls'
    if(int(year) == 2020):
        extension = '.ods'
    elif((int(year) == 2019) and (month in months)):
        extension = '.ods'

    #Download de dados
    final_url  = url + year + '/'+ data_type + '_' + year + "_" + month + extension

    try:
        response = requests.get(final_url,  allow_redirects=True)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        sys.stderr.write('A requisição para a url { ' + final_url + ' } excedeu o tempo limite.')
        os._exit(1)
    except requests.exceptions.TooManyRedirects:
        sys.stderr.write('A requisição para a url { ' + final_url + ' } não pôde acessar a pagina requisitada por ter sido redicionada muitas vezes.')
        os._exit(1)
    except requests.exceptions.HTTPError as error:
        sys.stderr.write('A requisição para a url { ' + final_url + ' } falhou retornando erro HTTP: ' + error) 
        os.exit(1)
 
    file_name =  output_path + '/' + data_type + '_' + year + "_" + month + extension
    write_file(response, file_name, output_path)
    return file_name

#Implementando o reuso de codigo,  de modo que só muda o data-type que buscamos 
#                       em cada consulta 
def crawl(year, month, output_path):
    file_names = []
    file_names.append(query(year, month, _REMU_MEMBROS_ATIVOS, output_path))
    file_names.append(query(year, month, _PROV_MEMBROS_INATIVOS, output_path))
    file_names.append(query(year, month, _REMU_SERVIDORES_ATIVOS, output_path))
    file_names.append(query(year, month, _PROV_SERVIDORES_INATIVOS, output_path))
    file_names.append(query(year, month, _VALORES_PERCEBIDOS_PENSIONISTAS, output_path))
    file_names.append(query(year, month, _VALORES_PERCEBIDOS_COLABORADORES, output_path))
    try:
        for file in query(year, month, _VERBAS_INDENIZATORIAS_REMU_TEMPORARIAS, output_path):
            file_names.append(file)
    except ValueError:
        print('This kind of consult can be only done between now and July 2019')
    finally:
        return file_names