import requests
import pathlib
import sys
import os
import re

base_URL = 'http://transparencia.mprj.mp.br/contracheque/'
expression = "var myResourceURL = '(.*)';"

func_types =  {1:'MATIV',
            }

fund_types = { 1: 1,
            }

url_complements = {1: 'remuneracao-de-todos-os-membros-ativos',
                   }

url_funds_complements = {1: 'membros-ativos',
                         }

# Adquire o conjunto de links para envio de requisições post.
def content_links():
    content_links = {}
    for key in url_complements:
        content_URL = base_URL + url_complements[key]
        resp = requests.get(content_URL)

        if resp.status_code != 200:
            sys.stderr.write('Http status code return: {} for download of the page{}'.format(resp.status_code, content_URL))
            os._exit(1)

        matches = re.compile(expression).findall(resp.content.decode('utf-8'))
        if len(matches) != 1:
            sys.stderr.write('Line format has changed: Use to be {}'.format(expression))
            os._exit(1)

        content_links[key] = matches[0]

    return content_links

# Adquire o conjunto de links para envio de requisições post.
def others_funds_links():
    other_funds_url = 'verbas-indenizatorias-e-outras-remuneracoes-temporarias-de-'
    other_contents = {}
    for key in url_funds_complements:
        content_URL = base_URL + other_funds_url + url_funds_complements[key]
        resp = requests.get(content_URL)

        if resp.status_code != 200:
            sys.stderr.write('Http status code return: {} for download of the page {}'.format(resp.status_code, content_URL))
            os._exit(1)

        matches = re.compile(expression).findall(resp.content.decode('utf-8'))
        if len(matches) != 1:
            sys.stderr.write('Line format has changed: Use to be {}'.format(expression))
            os._exit(1)

        other_contents[key] = matches[0]

    return other_contents

# Gera a url de acesso ás informações referentes as remunerações do mês e ano de um tipo de funcionário
def generate_remuneration_url(year, month):
    remuneration_links = content_links()
    links = {}
    for key in func_types:
        # Informações de funcionários do tipo COLAB são adquiridas por meio de um get request no endpoint
        if func_types[key] == 'COLAB':
            url =  "http://transparencia.mprj.mp.br//documents/8378943/57833637/{}_{}_colaboradores.ods".format(year, month)
        else:
            url = remuneration_links[key] +'&mes={}&ano={}&tipoFunc={}'.format(month, year, func_types[key])
        links[func_types[key]] = url

    return links

# Gera a url de acesso ás informações referentes á verbas indenizátorias do mes e ano de um tipo de funcionário
def generate_other_funds_url(year, month):
    other_funds_links = others_funds_links()
    other_content_links = {}

    # Não há informações adicionais sobre verbas indenizatórias destinadas á colaboradores
    for key in fund_types:
        url = other_funds_links[key] + '&mes={}&ano={}&tipoFunc={}'.format(month, year, fund_types[key])
        other_content_links[func_types[key]] = url

    return other_content_links

def download(url, file_path, method):
    try:
        if method == 'GET':
            response = requests.get(url)
        else:
            response = requests.post(url)
        with open(file_path, "wb") as file:
            file.write(response.content)

    except Exception as excep:
        sys.stderr.write("Não foi possível fazer o download do arquivo: " + file_path + '. O seguinte erro foi gerado: ' + excep )
        os._exit(1)

def crawl(year, month, output_path):
    urls_remunerations  = generate_remuneration_url(year,month)
    urls_other_funds = generate_other_funds_url(year,month)

    files = []

    pathlib.Path(output_path).mkdir(exist_ok=True)

    # O download de todas as verbas é de interesse apenas do ano de 2020.    
    if year == "2020":
        for key in urls_remunerations:
            if key != 'COLAB':
                method = 'POST'
            else:
                method = 'GET'

            file_name = year +'_' + month + '_' +  key + '.ods'
            file_path = output_path + "/" + file_name

            download(urls_remunerations[key], file_path, method)
            files.append(file_path)

        for key in urls_other_funds:
            file_name = year + '_' + month + '_' + 'Verbas Indenizatórias-' + key + '.ods'
            file_path =  output_path + '/' + file_name
            method = 'POST'

            download(urls_other_funds[key], file_path, method)
            files.append(file_path)
    else:
        key = 'MATIV'
        method = 'POST'
        
        #Download de remunerações simples refentes á membros ativos.
        file_name = year +'_' + month + '_' +  key + '.ods'
        file_path = output_path + "/" + file_name

        download(urls_remunerations[key], file_path, method)
        files.append(file_path)
        
    return files