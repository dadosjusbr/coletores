from dotenv import load_dotenv, find_dotenv
import os
import pathlib #pip install pathlib
from pathlib import Path   #pip install -U python-dotenv
import crawler

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
    fileNames  =  crawler.get_relevant_data(args["year"],args["month"],args["outputPath"])
    

args = get_args()
main(args)