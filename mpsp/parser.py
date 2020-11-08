#_*_ coding: utf-8 _*_
import pandas as pd
from pandas_ods_reader import read_ods
from dotenv import load_dotenv
import csv
import os


load_dotenv()
arquivo = os.getenv("EXAMPLE")

# Print dos funcionários
def parser(arquivo): 
    read = read_ods(arquivo, 1)
    print(read)


parser(arquivo)