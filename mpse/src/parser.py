import read_table
import parser_remuneration_odt
import parser_remuneration_2018_ods
import parser_indemnisation_ods


def parse(tabela, year, month):
    if int(year) == 2018:
        # Para pegar os documentos em .ods de remuneração todo o ano de 2018
        table_ods_remuneration = read_table.read_ods(tabela[0])
        employees = parser_remuneration_2018_ods.parser(table_ods_remuneration)
        return list(employees.values())
    
    else:
        if int(year) == 2019 and int(month) >= 7 or int(year)>= 2020:
            # Pega todos que tem remuneração e indenização correspondentes 
            # que estão no formatos .odt e .ods
            table_odt_remuneration = read_table.read_odt(tabela[1])
            employees = parser_remuneration_odt.parser(table_odt_remuneration)
            table_ods_indemnisation = read_table.read_ods(tabela[0])

            if int(year) == 2021 and int(month) >= 2:
                employees = parser_indemnisation_ods.update(employees, table_ods_indemnisation, True)
                return list(employees.values())

            else:
                employees = parser_indemnisation_ods.update(employees, table_ods_indemnisation)
                return list(employees.values())

        else:
            # Aqui vai pegar só do mês 1 ao 6 de 2019 que estão em no formato .odt
            table_odt_remuneration = read_table.read_odt(tabela[0])
            employees = parser_remuneration_odt.parser(table_odt_remuneration, no_budge_sheets = True)
            return list(employees.values())
