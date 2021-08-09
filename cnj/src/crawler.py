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
payroll_types = {1: ['QvFrame Document_TX3522', '12', 'Contracheque'],
                 2: ['QvFrame Document_TX3712', '13', 'Direitos Pessoais'],
                 3: ['QvFrame Document_TX3713', '15', 'Indenizações'],
                 4: ['QvFrame Document_TX3711', '6', 'Direitos Eventuais']
                }
                
def crawl(court, year, month, driver_path, output_path):
    files = []
    pathlib.Path(output_path).mkdir(exist_ok=True)
    driver = setup_driver(driver_path, output_path)
    select_court(court, driver)
    select_year(year, driver)
    select_month(month, driver)
    for payroll in payroll_types.values():
        file_path = download(court, year, month, payroll, output_path, driver)
        files.append(file_path)
    driver.quit()
    return files

def select_court(court, driver):
    driver.get(base_URL)

    # Opening the search bar - Tribunal
    # Other approaches, such as waiting for the elements to be visible, did not work. 
    # So, as it is necessary to wait for the page to load, time.sleep was used here
    # and below. (https://stackoverflow.com/questions/45347675/make-selenium-wait-10-seconds)
    time.sleep(15)
    courts = driver.find_element(By.XPATH, "//*[@title='Tribunal']")
    search_icon = courts.find_element(By.XPATH, "//*[@title='Pesquisar']")
    search_icon.click()

    # Selecting the input text in the search bar
    time.sleep(5)
    search_bar = driver.find_element_by_class_name("PopupSearch")
    input_text = search_bar.find_element(By.XPATH, "//input[@type='text']")
      
    # Searching by court name
    time.sleep(5)
    input_text.send_keys(court)
    input_text.send_keys(Keys.ENTER)
    sys.stderr.write("Court selected.\n")
    
    if court == "TJMS":
        time.sleep(5)
        search_icon = driver.find_element(By.XPATH, "//html/body/div[5]/div/div[4]/div[2]/div/div[1]/div[1]")
        search_icon.click()

def select_year(year, driver):
    # Opening the search bar - Ano
    time.sleep(10)
    select_year = driver.find_element(By.XPATH, "//*[@title='Ano']")       
    search_icon = select_year.find_element(By.XPATH, "//html/body/div[5]/div/div[13]/div[1]/div[1]")
    search_icon.click()
        
    ## Selecting the input text in the search bar
    time.sleep(5)
    search_bar = driver.find_element_by_class_name("PopupSearch")
    input_year = search_bar.find_element(By.XPATH, "//input[@type='text']")

     ## Searching by year
    time.sleep(5)
    input_year.send_keys(year)
    input_year.send_keys(Keys.ENTER)
    sys.stderr.write("Year selected.\n")

def select_month(month, driver):   
    # Opening the search bar - Month
    time.sleep(10)
    select_month = driver.find_element(By.XPATH, "//*[@title='Mês Referencia']")       
    search_icon = select_month.find_element(By.XPATH, "//html/body/div[5]/div/div[16]/div[1]/div[1]")
    search_icon.click()
    
    ## Selecting the input text in the search bar
    time.sleep(5)
    search_bar = driver.find_element_by_class_name("PopupSearch")
    input_month = search_bar.find_element(By.XPATH, "//input[@type='text']")

     ## Searching by month
    time.sleep(5)
    input_month.send_keys(month)
    input_month.send_keys(Keys.ENTER)
    sys.stderr.write("Month selected.\n")

def download(court, year, month, payroll, output_path, driver): 
    driver.get(base_URL) 
    
    # Selecting the payroll
    time.sleep(5)
    x_path = "//div[@class='" + payroll[0] + "'][@id='"+ payroll[1] + "']"
    current_payroll = driver.find_element(By.XPATH, x_path)
    current_payroll.click()
    sys.stderr.write("Payroll selected: {}.\n".format(payroll[2]))
    
    # Donwloading the file
    time.sleep(5)
    download = driver.find_element(By.XPATH, "//*[@title='Enviar para Excel']")
    download.click()
    time.sleep(60)
    sys.stderr.write("File downloaded.\n")

    # Formating the filename
    file_name = format_filename(output_path, payroll[2], court)

    return file_name

def setup_driver(driver_path, output_path):
    # Seting the directorys to be used by selenium
    current_directory = os.getcwd()
    path_chrome = current_directory + driver_path
    path_prefs = output_path

    # Attributing the paths to the webdriver
    prefs = {"download.default_directory" : path_prefs}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-setuid-sandbox")
    return webdriver.Chrome(executable_path = path_chrome, chrome_options = chrome_options)

def format_filename(output_path, payroll_name, court):
    # Identifying the name of the last downloaded file
    filename = max([os.path.join(output_path, f) for f in os.listdir(output_path)], key=os.path.getctime)

    # renaming the file properly, according to the payroll
    new_filename = court + "-" + payroll_name.lower().replace(" ","-") + ".xlsx"
    shutil.move(filename,os.path.join(output_path,r"{}".format(new_filename)))
    new_output_path = output_path + "/" + new_filename

    return new_output_path
