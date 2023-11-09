import sys
import os
import crawler
import parser

if('COURT' in os.environ):
    court = os.environ['COURT']
else:
    sys.stderr.write("Invalid arguments, missing parameter: 'COURT'.\n")
    os._exit(1)
if('YEAR' in os.environ):
    year = os.environ['YEAR']
else:
    sys.stderr.write("Invalid arguments, missing parameter: 'YEAR'.\n")
    os._exit(1)
if('DRIVER_PATH' in os.environ):
    driver_path = os.environ['DRIVER_PATH']
else:
    sys.stderr.write("Invalid arguments, missing parameter: 'DRIVER_PATH'.\n")
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

# Main execution
if __name__ == '__main__':
    file_names = crawler.crawl(court, year, driver_path, output_path)
    # file_names = ['./output/MPSC-1_2018-Membros Ativos.xlsx', './output/MPSC-2_2018-Membros Ativos.xlsx', './output/MPSC-3_2018-Membros Ativos.xlsx', './output/MPSC-4_2018-Membros Ativos.xlsx', './output/MPSC-5_2018-Membros Ativos.xlsx', './output/MPSC-6_2018-Membros Ativos.xlsx', './output/MPSC-7_2018-Membros Ativos.xlsx', './output/MPSC-8_2018-Membros Ativos.xlsx', './output/MPSC-9_2018-Membros Ativos.xlsx', './output/MPSC-10_2018-Membros Ativos.xlsx', './output/MPSC-11_2018-Membros Ativos.xlsx', './output/MPSC-12_2018-Membros Ativos.xlsx', './output/MPSC-1_2018-Verbas Indenizatórias.xlsx', './output/MPSC-2_2018-Verbas Indenizatórias.xlsx', './output/MPSC-3_2018-Verbas Indenizatórias.xlsx', './output/MPSC-4_2018-Verbas Indenizatórias.xlsx', './output/MPSC-5_2018-Verbas Indenizatórias.xlsx', './output/MPSC-6_2018-Verbas Indenizatórias.xlsx', './output/MPSC-7_2018-Verbas Indenizatórias.xlsx', './output/MPSC-8_2018-Verbas Indenizatórias.xlsx', './output/MPSC-9_2018-Verbas Indenizatórias.xlsx', './output/MPSC-10_2018-Verbas Indenizatórias.xlsx', './output/MPSC-11_2018-Verbas Indenizatórias.xlsx', './output/MPSC-12_2018-Verbas Indenizatórias.xlsx']
    files = parser.parse(court, year, file_names, output_path, crawler_version)
    print(files)