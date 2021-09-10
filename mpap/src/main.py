import sys
import os
import crawler
import json
from parser import parse
import datetime

if('MONTH' in os.environ):
    month = os.environ['MONTH']
    month = month.zfill(2)
else:
    sys.stderr.write("Invalid arguments, missing parameter: 'MONTH'.\n")
    os._exit(1)
if('YEAR' in os.environ):
    year = os.environ['YEAR']
else:
    sys.stderr.write("Invalid arguments, missing parameter: 'YEAR'.\n")
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

now = datetime.datetime.now()
current_year = now.year
current_month = now.month

def main():
    # file_names = crawler.crawl(month, year, driver_path, output_path)
    file_names = ["./output/2020-06-remuneracao-membros-ativos.csv",
    "./output/2020-06-verbas-indenizatorias-membros-ativos.xls"]
    employees = parse(file_names)
    cr = {
        'aid': 'mpro',
        'month': int(month),
        'year': int(year),
        'files': file_names,
        'crawler': {
            'id': 'mpro',
            'version': crawler_version,
        },
        'employees': employees,
        # https://hackernoon.com/today-i-learned-dealing-with-json-datetime-when-unmarshal-in-golang-4b281444fb67
        'timestamp': now.astimezone().replace(microsecond=0).isoformat(),
    }
    with open(f'./src/json/{month}-{year}.json', 'w') as fp:
        json.dump(cr, fp, indent=2, separators=(',', ': '), ensure_ascii=False)
    print(json.dumps({'cr': cr}, ensure_ascii=False))

if __name__ == '__main__':
    main()