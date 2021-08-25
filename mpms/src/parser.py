import table
import parser_remuneration
import parser_indemnization

def parse(filenames, year, month):
    df = table.read_ods(filenames[0])

    if(int(year) == 2018 or (int(year) == 2019 and int(month)<=6)):
        ods_remuneration = parser_remuneration.parser(df, True)
        return list(ods_remuneration.values())

    ods_remuneration = parser_remuneration.parser(df)

    if(int(year) != 2018 and (int(year) == 2019 and int(month)>=7)):
        df = table.read_ods(filenames[1])
        ods_remuneration = parser_indemnization.update(ods_remuneration, df)

    return list(ods_remuneration.values())