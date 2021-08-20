import pathlib
import os
import sys
import time
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

base_url = 'https://transparencia.mpsc.mp.br/QvAJAXZfc/opendoc.htm?document=Portal%20Transparencia%2FPortal%20Transp%20MPSC.qvw&host=QVS%40qvias&anonymous=true'

def crawl(court, year, driver_path, output_path):
    files = []
    pathlib.Path(output_path).mkdir(exist_ok=True)
    driver = setup_driver(driver_path, output_path)
    driver.get(base_url)
    time.sleep(5)
    contracheque = driver.find_element(By.XPATH, '//*[@id="16"]/div[3]')
    contracheque.click()
    print('CONTRACHEQUE')
    for flag in range(2):   # 0 for Membros Ativos
        select_year_and_document_type(year, driver, flag)
        for month in range(1, 13):
            file_path = download(court, str(month), year, output_path, driver, flag)
            files.append(file_path)
    driver.quit()
    return files

def select_year_and_document_type(year, driver, flag):
    driver.get(base_url)

    time.sleep(5)
    if(flag == 0):
        document_type = driver.find_element(By.XPATH, '//*[@id="56"]/div[3]')
        document_type.click()
        print('MEMBROS ATIVOS')
        # Selecting year
        time.sleep(5)
        if(year == "2018"):
            select_year = driver.find_element(By.XPATH, '/html/body/div[5]/div/div[64]/div[3]/div/div[1]/div[3]')
        elif(year == "2019"):
            select_year = driver.find_element(By.XPATH, '/html/body/div[5]/div/div[64]/div[3]/div/div[1]/div[4]')
        elif(year == "2020"):
            select_year = driver.find_element(By.XPATH, '/html/body/div[5]/div/div[64]/div[3]/div/div[1]/div[5]')
        elif(year == "2021"):
            select_year = driver.find_element(By.XPATH, '/html/body/div[5]/div/div[64]/div[3]/div/div[1]/div[6]')
    else:
        document_type = driver.find_element(By.XPATH, '//*[@id="65"]/div[3]')
        document_type.click()   
        print('VERBAS IDENIZATÓRIAS')  
        # Selecting year
        time.sleep(5)
        if(year == "2018"):
            select_year = driver.find_element(By.XPATH, '//*[@id="53"]/div[3]/div/div[1]/div[3]')
        elif(year == "2019"):
            select_year = driver.find_element(By.XPATH, '//*[@id="53"]/div[3]/div/div[1]/div[4]')
        elif(year == "2020"):
            select_year = driver.find_element(By.XPATH, '//*[@id="53"]/div[3]/div/div[1]/div[5]')
        elif(year == "2021"):
            select_year = driver.find_element(By.XPATH, '//*[@id="53"]/div[3]/div/div[1]/div[6]')

    select_year.click()
    print('ANO ' + str(year))
    
def download(court, month, year, output_path, driver, flag):  
    driver.get(base_url)

    time.sleep(4)
    x_path = '//*[@id="51"]/div[3]/div/div[1]/div[' + month + ']'
    current_month = driver.find_element(By.XPATH, x_path)
    current_month.click()
    print('MÊS ' + str(month))

    # Downloading the file
    time.sleep(2)
    if(flag == 0):
        download = driver.find_element(By.XPATH, '//*[@id="24"]/div[2]/div[1]')
        download.click()
    else:
        download = driver.find_element(By.XPATH, '//*[@id="66"]/div[1]/div[1]')
        download.click()
    sys.stderr.write("File downloaded.\n")

    # Formating the filename
    time.sleep(8)
    file_name = format_filename('.' + output_path, court, month, year, flag)
    time.sleep(2)
    ok_button = driver.find_element(By.XPATH, '/html/body/div[7]/div[2]/button')
    ok_button.click()

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
        new_filename = court + "-" + month + "_" + year + "-Membros Ativos" + ".xlsx"
    else:
        new_filename = court + "-" + month + "_" + year + "-Verbas Indenizatórias" + ".xlsx"

    shutil.move(filename,os.path.join(output_path,r"{}".format(new_filename)))
    new_output_path = output_path + "/" + new_filename

    return new_output_path