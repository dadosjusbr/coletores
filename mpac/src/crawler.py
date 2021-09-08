import pathlib
import os
import sys
from time import sleep
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select


BASE_URL_MEMBROS_ATIVOS = 'http://transparencia.mpac.mp.br/categoria_arquivos/112'
BASE_URL_VERBAS_INDENIZATORIAS = 'http://transparencia.mpac.mp.br/categoria_arquivos/119'

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
            file_path = download(str(month), year, output_path, driver, flag)
            files.append(file_path)
        elif flag == VERBAS_INDENIZATORIAS:
            driver.get(BASE_URL_VERBAS_INDENIZATORIAS)
            sleep(5)
            file_path = download(str(month), year, output_path, driver, flag)
            files.append(file_path)
    driver.quit()
    return files


def download(month, year, output_path, driver, flag):
    select_year = driver.find_element(By.XPATH, '//*[@id="ano"]')
    select_year.click()

    if(year in ['2018', '2019', '2020']):
        if(year == "2018"):
            select_year = driver.find_element(
                By.XPATH, '//*[@id="ano"]/option[4]')
        elif(year == "2019"):
            select_year = driver.find_element(
                By.XPATH, '//*[@id="ano"]/option[3]')
        elif(year == "2020"):
            select_year = driver.find_element(
                By.XPATH, '//*[@id="ano"]/option[2]')

        select_year.click()

    sleep(4)
    current_month = driver.find_element(By.XPATH, '//*[@id="numMes"]')
    select_month = Select(current_month)
    select_month.select_by_value(month.replace('0',''))

    sleep(2)
    button_download = driver.find_element(By.XPATH, '//*[@class="pesquisar"]')
    button_download.click()

    # Formating the filename
    sleep(2)
    file_name = format_filename('.' + output_path, month, year, flag)

    return file_name


def setup_driver(driver_path, output_path):
    # Seting the directorys to be used by selenium
    current_directory = os.getcwd()
    path_chrome = current_directory + driver_path
    path_prefs = current_directory + output_path

    # Attributing the paths to the webdriver
    prefs = {"download.default_directory": path_prefs}
    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_experimental_option("prefs", prefs)
    return webdriver.Chrome(executable_path=path_chrome, chrome_options=chrome_options)


def format_filename(output_path, month, year, flag):
    # Identifying the name of the last downloaded file
    filename = max([os.path.join(output_path, f)
                   for f in os.listdir(output_path)], key=os.path.getctime)

    # renaming the file properly, according to the month
    if(flag == REMUNERACAO):
        new_filename = year + "-" + month + "-" + flag + "-membros-ativos" + ".ods"
    elif(flag == VERBAS_INDENIZATORIAS):
        new_filename = year + "-" + month + "-" + flag + "-membros-ativos" + ".ods"

    shutil.move(filename, os.path.join(
        output_path, r"{}".format(new_filename)))
    new_output_path = output_path + "/" + new_filename

    return new_output_path
