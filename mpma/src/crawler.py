import pathlib
import os
from time import sleep
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

class Crawler:
    BASE_URL = 'https://folha.mpma.mp.br/transparencia/membrosativos/'
    REMUNERACAO = 'remuneracao'
    VERBAS_INDENIZATORIAS = 'verbas-indenizatorias'

    def __init__(self, month, year, driver_path, output_path):
        self.month = month
        self.year = year
        self.driver_path = driver_path
        self.output_path = output_path

    def crawl(self):
        pathlib.Path(self.output_path).mkdir(exist_ok=True)
        driver = self.setup_driver(self.driver_path, self.output_path)
        # Faz duas chamadas uma para pegar a remuneração e outra para pegar as verbas indenizatorias
        # Carrega a pagina de remuneração
        driver.get(self.BASE_URL)
        sleep(5)
        self.select_month_and_year(self.month, self.year, driver)
        file_path = self.download(self.month, self.year, self.output_path, driver)

        driver.quit()
        return file_path


    def select_month_and_year(self, month, year, driver):
        # Seleciona o ano
        current_year = driver.find_element(By.XPATH, '//*[@id="selAno"]')
        # Esse Select server para pegar as tags select, onde posso passar o valor diretamente,
        # para pegar qual opção o usuario quer.
        select_year = Select(current_year)
        select_year.select_by_value(year)
        sleep(5)

        current_month = driver.find_element(By.XPATH, '//*[@id="selMes"]')
        select_month = Select(current_month)
        select_month.select_by_value(month)
        sleep(2)

        button_enviar = driver.find_element(By.XPATH, '//*[@id="btOk"]')
        button_enviar.click()
        sleep(25)


    def download(self, month, year, output_path, driver):
        files = []
        # Baixa e dar um nome para as remunerações
        select_div_remuneration = driver.find_element(By.XPATH, '//*[@id="topo"]/p/a')
        select_div_remuneration.click()
        sleep(5)
        name_file_remuneration = self.format_filename(month, year, output_path, self.REMUNERACAO)
        files.append(name_file_remuneration)

        # Baixa e dar um nome para as verbas indenizatórias
        select_div_indemnization = driver.find_element(By.XPATH, '//*[@id="divremuneracoestemporarias"]/p/a')
        select_div_indemnization.click()
        sleep(5)
        name_file_indemnization = self.format_filename(month, year, output_path, self.VERBAS_INDENIZATORIAS)
        files.append(name_file_indemnization)

        return files

    # Faz a configuração do driver do navegador google chrome
    def setup_driver(self, driver_path, output_path):
        # Seting the directorys to be used by selenium
        current_directory = os.getcwd()
        path_chrome = current_directory + driver_path
        # Attributing the paths to the webdriver
        prefs = {"download.default_directory": output_path}
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-setuid-sandbox')
        chrome_options.add_experimental_option("prefs", prefs)
        return webdriver.Chrome(executable_path=path_chrome, chrome_options=chrome_options)


    def format_filename(self, month, year, output_path, flag):
        # Identifying the name of the last downloaded file
        filename = max([os.path.join(output_path, f) for f in os.listdir(output_path)], key=os.path.getctime)
        new_filename = ''

        # renaming the file properly, according to the month
        if(flag == self.REMUNERACAO):
            new_filename = month + "-" + year + "-" + flag +"-membros-ativos" + ".xls"
        elif(flag == self.VERBAS_INDENIZATORIAS):
            new_filename = month + "-" + year + "-" + flag + "-membros-ativos" + ".xls"

        shutil.move(filename,os.path.join(output_path,r"{}".format(new_filename)))
        new_output_path = output_path + "/" + new_filename
        return new_output_path 