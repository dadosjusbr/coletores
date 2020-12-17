import pandas
import csv
import requests
from pandas_ods_reader import read_ods
import pathlib

beneficiary_types = {1: 'Membros_ativos',
                     2: 'Membros_inativos',
                     3: 'Servidores_ativos',
                     4: 'Servidores_inativos',
                     5: 'Pensionistas_membros',
                     6: 'Pensionistas_servidores',
                     7: 'Colaboradores'
                    }

baseURL = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/'

# Os links para download das folhas de pagamente variam bastante, devido a isso existe no código vários condicionais
def links_remuneration(month, year):
    links_type = {}
    link = ""
    if(year == '2020'):
        for key in beneficiary_types:
            if(month in ['01', '02', '03', '04', '05', '06', '07']):
                if(beneficiary_types[key] == "Membros_ativos"):
                    link = baseURL + beneficiary_types[key] + '/Tabela%20I%20memb' + month + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(beneficiary_types[key] == "Membros_inativos"):
                    link = baseURL + beneficiary_types[key] + '/Tabela%20I%20membinat' + month + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(beneficiary_types[key] == "Servidores_ativos"):
                    link = baseURL + beneficiary_types[key] + '/Tabela%20I%20serv' + month + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(beneficiary_types[key] == "Servidores_inativos"):
                    link = baseURL +  'servidores_inativos/Tabela%20I%20servinat' + month + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(beneficiary_types[key] == "Pensionistas_membros"):
                    if(month == '01'):
                        link = baseURL + 'Pensionistas/' + beneficiary_types[key] + '/Beneficiarios%20Membros%20' + month + year + '.ods'
                        links_type[beneficiary_types[key]] = link
                    elif(month in ['02', '07']):
                        link = baseURL + 'Pensionistas/' + beneficiary_types[key] + '/Benef%20Membros%20' + month + year + '.ods'
                        links_type[beneficiary_types[key]] = link
                    elif(month in ['03', '04', '05']):
                        link = baseURL + 'Pensionistas/' + beneficiary_types[key] + '/Benefici%C3%A1rios%20Membros%20' + month + year + '.ods'
                        links_type[beneficiary_types[key]] = link
                    elif(month == '06'):
                        link = baseURL + 'Pensionistas/' + beneficiary_types[key] + '/BeneficiariosMembros' + month + year + '.ods'
                        links_type[beneficiary_types[key]] = link
                elif(beneficiary_types[key] == "Pensionistas_servidores"):
                    if(month in ['01', '03', '04', '05']):
                        link = baseURL + 'Pensionistas/' + beneficiary_types[key] + '/Benefici%C3%A1rios%20Servidores%20' + month + year + '.ods'
                        links_type[beneficiary_types[key]] = link
                    elif(month in ['02', '07']):
                        link = baseURL + 'Pensionistas/' + beneficiary_types[key] + '/Benef%20Servidores%20' + month + year + '.ods'
                        links_type[beneficiary_types[key]] = link
                    elif(month == '06'):
                        link = baseURL + 'Pensionistas/' + beneficiary_types[key] + '/BeneficiariosServidoress' + month + year + '.ods'
                        links_type[beneficiary_types[key]] = link
    
            elif(month in ['08', '09']):
                if(beneficiary_types[key] == "Membros_ativos"):
                    link = baseURL + beneficiary_types[key] + '/Tabela%201%20Membros%20Ativos%20ref%20' + month + '-' + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(beneficiary_types[key] == "Membros_inativos"):
                    link = baseURL + beneficiary_types[key] + '/Tabela%201%20Membros%20Inativos%20ref%20' + month + '-' + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(beneficiary_types[key] == "Servidores_ativos"):
                    link = baseURL + beneficiary_types[key] + '/Tabela%201%20Servidores%20Ativos%20ref%20' + month + '-' + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(beneficiary_types[key] == "Servidores_inativos"):
                    link = baseURL + beneficiary_types[key] + '/Tabela%201%20Servidores%20Inativos%20ref%20' + month + '-' + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(beneficiary_types[key] == 'Pensionistas_membros'):
                    link = baseURL + beneficiary_types[key] + '/Beneficiarios%20Membros%20ref%20' + month + '-' + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(beneficiary_types[key] == 'Pensionistas_servidores'):
                    link = baseURL + beneficiary_types[key] + '/Beneficiarios%20Servidores%20ref%20' + month + '-' + year + '.ods'
                    links_type[beneficiary_types[key]] = link

            elif(month == '10'):
                if(beneficiary_types[key] == "Membros_ativos"):
                    link = baseURL + beneficiary_types[key] + '/Membros%20Ativos%20tabela%201%20ref%20' + month + '-' + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(beneficiary_types[key] == "Membros_inativos"):
                    link = baseURL + beneficiary_types[key] + '/Membros%20Inativos%20tabela%201%20ref%20' + month + '-' + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(beneficiary_types[key] == "Servidores_ativos"):
                    link = baseURL + beneficiary_types[key] + '/Servidores%20Ativos%20tabela%201%20ref%20' + month + '-' + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(beneficiary_types[key] == "Servidores_inativos"):
                    link = baseURL + beneficiary_types[key] + '/Servidores%20Inativos%20tabela%201%20ref%20' + month + '-' + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(beneficiary_types[key] == 'Pensionistas_membros'):
                    link = baseURL + beneficiary_types[key] + '/Beneficiarios%20Membros%20ref%20' + month + '-' + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(beneficiary_types[key] == 'Pensionistas_servidores'):
                    link = baseURL + beneficiary_types[key] + '/Beneficiarios%20Servidores%20ref%20' + month + '-' + year + '.ods'
                    links_type[beneficiary_types[key]] = link

    elif(year == '2019'):
        for key in beneficiary_types:
            if(beneficiary_types[key] == 'Membros_ativos'):
                if(month in ['01', '02', '03', '04', '05']):
                    link = baseURL + beneficiary_types[key] + '/Tabela%20I%20membros%20ativos%20ref' + month + '19' + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '06'):
                    link = baseURL + beneficiary_types[key] + '/Tabela%20I%20Membros%20Ativos%20ref' + month + '19' + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month in ['07', '08']):
                    link = baseURL + beneficiary_types[key] + '/Membros%20Ativos%20-%20Tabela%20I%20ref%20' + month + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month in ['09', '12']):
                    link = baseURL + beneficiary_types[key] + '/Tabela%20I%20memb' + month +  year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '10'):
                    link = baseURL + beneficiary_types[key] + '/Tabela%20I%20memb09' +  year + '_1' + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '11'):
                    link = baseURL + beneficiary_types[key] + '/Tabela%20I%20memb' + month + year + 'A' + '.ods'
                    links_type[beneficiary_types[key]] = link
            
            elif(beneficiary_types[key] == 'Membros_inativos'):
                if(month == '01'):
                    link = baseURL + beneficiary_types[key] + '/Tabela%20I%20membros%20inativos%20ref12-a' + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '02'):
                    link = baseURL + beneficiary_types[key] + '/Tabela%20I%20membros%20inativos%20ref0119-a' + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month in ['03', '04', '05']):
                    link = baseURL + beneficiary_types[key] + '/Tabela%20I%20membros%20inativos%20ref' + month + '19.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '06'):
                    link = baseURL + beneficiary_types[key] + '/Tabela%20I%20Membros%20Inativos%20ref' + month + '19.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '07'):
                    link = baseURL + beneficiary_types[key] + '/Membros%20Inativos%20-%20Tabela%20I%20ref%20' + month + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '08'):
                    link = baseURL + beneficiary_types[key] + '/Tabela%20I%20membros%20inativos%20ref' + month + 'A' + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month in ['09', '11', '12']):
                    link = baseURL + beneficiary_types[key] + 'Tabela%20I%20membinat' + month + year + 'a.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '10'):
                    link = baseURL + beneficiary_types[key] + 'Tabela%20I%20membinat' + month + year + '.ods'
                    links_type[beneficiary_types[key]] = link

            elif(beneficiary_types[key] == 'Servidores_ativos'):
                if(month in  ['01', '03', '04', '05', '06']):
                    link = baseURL + beneficiary_types[key] + '/Tabela%20I%20%20servidores%20ativos%20ref' + month + '19.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '02'):
                    link = baseURL + beneficiary_types[key] + '/Tabela%20I%20%20servidores%20ativos%20ref' + month + '19-a.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '07'):
                    link = baseURL + beneficiary_types[key] + '/Servidores%20Ativos%20-%20Tabela%20I%20ref%20' + month + year +'.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '08'):
                    link = baseURL + beneficiary_types[key] + '/Servidores%20Ativos%20-%20Tabela%20I%20ref' + month + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '09'):
                    link = baseURL + beneficiary_types[key] + '/Tabela%20III%20serv' + month + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '10'):
                    link = baseURL + beneficiary_types[key] + '/Tabela%20I%20serv09' + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '11'):
                    link = baseURL + beneficiary_types[key] + '/Tabela%20I%20serv' + month + year + 'A.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '12'):
                    link = baseURL + beneficiary_types[key] + '/Tabela%20I%20serv' + month + year + '.ods'
                    links_type[beneficiary_types[key]] = link

            elif(beneficiary_types[key] == 'Servidores_inativos'):
                if(month in ['01', '02', '03', '04', '05']):
                    link = baseURL + beneficiary_types[key] + '/Tabela%20I%20servidores%20inativos%20ref' + month + '19.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '06'):
                    link = baseURL + beneficiary_types[key] + '/Tabela%20I%20Servidores%20Inativos%20ref' + month + '19.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '07'):
                    link = baseURL + beneficiary_types[key] + '/Servidores%20Inativos%20-%20Tabela%20I%20ref%20' + month + year +'.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '08'):
                    link = baseURL + beneficiary_types[key] + 'Servidores%20Inativos%20-%20Tabela%20I%20ref' + month + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month in ['09', '11', '12']):
                    link = baseURL + beneficiary_types[key] + 'Tabela%20I%20servinat' + month + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '10'):
                    link = baseURL + beneficiary_types[key] + '/Tabela%20I%20servinat09' + year + '_1.ods'
                    links_type[beneficiary_types[key]] = link
            
            elif(beneficiary_types[key] == 'Pensionistas_membros'):
                if(month == '01'):
                    link = baseURL + 'Pensionistas/' + beneficiary_types[key] + '/Benefici%C3%A1rios%20Membros%20ref%20' + month + year +'.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '02'):
                    link = baseURL + 'Pensionistas/' + beneficiary_types[key] + '/Benefici%C3%A1rios%20do%20Minist%C3%A9rio%20P%C3%BAblico%20Membros%20ref%20' + month + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month in ['03', '04', '05', '06']):
                    link = baseURL + 'Pensionistas/' + beneficiary_types[key] + '/Benefici%C3%A1rios%20Membros%20do%20Minist%C3%A9rio%20P%C3%BAblico%20' + month + year +'.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '07'):
                    link = baseURL + 'Pensionistas/' + beneficiary_types[key] + '/Pensionista_JULHO_' + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '08'):
                    link = baseURL + 'Pensionistas/' + beneficiary_types[key] + '/Pensionista_AGOSTO_' + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '09'):
                    link = baseURL + 'Pensionistas/' + beneficiary_types[key] + '/Pensionista_SETEMBRO_' + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '10'):
                    link = baseURL + 'Pensionistas/' + beneficiary_types[key] + '/Beneficiarios'  + month + year + 'Membros.xlsx'
                    links_type[beneficiary_types[key]] = link
                elif(month == '11'):
                    link = baseURL + 'Pensionistas/' + beneficiary_types[key] + '/Beneficiarios%20' + month + year + '%20Membros.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '12'):
                    link = baseURL + 'Pensionistas/' + beneficiary_types[key] + '/Benef%20Membros%20' + month + year + '.ods'
                    links_type[beneficiary_types[key]] = link
            
            elif(beneficiary_types[key] == 'Pensionistas_servidores'):
                if(month == '01'):
                    link = baseURL + 'Pensionistas/' + beneficiary_types[key] + '/Benefici%C3%A1rios%20Servidores%20ref%20' + month + year +'.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '02'):
                    link = baseURL + 'Pensionistas/' + beneficiary_types[key] + '/Benefici%C3%A1rios%20do%20Minist%C3%A9rio%20P%C3%BAblico%20Servidores%20ref%20' + month + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month in ['03', '04', '05', '06']):
                    link = baseURL + 'Pensionistas/' + beneficiary_types[key] + '/Benefici%C3%A1rios%20Servidores%20do%20Minist%C3%A9rio%20P%C3%BAblico%20' + month + year +'.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '07'):
                    link = baseURL + 'Pensionistas/' + beneficiary_types[key] + '/Pensionista_JULHO_' + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '08'):
                    link = baseURL + 'Pensionistas/' + beneficiary_types[key] + '/Pensionista_AGOSTO_' + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '09'):
                    link = baseURL + 'Pensionistas/' + beneficiary_types[key] + '/Pensionista_SETEMBRO_' + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '10'):
                    link = baseURL + 'Pensionistas/' + beneficiary_types[key] + '/Beneficiarios'  + month + year + 'Membros.xlsx'
                    links_type[beneficiary_types[key]] = link
                elif(month == '11'):
                    link = baseURL + 'Pensionistas/' + beneficiary_types[key] + '/Beneficiarios%20' + month + year + '%20Membros.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '12'):
                    link = baseURL + 'Pensionistas/' + beneficiary_types[key] + '/Benef%20Membros%20' + month + year + '.ods'
                    links_type[beneficiary_types[key]] = link

    return links_type
def download(url, file_path):
    response = requests.get(url, allow_redirects=True)
    with open(".//" + file_path, "wb") as file:
        file.write(response.content)
    file.close()
    
def crawl(year, month, output_path):
    urls_remuneration = links_remuneration(month, year)
    files = []
 
    for element in urls_remuneration:
        print(urls_remuneration[element])
        pathlib.Path('./' + output_path).mkdir(exist_ok=True)
        file_name = element + "-" + month + '-' + year + '.ods'
        file_path = output_path + "/" + file_name
        download(urls_remuneration[element], file_path)
        files.append(file_path)

    return files
