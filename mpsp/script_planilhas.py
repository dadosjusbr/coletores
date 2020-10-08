import pandas
import csv
import requests
import os
from dotenv import load_dotenv
from link_generator import download
from pandas_ods_reader import read_ods

load_dotenv()

# Inputs para mês e ano
mes = os.getenv("MONTH")
ano = os.getenv("YEAR")

# Chama função para definir os links das planilhas
download(mes, ano)