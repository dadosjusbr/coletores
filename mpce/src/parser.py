import sys
import os
import pandas as pd
def clean_currency_val(value):
    if isinstance(value, str):
        return float(value.replace('R$', '').replace('.', '').replace(',', '.').replace(' ', '').replace('"','').replace("'",''))
    return float(value)

def clean_currency(data, beg_col, end_col):
    for col in data.columns[beg_col:end_col]:
        data[col] = data[col].apply(clean_currency_val)

def read(path):
    try:
        data = pd.read_html(path)
        data = data[0]
        return data

    except Exception as excep:
        sys.stderr.write("'Não foi possível ler o arquivo: " + path + '. O seguinte erro foi gerado: ' + excep)
        os._exit(1)

def employees_parser(file_path):
    data = read(file_path)
    data = data[: -1]
    clean_currency(data, 4, 18)
    
    #Parsing data
    rows = data.to_numpy()
    employees = {}   
    for row in rows:
        
        reg = row[0] #Matrícula
        name = row[1] #Nome
        role = row[2] #Cargo
        workplace = row[3] #Lotação
        remuneration = row[4] #Remuneração do Cargo Efetivo
        other_verbs = row[5] #Outras Verbas Remuneratórias,Legais ou Judiciais	
        trust_pos = row[6] #Função de Confiança ou Cargo em Comissão	
        christmas_bonus = row[7] #Gratificação Natalina	
        terco_ferias = row[8] #Férias(1/3 constitucional)	
        abono_permanencia = row[9] #Abono de Permanência
        temp_remu = row[10] #Outras Remunerações Temporárias
        idemnity = row[11] #Verbas Indenizatórias	
        total = row[12] #Total de Rendimentos Brutos	
        prev_contrib = row[13] #Contribuição Previdenciária
        imposto_renda = row[14] #Imposto de Renda
        ceil_ret = row[15] #Retenção por Teto Constitucional

        employees[reg] = {
            'reg': str(reg),
            'name': name,
            'role': role,
            'type': 'membro',
            'workplace': workplace,
            'active': True,
            "income":
            {
                'total': total,
                'wage': remuneration + other_verbs,
                'perks':{
                    'total': idemnity,
                },
                'other':
                { 
                    'total': trust_pos + christmas_bonus + terco_ferias + abono_permanencia + temp_remu,
                    'trust_position': trust_pos,
                    'eventual_benefits': temp_remu,
                    'others_total': christmas_bonus + terco_ferias + abono_permanencia,
                    'others': {
                        'Gratificação Natalina': christmas_bonus,
                        'Férias (1/3 constitucional)': terco_ferias,
                        'Abono de permanência': abono_permanencia,
                    }
                },

            },
            'discounts':
            {
                'total': round(prev_contrib + ceil_ret + imposto_renda, 2),
                'prev_contribution': prev_contrib,
                'ceil_retention': ceil_ret,
                'income_tax': imposto_renda
            }
    }

    return employees

def parse(files):
    employees = {}

    for file_name in files:
        if 'vi' not in file_name:
            employees.update(employees_parser(file_name))

    return list(employees.values())