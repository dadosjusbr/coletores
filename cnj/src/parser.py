import pandas as pd
import sys
import os
import datetime
import json

def parse(court, file_names, output_path, crawler_version):
    now = datetime.datetime.now()
    current_month = now.month
    current_year = now.year
    months = list(range(1, 13))
    years = list(range(2018, current_year + 1))
    files = []

    for year in years:
        for month in months:
            if year == current_year and month >= current_month:
                break
            employees = {}
            employees.update(parse_files(court, file_names, month, year))
            file_path = save_file(court, month, year, file_names, output_path, crawler_version, employees)
            files.append(file_path)
    
    return files

def parse_files(court, file_names, month, year):
    employees = {}
    # As outras tabelas precisam de um parser distinto
    for fn in file_names:
        data = filter_by_date(fn, month, year)
        if (court + "-contracheque" in fn):
            employees.update(parse_employees(data))
    return employees

# Retorna o dataframe contendo apenas os dados do mes/ano especificado
def filter_by_date(fn, month, year):
    data = read_data(fn)
    if month < 10:
        parsing_date = "0" + str(month) + "/" + str(year)
    else:
        parsing_date = str(month) + "/" + str(year)
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

def save_file(court, month, year, file_names, output_path, crawler_version, employees):
    now = datetime.datetime.now()
    cr = {
        'aid': court,
        'month': int(month),
        'year': int(year),
        'files': file_names,
        'crawler': {
            'id': 'mprs',
            'version': crawler_version,
        },
        'employees': employees,
        # https://hackernoon.com/today-i-learned-dealing-with-json-datetime-when-unmarshal-in-golang-4b281444fb67
        'timestamp': now.astimezone().replace(microsecond=0).isoformat(),
    }
    final_file_name = court + "-" + str(month) + "-" + str(year) + ".json"
    file_path = "." + output_path + "/" + final_file_name
    with open(file_path, "w") as file:
        file.write(json.dumps({'cr': cr}, ensure_ascii=False))

    return file_path

