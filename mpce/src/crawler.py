import requests
import sys
import os
import pathlib
from bs4 import BeautifulSoup
from urllib.request import urlopen

base_url = 'http://wapp.mpce.mp.br/PortalTransparenciaConsultas/Visao/extratos.aspx{}'

url_formats = {
    'remu':'?opt=1',
    'vi':'?opt=9'
    }

url_params = {
    'remu': (('opt','1'),),
    'vi': (('opt', '9'),)
}

#Armazena informações para o envio de requisições referente aos formatos 
class request:

    def __init__(self, url, params):
        self.url = url
        self.params = params

    def make_payload(self, viewstate, viewstate_gen, event_validation, ddlmes, ddlano, txtNome):
        self.payload = {
            #Variáveis responsáveis por identificar a tabela
            '__VIEWSTATE': str(viewstate),
            '__VIEWSTATEGENERATOR': str(viewstate_gen),
            '__EVENTVALIDATION': str(event_validation), 
            #Variáveis responsáveis por armazenar o mês de ano referente á tabela de coleta.
            'ddlMes': str(ddlmes),
            'ddlAno': str(ddlano),
            #Garante que a busca seja por todos os membros e não apenas um especifico
            'txtNome': str(txtNome),
            'btnPesquisar': 'Pesquisar' 
        }

def download(request, file_path):
    try:
      response = requests.post(request.url , params=request.params, data=request.payload, allow_redirects=True)
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
def init_requests(year, month):
    requests = {}

    for key in url_formats:
        #Adquire os valores referentes ás variáveis __VIEWSTATEGENERATOR _VIEWSTATE e _EVENTVALIDATION
        url_key = base_url.format(url_formats[key])
        page = urlopen(url_key)
        soup = BeautifulSoup(page, features='lxml')

        view_generator = soup.body.find('input',{'id': '__VIEWSTATEGENERATOR'}).get('value')
        view_state = soup.body.find('input',{'id': '__VIEWSTATE'}).get('value')
        event_validation = soup.body.find('input',{'id': '__EVENTVALIDATION'}).get('value')

        #Cria objeto referente á requisição
        params  = url_params[key]
        request_obj = request(base_url.format(''), params)
        request_obj.make_payload(view_state, view_generator, event_validation, month, year, '')

        requests[key] = request_obj

    return requests

def crawl(year, month, output_path):
    files = []

    # Realizando download da folha de remunerações simples 
    requests = init_requests(year, month)
    for key in requests:        
        pathlib.Path(output_path).mkdir(exist_ok=True)
        filename = year + '_' + month + '_' + key
        file_path =  output_path + '/' + filename + '.html'
        download(requests[key], file_path)

        files.append(file_path)

    return files