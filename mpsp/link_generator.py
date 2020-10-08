import pandas
import csv
import requests
from pandas_ods_reader import read_ods

def download(mes, ano):
    if ano == '2020':
        MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20memb' + mes + ano + '.ods'
        MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membinat' + mes + ano + '.ods'
        MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servinat' + mes + ano + '.ods'
        MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20serv' + mes + ano + '.ods'
        if mes == '06':
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/BeneficiariosServidoress' + mes + ano + '.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/BeneficiariosMembros' + mes + ano + '.ods'
        elif (mes == '02' or mes == '07'):
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benef%20Servidores%20' + mes + ano + '.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benef%20Membros%20' + mes + ano + '.ods'
        else:
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20Servidores%20' + mes + ano + '.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Beneficiarios%20Membros%20' + mes + ano + '.ods'

    elif ano == 2019:
        if mes in ['03', '04', '05', '06']:
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20Servidores%20do%20Minist%C3%A9rio%20P%C3%BAblico%20' + mes + ano + '.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20Membros%20do%20Minist%C3%A9rio%20P%C3%BAblico%20' + mes + ano + '.ods'
        if mes == '01':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20membros%20ativos%20ref' + mes + '19.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membros%20inativos%20ref12-a.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servidores%20inativos%20ref0119.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20%20servidores%20ativos%20ref0119.ods'
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20Servidores%20ref%200119.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20Membros%20ref%200119.ods'
        if mes == '02':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20membros%20ativos%20ref' + mes + '19.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membros%20inativos%20ref0119-a.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servidores%20inativos%20ref0219.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20%20servidores%20ativos%20ref0219-a.ods'
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20do%20Minist%C3%A9rio%20P%C3%BAblico%20Servidores%20ref%20022019.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20do%20Minist%C3%A9rio%20P%C3%BAblico%20Membros%20ref%20022019.ods'
        if mes == '03':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20membros%20ativos%20ref' + mes + '19.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membros%20inativos%20ref0319.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servidores%20inativos%20ref0319.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20%20servidores%20ativos%20ref0319.ods'
        if mes == '04':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20membros%20ativos%20ref' + mes + '19.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membros%20inativos%20ref0419.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servidores%20inativos%20ref0419.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20servidores%20ativos%20ref0419.ods'
        if mes == '05':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20membros%20ativos%20ref' + mes + '19.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membros%20inativos%20ref0519.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servidores%20inativos%20ref0519.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20servidores%20ativos%20ref0519.ods'
        if mes == '06':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20Membros%20Ativos%20ref0619.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20Membros%20Inativos%20ref0619.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20Servidores%20Inativos%20ref0619.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20Servidores%20Ativos%20ref0619.ods'
        if mes == '07':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Membros%20Ativos%20-%20Tabela%20I%20ref%20072019.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Membros%20Inativos%20-%20Tabela%20I%20ref%20072019.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Servidores%20Inativos%20-%20Tabela%20I%20ref%20072019.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Servidores%20Ativos%20-%20Tabela%20I%20ref%20072019.ods'
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Gestao_Pessoas/Pensionistas_gestao/Pensionistas_2019/Pensionista_JULHO_2019.ods' 
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Gestao_Pessoas/Pensionistas_gestao/Pensionistas_2019/Pensionista_JULHO_2019.ods'
        if mes == '08':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Membros%20Ativos%20-%20Tabela%20I%20ref%20082019.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Membros%20Inativos%20-%20Tabela%20I%20ref%20082019a.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Servidores%20Inativos%20-%20Tabela%20I%20ref082019.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Servidores%20Ativos%20-%20Tabela%20I%20ref082019.ods'
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Gestao_Pessoas/Pensionistas_gestao/Pensionistas_2019/Pensionista_AGOSTO_2019.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Gestao_Pessoas/Pensionistas_gestao/Pensionistas_2019/Pensionista_AGOSTO_2019.ods'
        if mes == '09':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20memb092019.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membinat092019a.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servinat092019.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20III%20serv092019.ods'
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Gestao_Pessoas/Pensionistas_gestao/Pensionistas_2019/Pensionista_SETEMBRO_2019.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Gestao_Pessoas/Pensionistas_gestao/Pensionistas_2019/Pensionista_SETEMBRO_2019.ods'
        if mes == '10':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20memb092019_1.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membinat102019.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servinat092019_1.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20serv092019.ods'
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Beneficiarios102019Servidores.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Beneficiarios102019Membros.xlsx'
        if mes == '11':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20memb112019A.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membinat112019a.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servinat112019.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20serv112019A.ods'
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Beneficiarios%20112019%20Servidores.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Beneficiarios%20112019%20Membros.ods'
        if mes == '12':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20memb122019.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membinat122019a.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servinat122019.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20serv122019.ods'
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benef%20Servidores%20122019.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benef%20Membros%20122019.ods'
    else:
        MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membros%20inativos%20ref' + mes + '.ods'
        MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servidores%20inativos%20ref' + mes + '.ods'
        
        if mes != '12':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20membros%20ativos%20ref' + mes + '.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20%20servidores%20ativos%20ref' + mes + '.ods'
        else:
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20membros%20ativos%20ref122018.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20%20servidores%20ativos%20ref122018.ods'
        
        if mes in ['05', '06', '07']:
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Beneficiarios%20Servidores%20ref' + mes + '%202018.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20Membros%20ref' + mes + '%202018.ods'

        if mes == '01':
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20Servidores%20jan%202018.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20Membros%20jan%202018.ods'
        if mes == '02':
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20Servidores%20fev%202018.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20Membros%20fev%202018.ods'
        if mes == '03':
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Beneficiarios%20Servidores%20mar%202018.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Beneficiarios%20Membros%20mar%202018.ods'
        if mes == '04':
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Beneficiarios%20Servidores%20abr%202018.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Beneficiarios%20Membros%20abr%202018.ods'
        if mes == '08':
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20Servidores%20ago%202018.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20Membros%20ago%202018.ods'
        if mes == '09':
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/BeneficiariosServidoresSet2018.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/BeneficiariosMembrosSet2018.ods'
        if mes == '10':
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20do%20MP%20Servidores%20out%202018.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20do%20MP%20Membros%20out%202018.ods'
        if mes == '11':
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20do%20MP%20Servidores%20nov%202018.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20do%20MP%20Membros%20nov%202018.ods'
        if mes == '12':
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20do%20MP%20Servidores%20dez%202018.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20do%20MP%20Membros%20dez%202018.ods'
    
    r = requests.get(MPSP_URL_MEMB_ATIVOS, allow_redirects=True)
    open('output/membros_ativos' + mes + ano, 'wb').write(r.content)
    r = requests.get(MPSP_URL_MEMB_INATIVOS, allow_redirects=True)
    open('output/membros_inativos' + mes + ano, 'wb').write(r.content)
    r = requests.get(MPSP_URL_SERV_INATIVOS, allow_redirects=True)
    open('output/servidores_inativos' + mes + ano, 'wb').write(r.content)
    r = requests.get(MPSP_URL_SERV_ATIVOS, allow_redirects=True)
    open('output/servidores_ativos' + mes + ano, 'wb').write(r.content)
    r = requests.get(MPSP_URL_PENS_SERVIDORES, allow_redirects=True)
    open('output/pensionistas_servidores' + mes + ano, 'wb').write(r.content)
    r = requests.get(MPSP_URL_PENS_MEMBROS, allow_redirects=True)
    open('output/pensionistas_membros' + mes + ano, 'wb').write(r.content) 


