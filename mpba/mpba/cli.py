import argparse
import os
from pprint import pprint
import json
from mpba.crawler import crawl, save
from mpba.parser import build_crawler_result, parse
import datetime
import sys

if('MONTH' in os.environ):
    month = os.environ['MONTH']
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

if((int(month) < 1) | (int(month) > 12)):
    sys.stderr.write("Invalid month {}: InvalidParameters.\n".format(month))
    os._exit(1)
if((int(year) == current_year) & (int(month) > current_month)):
    sys.stderr.write("Invalid month {}: InvalidParameters.\n".format(month))
    os._exit(1)
if(int(year) > current_year):
    sys.stderr.write("Invalid year {}: InvalidParameters.\n".format(year))
    os._exit(1)

def main():

    payload = crawl(month, year)
    filename = f"mpba-{month}-{year}.json"
    filepath = save(filename, payload, output_path)

    employees = parse(filepath)
    crawler_result = build_crawler_result(month, year, employees, [filepath])
    print(json.dumps({'cr': crawler_result}, ensure_ascii=False))


if __name__ == "__main__":
    main()
