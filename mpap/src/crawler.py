import pathlib
import os
import csv
from time import sleep
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

    # Faz duas chamadas uma para pegar a remuneração e outra para pegar as verbas indenizatorias
    # Carrega a pagina de remuneração
    driver.get(BASE_URL_MEMBROS_ATIVOS)
    sleep(5)
    select_month_and_year(month, year, driver)
    file_path = download_remuneracao(driver, output_path, month, year)
    files.append(file_path)

    # Carrega a pagina de verbas indenizatorias
    if year != '2018':
        driver.get(BASE_URL_VERBAS_INDENIZATORIAS)
        sleep(5)
        select_month_and_year(month, year, driver)
        file_path = download_indenizacao(driver, output_path, month, year)
        files.append(file_path)

    driver.quit()
    return files


def select_month_and_year(month, year, driver):
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
    # uso isso para remover, e pegar corretamente o valor da tag,.
    select_month.select_by_value(month.replace('0', '') if month != '10' else month)
    sleep(2)

    button_enviar = driver.find_element(By.XPATH, '//*[@id="enviar"]')
    button_enviar.click()
    sleep(6)


# Pega a planilha do html
def find_trs(driver):
    # Aqui o selenium pega a pagina.
    page = driver.page_source
    # Transforma em objeto beautifulsoup.
    site = BeautifulSoup(page, 'html.parser')
    table = site.select_one("table")
    data = [d for d in table.select("tbody tr")]
    return data


# Transforma a planilha de remuneracao html, em csv
def download_remuneracao(driver, output_path, month, year):
    data = find_trs(driver)
    # Dá um nome para o arquivo
    filename = year + "-" + month + "-remuneracao-membros-ativos" + ".csv"
    path = output_path + "/" + filename

    # Cria um documento csv e cria um header para esse documento.
    f = csv.writer(open(path, 'w'))
    f.writerow(['MATRÍCULA', 'NOME', 'CARGO', 'LOTAÇÃO', 'REMUNERAÇÃO_DO_CARGO_EFETIVO', 'OUTRAS_VERBAS_REMUNERATÓRIAS_LEGAIS_OU_JUDICIAIS',
                'FUNÇÃO_DE_CONFIANÇA_OU_CARGO_EM_COMISSÃO', 'GRATIFICAÇÃO_NATALINA', 'FÉRIAS(1/3_CONSTITUCIONAL)', 'ABONO_PERMANÊNCIA',
                'OUTRAS_REMUNERAÇÕES_TEMPORÁRIAS', 'VERBAS_INDENIZATÓRIAS', 'TOTAL_DE_RENDIMENTOS BRUTOS', 'CONTRIBUIÇÃO_PREVIDENCIÁRIA',
                'IMPOSTO_DE_RENDA', 'RETENÇÃO_TETO', 'TOTAL_DESCONTOS', 'RENDIMENTO_LÍQUIDO'])

    # Pega o valor linha por linha.
    for d in data:
        linha = []
        for t in d.select("td"):
            linha.append(t.text)
        f.writerow(linha)

    return path


# Transforma a planilha de verbas indenizatorias html, em csv
def download_indenizacao(driver, output_path, month, year):
    data = find_trs(driver)
    # Dá um nome para o arquivo
    filename = year + "-" + month + "-verbas-indenizatorias-membros-ativos" + ".csv"
    path = output_path + "/" + filename

    # Cria um documento csv e cria um header para esse documento.
    f = csv.writer(open(path, 'w'))
    f.writerow(['Matrícula', 'Nome', 'Cargo', 'Lotação', 'Auxílio_Saúde', 'Auxílio_Doença',
                'Auxílio_Moradia', 'Auxílio_Alimentação', 'Licença_Prêmio', 'Indenização_de_Férias',
                'Abono_Pecuniário', 'Recesso_Administrativo', 'Diferença_Indenizada', 'Plantão_indenizado',
                'Total1', 'Substituição', 'Hora-Extra', 'Plantão', 'Diferença_de_Recebimentos', 'Cumulação',
                'Devoluções_de_Desconto', 'Gratificações', 'Total2'])

    # Pega o valor linha por linha.
    for d in data:
        linha = []
        for t in d.select("td"):
            linha.append(t.text)
        f.writerow(linha)

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
