import pandas
import csv
import requests
from pandas_ods_reader import read_ods

def download(mes, ano):
    if ano == '2020':
        if mes == '01':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20memb012020.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membinat012020.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servinat012020.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20serv012020.ods'
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20Servidores%20012020.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Beneficiarios%20Membros%20012020.ods'
        if mes == '02':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20memb022020.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membinat022020.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servinat022020.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20serv022020.ods'
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benef%20Servidores%20022020.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benef%20Membros%20022020.ods'
        if mes == '03':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20memb032020.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membinat032020.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servinat032020.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20serv032020.ods'
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20Servidores%20032020.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20Membros%20032020.ods'
        if mes == '04':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20memb042020.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membinat042020.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servinat042020.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20serv042020.ods'
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20Servidores%20042020.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20Membros%20042020.ods'
        if mes == '05':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20memb052020.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membinat052020.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servinat052020.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20serv052020.ods'
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20Servidores%20052020.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20Membros%20052020.ods'
        if mes == '06':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20memb062020.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membinat062020.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servinat062020.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20serv062020.ods'
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/BeneficiariosServidoress062020.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/BeneficiariosMembros062020.ods'
        if mes == '07':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20memb072020.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membinat072020.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servinat072020.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20serv072020.ods'
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benef%20Servidores%20072020.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benef%20Membros%20072020.ods'
        if mes == '08':
            MPSP_URL_MEMB_ATIVOS = ''
            MPSP_URL_MEMB_INATIVOS = ''
            MPSP_URL_SERV_INATIVOS = ''
            MPSP_URL_SERV_ATIVOS = ''
            MPSP_URL_PENS_SERVIDORES = ''
            MPSP_URL_PENS_MEMBROS = ''
        if mes == '09':
            MPSP_URL_MEMB_ATIVOS = ''
            MPSP_URL_MEMB_INATIVOS = ''
            MPSP_URL_SERV_INATIVOS = ''
            MPSP_URL_SERV_ATIVOS = ''
            MPSP_URL_PENS_SERVIDORES = ''
            MPSP_URL_PENS_MEMBROS = ''
        if mes == '10':
            MPSP_URL_MEMB_ATIVOS = ''
            MPSP_URL_MEMB_INATIVOS = ''
            MPSP_URL_SERV_INATIVOS = ''
            MPSP_URL_SERV_ATIVOS = ''
            MPSP_URL_PENS_SERVIDORES = ''
            MPSP_URL_PENS_MEMBROS = ''
        if mes == '11':
            MPSP_URL_MEMB_ATIVOS = ''
            MPSP_URL_MEMB_INATIVOS = ''
            MPSP_URL_SERV_INATIVOS = ''
            MPSP_URL_SERV_ATIVOS = ''
            MPSP_URL_PENS_SERVIDORES = ''
            MPSP_URL_PENS_MEMBROS = ''
        if mes == '12':
            MPSP_URL_MEMB_ATIVOS = ''
            MPSP_URL_MEMB_INATIVOS = ''
            MPSP_URL_SERV_INATIVOS = ''
            MPSP_URL_SERV_ATIVOS = ''
            MPSP_URL_PENS_SERVIDORES = ''
            MPSP_URL_PENS_MEMBROS = ''
    elif ano == 2019:
        if mes == '01':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20membros%20ativos%20ref0119.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membros%20inativos%20ref12-a.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servidores%20inativos%20ref0119.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20%20servidores%20ativos%20ref0119.ods'
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20Servidores%20ref%200119.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20Membros%20ref%200119.ods'
        if mes == '02':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20membros%20ativos%20ref0219.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membros%20inativos%20ref0119-a.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servidores%20inativos%20ref0219.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20%20servidores%20ativos%20ref0219-a.ods'
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20do%20Minist%C3%A9rio%20P%C3%BAblico%20Servidores%20ref%20022019.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20do%20Minist%C3%A9rio%20P%C3%BAblico%20Membros%20ref%20022019.ods'
        if mes == '03':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20membros%20ativos%20ref0319.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membros%20inativos%20ref0319.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servidores%20inativos%20ref0319.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20%20servidores%20ativos%20ref0319.ods'
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20Servidores%20do%20Minist%C3%A9rio%20P%C3%BAblico%20032019.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20Membros%20do%20Minist%C3%A9rio%20P%C3%BAblico%20032019.ods'
        if mes == '04':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20membros%20ativos%20ref0419.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membros%20inativos%20ref0419.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servidores%20inativos%20ref0419.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20servidores%20ativos%20ref0419.ods'
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20Servidores%20do%20Minist%C3%A9rio%20P%C3%BAblico%20042019.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20Membros%20do%20Minist%C3%A9rio%20P%C3%BAblico%20042019.ods'
        if mes == '05':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20membros%20ativos%20ref0519.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membros%20inativos%20ref0519.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servidores%20inativos%20ref0519.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20servidores%20ativos%20ref0519.ods'
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20Servidores%20do%20Minist%C3%A9rio%20P%C3%BAblico%20052019.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20Membros%20do%20Minist%C3%A9rio%20P%C3%BAblico%20052019.ods'
        if mes == '06':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20Membros%20Ativos%20ref0619.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20Membros%20Inativos%20ref0619.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20Servidores%20Inativos%20ref0619.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20Servidores%20Ativos%20ref0619.ods'
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20Servidores%20do%20Minist%C3%A9rio%20P%C3%BAblico%20062019.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20Membros%20do%20Minist%C3%A9rio%20P%C3%BAblico%20062019.ods'
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
        if mes == '01':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20membros%20ativos%20ref01.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membros%20inativos%20ref01.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servidores%20inativos%20ref01.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20%20servidores%20ativos%20ref01.ods'
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20Servidores%20jan%202018.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20Membros%20jan%202018.ods'
        if mes == '02':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20membros%20ativos%20ref02.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membros%20inativos%20ref02.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servidores%20inativos%20ref02.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20%20servidores%20ativos%20ref02.ods'
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20Servidores%20fev%202018.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20Membros%20fev%202018.ods'
        if mes == '03':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20membros%20ativos%20ref03.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membros%20inativos%20ref03.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servidores%20inativos%20ref03.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20%20servidores%20ativos%20ref03.ods'
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Beneficiarios%20Servidores%20mar%202018.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Beneficiarios%20Membros%20mar%202018.ods'
        if mes == '04':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20membros%20ativos%20ref04.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membros%20inativos%20ref04.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servidores%20inativos%20ref04.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20%20servidores%20ativos%20ref04.ods'
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Beneficiarios%20Servidores%20abr%202018.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Beneficiarios%20Membros%20abr%202018.ods'
        if mes == '05':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20membros%20ativos%20ref05.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membros%20inativos%20ref05.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servidores%20inativos%20ref05.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20%20servidores%20ativos%20ref05.ods'
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Beneficiarios%20Servidores%20ref05%202018.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20Membros%20ref05%202018.ods'
        if mes == '06':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20membros%20ativos%20ref06.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membros%20inativos%20ref06.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servidores%20inativos%20ref06.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20%20servidores%20ativos%20ref06.ods'
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20Servidores%20ref06%202018.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20Membros%20ref06%202018.ods'
        if mes == '07':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20membros%20ativos%20ref07.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membros%20inativos%20ref07.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servidores%20inativos%20ref07.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20%20servidores%20ativos%20ref07.ods'
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20Servidores%20ref07%202018.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20Membros%20ref07%202018.ods'
        if mes == '08':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20membros%20ativos%20ref08.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membros%20inativos%20ref08.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servidores%20inativos%20ref08.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20%20servidores%20ativos%20ref08.ods'
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20Servidores%20ago%202018.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20Membros%20ago%202018.ods'
        if mes == '09':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20membros%20ativos%20ref09.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membros%20inativos%20ref09.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servidores%20inativos%20ref09.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20%20servidores%20ativos%20ref09.ods'
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/BeneficiariosServidoresSet2018.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/BeneficiariosMembrosSet2018.ods'
        if mes == '10':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20membros%20ativos%20ref10.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membros%20inativos%20ref10.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servidores%20inativos%20ref10.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20%20servidores%20ativos%20ref10.ods'
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20do%20MP%20Servidores%20out%202018.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20do%20MP%20Membros%20out%202018.ods'
        if mes == '11':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20membros%20ativos%20ref11.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membros%20inativos%20ref11.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servidores%20inativos%20ref11.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20%20servidores%20ativos%20ref11.ods'
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20do%20MP%20Servidores%20nov%202018.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20do%20MP%20Membros%20nov%202018.ods'
        if mes == '12':
            MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20membros%20ativos%20ref122018.ods'
            MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membros%20inativos%20ref12.ods'
            MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servidores%20inativos%20ref12.ods'
            MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20%20servidores%20ativos%20ref122018.ods'
            MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20do%20MP%20Servidores%20dez%202018.ods'
            MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Benefici%C3%A1rios%20do%20MP%20Membros%20dez%202018.ods'
    
    r = requests.get(MPSP_URL_MEMB_ATIVOS, allow_redirects=True)
    open('membros_ativos' + mes + ano, 'wb').write(r.content)
    r = requests.get(MPSP_URL_MEMB_INATIVOS, allow_redirects=True)
    open('membros_inativos' + mes + ano, 'wb').write(r.content)
    r = requests.get(MPSP_URL_SERV_INATIVOS, allow_redirects=True)
    open('servidores_inativos' + mes + ano, 'wb').write(r.content)
    r = requests.get(MPSP_URL_SERV_ATIVOS, allow_redirects=True)
    open('servidores_ativos' + mes + ano, 'wb').write(r.content)
    r = requests.get(MPSP_URL_PENS_SERVIDORES, allow_redirects=True)
    open('pensionistas_servidores' + mes + ano, 'wb').write(r.content)
    r = requests.get(MPSP_URL_PENS_MEMBROS, allow_redirects=True)
    open('pensionistas_membros' + mes + ano, 'wb').write(r.content) 

















#       MPSP_URL_MEMB_ATIVOS = 
#      MPSP_URL_MEMB_INATIVOS = 
#        MPSP_URL_SERV_INATIVOS = 
#       MPSP_URL_SERV_ATIVOS = 
#      MPSP_URL_PENS_SERVIDORES = 
#     MPSP_URL_PENS_MEMBROS = 