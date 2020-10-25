#_*_ coding: utf-8 _*_
import pandas
from pandas_ods_reader import read_ods
from dotenv import load_dotenv
import csv
import os


load_dotenv()
arquivo = os.getenv("EXAMPLE")

def parsear(arquivo): 
    with open(arquivo, encoding='utf8', errors='ignore') as file:
        read = csv.reader(file)
        for line in read:
            print(line)

parsear(arquivo)