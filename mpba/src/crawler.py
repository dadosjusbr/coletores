import requests
import pathlib
import sys
import os
import urllib3

base_url = "https://www.mpba.mp.br/sites/default/files/biblioteca/portal-transparencia/contracheque/"
cod_meses = {
    "01": "",
    "02": "_0",
    "03": "_1",
    "04": "_2",
    "05": "_3",
    "06": "_4",
    "07": "_5",
    "08": "_6",
    "09": "_7",
    "10": "_8",
    "11": "_9",
    "12": "_10",
}
# Generate endpoints able to download


def links_remuneration(month, year):
    links_type = {}
    link = ""
    for key in cod_meses:
        if key == str(month):
            link = (
                base_url
                + "remuneracao-de-todos-os-membros-ativos/"
                + year
                + "/quadro_remuneratorio_membros_ativos"
                + cod_meses[key]
                + ".ods"
            )

            links_type["Membros ativos"] = link
    return links_type


def links_perks_temporary_funds(month, year):
    links_type = {}
    link = ""
    for key in cod_meses:
        if key == str(month):
            if key == "01":
                link = (
                    base_url
                    + "verbas-indenizatorias-temporarias/"
                    + year
                    + "/verbas_indenizatorias"
                    + cod_meses[key]
                    + ".ods"
                )
            else:
                link = (
                    base_url
                    + "verbas-indenizatorias-temporarias/"
                    + year
                    + "/verbas_indenizatoria"
                    + cod_meses[key]
                    + ".ods"
                )

            links_type["Membros ativos"] = link
    return links_type


def download(url, file_path):

    try:
        response = requests.get(url, allow_redirects=True, verify=False)
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
    urls_perks = links_perks_temporary_funds(month, year)
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
        print(urls_perks[element])
        download(urls_perks[element], file_path_indemnity)
        files.append(file_path_indemnity)

    return files
