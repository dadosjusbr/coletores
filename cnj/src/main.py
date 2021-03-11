import sys
import os
import datetime
import crawler
import parser

if('COURT' in os.environ):
    court = os.environ['COURT']
else:
    sys.stderr.write("Invalid arguments, missing parameter: 'COURT'.\n")
    os._exit(1)
if('DRIVER_PATH' in os.environ):
    driver_path = os.environ['DRIVER_PATH']
else:
    sys.stderr.write("Invalid arguments, missing parameter: 'DRIVER_PATH'.\n")
    os._exit(1)
if('OUTPUT_FOLDER' in os.environ):
    output_path = os.environ['OUTPUT_FOLDER']
else:
    output_path = "/output"
if('GIT_COMMIT' in os.environ):
    crawler_version = os.environ['GIT_COMMIT']
else:
    sys.stderr.write("crawler_version cannot be empty")
    os._exit(1)

# Main execution
if __name__ == '__main__':
    file_names = crawler.crawl(court, driver_path, output_path)
    
    now = datetime.datetime.now()
    current_month = now.month
    current_year = now.year
    months = list(range(1, 13))
    years = list(range(2018, current_year + 1))

    for year in years:
        for month in months:
            if year == current_year and month >= current_month:
                break
            if month < 10:
                parsing_date = "0" + str(month) + "/" + str(year)
            else:
                parsing_date = str(month) + "/" + str(year)

            employees = parser.parse(file_names, parsing_date)
            print(employees)