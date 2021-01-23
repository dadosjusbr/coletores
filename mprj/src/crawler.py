import requests
import pathlib
import sys
import os
import re

baseURL = 'http://transparencia.mprj.mp.br/contracheque/'
func_types =  {1:'MATIV',
               2:'MINAT',
               3:'SATIV',
               4:'SINAT',
               5:'PENSI',
               6:'COLAB' 
}

url_complements = {1: 'remuneracao-de-todos-os-membros-ativos',
                   2: 'proventos-de-todos-os-membros-inativos',
                   3: 'remuneracao-de-todos-os-servidores-ativos',
                   4: 'proventos-de-todos-os-servidores-inativos',
                   5: 'valores-percebidos-por-todos-os-pensionistas',}

def content_links():
    content_links = {}
    expression = "var myResourceURL = '(.*)';"
    for key in url_complements:
        contentURL = baseURL + url_complements[key]
        resp = requests.get(contentURL)

        if(resp.status_code != 200):
            sys.stderr.write('Http status code return: {} for download of the page{}'.format(resp.status_code,contentURL))
            os._exit(1)
        
        matches = re.compile(expression).findall(resp.content.decode('utf-8'))
        if( len(matches) != 1):
            sys.stderr.write('Line format has changed: Use to be {}'.format(expression))
            os._exit(1)

        content_links[key] = matches[0]

    return content_links
        
# COLAB func-type must be downloaded by get request on endpoint
def links_remuneration(year, month):
    remuneration_links = content_links()
    links = {}
    for key in func_types:
        if (func_types[key] == 'COLAB'):
            url =  "http://transparencia.mprj.mp.br//documents/8378943/57833637/{}_{}_colaboradores.ods".format(year,month)
        else:
            url = remuneration_links[key] +'&mes={}&ano={}&tipoFunc={}'.format(month,year,func_types[key])
        links[func_types[key]] = url

    return links

def download(url, file_path, method):
    try:
        if(method == 'GET'):
            response = requests.get(url)
        else:
            response = requests.post(url)
        with open(file_path, "wb") as file:
            file.write(response.content)
        file.close()
    except Exception as excep:
        sys.stderr.write("Não foi possível fazer o download do arquivo: " + file_path + '. O seguinte erro foi gerado: ' + excep )
        os._exit(1)

def crawl(year, month, output_path):
    urls_remunerations  = links_remuneration(year,month)
    files = []
    for key in urls_remunerations:
        if(key != 'COLAB'):
            method = 'POST'
        else:
            method = 'GET'

        pathlib.Path(output_path).mkdir(exist_ok=True)
        file_name = year +'_' + month + '_' +  key
        file_path = output_path + "/" + file_name
        
        download(urls_remunerations[key], file_path, method)
        files.append(file_path)
    
    return files