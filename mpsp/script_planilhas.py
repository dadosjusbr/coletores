import pandas
import csv
import requests
from link_generator import download
from pandas_ods_reader import read_ods


# Inputs para mês e ano
mes = input('Digite o mes: ')
ano = input('Digite o ano: ')

# Chama função para definir os links das planilhas
download(mes, ano)