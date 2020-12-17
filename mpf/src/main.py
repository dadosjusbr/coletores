from dotenv import load_dotenv, find_dotenv
import os
import pathlib 
from pathlib import Path 
import crawler
import parser

#Pegando argumentos da variável ambiente
def get_args():
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)

    month = os.getenv("MONTH")
    month = get_month_name(int(month))
    year = os.getenv("YEAR")
    outputPath = os.getenv("OUTPUT_FOLDER")
    crawl_version = os.getenv('GIT_COMMIT')

    return {
        "month": month,
        "year": year,
        "outputPath": outputPath,
        'version':crawl_version
    }

#Metodo auxiliar responsável pela tradução do numero do mês em String
def get_month_name(month):
    months = { 1:'Janeiro' ,
               2:'Fevereiro' ,
               3:'Março',
               4:'Abril',
               5:'Maio',
               6:'Junho',
               7:'Julho',
               8:'Agosto',
               9:'Setembro',
              10:'Outubro',
              11:'Novembro',
              12:'Dezembro'
            }
    return months[month]

#Execução principal 
def main(args):
    file_names  =  crawler.get_relevant_data(args["year"],args["month"],args["outputPath"])
    result  =  parser.crawler_result(args['year'],args['month'],args['outputPath'],args['version'],file_names)
    print(result)

args = get_args()
main(args)