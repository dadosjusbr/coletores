import pandas
import csv
import requests
from pandas_ods_reader import read_ods

# Baixa e salva as planilhas
def download(mes, ano):
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

# Inputs para mês e ano
mes = input('Digite o mes: ')
ano = input('Digite o ano: ')

# Links base para downloadd as planilhas
MPSP_URL_MEMB_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_ativos/Tabela%20I%20memb' + mes + ano + '.ods'
MPSP_URL_MEMB_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Membros_inativos/Tabela%20I%20membinat' + mes + ano + '.ods'
MPSP_URL_SERV_INATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/servidores_inativos/Tabela%20I%20servinat' + mes + ano + '.ods'
MPSP_URL_SERV_ATIVOS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Servidores_ativos/Tabela%20I%20serv' + mes + ano + '.ods'
MPSP_URL_PENS_SERVIDORES = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_servidores/Benefici%C3%A1rios%20Servidores%20' + mes + ano + '.ods'
MPSP_URL_PENS_MEMBROS = 'http://www.mpsp.mp.br/portal/page/portal/Portal_da_Transparencia/Contracheque/Pensionistas/Pensionistas_membros/Beneficiarios%20Membros%20' + mes + ano + '.ods'

# Executando ação de download
download(mes, ano)