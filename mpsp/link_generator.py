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
            if(month == '01' | month == '02' | month == '03' | month == '04' | month == '05' | month == '06'| month == '07'):
                if(beneficiary_types[key] == "Membros_ativos"):
                    link = baseURL + beneficiary_types[key] + '/Tabela%20I%20memb' + month + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(beneficiary_types[key] == "Membros_inativos"):
                    link = baseURL + beneficiary_types[key] + '/Tabela%20I%20membinat' + month + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(beneficiary_types[key] == "Servidores_ativos"):
                    link = baseURL + beneficiary_types[key] + '/Tabela%20I%20serv012020' + month + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(beneficiary_types[key] == "Servidores_inativos"):
                    link = baseURL + beneficiary_types[key] + '/Tabela%20I%20servinat' + month + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(beneficiary_types[key] == "Pensionistas_membros"):
                    if(month == '01'):
                        link = baseURL + 'Pensionistas' + beneficiary_types[key] + '/Beneficiarios%20Membros%20' + month + year + '.ods'
                        links_type[beneficiary_types[key]] = link
                    elif(month == '02' | month == '07'):
                        link = baseURL + 'Pensionistas' + beneficiary_types[key] + '/Benef%20Membros%20' + month + year + '.ods'
                        links_type[beneficiary_types[key]] = link
                    elif(month == '03' | month == '04' | month == '05'):
                        link = baseURL + 'Pensionistas' + beneficiary_types[key] + '/Benefici%C3%A1rios%20Membros%20' + month + year + '.ods'
                        links_type[beneficiary_types[key]] = link
                    elif(month == '06'):
                        link = baseURL + 'Pensionistas' + beneficiary_types[key] + '/BeneficiariosMembros' + month + year + '.ods'
                        links_type[beneficiary_types[key]] = link
                elif(beneficiary_types[key] == "Pensionistas_servidores"):
                    if(month == '01' | month == '03' | month == '04' | month == '05'):
                        link = baseURL + 'Pensionistas' + beneficiary_types[key] + '/Benefici%C3%A1rios%20Servidores%20' + month + year + '.ods'
                        links_type[beneficiary_types[key]] = link
                    elif(month == '02' | month == '07'):
                        link = baseURL + 'Pensionistas' + beneficiary_types[key] + '/Benef%20Servidores%20' + month + year + '.ods'
                        links_type[beneficiary_types[key]] = link
                    elif(month == '06'):
                        link = baseURL + 'Pensionistas' + beneficiary_types[key] + '/BeneficiariosServidoress' + month + year + '.ods'
                        links_type[beneficiary_types[key]] = link
    
            elif(month =='08' | month =='09'):
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
                if(month == '01' | month == '02' | month == '03' | month == '04' | month == '05'):
                    link = baseURL + beneficiary_types[key] + '/Tabela%20I%20membros%20ativos%20ref' + month + '19' + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '06'):
                    link = baseURL + beneficiary_types[key] + '/Tabela%20I%20Membros%20Ativos%20ref' + month + '19' + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '07' | month == '08'):
                    link = baseURL + beneficiary_types[key] + '/Membros%20Ativos%20-%20Tabela%20I%20ref%20' + month + year + '.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '09' | month == '12'):
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
                elif(month == '03' | month == '04' | month == '05'):
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
                elif(month == '09' | month == '11' | month == '12'):
                    link = baseURL + beneficiary_types[key] + 'Tabela%20I%20membinat' + month + year + 'a.ods'
                    links_type[beneficiary_types[key]] = link
                elif(month == '10'):
                    link = baseURL + beneficiary_types[key] + 'Tabela%20I%20membinat' + month + year + '.ods'
                    links_type[beneficiary_types[key]] = link

            elif(beneficiary_types[key] == 'Servidores_ativos'):
                if(month == '01' | month == '03' | month == '04' | month == '05' | month == '06'):
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
                if(month == '01' | month == '02' | month == '03' | month == '04' | month == '05'):
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
                elif(month == '09' | month == '11' | month == '12'):
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
                elif(month == '03' | month == '04' | month == '05'| month == '06'):
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
                elif(month == '03' | month == '04' | month == '05'| month == '06'):
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
links_remuneration(8,2020)

#def download(mes, ano, caminho):
    # if ano == '2020':
    #     MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20memb' + mes + ano + '.ods'
    #     MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membinat' + mes + ano + '.ods'
    #     MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servinat' + mes + ano + '.ods'
    #     MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20serv' + mes + ano + '.ods'
    #     if mes == '06':
    #         MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/BeneficiariosServidoress' + mes + ano + '.ods'
    #         MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/BeneficiariosMembros' + mes + ano + '.ods'
    #     elif (mes == '02' or mes == '07'):
    #         MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benef%20Servidores%20' + mes + ano + '.ods'
    #         MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benef%20Membros%20' + mes + ano + '.ods'
    #     else:
    #         MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20Servidores%20' + mes + ano + '.ods'
    #         MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Beneficiarios%20Membros%20' + mes + ano + '.ods'

    # elif ano == 2019:
    #     if mes in ['03', '04', '05', '06']:
    #         MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20Servidores%20do%20Minist%C3%A9rio%20P%C3%BAblico%20' + mes + ano + '.ods'
    #         MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20Membros%20do%20Minist%C3%A9rio%20P%C3%BAblico%20' + mes + ano + '.ods'
    #     if mes == '01':
    #         MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20membros%20ativos%20ref' + mes + '19.ods'
    #         MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membros%20inativos%20ref12-a.ods'
    #         MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servidores%20inativos%20ref0119.ods'
    #         MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20%20servidores%20ativos%20ref0119.ods'
    #         MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20Servidores%20ref%200119.ods'
    #         MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20Membros%20ref%200119.ods'
    #     if mes == '02':
    #         MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20membros%20ativos%20ref' + mes + '19.ods'
    #         MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membros%20inativos%20ref0119-a.ods'
    #         MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servidores%20inativos%20ref0219.ods'
    #         MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20%20servidores%20ativos%20ref0219-a.ods'
    #         MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20do%20Minist%C3%A9rio%20P%C3%BAblico%20Servidores%20ref%20022019.ods'
    #         MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20do%20Minist%C3%A9rio%20P%C3%BAblico%20Membros%20ref%20022019.ods'
    #     if mes == '03':
    #         MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20membros%20ativos%20ref' + mes + '19.ods'
    #         MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membros%20inativos%20ref0319.ods'
    #         MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servidores%20inativos%20ref0319.ods'
    #         MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20%20servidores%20ativos%20ref0319.ods'
    #     if mes == '04':
    #         MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20membros%20ativos%20ref' + mes + '19.ods'
    #         MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membros%20inativos%20ref0419.ods'
    #         MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servidores%20inativos%20ref0419.ods'
    #         MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20servidores%20ativos%20ref0419.ods'
    #     if mes == '05':
    #         MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20membros%20ativos%20ref' + mes + '19.ods'
    #         MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membros%20inativos%20ref0519.ods'
    #         MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servidores%20inativos%20ref0519.ods'
    #         MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20servidores%20ativos%20ref0519.ods'
    #     if mes == '06':
    #         MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20Membros%20Ativos%20ref0619.ods'
    #         MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20Membros%20Inativos%20ref0619.ods'
    #         MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20Servidores%20Inativos%20ref0619.ods'
    #         MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20Servidores%20Ativos%20ref0619.ods'
    #     if mes == '07':
    #         MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Membros%20Ativos%20-%20Tabela%20I%20ref%20072019.ods'
    #         MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Membros%20Inativos%20-%20Tabela%20I%20ref%20072019.ods'
    #         MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Servidores%20Inativos%20-%20Tabela%20I%20ref%20072019.ods'
    #         MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Servidores%20Ativos%20-%20Tabela%20I%20ref%20072019.ods'
    #         MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Gestao_Pessoas/Pensionistas_gestao/Pensionistas_2019/Pensionista_JULHO_2019.ods' 
    #         MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Gestao_Pessoas/Pensionistas_gestao/Pensionistas_2019/Pensionista_JULHO_2019.ods'
    #     if mes == '08':
    #         MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Membros%20Ativos%20-%20Tabela%20I%20ref%20082019.ods'
    #         MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Membros%20Inativos%20-%20Tabela%20I%20ref%20082019a.ods'
    #         MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Servidores%20Inativos%20-%20Tabela%20I%20ref082019.ods'
    #         MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Servidores%20Ativos%20-%20Tabela%20I%20ref082019.ods'
    #         MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Gestao_Pessoas/Pensionistas_gestao/Pensionistas_2019/Pensionista_AGOSTO_2019.ods'
    #         MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Gestao_Pessoas/Pensionistas_gestao/Pensionistas_2019/Pensionista_AGOSTO_2019.ods'
    #     if mes == '09':
    #         MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20memb092019.ods'
    #         MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membinat092019a.ods'
    #         MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servinat092019.ods'
    #         MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20III%20serv092019.ods'
    #         MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Gestao_Pessoas/Pensionistas_gestao/Pensionistas_2019/Pensionista_SETEMBRO_2019.ods'
    #         MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Gestao_Pessoas/Pensionistas_gestao/Pensionistas_2019/Pensionista_SETEMBRO_2019.ods'
    #     if mes == '10':
    #         MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20memb092019_1.ods'
    #         MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membinat102019.ods'
    #         MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servinat092019_1.ods'
    #         MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20serv092019.ods'
    #         MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Beneficiarios102019Servidores.ods'
    #         MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Beneficiarios102019Membros.xlsx'
    #     if mes == '11':
    #         MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20memb112019A.ods'
    #         MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membinat112019a.ods'
    #         MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servinat112019.ods'
    #         MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20serv112019A.ods'
    #         MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Beneficiarios%20112019%20Servidores.ods'
    #         MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Beneficiarios%20112019%20Membros.ods'
    #     if mes == '12':
    #         MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20memb122019.ods'
    #         MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membinat122019a.ods'
    #         MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servinat122019.ods'
    #         MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20serv122019.ods'
    #         MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benef%20Servidores%20122019.ods'
    #         MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benef%20Membros%20122019.ods'
    # else:
    #     MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membros%20inativos%20ref' + mes + '.ods'
    #     MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servidores%20inativos%20ref' + mes + '.ods'
        
    #     if mes != '12':
    #         MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20membros%20ativos%20ref' + mes + '.ods'
    #         MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20%20servidores%20ativos%20ref' + mes + '.ods'
    #     else:
    #         MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20membros%20ativos%20ref122018.ods'
    #         MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20%20servidores%20ativos%20ref122018.ods'
        
    #     if mes in ['05', '06', '07']:
    #         MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Beneficiarios%20Servidores%20ref' + mes + '%202018.ods'
    #         MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20Membros%20ref' + mes + '%202018.ods'

    #     if mes == '01':
    #         MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20Servidores%20jan%202018.ods'
    #         MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20Membros%20jan%202018.ods'
    #     if mes == '02':
    #         MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20Servidores%20fev%202018.ods'
    #         MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20Membros%20fev%202018.ods'
    #     if mes == '03':
    #         MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Beneficiarios%20Servidores%20mar%202018.ods'
    #         MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Beneficiarios%20Membros%20mar%202018.ods'
    #     if mes == '04':
    #         MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Beneficiarios%20Servidores%20abr%202018.ods'
    #         MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Beneficiarios%20Membros%20abr%202018.ods'
    #     if mes == '08':
    #         MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20Servidores%20ago%202018.ods'
    #         MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20Membros%20ago%202018.ods'
    #     if mes == '09':
    #         MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/BeneficiariosServidoresSet2018.ods'
    #         MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/BeneficiariosMembrosSet2018.ods'
    #     if mes == '10':
    #         MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20do%20MP%20Servidores%20out%202018.ods'
    #         MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20do%20MP%20Membros%20out%202018.ods'
    #     if mes == '11':
    #         MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20do%20MP%20Servidores%20nov%202018.ods'
    #         MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20do%20MP%20Membros%20nov%202018.ods'
    #     if mes == '12':
    #         MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20do%20MP%20Servidores%20dez%202018.ods'
    #         MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20do%20MP%20Membros%20dez%202018.ods'
    
    # pathlib.Path('./' + caminho).mkdir(exist_ok=True)
    # print(MPSP_URL_MEMB_ATIVOS)
    # r = requests.get(MPSP_URL_MEMB_ATIVOS, allow_redirects=True)
    # open(caminho + 'membros_ativos' + mes + ano, 'wb').write(r.content)
    # r = requests.get(MPSP_URL_MEMB_INATIVOS, allow_redirects=True)
    # open(caminho + 'membros_inativos' + mes + ano, 'wb').write(r.content)
    # r = requests.get(MPSP_URL_SERV_INATIVOS, allow_redirects=True)
    # open(caminho + 'servidores_inativos' + mes + ano, 'wb').write(r.content)
    # r = requests.get(MPSP_URL_SERV_ATIVOS, allow_redirects=True)
    # open(caminho + 'servidores_ativos' + mes + ano, 'wb').write(r.content)
    # r = requests.get(MPSP_URL_PENS_SERVIDORES, allow_redirects=True)
    # open(caminho + 'pensionistas_servidores' + mes + ano, 'wb').write(r.content)
    # r = requests.get(MPSP_URL_PENS_MEMBROS, allow_redirects=True)
    # open(caminho + 'pensionistas_membros' + mes + ano, 'wb').write(r.content) 