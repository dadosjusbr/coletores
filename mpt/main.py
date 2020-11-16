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
        print("Invalid month: {}".format(month))
        sys.exit(0)
    if((int(year) == current_year) & (int(month) > current_month)):
        print("Invalid month: {}".format(month))
        sys.exit(0)
    if(int(year) > current_year):
        print("Invalid year: {}".format(year))
        sys.exit(0)
    
    output_path = "./output"
    files  =  crawler.crawl(output_path, month, year)

main()




