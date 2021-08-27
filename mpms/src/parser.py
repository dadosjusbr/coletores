import table
import parser_remuneration
import parser_indemnization

def parse(filenames, year, month):
    table_excel = table.read_xlsx(filenames[0])

    if(int(year) == 2018 or (int(year) == 2019 and int(month)<=6)):
        xlsx_remuneration = parser_remuneration.parser(table_excel, True)
        return list(xlsx_remuneration.values())

    xlsx_remuneration = parser_remuneration.parser(table_excel)

    table_excel = table.read_ods(filenames[1])
    xlsx_remuneration = parser_indemnization.update(xlsx_remuneration, table_excel)

    return list(xlsx_remuneration.values())