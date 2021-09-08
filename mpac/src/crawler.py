import pathlib
import os
from time import sleep
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


BASE_URL_MEMBROS_ATIVOS = 'http://transparencia.mpac.mp.br/categoria_arquivos/112'


def crawl(month, year, driver_path, output_path):
    files = []

    pathlib.Path(output_path).mkdir(exist_ok=True)
    driver = setup_driver(driver_path, output_path)

    sleep(4)

    driver.get(BASE_URL_MEMBROS_ATIVOS)
    sleep(5)
    file_path = download(str(month), year, output_path, driver)

    driver.quit()
    return file_path


def download(month, year, output_path, driver):
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
    file_name = format_filename(output_path, month, year)

    return file_name


def setup_driver(driver_path, output_path):
    # Seting the directorys to be used by selenium
    current_directory = os.getcwd()
    path_chrome = current_directory + driver_path
    path_prefs = output_path

    # Attributing the paths to the webdriver
    prefs = {"download.default_directory": path_prefs}
    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_experimental_option("prefs", prefs)
    return webdriver.Chrome(executable_path = path_chrome, chrome_options = chrome_options)


def format_filename(output_path, month, year):
    # Identifying the name of the last downloaded file
    filename = max([os.path.join(output_path, f)
                   for f in os.listdir(output_path)], key=os.path.getctime)
    # renaming the file properly, according to the month
    new_filename = year + "-" + month + "-" + "remuneracao-membros-ativos" + ".ods"

    shutil.move(filename, os.path.join(output_path, r"{}".format(new_filename)))
    new_output_path = output_path + "/" + new_filename

    return new_output_path
