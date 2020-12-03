from dotenv import load_dotenv, find_dotenv
from pathlib import Path 
import sys, os, datetime
import crawler
import parser

def get_args():
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)

    month = os.getenv("MONTH")
    year = os.getenv("YEAR")
    outputPath = str(os.getenv("OUTPUT_FOLDER"))

    # now = datetime.datetime.now()
    # current_year = now.year
    # current_month = now.month

    # if((int(month) < 1) | (int(month) > 12)):
    #     sys.stderr.write("Invalid month {}: InvalidParameters.\n".format(month))
    #     os._exit(1)
    # if((int(year) == current_year) & (int(month) > current_month)):
    #     sys.stderr.write("Invalid month {}: InvalidParameters.\n".format(month))
    #     os._exit(1)
    # if(int(year) > current_year):
    #     sys.stderr.write("Invalid year {}: InvalidParameters.\n".format(year))
    #     os._exit(1)

    return {
        "month": month,
        "year": year,
        "outputPath": outputPath
    }

# Main execution
def main(args):
    file_names  =  crawler.crawl(args["year"],args["month"],args["outputPath"])
    result  =  parser.crawler_result(args["year"],args["month"], file_names)
    print(result)

args = get_args()
main(args)
