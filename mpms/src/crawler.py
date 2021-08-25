import pathlib
import os
import sys
from time import sleep
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By

BASE_URL = 'https://transparencia.mpms.mp.br/QvAJAXZfc/opendoc.htm?document=portaltransparencia%5Cportaltransparencia.qvw&lang=pt-BR&host=QVS%40srv-1645&anonymous=true'

MONTHS = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
          'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']


def crawl(year, month, driver_path, output_path):
    file = []
    pathlib.Path(output_path).mkdir(exist_ok=True)
    driver = setup_driver(driver_path, output_path)

    step_one(driver)
    select_contracheque(driver)
    
    if(year != '2021'):
        select_year(year, driver)
    # Usar o mês passado como parâmetro para pegar o equivalente em string
    select_month(MONTHS[int(month) - 1], driver)
    file.append(download(output_path, driver, year, month, 'remuneracao'))

    if(year != '2018' and (year == '2019' and int(month)>=7)):
        select_indenizacoes(driver)

        if(year != '2021'):
            select_year(year, driver)
        # Usar o mês passado como parâmetro para pegar o equivalente em string
        select_month(MONTHS[int(month) - 1], driver)
        file.append(download(output_path, driver, year, month, 'indenizacao'))

    return file


def setup_driver(driver_path, output_path):
    # Seting the directorys to be used by selenium
    current_directory = os.getcwd()
    path_chrome = current_directory + driver_path
    path_prefs = current_directory + output_path

    # Attributing the paths to the webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": path_prefs,
        "download.prompt_for_download": False
    })

    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-setuid-sandbox")
    return webdriver.Chrome(executable_path=path_chrome, chrome_options=chrome_options)

def step_one(driver):
    driver.get(BASE_URL)
    sleep(15)

    # Limpar depois
    n1 = driver.find_element_by_id('20')
    n2 = n1.find_elements_by_class_name(name='QvContent')[0]
    n3 = n2.find_element_by_class_name(name='TextObject')
    n3.click()
    sleep(3)

def select_contracheque(driver):
    # Limpar depois
    n1 = driver.find_element_by_id('26')
    n2 = n1.find_elements_by_class_name(name='QvContent')[0]
    n3 = n2.find_element_by_class_name(name='TextObject')
    n3.click()
    sleep(3)


def select_indenizacoes(driver):
    # Limpar depois
    n1 = driver.find_element_by_id('83')
    n2 = n1.find_elements_by_class_name(name='QvContent')[0]
    n3 = n2.find_element_by_class_name(name='TextObject')
    n3.click()
    sleep(3)


def select_year(year, driver):
    # Usado para selecionar a div e o ano dele
    div_year = driver.find_element(By.XPATH, '//*[@title="Ano"]/div')
    div_year.click()
    sleep(1)
    year_selected = driver.find_element(By.XPATH, f'//*[@title="{year}"]')
    year_selected.click()
    sleep(2)


def select_month(month, driver):
    # Estava dando erro quando o mês já estava selecionado, para resolver, apenas ignoro
    try:
        # Usado para selecionar a div e o mês dele
        div_month = driver.find_element(By.XPATH, '//*[@title="Mês"]/div')
        div_month.click()
        sleep(1)
        month_selected = driver.find_element(By.XPATH, f'//*[@title="{month}"]')
        month_selected.click()
        sleep(2)
    except:
        pass

def download(output_path, driver, year, month, name):
    n1 = driver.find_element(By.XPATH, "//*[@title='Enviar para Excel']")
    n1.click()
    sleep(15)

    file_name = format_filename(output_path, year, month, name)

    return file_name

def format_filename(output_path, year, month, name):
    current_directory = os.getcwd() + output_path
    # Identifying the name of the last downloaded file
    filename = max([os.path.join(current_directory, f) for f in os.listdir(current_directory)],
                   key=os.path.getctime)

    # renaming the file properly, according to the payroll
    new_filename = name + "-" + year + '-' + month + ".xlsx"
    shutil.move(filename,os.path.join(current_directory,f"{new_filename}"))
    new_output_path =current_directory + "/" + new_filename

    return new_output_path
