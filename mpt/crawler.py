import os
import sys
import time
import pathlib 
import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

# Constants
BASE_URL = "https://mpt.mp.br/MPTransparencia/pages/portal/"
## Identification of the element "Pesquisar", to be used when the search by link text doesn't works
SEARCH_NAME = "j_idt143"
## Identification of the extension type to be used in the download. In this case, .ods
EXTENSION_CODE = ":j_idt157"
TYPES = {
        0 : "remuneracaoMembrosAtivos",
        1 : "proventosMembrosInativos",
        2 : "remuneracaoServidoresAtivos",
        3 : "proventosServidoresInativos",
        4 : "proventosPensionistas",
        5 : "proventosColaboradores"
    }
MONTHS = {
        '1' : "Janeiro",
        '2' : "Fevereiro",
        '3' : "Março",
        '4' : "Abril",
        '5' : "Maio",
        '6' : "Junho",
        '7' : "Julho",
        '8' : "Agosto",
        '9' : "Setembro",
        '10' : "Outubro",
        '11' : "Novembro",
        '12' : "Dezembro"
    }

# Retrieves payment files from MPT
def crawl(output_path, month, year):
    files = []
    urls = links()

    # Creates the download directory (if it doesn't exists)
    pathlib.Path('./' + output_path).mkdir(exist_ok = True)
    
    for i, url in zip(TYPES.keys(), urls):
        file_name = TYPES[i] + '-' + month + "-" + year + '.ods'
        
        file_path = (output_path + "/" + file_name)
        download(url, output_path, month, year)
        files.append(file_path)

    return files

def links():
    links = []
    for i in range(len(TYPES)):
        links.append(BASE_URL + TYPES[i] + ".xhtml")
    return links

def download(url, file_path, month, year):
    driver = setup_driver()
    driver.get(url)
    years = driver.find_element_by_id("j_idt140")
    now = datetime.datetime.now()
    current_year = now.year
    
    for _ in range(current_year - int(year)):
        years.send_keys(Keys.ARROW_DOWN)
    try:
        WebDriverWait(driver, 10)
        search = driver.find_element_by_link_text("Pesquisar")
        search.click()
    except NoSuchElementException:
        try:
            search = driver.find_element_by_name(SEARCH_NAME)
            search.click()
        finally:
            sys.stderr.write("Ano identificado.\n")

    id_month = "tabelaRemuneracao:" + str(int(month) - 1) + EXTENSION_CODE
    try:
        archive = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, id_month))
        )
        try:
            archive.send_keys("\n")
            driver.execute_script("arguments[0].click();", archive)
            WebDriverWait(driver, 10)
        finally:
            sys.stderr.write("Mês identificado.\n")
    finally:
        sys.stderr.write("Download efetuado.\n")
    driver.quit()

def setup_driver():
    env_path = '.env'
    load_dotenv(dotenv_path = env_path)
    current_directory = os.getcwd()

    RELATIVE_PATH_CHROME = os.getenv("PATH_DRIVER")
    RELATIVE_PATH_PREFS = os.getenv("OUTPUT_FOLDER")
    PATH_CHROME = current_directory + RELATIVE_PATH_CHROME
    PATH_PREFS = current_directory + RELATIVE_PATH_PREFS
    
    prefs = {"download.default_directory" : PATH_PREFS}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(executable_path = PATH_CHROME, chrome_options = chrome_options)
    return driver