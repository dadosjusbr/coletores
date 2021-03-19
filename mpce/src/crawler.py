import requests
import sys
import os
import pathlib
from bs4 import BeautifulSoup
from urllib.request import urlopen

base_url = 'http://wapp.mpce.mp.br/PortalTransparenciaConsultas/Visao/extratos.aspx{}'

# Estrututa os dados necessários para o request que recupera informações acerca de remunerações basicas
remu_request_data = {
    'url': base_url.format(''),
    'data':{
        #Variáveis responsáveis por identificar a tabela
        '__VIEWSTATE': '',
        '__VIEWSTATEGENERATOR': '',
        '__EVENTVALIDATION': '',        
        #Variáveis responsáveis por armazenar o mês de ano referente á tabela de coleta.
        'ddlMes': '00',
        'ddlAno': '00',
        #Garante que a busca seja por todos os membros e não apenas um especifico
        'txtNome': '',
        'btnPesquisar': 'Pesquisar'
    }
}

request_formats = {
        'remu': remu_request_data,
        #'vi': vi_request_data 
}

def download(request_data, file_path):
    try:
      response = requests.post(request_data['url'], params= (('opt','1'),), data=request_data['data'], allow_redirects=True)
    except Exception as excep:
        sys.stderr.write("Não foi possível fazer o download do arquivo: " + file_path + ' . A requisição foi enviada para a url: ' + request_data['url'] + ' . E o foi retornado status code:' + response.status_code)
    try:    
      with open(file_path, "wb") as file:
          file.write(response.content)
      file.close()
    except Exception as excep:
        sys.stderr.write("Não foi possível fazer a escrita do arquivo: " + file_path + ' em disco. O seguinte erro foi gerado: ' + excep )
        os._exit(1)

#Este metódo seta os valores necessários para o envio da requisição http
def init_request(year, month):

    #Adquire os valores referentes ás variáveis __VIEWSTATEGENERATOR _VIEWSTATE e _EVENTVALIDATION
    url_key = base_url.format('?opt=1')
    page = urlopen(url_key)
    soup = BeautifulSoup(page, features='lxml')

    view_generator = soup.body.find('input',{'id': '__VIEWSTATEGENERATOR'}).get('value')
    view_state = soup.body.find('input',{'id': '__VIEWSTATE'}).get('value')
    event_validation = soup.body.find('input',{'id': '__EVENTVALIDATION'}).get('value')

    #Setando valores necessários ao envio da requisição http
    for key in request_formats:
        request_formats[key]['data']['ddlMes'] = str(month)
        request_formats[key]['data']['ddlAno'] = str(year)
        request_formats[key]['data']['__VIEWSTATEGENERATOR'] = str(view_generator)
        request_formats[key]['data']['__VIEWSTATE'] = str(view_state)
        request_formats[key]['data']['__EVENTVALIDATION'] = str(event_validation)

def crawl(year, month, output_path):
    files = [] 
    
    init_request(year, month)
    for key in request_formats:
            
        pathlib.Path(output_path).mkdir(exist_ok=True)
        filename = year + '_' + month + '_' + key
        file_path =  output_path + '/' + filename + '.html'
        download(request_formats[key],file_path)
        
        files.append(file_path)
    
    return files

