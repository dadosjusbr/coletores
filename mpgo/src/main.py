from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import sys
import os
import datetime
import crawler
import json
import parser

if('MONTH' in os.environ):
    month = os.environ['MONTH']
else:
    sys.stderr.write("Invalid arguments, missing environment variable: 'MONTH'.\n")
    os._exit(1)
if('YEAR' in os.environ):
    year = os.environ['YEAR']
else:
    sys.stderr.write("Invalid arguments, missing environment variable: 'YEAR'.\n")
    os._exit(1)
if('OUTPUT_FOLDER' in os.environ):
    output_path = os.environ['OUTPUT_FOLDER']
else:
    output_path = "./output"
if('GIT_COMMIT' in os.environ):
    crawler_version = os.environ['GIT_COMMIT']
else:
    sys.stderr.write("Invalid arguments, missing environment variable: 'GIT_COMMIT'.\n")
    os._exit(1)

now = datetime.datetime.now()
current_year = now.year
current_month = now.month

if((int(month) < 1) | (int(month) > 12)):
    sys.stderr.write("Invalid month {}: InvalidParameters.\n".format(month))
    os._exit(1)
if((int(year) == current_year) & (int(month) > current_month)):
    sys.stderr.write("As master Yoda would say: 'one must not crawl/parse the future {}/{}'.\n".format(month, year))
    os._exit(1)
if(int(year) > current_year):
    sys.stderr.write("As master Yoda would say: 'one must not crawl/parse the future {}/{}'.\n".format(month, year))
    os._exit(1)

# Main execution
def main():
    file_names = crawler.crawl(year, month, output_path)
    employees = parser.parse(file_names)
    cr = {
        'aid': 'mpgo',
        'month': int(month),
        'year': int(year),
        'files': file_names,
        'crawler': {
            'id': 'mpgo',
            'version': crawler_version,
        },
        'employees': employees,
        # https://hackernoon.com/today-i-learned-dealing-with-json-datetime-when-unmarshal-in-golang-4b281444fb67
        'timestamp': now.astimezone().replace(microsecond=0).isoformat(),
    }
    print(json.dumps({'cr': cr}, ensure_ascii=False))


if __name__ == '__main__':
    main()
