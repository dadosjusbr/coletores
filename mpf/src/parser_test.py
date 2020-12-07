import parser
import os

# ----- Teste de unidade referente a data de Janeiro de 2020  buscando validar --------#
#---- o parser para situações onde temos informações sobre verbas indenizatórias ----#

file_names = ["remuneracao-membros-ativos_2020_Janeiro.ods",'provento-membros-inativos_2020_Janeiro.ods',
"remuneracao-servidores-ativos_2020_Janeiro.ods","provento-servidores-inativos_2020_Janeiro.ods",
"valores-percebidos-pensionistas_2020_Janeiro.ods","valores-percebidos-colaboradores_2020_Janeiro.ods"]

vi = ["verbas-indenizatorias-e-outras-remuneracoes-temporarias_2020_Janeiro_membros-ativos.ods",
"verbas-indenizatorias-e-outras-remuneracoes-temporarias_2020_Janeiro_membros-inativos.ods",
"verbas-indenizatorias-e-outras-remuneracoes-temporarias_2020_Janeiro_servidores-ativos.ods",
"verbas-indenizatorias-e-outras-remuneracoes-temporarias_2020_Janeiro_servidores-inativos.ods",
"verbas-indenizatorias-e-outras-remuneracoes-temporarias_2020_Janeiro_pensionistas.ods",
'verbas-indenizatorias-e-outras-remuneracoes-temporarias_2020_Janeiro_colaboradores.ods']

def unit_test_with_vi():
    file_path = 'test_files'
    year = 2020
    month = 'Janeiro'

    all_files = [] 

    for file in file_names:
        all_files.append(file)
    all_files.append(vi)

    return parser.crawler_result(year,month,file_path,all_files)

def show_test_result():
    result  =  unit_test_with_vi()
    print(result)

show_test_result()



