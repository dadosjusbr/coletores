import pathlib
import os
import sys
import csv
from time import sleep
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup


BASE_URL_MEMBROS_ATIVOS = 'https://www.mpap.mp.br/transparencia/index.php?pg=consulta_folha_membros_ativos'
BASE_URL_VERBAS_INDENIZATORIAS = 'https://www.mpap.mp.br/transparencia/index.php?pg=consulta_verbas_indenizatorias'

FLAG = ['remuneracao', 'verbas-indenizatorias']
REMUNERACAO = 'remuneracao'
VERBAS_INDENIZATORIAS = 'verbas-indenizatorias'


def crawl(month, year, driver_path, output_path):
    files = []

    pathlib.Path(output_path).mkdir(exist_ok=True)
    driver = setup_driver(driver_path, output_path)

    sleep(4)
    for flag in FLAG:
        if flag == REMUNERACAO:
            driver.get(BASE_URL_MEMBROS_ATIVOS)
            sleep(5)
            file_path = download(month, year, output_path, driver, flag)
            files.append(file_path)
        elif flag == VERBAS_INDENIZATORIAS:
            driver.get(BASE_URL_VERBAS_INDENIZATORIAS)
            sleep(5)
            file_path = download(month, year, output_path, driver, flag)
            files.append(file_path)

    driver.quit()
    return files


def download(month, year, output_path, driver, flag):
    try:
        current_year = driver.find_element(By.XPATH, '//*[@id="ano"]')
    except:
        current_year = driver.find_element(By.XPATH, '//*[@id="ano_verbas"]')

    select_year = Select(current_year)
    select_year.select_by_value(year)

    sleep(4)
    current_month = driver.find_element(By.XPATH, '//*[@id="mes"]')
    select_month = Select(current_month)
    select_month.select_by_value(month.replace('0',''))

    sleep(2)
    button_enviar = driver.find_element(By.XPATH, '//*[@id="enviar"]')
    button_enviar.click()

    # Formating the filename
    sleep(6)
    file_name = ''
    if flag == REMUNERACAO:
        file_name = download_remuneracao(driver, output_path, month, year, flag)
    elif flag == VERBAS_INDENIZATORIAS:
        file_name = download_indenizacao(driver, output_path, month, year, flag)

    return file_name

def download_remuneracao(driver, output_path, month, year, flag):
    print('remuneração')
    page = driver.page_source
    site = BeautifulSoup(page, 'html.parser')
    table = site.select_one("table")

    data = [d for d in table.select("tbody tr")]
    path = format_filename(output_path, month, year, flag)

    f = csv.writer(open(path, 'w'))
    f.writerow(['MATRÍCULA', 'NOME', 'CARGO', 'LOTAÇÃO', 'REMUNERAÇÃO_DO_CARGO_EFETIVO', 'OUTRAS_VERBAS_REMUNERATÓRIAS,_LEGAIS_OU_JUDICIAIS',
            'FUNÇÃO_DE_CONFIANÇA_OU_CARGO_EM_COMISSÃO', 'GRATIFICAÇÃO_NATALINA', 'FÉRIAS(1/3_CONSTITUCIONAL)', 'ABONO_PERMANÊNCIA',
            'OUTRAS_REMUNERAÇÕES_TEMPORÁRIAS', 'VERBAS_INDENIZATÓRIAS', 'TOTAL_DE_RENDIMENTOS BRUTOS', 'CONTRIBUIÇÃO_PREVIDENCIÁRIA',
            'IMPOSTO_DE_RENDA', 'RETENÇÃO_TETO','TOTAL_DESCONTOS', 'RENDIMENTO_LÍQUIDO'])

    for d in data:
        linha = []
        for t in d.select("td"):
            linha.append(t.text)
        f.writerow(linha)

    return path

def download_indenizacao(driver, output_path, month, year, flag):
    print('indenização')
    button_download = driver.find_element(By.XPATH, '//*[@class="btn btn-small btn-success"]')
    button_download.click()
    path = format_filename(output_path, month, year, flag)
    return path

def setup_driver(driver_path, output_path):
    # Seting the directorys to be used by selenium
    current_directory = os.getcwd()
    path_chrome = current_directory + driver_path
    path_prefs = current_directory+output_path

    # Attributing the paths to the webdriver
    prefs = {"download.default_directory": path_prefs}
    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_experimental_option("prefs", prefs)
    return webdriver.Chrome(executable_path=path_chrome, chrome_options=chrome_options)


def format_filename(output_path, month, year, flag):
    new_filename = ""
    if(flag == REMUNERACAO):
        new_filename = year + "-" + month + "-" + flag + "-membros-ativos" + ".csv"
        new_output_path = output_path + "/" + new_filename
        return new_output_path

    # Identifying the name of the last downloaded file
    filename = max([os.path.join(output_path, f)
                   for f in os.listdir(output_path)], key=os.path.getctime)
    # renaming the file properly, according to the month
    
    new_filename = year + "-" + month + "-" + flag + "-membros-ativos" + ".ods"
    shutil.move(filename, os.path.join(
        output_path, r"{}".format(new_filename)))
    new_output_path = output_path + "/" + new_filename
    return new_output_path
