import argparse

from pprint import pprint

from mpba.crawler import crawl


def main():
    parser = argparse.ArgumentParser(description="", prog="mpba")
    parser.add_argument("--mes", dest="month", required=True, type=int, help="")
    parser.add_argument("--ano", dest="year", required=True, type=int, help="")

    args = parser.parse_args()
    pprint(crawl(args.month, args.year))


if __name__ == "__main__":
    main()
