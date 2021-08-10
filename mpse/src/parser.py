import read_table
import parser_remuneration_odt
import parser_remuneration_2018_ods
import parser_indemnisation_ods


def parse(tabela, year, month):
    if int(year) == 2018:
        # Para pegar os documentos em .ods de remuneração todo o ano de 2018
        table_ods_remuneration = read_table.read_ods(tabela[0])
        employees = parser_remuneration_2018_ods.parser(table_ods_remuneration)
        return employees
    
    else:
        if int(year) == 2019 and int(month) >= 7 or int(year)>= 2020:
            # Pega todos que tem remuneração e indenização correspondentes 
            # que estão no formatos .odt e .ods
            table_odt_remuneration = read_table.read_odt(tabela[1])
            employees = parser_remuneration_odt.parser(table_odt_remuneration)
            table_ods_indemnisation = read_table.read_ods(tabela[0])

            if int(year) == 2021 and int(month) >= 2:
                employees = parser_indemnisation_ods.update_fev_em_diante(employees, table_ods_indemnisation)
                return employees

            else:
                employees = parser_indemnisation_ods.update(employees, table_ods_indemnisation)
                return employees

        else:
            # Aqui vai pegar só do mês 1 ao 6 de 2019 que estão em no formato .odt
            table_odt_remuneration = read_table.read_odt(tabela[0])
            employees = parser_remuneration_odt.parser(table_odt_remuneration)
            return employees
