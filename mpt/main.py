import os
import sys
import datetime
from dotenv import load_dotenv

import crawler

now = datetime.datetime.now()
current_year = now.year
current_month = now.month
month = sys.argv[1]
year = sys.argv[2]

if((int(month) < 1) | (int(month) > 12)):
    sys.stderr.write("Invalid month {}: InvalidParameters.\n".format(month))
    os._exit(1)
if((int(year) == current_year) & (int(month) > current_month)):
    sys.stderr.write("Invalid month {}: InvalidParameters.\n".format(month))
    os._exit(1)
if(int(year) > current_year):
    sys.stderr.write("Invalid year  {}: InvalidParameters.\n".format(year))
    os._exit(1)

output_path = "/output"
files  =  crawler.crawl(output_path, month, year)
