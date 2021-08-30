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

    find_paycheck(driver)
    select_remuneration(driver)
    
    if(year != '2021'):
        select_year(year, driver)
    # Usar o mês passado como parâmetro para pegar o equivalente em string
    select_month(MONTHS[int(month) - 1], driver)
    file.append(download(output_path, driver, year, month, 'remuneracao'))

    if year == '2020' or year == '2021' or (year == '2019' and int(month)>=7):
        select_indemnization(driver)

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
    path_prefs = output_path

    # Attributing the paths to the webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"')
    chrome_options.add_experimental_option('prefs', {
        'download.default_directory': path_prefs,
        'download.prompt_for_download': False
    })

    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument('start-maximized')
    return webdriver.Chrome(executable_path=path_chrome, chrome_options=chrome_options)


def find_paycheck(driver):
    driver.get(BASE_URL)
    
    sleep(15)

    # find_main_contain = driver.find_element_by_css_selector('.QvPageBody')
    find_div_by_id = driver.find_element_by_class_name('Document_TX28')
    selected_div_qvcontent = find_div_by_id.find_elements_by_class_name(name='QvContent')[0]
    find_div_clickable = selected_div_qvcontent.find_element_by_class_name(name='TextObject')
    find_div_clickable.click()
    sleep(3)

def select_remuneration(driver):
    find_div_by_id = driver.find_element_by_id('26')
    selected_div_qvcontent = find_div_by_id.find_elements_by_class_name(name='QvContent')[0]
    find_div_clickable = selected_div_qvcontent.find_element_by_class_name(name='TextObject')
    find_div_clickable.click()
    sleep(3)


def select_indemnization(driver):
    find_div_by_id = driver.find_element_by_id('83')
    selected_div_qvcontent = find_div_by_id.find_elements_by_class_name(name='QvContent')[0]
    find_div_clickable = selected_div_qvcontent.find_element_by_class_name(name='TextObject')
    find_div_clickable.click()
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
    # Identifying the name of the last downloaded file
    filename = max([os.path.join(output_path, f) for f in os.listdir(output_path)],
                   key=os.path.getctime)

    # renaming the file properly, according to the payroll
    new_filename = name + "-" + year + '-' + month + ".xlsx"
    shutil.move(filename,os.path.join(output_path,f"{new_filename}"))
    new_output_path =output_path + "/" + new_filename

    return new_output_path
