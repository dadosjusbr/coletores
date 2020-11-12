from pathlib import Path 
from dotenv import load_dotenv, find_dotenv

import os
import crawler

# Get env args
def get_args():

    try:
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path)
    except IOError:
        print("No .env file to load")

    try:
        month = os.getenv("MONTH")
    except BaseException as e:
        print("Invalid month: {}" .format(e))
        raise e 

    try:
        year = os.getenv("YEAR")
    except BaseException as e:
        print("Invalid month: {}" .format(e))
        raise e 

    outputPath = os.getenv("OUTPUT_FOLDER")

    return {
        "month": month,
        "year": year,
        "outputPath": outputPath
    }

# Main execution
def main(args):
    file_names  =  crawler.crawl(args["outputPath"],args["year"],args["month"])
  
args = get_args()
main(args)

