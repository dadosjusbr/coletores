import requests
import pathlib 

_REMU_MEMBROS_ATIVOS ='remuneracao-membros-ativos'
_REMU_SERVIDORES_ATIVOS ='remuneracao-servidores-ativos'
_PROV_SERVIDORES_INATIVOS = 'provento-servidores-inativos'
_PROV_MEMBROS_INATIVOS ='provento-membros-inativos'
_VALORES_PERCEBIDOS_PENSIONISTAS ='valores-percebidos-pensionistas'

#Processo de download dos dados do MPF
def query(year,month,data_type,output_path):
    base_url = 'http://www.transparencia.mpf.mp.br/conteudo/contracheque/'+ data_type +'/'
   
    #Não trabalha com determinados caracteres
    if(month == 'Março'):
        month = 'Marco'

    #O formato dos arquivos (extension) muda para .ods a partir de Junho de 2019 
    months = ['Junho',"Julho","Agosto","Setembro","Outubro","Novembro",'Dezembro']
    extension = '.xls'
    if(int(year) == 2020):
        extension = '.ods'
    elif((int(year) == 2019) and (month in months)):
        extension = '.ods'

    #Download de dados
    final_url  = base_url + year + '/'+ data_type + '_' + year + "_" + month + extension
    response  = requests.get(final_url, allow_redirects=True)

    #Cria o diretório de download (caso nao exista)
    pathlib.Path('.//' + output_path).mkdir(exist_ok=True) 

    #Transcrição da resposta HTTP para o disco
    file_name =  data_type + '_' + year + "_" + month + extension
    with open(".//" + output_path + "//" + file_name, "wb") as file :
        file.write(response.content)
    
    file.close()

    return file_name

#Implementando o reuso de codigo, de modo que só muda o data-type que buscamos 
#                       em cada consulta 
def get_relevant_data(year,month,output_path):
    file_names = []
    file_names.append(query(year,month,_REMU_MEMBROS_ATIVOS,output_path))
    file_names.append(query(year,month,_REMU_SERVIDORES_ATIVOS,output_path))
    file_names.append(query(year,month,_PROV_SERVIDORES_INATIVOS,output_path))
    file_names.append(query(year,month,_PROV_MEMBROS_INATIVOS,output_path))
    file_names.append(query(year,month,_VALORES_PERCEBIDOS_PENSIONISTAS,output_path))

    return file_names