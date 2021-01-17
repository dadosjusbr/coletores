from dotenv import load_dotenv,  find_dotenv
import os
import pathlib 
import datetime
import numpy
from pathlib import Path 
import crawler
import parserA
import parserB
import json

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

#Pegando argumentos da variável ambiente
if('MONTH' in os.environ):
    month = os.environ['MONTH']
    month_name = get_month_name(int(month))
else:
    sys.stderr.write("Invalid arguments, missing parameter: 'MONTH'.\n")
    os._exit(1)
if('YEAR' in os.environ):
    year = os.environ['YEAR']
else:
    sys.stderr.write("Invalid arguments, missing parameter: 'YEAR'.\n")
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
months_b = list(range(7,13))


if((int(month) < 1) | (int(month) > 12)):
    sys.stderr.write("Invalid month {}: InvalidParameters.\n".format(month))
    os._exit(1)
if((int(year) == current_year) & (int(month) > current_month)):
    sys.stderr.write("Invalid month {}: InvalidParameters.\n".format(month))
    os._exit(1)
if(int(year) > current_year):
    sys.stderr.write("Invalid year {}: InvalidParameters.\n".format(year))
    os._exit(1)

# Main execution
# There is two model of parser's, parser A cover months since 07/2019, 
# and parserB cover months before 07/2019.
# parserA is our default parser, because cover the last month with data.
def main():
    file_names  =  crawler.crawl(year, month_name, output_path)
    if(((int(month) not in months_b) and year == '2019') or year =='2018'):
        employees = parserB.parse(file_names, year, month)
    else:
        employees = parserA.parse(file_names)
    cr = {
        'aid': 'mpf',
        'month': int(month),
        'year': int(year),
        'files': file_names,
        'crawler': {
            'id': 'mpf',
            'version': crawler_version,
        },
        'employees': employees,
        # https://hackernoon.com/today-i-learned-dealing-with-json-datetime-when-unmarshal-in-golang-4b281444fb67
        'timestamp': now.astimezone().replace(microsecond=0).isoformat(),
    }
    print(json.dumps({'cr': cr}, ensure_ascii=False))

if __name__ == '__main__':
    main()
