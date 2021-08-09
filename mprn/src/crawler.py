import requests
import pathlib
import sys
import os
import datetime

baseURL = "http://transparencia.mprn.mp.br/Arquivos/C0007/"


def links_remuneration(month, year):
    # A formação do link possui um código referente a cada mês
    cod_2018 = {
        '1': "21203",
        '2': "21323",
        '3': "21398",
        '4': "22561",
        '5': "23763",
        '6': "23897",
        '7': "24080",
        '8': "24198",
        '9': "24344",
        '10': "25526",
        '11': "27659",
        '12': "29710",
    }

    cod_2019 = {
        '1': "30860",
        '2': "31960",
        '3': "34312",
        '4': "34491",
        '5': "34618",
        '6': "35780",
        '7': "36832",
        '8': "37994",
        '9': "38166",
        '10': "39353",
        '11': "40516",
        '12': "41799",
    }

    cod_2020 = {
        '1': "41800",
        '2': "41849",
        '3': "41918",
        '4': "42095",
        '5': "42174",
        '6': "42299",
        '7': "43434",
        '8': "43558",
        '9': "43645",
        '10': "44741",
        '11': "45874",
        '12': "47869",
    }
    cod_2021 = {
        '1': "48049",
        '2': "48235",
        '3': "48344",
        '4': "48525",
        '5': "48664",
        '6': "48786",
        '7': "48905",
        '8': "",
        '9': "",
        '10': "",
        '11': "",
        '12': "",
    }
    links_type = {}
    link = ""
    if year == "2018":
        for key in cod_2018:
            
            if month.zfill(2) == key.zfill(2):
                link = baseURL + year + '/R0082/' + cod_2018[key] + '.ods'
                links_type["Membros ativos"] = link
         
    elif year == "2019":
        for key in cod_2019:
            if month.zfill(2) == key.zfill(2):
                link = baseURL + year + '/R0082/' + cod_2019[key] + '.ods'
                links_type["Membros ativos"] = link
    
    elif year == "2020":
        for key in cod_2020:
            if month.zfill(2) == key.zfill(2):
                link = baseURL + year + '/R0082/' + cod_2020[key] + '.ods'
                links_type["Membros ativos"] = link
    
    elif year == "2021":
        for key in cod_2021:
            if month.zfill(2) == key.zfill(2):
                link = baseURL + year + '/R0082/' + cod_2021[key] + '.ods'
                links_type["Membros ativos"] = link
        
    return links_type

  


def links_other_funds(month, year):
    links_type = {}
    link = ""

    cod_2020 = {
        '1': "42383",
        '2': "42382",
        '3': "42381",
        '4': "42380",
        '5': "42379",
        '6': "42370",
        '7': "43440",
        '8': "43578",
        '9': "43674",
        '10': "44776",
        '11': "46826",
        '12': "47898",
    }
    cod_2021 = {
        '1': "48057",
        '2': "48100",
        '3': "48421",
        '4': "48556",
        '5': "48656",
        '6': "48808",
        '7': "",
        '8': "",
        '9': "",
        '10': "",
        '11': "",
        '12': "",
    }
    if year == "2020":
        for key in cod_2020:
            if month.zfill(2) == key.zfill(2):
                link = baseURL + year + '/R2167/' + cod_2020[key] + '.ods'
                links_type["Membros ativos"] = link
    
    elif year == "2021":
        for key in cod_2021:
            if month.zfill(2) == key.zfill(2):
                link = baseURL +  year + '/R2167/' + cod_2021[key] + '.ods'
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


# Crawl retrieves payment files from MPM.


def crawl(year, month, output_path):
    urls_remuneration = links_remuneration(month, year)
    urls_other_funds = links_other_funds(month, year)
    files = []
    

    for element in urls_remuneration:
        pathlib.Path(output_path).mkdir(exist_ok=True)
        file_name = element + "-" + month + "-" + year + ".ods"
        file_path = output_path + "/" + file_name
        download(urls_remuneration[element], file_path)
        files.append(file_path)

    for element in urls_other_funds:
        pathlib.Path(output_path).mkdir(exist_ok=True)
        file_name_indemnity = element + "-" + \
            "Verbas Indenizatorias" + "-" + month + '-' + year + '.ods'
        file_path_indemnity = output_path + "/" + file_name_indemnity
        download(urls_other_funds[element], file_path_indemnity)
        files.append(file_path_indemnity)

    return files
