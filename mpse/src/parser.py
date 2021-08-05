import read_ods
import table



def parse(tabela):
    df = read_ods.together_array(tabela[1])
    begin_row = table.get_begin_row(df, 'Matrícula')
    end_row = table.get_end_row(df, 'Data da última atualização:')
    curr_row = 0

    for nome in df:
        curr_row +=1
        if curr_row <= begin_row:
            continue

        print(nome[1])

        if curr_row > end_row:
            break
