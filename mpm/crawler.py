import requests
import pathlib 
from pathlib import Path 

baseURL = 'https://www.mpm.mp.br/sistemas/consultaFolha/php/'

beneficiary_types = {1: 'Membros ativos',
                     2: 'Membros inativos',
                     3: 'Servidores ativos',
                     4: 'Servidores inativos',
                     5: 'Pensionistas',
                     6: 'Colaboradores'}

# Generate endpoints able to download
def links(month, year):
  file_names = []
  for key in beneficiary_types:
    file_names.append(baseURL + 'RelatorioRemuneracaoMensal.php?grupo=' + str(key) + '&mes=' + str(month) + '&ano=' + str(year) + '&tipo=xlsx')
  return file_names


def download(url, file_path):
  response  = requests.get(url, allow_redirects=True) 
  with open(".//" + file_path, "wb") as file:
    file.write(response.content)
  file.close()

# Crawl retrieves payment files from MPM.
def crawler(output_path, year, month):
  urls = links(month, year)
  files = []
  cont = 1
  
  for url in urls:
    pathlib.Path('.//' + output_path).mkdir(exist_ok=True) 
    file_name = beneficiary_types[cont] + "-" + month + '-' + year + '.xlsx'
    cont +=1
    file_path = output_path + "/" + file_name 
    download(url, file_path)
    files.append(file_path)
   
  return files