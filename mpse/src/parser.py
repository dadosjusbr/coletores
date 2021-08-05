import pandas as pd

def get_begin_row(data, begin_string):
    begin_row = 0
    for row in data:
        begin_row += 1
        if(row[0] == begin_string):
            break
    return begin_row + 1

def get_end_row(data, end_string):
    end_row = 0

    for row in data:
        end_row +=1
        if row[0] == end_string:
            break
    return end_row - 2
    

def parse(tabela):
    df = pd.read_excel(tabela[0], engine='odf').to_numpy()
    begin_row = get_begin_row(df, 'Matrícula')
    end_row = get_end_row(df, 'TOTAL:')

    curr_row = 0

    for nome in df:

        curr_row +=1
        if curr_row < begin_row:
            continue

        print(nome[0])

        if curr_row > end_row:
            break
        # i += 1
        # if i == 10:
        #     break

