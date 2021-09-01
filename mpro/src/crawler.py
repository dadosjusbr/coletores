import pathlib
import os
import sys
import time
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

BASE_URL = 'https://servicos-portal.mpro.mp.br/web/mp-transparente/contracheque'
BASE_URL_MEMBROS_ATIVOS = 'https://servicos-portal.mpro.mp.br/plcVis/frameset?__report=..%2FROOT%2Frel%2Fcontracheque%2Fmembros%2FremuneracaoMembrosAtivos.rptdesign&anomes='
BASE_URL_VERBAS_INDENIZATORIAS = 'https://servicos-portal.mpro.mp.br/plcVis/frameset?__report=..%2FROOT%2Frel%2Fcontracheque%2Fmembros%2FverbasIndenizatoriasMembrosAtivos.rptdesign&anomes='
FLAG = ['remuneracao','verbas-indenizatorias']

def crawl(month, year, driver_path, output_path):
    files = []
    pathlib.Path(output_path).mkdir(exist_ok=True)
    driver = setup_driver(driver_path, output_path)
    driver.get(BASE_URL)
    time.sleep(4)
    for flag in FLAG:   # 0 for Membros Ativos
        file_path = download(str(month), year, output_path, driver, flag)
        files.append(file_path)
    driver.quit()
    return files


def download(month, year, output_path, driver, flag):  
    driver.get(BASE_URL)
    main_tab = driver.window_handles[0]
    time.sleep(3)

    if(flag == 'remuneracao'):
        document_type = driver.find_element(By.XPATH, '//*[@id="article_10154_29101_2483282_1.3"]/p/span/a')
        document_type.click()
    else:
        document_type = driver.find_element(By.XPATH, '//*[@id="article_10154_29101_2483282_1.3"]/p/span/span/span/span/span/a')
        document_type.click()   

    time.sleep(3)
    select_year = driver.find_element(By.XPATH, '//*[@id="selectAno"]')
    select_year.click()
    if(year in ['2018', '2019', '2020']):
        if(year == "2018"):
            select_year = driver.find_element(By.XPATH, '//*[@id="selectAno"]/option[4]')
        elif(year == "2019"):
            select_year = driver.find_element(By.XPATH, '//*[@id="selectAno"]/option[3]')
        elif(year == "2020"):
            select_year = driver.find_element(By.XPATH, '//*[@id="selectAno"]/option[2]')

        select_year.click()
        
    time.sleep(1)
    x_path = '//*[@id="selectMes"]/option[' + month + ']'
    current_month = driver.find_element(By.XPATH, x_path)
    current_month.click()
    time.sleep(1)
    new_url = ''

    # Downloading the file
    if(flag == 'remuneracao'):
        show_data = driver.find_element(By.XPATH, '//*[@id="article_10154_29101_2483760_1.9"]/table/tbody/tr[4]/td[1]/input')
        show_data.click()
        new_url = BASE_URL_MEMBROS_ATIVOS + year + month + '&nome=&cargo=&lotacao='

    elif(flag == 'verbar-indenizatorias'):
        show_data = driver.find_element(By.XPATH, '//*[@id="article_10154_29101_5313882_1.3"]/table/tbody/tr[4]/td[1]')
        show_data.click()
        new_url = BASE_URL_VERBAS_INDENIZATORIAS + year + month

    new_tab = driver.window_handles[1]
    time.sleep(2)
    driver.get(new_url)
    time.sleep(8)
    export = driver.find_element(By.XPATH, '//*[@id="toolbar"]/table/tbody/tr[2]/td[6]/input')
    export.click()
    time.sleep(2)
    select_columns = driver.find_element(By.XPATH, '//*[@id="simpleExportDialogBody"]/tbody/tr[5]/td[2]/table/tbody/tr/td/table/tbody/tr[1]/td')
    select_columns.click()
    download = driver.find_element(By.XPATH, '//*[@id="simpleExportDataDialogokButton"]')
    download.click()

    # Formating the filename
    time.sleep(4)
    file_name = format_filename('.' + output_path, month, year, flag)
    time.sleep(2)

    # Closing new tabs
    driver.switch_to_window(new_tab)
    driver.close()
    driver.switch_to_window(main_tab)

    return file_name

def setup_driver(driver_path, output_path):
    # Seting the directorys to be used by selenium
    current_directory = os.getcwd()
    path_chrome = current_directory + driver_path
    path_prefs = current_directory + output_path

    # Attributing the paths to the webdriver
    prefs = {"download.default_directory" : path_prefs}
    chrome_options = webdriver.ChromeOptions()
    
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_experimental_option("prefs", prefs)
    return webdriver.Chrome(executable_path = path_chrome, chrome_options = chrome_options)

def format_filename(output_path, month, year, flag):
    # Identifying the name of the last downloaded file
    filename = max([os.path.join(output_path, f) for f in os.listdir(output_path)], key=os.path.getctime)

    # renaming the file properly, according to the month
    if(flag == 'remuneracao'):
        new_filename = month + "-" + year + "-" +flag +"-membros-ativos" + ".csv"
    elif(flag == 'verbar-indenizatorias'):
        new_filename = month + "-" + year + "-" +flag + "-membros-ativos" + ".csv"

    shutil.move(filename,os.path.join(output_path,r"{}".format(new_filename)))
    new_output_path = output_path + "/" + new_filename

    return new_output_path 