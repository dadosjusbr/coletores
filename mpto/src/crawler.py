import requests
import pathlib
import sys
import os
import datetime


baseURL = "https://athenas.mpto.mp.br/athenas/FileUploadController/get_public_file/"

def links_remuneration(month, year):

    cod_2018 = {
        '1': "51b99d5dba4ddb8f5e5708d4faac77bb",
        '2': "8052142001c197100ec8dad47aa15383",
        '3': "8efdba698acbfc6b22ed42fb18fb886d",
        '4': "6a0f72498b6eb22c3c498c21944bc2da",
        '5': "957d3a5f61d1d08349038ada19291cf7",
        '6': "faca1dc0a91720b4eb2db18b31b52521",
        '7': "da5e7a67c3bcffb78881b19462c0948f",
        '8': "c124389f556f4f011f027f3ded9ceee8",
        '9': "6f9aed4bb6ea4841dfc5183753eca6fe",
        '10': "53d7e7d96947dd568c6014541b64e178",
        '11': "c1aea083fbe58891b4f4af6804ed3281",
        '12': "38a1c7c5e1f9d41db27d020c936426f0",
        '13': "3bfa07fb5b837e8d0885ce015b0a4152"
    }

    cod_2019 = {
        '1': "5546ad9f97a6b5641a13f08198b58a14",
        '2': "d717665e539a0524f3f4930f173b258a",
        '3': "71c14721178d5f9603e8c8515467baf5",
        '4': "20fcd1a8755124e1f400d5330e6b9cfa",
        '5': "df1a62a53228391791fe06bee9d0fd0c",
        '6': "9b11404b3b253f95db3273213a74f5ff",
        '7': "fbf56380335f5f3aa1c28d88d32bec7f",
        '8': "1cb50f22a73cfc2a8330d109dff4198e",
        '9': "0dac82f5d69cb4d91847143db23c4106",
        '10': "afafa60e16704294c21759ae05ea089e",
        '11': "2d5da9c8cdf3adc4c02b522db6d4448e",
        '12': "78b627087ca6ac295fd12ca5e767d52c",
        '13': "6461cd7f8ddd33f21a5ac200202ddbe2"
    }

    cod_2020 = {
        '1': "d536c9af99c33a1430d92fd8b0fb052f",
        '2': "d16f97738e8ec52d3d9223f07d0fa864",
        '3': "c2145e61d26216665a354ec872445a66",
        '4': "904eab1746cc3d1a7ec11dde6ec992d6",
        '5': "fb744c95b5bc5681ae28b27c7a701cad",
        '6': "448a8f7cf868c436ac118ab1e4131d2c",
        '7': "5ef5128146ade35741101625ce040f0b",
        '8': "5e8a980e47fbc53a473c95dc14658ec4",
        '9': "e3ee94c90f572f986217c515ce3aafd5",
        '10': "da62a7330f6ad2b5e139e2dc7ca18844",
        '11': "02fb63c26b0429f6e755b2da50078318",
        '12': "36af7e0612a45e10ea044f6403925438",
        '13': "9f71c9b57f9853fb2040de9621aab197"
    }

    cod_2021 = {
        '1': "adbe0060735791381382c90715dc54c0",
        '2': "b657eec3e4d1374afd7e493a19082fd0",
        '3': "63e9cad17572986b9ec1c45f741bbf9b",
        '4': "b9850614b6517df33d414842f585e6a0",
        '5': "",
        '6': "",
        '7': "",
        '8': "",
        '9': "",
        '10': "",
        '11': "",
        '12': "",
        '13': ""
    }

    links_type = {}
    link = ""
    if year == "2018":
        for key in cod_2018:
            
            if month.zfill(2) == key.zfill(2):
                link = baseURL + cod_2018[key]
                links_type["Membros ativos"] = link

                if month == 12:
                    link_decimo_terceiro = baseURL + cod_2018[13]
                    links_type["Membros ativos"] = link_decimo_terceiro
         
    elif year == "2019":
        for key in cod_2019:
            if month.zfill(2) == key.zfill(2):
                link = baseURL + cod_2019[key]
                links_type["Membros ativos"] = link

                if month == 12:
                    link_decimo_terceiro = baseURL + cod_2019[13]
                    links_type["Membros ativos"] = link_decimo_terceiro
    
    elif year == "2020":
        for key in cod_2020:
            if month.zfill(2) == key.zfill(2):
                link = baseURL + cod_2020[key]
                links_type["Membros ativos"] = link

                if month == 12:
                    link_decimo_terceiro = baseURL + cod_2020[13]
                    links_type["Membros ativos"] = link_decimo_terceiro
    
    elif year == "2021":
        for key in cod_2021:
            if month.zfill(2) == key.zfill(2):
                link = baseURL + cod_2021[key]
                links_type["Membros ativos"] = link

                if month == 12:
                    link_decimo_terceiro = baseURL + cod_2021[13]
                    links_type["Membros ativos"] = link_decimo_terceiro
        
    return links_type


def links_other_funds(month, year):

    cod_2018 = {
        '1': "06b6cb0905114fc808636ac9a14c1772",
        '2': "4c2dcb383e890f04524fe0cdcff4efd4",
        '3': "374a99ec3622c7a2a96bbac7ecca7597",
        '4': "1f728e707b3ff5e73ecf8f8fced5b4f8",
        '5': "eac50d60652624ca9ab7200214575923",
        '6': "6faddfcefcf040b9dbc8dbff4eb86779",
        '7': "71adad9de61fc857b159681ff23da440",
        '8': "a7452ba38eb4192f2183b65d708f1ac1",
        '9': "f16c2ff9159fb3033168d6abb378d6d0",
        '10': "c4519c2563c3354ca8ff31a31b70931b",
        '11': "cf19b405fc5b0de8aab03c7bfadc5086",
        '12': "503a0203aada012f3871430aae5fd7ae"
    }

    cod_2019 = {
        '1': "200bc51d662a8ab43ac5766edb174624",
        '2': "1079d1c2ed48d774c0fc34931465a509",
        '3': "a85227ec57a0c47d4750ece9e5b4e672",
        '4': "5c184a8009914c560b09bcc6b42ee451",
        '5': "956380814c33f8dd61227edbb68349a6",
        '6': "d44dcda6255f5899e52601eaa1135b87",
        '7': "bdf672f027fa8369522cfc85f9816e6c",
        '8': "367897d0305fc6fcdaa5bd5c50f29110",
        '9': "065541eb10e5e34315b9aa95b6fa833b",
        '10': "83dbcc1d6539a671aa268bea74cd4651",
        '11': "5d03a301149eae3a209aefcdaa88eaea",
        '12': "bbfbc981421c47b67c5f7da722f0905b"
    }

    cod_2020 = {
        '1': "53f9e14e39a172ac6a394362599a3b8c",
        '2': "0309d25a19fcfb554a64ef91f2a70b60",
        '3': "ae74606e3e39bb742f9f1d023b1ed12f",
        '4': "8d5c7930bb291ef8461d961cb74e82e3",
        '5': "e953f2343f100b1496619a20fa348fc8",
        '6': "466dd74d975f04d5a7c59d5ccc8c3f04",
        '7': "fa520e152604ccbffde51a959446b2d9",
        '8': "bc10ef38b7dc74b873b20a2e68c3357a",
        '9': "42920f0bed9542c4992e6eba27e1c330",
        '10': "c0cc66debcde38e31302866576e7b656",
        '11': "9a36879759d174e570b773f73a511688",
        '12': "05eba8cef6332a36c9492bc21e931106"
    }

    cod_2021 = {
        '1': "477f514ff667cbb8d89c3e25e5be8798",
        '2': "f29c7d8bb6f6f23335e20756295ba6f8",
        '3': "60a2c7826121f1b20d182b2ff6aa5514",
        '4': "40e787a2b07afa60153f4c69ee3a7b66",
        '5': "",
        '6': "",
        '7': "",
        '8': "",
        '9': "",
        '10': "",
        '11': "",
        '12': ""
    }

    links_type = {}
    link = ""
    if year == "2018":
        for key in cod_2018:
            
            if month.zfill(2) == key.zfill(2):
                link = baseURL + cod_2018[key]
                links_type["Membros ativos"] = link
         
    elif year == "2019":
        for key in cod_2019:
            if month.zfill(2) == key.zfill(2):
                link = baseURL + cod_2019[key]
                links_type["Membros ativos"] = link
    
    elif year == "2020":
        for key in cod_2020:
            if month.zfill(2) == key.zfill(2):
                link = baseURL + cod_2020[key]
                links_type["Membros ativos"] = link
    
    elif year == "2021":
        for key in cod_2021:
            if month.zfill(2) == key.zfill(2):
                link = baseURL + cod_2021[key]
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
