import argparse
import os
from pprint import pprint

from mpba.crawler import crawl
from mpba.parser import build_crawler_result, parse


def main():
    parser = argparse.ArgumentParser(prog="mpba")
    parser.add_argument("--mes", dest="month", type=int, default=os.getenv("MONTH"))
    parser.add_argument("--ano", dest="year", type=int, default=os.getenv("YEAR"))

    args = parser.parse_args()
    payload = crawl(args.month, args.year)
    employees = parse(payload)
    crawler_result = build_crawler_result(args.month, args.year, employees)
    pprint(crawler_result)


if __name__ == "__main__":
    main()
