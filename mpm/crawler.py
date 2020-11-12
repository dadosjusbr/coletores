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
  links_type = {}
  link = ""
  for key in beneficiary_types:
    link = baseURL + 'RelatorioRemuneracaoMensal.php?grupo=' + str(key) + '&mes=' + str(month) + '&ano=' + str(year) + '&tipo=xlsx'
    links_type[beneficiary_types[key]] = link
  return links_type

def download(url, file_path):
  response  = requests.get(url, allow_redirects=True) 
  with open(".//" + file_path, "wb") as file:
    file.write(response.content)
  file.close()

# Crawl retrieves payment files from MPM.
def crawl(output_path, year, month):
  urls_type = links(month, year)
  files = []
  
  for element in urls_type:
    pathlib.Path('.//' + output_path).mkdir(exist_ok=True) 
    file_name = element + "-" + month + '-' + year + '.xlsx'
    file_path = output_path + "/" + file_name 
    download(urls_type[element], file_path)
    files.append(file_path)
   
  return files