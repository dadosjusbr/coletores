import pandas as pd
import sys
import os

def parse(file_names, parsing_date):
    employees = {}

    # As outras tabelas precisam de um parser distinto
    for fn in file_names:
        data = filter_by_date(fn, parsing_date)
        if ('Contracheque' in fn):
            employees.update(parse_employees(data))

    return list(employees.values())

# Retorna o dataframe contendo apenas os dados do mes/ano especificado
def filter_by_date(fn, parsing_date):
    data = read_data(fn)
    filter_df  = data['Mês/Ano Ref.'] == parsing_date
    current_data = data[filter_df]

    return current_data

# Lê os dados baixados pelo crawler
def read_data(path):
    try:
        data = pd.read_excel(path)
    except Exception as excep:
        sys.stderr(
            "Não foi possível fazer a leitura do arquivo: " + path
            + ". O seguinte erro foi gerado:" + str(excep)
        )
        os._exit(1)

    return data

def parse_employees(data):
    rows = data.to_numpy()
    employees = {}

    for row in rows:
        name = row[1]
        subsidio = row[3]
        direitos_pessoais = row[4]
        indenizacoes = row[5] 
        direitos_eventuais = row[6]
        previdencia = row[8]
        imposto_renda = row[9]
        descontos_diversos = row[10]
        retencao_teto = row[11]
        remuneracao_orgao_origem = row[14]
        diarias = row[15]

        total_gratificacoes = direitos_pessoais + direitos_eventuais + diarias
        total_descontos = previdencia + imposto_renda + descontos_diversos + retencao_teto
        total_bruto = (
            subsidio
            + remuneracao_orgao_origem
            + indenizacoes
            + total_gratificacoes
        )

        employees[name] = {
            "name": name,
            "income": {
                "total": round(total_bruto, 2),
                "wage": round(subsidio + remuneracao_orgao_origem, 2),
                "perks": {
                    "total": indenizacoes,
                },
                "other": {  # Gratificações
                    "total": round(total_gratificacoes, 2),
                    "others_total": total_gratificacoes,
                    'others': {
                        'Daily': diarias
                    }
                },
            },
            "discounts": {
                "total": abs(total_descontos),
                "prev_contribution": abs(previdencia),
                "ceil_retention": abs(retencao_teto),
                "income_tax": abs(imposto_renda),
                "Sescontos Diversos": abs(descontos_diversos)
            },
        }
        
    return employees
