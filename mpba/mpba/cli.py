import argparse
from pprint import pprint

from mpba.crawler import crawl
from mpba.parser import build_crawler_result, parse


def main():
    parser = argparse.ArgumentParser(prog="mpba")
    parser.add_argument("--mes", dest="month", required=True, type=int)
    parser.add_argument("--ano", dest="year", required=True, type=int)

    args = parser.parse_args()
    payload = crawl(args.month, args.year)
    employees = parse(payload)
    crawler_result = build_crawler_result(args.month, args.year, employees)
    pprint(crawler_result)


if __name__ == "__main__":
    main()
