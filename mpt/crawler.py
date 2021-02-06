import os
import sys
import time
import pathlib 
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

# Constants
BASE_URL = "https://mpt.mp.br/MPTransparencia/pages/portal/"
## Year dropdown identification, used to set the year
YEARS = "j_idt140"
## Identification of the element "Pesquisar", to be used when the search by link text doesn't works
SEARCH_NAME = "j_idt143"
## Identification of the extension type to be used in the download.
EXTENSION_CODE = ":j_idt162"
## Expected download extension, in this case .xls
EXTENSION  =  '.xls'
TYPES = {
        0 : "remuneracaoMembrosAtivos",
        1 : "proventosMembrosInativos",
        2 : "remuneracaoServidoresAtivos",
        3 : "proventosServidoresInativos",
        4 : "proventosPensionistas",
        5 : "proventosColaboradores"
    }
MONTHS = {
        '1' : "jan",
        '2' : "fev",
        '3' : "mar",
        '4' : "abr",
        '5' : "mai",
        '6' : "jun",
        '7' : "jul",
        '8' : "ago",
        '9' : "set",
        '10' : "out",
        '11' : "nov",
        '12' : "dez"
    }

# Retrieves payment files from MPT
def crawl(output_path, driver_path, month, year):
    files = []
    urls = links()
    # Creates the download directory (if it doesn't exists)
    pathlib.Path('./' + output_path).mkdir(exist_ok = True)

    for key, url in zip(TYPES.keys(), urls):
        download(url, output_path, driver_path, month, year)
        new_file_path = rename_file(key, output_path, month, year)
        files.append(new_file_path)
    return files

def links():
    links = []
    for i in range(len(TYPES)):
        links.append(BASE_URL + TYPES[i] + ".xhtml")
    return links

def download(url, output_path, driver_path, month, year):
    driver = setup_driver(output_path, driver_path)
    driver.get(url)
    years = driver.find_element_by_id(YEARS)
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

def setup_driver(output_path, driver_path):
    current_directory = os.getcwd()
    path_chrome = current_directory + driver_path
    path_prefs = current_directory + output_path
    
    prefs = {"download.default_directory" : path_prefs}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", prefs)
    return webdriver.Chrome(executable_path = path_chrome, chrome_options = chrome_options)

def rename_file(key, output_path, month, year):
    prev_types = ["RemuneracaoMembrosAtivos", "ProventosMembrosInativos",
                 "RemuneracaoServidoresAtivos", "RemuneracaoServidoresInativos",
                 "RemuneracaoPensionistas", "RemuneracaoColaboradores"]
    prev_file_name = prev_types[key] + '-' + MONTHS[month] + "-" + year + EXTENSION
    prev_file_path = ("./" + output_path + "//" + prev_file_name)
    
    time_to_wait = 10
    time_counter = 0
    while not os.path.exists(prev_file_path):
        time.sleep(1)
        time_counter += 1
        if time_counter > time_to_wait:
            sys.stderr.write("Tempo esgotado para localização do arquivo {}: SystemError.".format(prev_file_name))
            os._exit(2)
    
    new_file_name = TYPES[key] + '-' + month + "-" + year + EXTENSION
    new_file_path = ("./" + output_path + "//" + new_file_name)
    os.rename(prev_file_path, new_file_path)
    return new_file_path
