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
    year = os.getenv("YEAR")
    outputPath = os.getenv("OUTPUT_FOLDER")

    return {
        "month": month,
        "year": year,
        "outputPath": outputPath
    }

#Execução principal 
def main(args):
    file_names  =  crawler.get_relevant_data(args["year"],args["month"],args["outputPath"])
    result  =  parser.crawler_result(args['year'],args['month'],args['outputPath'],file_names)
    print(result)

args = get_args()
main(args)