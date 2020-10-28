#_*_ coding: utf-8 _*_
import pandas
from pandas_ods_reader import read_ods
from dotenv import load_dotenv
import csv
import os


load_dotenv()
arquivo = os.getenv("EXAMPLE")

def parsear(arquivo): 
    read = read_ods(arquivo, 1)
    print(read)

parsear(arquivo)