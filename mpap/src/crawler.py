import pathlib
import os
import sys
import csv
from time import sleep
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup


BASE_URL_MEMBROS_ATIVOS = 'https://www.mpap.mp.br/transparencia/index.php?pg=consulta_folha_membros_ativos'
BASE_URL_VERBAS_INDENIZATORIAS = 'https://www.mpap.mp.br/transparencia/index.php?pg=consulta_verbas_indenizatorias'


def crawl(month, year, driver_path, output_path):
    files = []

    pathlib.Path(output_path).mkdir(exist_ok=True)
    driver = setup_driver(driver_path, output_path)

    sleep(4)

    # Faz duas chamadas uma para pegar a remuneração e outra para pegar as verbas indenizatorias
    # Carrega a pagina de remuneração
    driver.get(BASE_URL_MEMBROS_ATIVOS)
    sleep(5)
    download(month, year, driver)
    file_path = download_remuneracao(driver, output_path, month, year)
    files.append(file_path)

    # Carrega a pagina de verbas indenizatorias
    driver.get(BASE_URL_VERBAS_INDENIZATORIAS)
    sleep(5)
    download(month, year, driver)
    file_path = download_indenizacao(driver, output_path, month, year)
    files.append(file_path)

    driver.quit()
    return files


def download(month, year, driver):
    # Como o id de ano muda nas páginas, usei o try except para se der erro em um é o outro.
    try:
        current_year = driver.find_element(By.XPATH, '//*[@id="ano"]')
    except:
        current_year = driver.find_element(By.XPATH, '//*[@id="ano_verbas"]')

    # Esse Select server para pegar as tags select, onde posso passar o valor diretamente,
    # para pegar qual opção eu quero.
    select_year = Select(current_year)
    select_year.select_by_value(year)

    sleep(4)
    current_month = driver.find_element(By.XPATH, '//*[@id="mes"]')
    select_month = Select(current_month)
    # Como os numeros passados quando convertidos para string ficam com um "0" na frente,
    # uso isso para remover, e pegar corretamente o valor da tag.
    select_month.select_by_value(month.replace('0',''))
    sleep(2)

    button_enviar = driver.find_element(By.XPATH, '//*[@id="enviar"]')
    button_enviar.click()
    sleep(6)


# Usado para transformar a pagina html com a planilha, em doc csv, com os valores.
def download_remuneracao(driver, output_path, month, year):
    # Aqui o selenium pega a pagina.
    page = driver.page_source
    # Transforma em objeto beautifulsoup.
    site = BeautifulSoup(page, 'html.parser')
    table = site.select_one("table")
    data = [d for d in table.select("tbody tr")]

    # Dá um nome para o arquivo
    filename = year + "-" + month + "-remuneracao-membros-ativos" + ".csv"
    path = output_path + "/" + filename

    # Cria um documento csv e cria um header para esse documento.
    f = csv.writer(open(path, 'w'))
    f.writerow(['MATRÍCULA', 'NOME', 'CARGO', 'LOTAÇÃO', 'REMUNERAÇÃO_DO_CARGO_EFETIVO', 'OUTRAS_VERBAS_REMUNERATÓRIAS_LEGAIS_OU_JUDICIAIS',
            'FUNÇÃO_DE_CONFIANÇA_OU_CARGO_EM_COMISSÃO', 'GRATIFICAÇÃO_NATALINA', 'FÉRIAS(1/3_CONSTITUCIONAL)', 'ABONO_PERMANÊNCIA',
            'OUTRAS_REMUNERAÇÕES_TEMPORÁRIAS', 'VERBAS_INDENIZATÓRIAS', 'TOTAL_DE_RENDIMENTOS BRUTOS', 'CONTRIBUIÇÃO_PREVIDENCIÁRIA',
            'IMPOSTO_DE_RENDA', 'RETENÇÃO_TETO','TOTAL_DESCONTOS', 'RENDIMENTO_LÍQUIDO'])

    # Pega o valor linha por linha.
    for d in data:
        linha = []
        for t in d.select("td"):
            linha.append(t.text)
        f.writerow(linha)

    return path

# Usado para baixar as planilhas no formato xls
def download_indenizacao(driver, output_path, month, year):
    sleep(5)
    button_download = driver.find_element(By.XPATH, '//*[@class="btn btn-small btn-success"]')
    button_download.click()
    sleep(10)
    path = format_filename(output_path, month, year)
    return path

# Faz a configuração do driver do navegador google chrome
def setup_driver(driver_path, output_path):
    # Seting the directorys to be used by selenium
    current_directory = os.getcwd()
    path_chrome = current_directory + driver_path
    # Attributing the paths to the webdriver
    prefs = {"download.default_directory": output_path}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_experimental_option("prefs", prefs)
    return webdriver.Chrome(executable_path=path_chrome, chrome_options=chrome_options)


# Encontra a planilha de verbas indenizatorias no 'output_path', e altera para um nome padrão.
def format_filename(output_path, month, year):
    # Identifying the name of the last downloaded file
    filename = max([os.path.join(output_path, f) for f in os.listdir(output_path)], key=os.path.getctime)
    
    # Renaming the file properly, according to the month
    new_filename = year + "-" + month + "-verbas-indenizatorias-membros-ativos" + ".xls"
    shutil.move(filename, os.path.join(output_path, r"{}".format(new_filename)))
    new_output_path = output_path + "/" + new_filename
    return new_output_path