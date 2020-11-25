import sys
import crawler, parser

# Main execution
def main():
    month = sys.argv[1]
    year = sys.argv[2]
    file_names  =  crawler.crawl(year,month)
    #result  =  parser.crawler_result(year, month, file_names)
    print(file_names)

main()
