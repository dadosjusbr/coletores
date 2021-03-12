import requests
import sys
import os
import pathlib

url_formats = { "remu": "https://www.mpgo.mp.br/transparencia/contracheque/detalhamento_folha? \
                utf8=%E2%9C%93&contracheque_tb_detalhamento_folha%5Btipo%5D=r_membro_ativo\
                &contracheque_tb_detalhamento_folha%5Bano%5D={}&contracheque_tb_detalhamento_folha\
                %5Bmes%5D={}&contracheque_tb_detalhamento_folha%5Bcdg_ordem%5D=&contracheque_tb_detalhamento_\
                folha%5Bnm_pessoa%5D=&commit=CSV",
                "vi": "https://www.mpgo.mp.br/transparencia/contracheque/tb_verbas_indeniz_remun?utf8=%E2%9C%93\
                &contracheque_tb_verbas_indeniz_remun%5Bano%5D={}&contracheque_tb_verbas_indeniz_remun%5Bmes%5D={}\
                &contracheque_tb_verbas_indeniz_remun%5Bnm_pessoa%5D=&commit=CSV"
 }

def download(url, file_path):
    try:
      response = requests.get(url, allow_redirects=True)
    except Exception as excep:
        sys.stderr.write("Não foi possível fazer o download do arquivo: " + file_path + ' . A requisição foi enviada para a url: ' + url + ' . E o foi retornado status code:' + response.status_code)
    try:    
      with open(file_path, "wb") as file:
          file.write(response.content)
      file.close()
    except Exception as excep:
        sys.stderr.write("Não foi possível fazer a escrita do arquivo: " + file_path + ' em disco. O seguinte erro foi gerado: ' + excep )
        os._exit(1)

def crawl(year, month, output_path):
    files = [] 
    
    for key in url_formats:
        pathlib.Path(output_path).mkdir(exist_ok=True)
        filename = year + '_' + month +'_' + key 
        file_path = output_path + '/' + filename + '.csv'
        url = url_formats[key].format(year, month)
        download(url, file_path)
        
        files.append(file_path)
    
    return files


