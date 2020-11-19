import os
import sys
import datetime

import crawler

try:
    month = os.environ['MONTH']
    year = os.environ['YEAR']
    path_driver = os.environ['DRIVER']
except KeyError:
    sys.stderr.write("Invalid arguments, missing parameters.\n")
    os._exit(1)
try:
    output_path = os.environ['OUTPUT_PATH']
except KeyError:
    output_path = "/output"

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

files = crawler.crawl(output_path, path_driver, month, year)
