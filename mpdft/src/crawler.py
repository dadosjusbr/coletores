import requests
import pathlib
import sys
import os

base_url = "https://www.mpdft.mp.br/remuneracao/controle?_act=print&tipo=membrosAtivos&relatorio="

# Generate endpoints able to download
def links_remuneration(month, year):
    links_type = {}
    link = ""
    link = (
        base_url
        + "remuneracao&format=ods&iMes=" + month + "&exercicio=" + year 
    )

    links_type["Membros ativos"] = link
    return links_type

def links_perks(month, year):
    links_type = {}
    link = ""
    link = (
        base_url
        + "indenizacoes&format=ods&iMes=" + month + "&exercicio=" + year 
    )

    links_type["Membros ativos"] = link
    return links_type

def links_temporary_funds(month, year):
    links_type = {}
    link = ""
    link = (
        base_url
        + "verbastemporarias&format=ods&iMes=" + month + "&exercicio=" + year 
    )

    links_type["Membros ativos"] = link
    return links_type

def download(url, file_path):
    try:
        response = requests.get(url, allow_redirects=True)
        with open(file_path, "wb") as file:
            file.write(response.content)
        file.close()
    except Exception as excep:
        sys.stderr.write(
            "Não foi possível fazer o download do arquivo: "
            + file_path
            + ". O seguinte erro foi gerado: "
            + excep
        )
        os._exit(1)

# Crawl retrieves payment files from MPDFT.
def crawl(year, month, output_path):
    urls_remuneration = links_remuneration(month, year)
    urls_perks = links_perks(month, year)
    urls_temporary_funds= links_temporary_funds(month, year)
    files = []

    for element in urls_remuneration:
        pathlib.Path(output_path).mkdir(exist_ok=True)
        file_name = element + "-" + month + "-" + year + ".ods"
        file_path = output_path + "/" + file_name
        download(urls_remuneration[element], file_path)
        files.append(file_path)

    for element in urls_perks:
        pathlib.Path(output_path).mkdir(exist_ok=True)
        file_name_indemnity = (
            element + "-" + "Verbas Indenizatorias" + "-" + month + "-" + year + ".ods"
        )

        file_path_indemnity = output_path + "/" + file_name_indemnity
        download(urls_perks[element], file_path_indemnity)
        files.append(file_path_indemnity)

    for element in urls_temporary_funds:
        pathlib.Path(output_path).mkdir(exist_ok=True)
        file_name_indemnity = (
            element + "-" + "Verbas temporarias" + "-" + month + "-" + year + ".ods")

        file_path_indemnity = output_path + "/" + file_name_indemnity
        download(urls_temporary_funds[element], file_path_indemnity)
        files.append(file_path_indemnity)

    return files