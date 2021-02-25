import argparse
import os
from pprint import pprint
import json
from mpba.crawler import crawl, save
from mpba.parser import build_crawler_result, parse


def main():
    parser = argparse.ArgumentParser(prog="mpba")
    parser.add_argument("--mes", dest="month", type=int, default=os.getenv("MONTH"))
    parser.add_argument("--ano", dest="year", type=int, default=os.getenv("YEAR"))
    parser.add_argument("--saida", dest="output_folder", default=os.getenv("OUTPUT_FOLDER"))

    args = parser.parse_args()
    payload = crawl(args.month, args.year)
    filename = f"mpba-{args.month}-{args.year}.json"
    filepath = save(filename, payload, args.output_folder)

    employees = parse(payload)
    crawler_result = build_crawler_result(args.month, args.year, employees, [filepath])
    print(json.dumps({'cr': crawler_result}, ensure_ascii=False))


if __name__ == "__main__":
    main()
