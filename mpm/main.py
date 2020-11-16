import sys
import crawler

# Main execution
def main():
    month = sys.argv[1]
    year = sys.argv[2]
    file_names  =  crawler.crawl(year,month)

main()

