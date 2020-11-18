import os
import sys
import datetime
from dotenv import load_dotenv

import crawler

def main():
    now = datetime.datetime.now()
    current_year = now.year
    current_month = now.month
    month = sys.argv[1]
    year = sys.argv[2]
    
    if((int(month) < 1) | (int(month) > 12)):
        print("Invalid month {}: InvalidParameters".format(month))
        os._exit(1)
    if((int(year) == current_year) & (int(month) > current_month)):
        print("Invalid month {}: InvalidParameters".format(month))
        os._exit(1)
    if(int(year) > current_year):
        print("Invalid year {}: InvalidParameters".format(year))
        os._exit(1)
    
    env_path = ".env"
    load_dotenv(dotenv_path = env_path)
    output_path = "." + os.getenv("OUTPUT_FOLDER")
    files  =  crawler.crawl(output_path, month, year)

main()




