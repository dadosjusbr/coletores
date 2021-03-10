import pathlib
import os
import sys
import time
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

base_URL = 'https://paineis.cnj.jus.br/QvAJAXZfc/opendoc.htm?document=qvw_l%2FPainelCNJ.qvw&host=QVS%40neodimio03&anonymous=true&sheet=shPORT63Relatorios'

# The types described below are the payrolls, followed by their ids on the html 
# page, used in the element identification, and their name
payroll_types = {1: ['QvFrame Document_TX3522', '13', 'Contracheque'],
                 2: ['QvFrame Document_TX3712', '14', 'Direitos Pessoais'],
                 3: ['QvFrame Document_TX3713', '16', 'Indenizações'],
                 4: ['QvFrame Document_TX3711', '6', 'Direitos Eventuais']
                }

def crawl(court, driver_path, output_path):
    files = []
    pathlib.Path(output_path).mkdir(exist_ok=True)
    for payroll in payroll_types.values():
        file_path = download(court, payroll, driver_path, output_path)
        files.append(file_path)
    return files

def download(court, payroll, driver_path, output_path):
    driver = setup_driver(driver_path, output_path)
    driver.get(base_URL)
    
    ## Opening the search bar
    time.sleep(10)
    courts = driver.find_element(By.XPATH, "//*[@title='Tribunal']")
    search_icon = courts.find_element(By.XPATH, "//*[@title='Pesquisar']")
    search_icon.click()

    ## Selecting the input text in the search bar
    time.sleep(10)
    search_bar = driver.find_element_by_class_name("PopupSearch")
    input_text = search_bar.find_element(By.XPATH, "//input[@type='text']")

    ## Searching by court name
    time.sleep(10)
    input_text.send_keys(court)
    input_text.send_keys(Keys.ENTER)
    sys.stderr.write("Court selected.\n")

    # Selecting the payroll
    time.sleep(10)
    x_path = "//div[@class='" + payroll[0] + "'][@id='"+ payroll[1] + "']"
    current_payroll = driver.find_element(By.XPATH, x_path)
    current_payroll.click()
    sys.stderr.write("Payroll selected: {}.\n".format(payroll[2]))

    # Donwloading the file
    time.sleep(10)
    download = driver.find_element(By.XPATH, "//*[@title='Enviar para Excel']")
    download.click()
    time.sleep(30)
    sys.stderr.write("File downloaded.\n")

    # Formating the filename
    file_name = format_filename('.' + output_path, payroll[2])
    driver.quit()

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

def format_filename(output_path, payroll_name):
    # Identifying the name of the last downloaded file
    filename = max([os.path.join(output_path, f) for f in os.listdir(output_path)], key=os.path.getctime)

    # renaming the file properly, according to the payroll
    new_filename = payroll_name + ".xlsx"
    shutil.move(filename,os.path.join(output_path,r"{}".format(new_filename)))
    new_output_path = output_path + "/" + new_filename

    return new_output_path
