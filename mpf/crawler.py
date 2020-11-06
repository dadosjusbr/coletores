import requests
from pyexcel_ods import get_data #pip install pyexcel-ods
from pyexcel_xls import get_data #pip install pyexcel-xls
import pathlib #pip install pathlib


#Processo de download dos dados do MPF
def consulta(year,month,data_type,output_path):
    base_url = 'http://www.transparencia.mpf.mp.br/conteudo/contracheque/'+ data_type +'/'
   
    #Não trabalha com determinados caracteres
    if(month == 'Março'):
        month = 'Marco'

    #O formato dos arquivos (extension) muda para .ods a partir de Junho de 2019 
    extension = '.xls'
    if(int(year) == 2020):
        extension = '.ods'
    elif((int(year) == 2019) and ( (month == 'Junho') or (month == "Julho") or (month == "Agosto") or (month == "Setembro") or (month == "Outubro") or (month == "Novembro") or (month == 'Dezembro'))):
        extension = '.ods'

    #Download de dados
    final_url  = base_url + year + '/'+ data_type + '_' + year + "_" + month + extension
    response  = requests.get(final_url, allow_redirects=True)

    #Cria o diretório de download (caso nao exista)
    pathlib.Path('.//' + output_path).mkdir(exist_ok=True) 

    #Transcrição da resposta HTTP para o disco
    file_name =  data_type + '_' + year + "_" + month + extension
    open(".//" + output_path + "//" + file_name, "wb").write(response.content)
    return file_name


#Implementando o reuso de codigo, de modo que só muda o data-type que buscamos 
#                       em cada consulta 
def get_relevant_data(year,month,output_path):
    file_names = []
    file_names.append(consulta(year,month,'remuneracao-membros-ativos',output_path))
    file_names.append(consulta(year,month,'remuneracao-servidores-ativos',output_path))
    file_names.append(consulta(year,month,'provento-servidores-inativos',output_path))
    file_names.append(consulta(year,month,'provento-membros-inativos',output_path))
    file_names.append(consulta(year,month,'valores-percebidos-pensionistas',output_path))
    return file_names

    