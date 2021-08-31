import pathlib
import os
import sys
import time
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

base_url = 'https://servicos-portal.mpro.mp.br/web/mp-transparente/contracheque'
base_url_membros_ativos = 'https://servicos-portal.mpro.mp.br/plcVis/frameset?__report=..%2FROOT%2Frel%2Fcontracheque%2Fmembros%2FremuneracaoMembrosAtivos.rptdesign&anomes='
base_url_verbas_indenizatorias = 'https://servicos-portal.mpro.mp.br/plcVis/frameset?__report=..%2FROOT%2Frel%2Fcontracheque%2Fmembros%2FverbasIndenizatoriasMembrosAtivos.rptdesign&anomes='

def crawl(court, year, driver_path, output_path):
    files = []
    pathlib.Path(output_path).mkdir(exist_ok=True)
    driver = setup_driver(driver_path, output_path)
    driver.get(base_url)
    time.sleep(4)
    for flag in range(2):   # 0 for Membros Ativos
        for month in range(1, 13):
            file_path = download(court, str(month), year, output_path, driver, flag)
            files.append(file_path)
    driver.quit()
    return files


def download(court, month, year, output_path, driver, flag):  
    driver.get(base_url)
    main_tab = driver.window_handles[0]
    time.sleep(3)

    if(flag == 0):
        document_type = driver.find_element(By.XPATH, '//*[@id="article_10154_29101_2483282_1.3"]/p/span/a')
        document_type.click()
        print('MEMBROS ATIVOS')
    else:
        document_type = driver.find_element(By.XPATH, '//*[@id="article_10154_29101_2483282_1.3"]/p/span/span/span/span/span/a')
        document_type.click()   
        print('VERBAS IDENIZATÓRIAS')

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
        print('ANO ' + str(year))
    else:
        print('ANO ' + str(year))
    time.sleep(1)
    select_month = driver.find_element(By.XPATH, '//*[@id="selectMes"]')
    x_path = '//*[@id="selectMes"]/option[' + month + ']'
    current_month = driver.find_element(By.XPATH, x_path)
    current_month.click()
    time.sleep(1)
    print('MÊS ' + str(month))
    new_url = ''

    # Downloading the file
    if(flag == 0):
        show_data = driver.find_element(By.XPATH, '//*[@id="article_10154_29101_2483760_1.9"]/table/tbody/tr[4]/td[1]/input')
        show_data.click()
        new_url = base_url_membros_ativos + year + '0' + month + '&nome=&cargo=&lotacao='

    else:
        show_data = driver.find_element(By.XPATH, '//*[@id="article_10154_29101_5313882_1.3"]/table/tbody/tr[4]/td[1]')
        show_data.click()
        new_url = base_url_verbas_indenizatorias + year + '0' + month

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
    sys.stderr.write("File downloaded.\n")

    # Formating the filename
    time.sleep(4)
    file_name = format_filename('.' + output_path, court, month, year, flag)
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
    chrome_options.add_experimental_option("prefs", prefs)
    return webdriver.Chrome(executable_path = path_chrome, chrome_options = chrome_options)

def format_filename(output_path, court, month, year, flag):
    # Identifying the name of the last downloaded file
    filename = max([os.path.join(output_path, f) for f in os.listdir(output_path)], key=os.path.getctime)

    # renaming the file properly, according to the month
    if(flag == 0):
        new_filename = court + "-" + month + "_" + year + "-Membros Ativos" + ".csv"
    else:
        new_filename = court + "-" + month + "_" + year + "-Verbas Indenizatórias" + ".csv"

    shutil.move(filename,os.path.join(output_path,r"{}".format(new_filename)))
    new_output_path = output_path + "/" + new_filename

    return new_output_path 