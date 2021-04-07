import requests
import pathlib
import os
import sys


# Url base para os metodos GET.
base_url = "http://www.transparencia.mpf.mp.br/conteudo/contracheque/"


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


# Processo de download Especifico para Verbas Indenizatórias e remunerações Temporarias


def links_other_funds(month, year):
    links_type = {}
    link = ""
    
    if month == "Março":
        month = "Marco"
    
    if (
        month in ["Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        and year == "2019"
        or int(year) >= 2020
    ):
        link = (
            base_url
            + "verbas-indenizatorias-e-outras-remuneracoes-temporarias/membros-ativos/"
            + year
            + "/verbas-indenizatorias-e-outras-remuneracoes-temporarias_"
            + year
            + "_"
            + month
            + ".ods"
        )

        links_type["Membros ativos"] = link
    return links_type


# Processo de download Generico dos dados do MPF
def links_remuneration(month, year):
    links_type = {}
    link = ""

    # Não trabalha com determinados caracteres
    if month == "Março":
        month = "Marco"

    if (
        year == "2018"
        or (month in ["Janeiro", "Fevereiro", "Marco", "Abril", "Maio"])
        and year == "2019"
    ):
        link = (
            base_url
            + "remuneracao-membros-ativos/"
            + year
            + "/remuneracao-membros-ativos_"
            + year
            + "_"
            + month
            + ".xls"
        )
    else:
        link = (
            base_url
            + "remuneracao-membros-ativos/"
            + year
            + "/remuneracao-membros-ativos_"
            + year
            + "_"
            + month
            + ".ods"
        )

    links_type["Membros ativos"] = link
    return links_type


# Implementando o reuso de codigo,  de modo que só muda o data-type que buscamos
#                       em cada consulta
def crawl(year, month, output_path):

    urls_remuneration = links_remuneration(month, year)
    urls_other_funds = links_other_funds(month, year)
    files = []

    for element in urls_remuneration:
        pathlib.Path(output_path).mkdir(exist_ok=True)
        if year == "2018" or (
            month in ["Janeiro", "Fevereiro", "Marco", "Abril", "Maio"]
            and year == "2019"
        ):
            file_name = element + "-" + month + "-" + year + ".xls"
        else:
            file_name = element + "-" + month + "-" + year + ".ods"
        file_path = output_path + "/" + file_name
        download(urls_remuneration[element], file_path)
        files.append(file_path)

    for element in urls_other_funds:
        pathlib.Path(output_path).mkdir(exist_ok=True)
        file_name_indemnity = (
            element + "-" + "Verbas Indenizatorias" + "-" + month + "-" + year + ".ods"
        )
        file_path_indemnity = output_path + "/" + file_name_indemnity
        download(urls_other_funds[element], file_path_indemnity)
        files.append(file_path_indemnity)

    return files
