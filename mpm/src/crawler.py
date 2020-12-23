import requests
import pathlib
import sys
import os
baseURL = 'https://www.mpm.mp.br/sistemas/consultaFolha/php/'

beneficiary_types = {1: 'Membros ativos',
                     2: 'Membros inativos',
                     3: 'Servidores ativos',
                     4: 'Servidores inativos',
                     5: 'Pensionistas',
                     6: 'Colaboradores'}

# Generate endpoints able to download


def links_remuneration(month, year):
    links_type = {}
    link = ""
    for key in beneficiary_types:
        link = baseURL + 'RelatorioRemuneracaoMensal.php?grupo=' + \
            str(key) + '&mes=' + str(month) + \
            '&ano=' + str(year) + '&tipo=xlsx'
        links_type[beneficiary_types[key]] = link
    return links_type


def links_other_funds(month, year):
    links_type = {}
    link = ""
    for key in beneficiary_types:
        link = baseURL + 'RelatorioRemuneracaoMensalVerbasIndenizatorias.php?grupo=' + \
            str(key) + '&mes=' + str(month) + \
            '&ano=' + str(year) + '&tipo=xlsx'
        links_type[beneficiary_types[key]] = link
    return links_type


def download(url, file_path):
    try:
      response = requests.get(url, allow_redirects=True)
      with open(".//" + file_path, "wb") as file:
          file.write(response.content)
      file.close()
    except Exception as excep:
        sys.stderr.write("Não foi possível fazer o download do arquivo: " + file_path + '. O seguinte erro foi gerado: ' + excep )
        os._exit(1)

# Crawl retrieves payment files from MPM.


def crawl(year, month, output_path):
    urls_remuneration = links_remuneration(month, year)
    urls_other_funds = links_other_funds(month, year)
    files = []

    for element in urls_remuneration:
        pathlib.Path(output_path).mkdir(exist_ok=True)
        file_name = element + "-" + month + '-' + year + '.xlsx'
        file_path = output_path + "/" + file_name
        download(urls_remuneration[element], file_path)
        files.append(file_path)

    for element in urls_other_funds:
        pathlib.Path(output_path).mkdir(exist_ok=True)
        file_name_indemnity = element + "-" + \
            "Verbas Indenizatorias" + "-" + month + '-' + year + '.xlsx'
        file_path_indemnity = output_path + "/" + file_name_indemnity
        download(urls_other_funds[element], file_path_indemnity)
        files.append(file_path_indemnity)

    return files
