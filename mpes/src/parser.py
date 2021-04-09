import sys
import pandas as pd
import os

def read(path):
    try:
        data = pd.read_excel(path, engine='openpyxl')
        return data
    except Exception as excep:
        sys.stderr.write("'Não foi possível ler o arquivo: " + path + '. O seguinte erro foi gerado: ' + excep)
        os._exit(1)

def clean_currency(data, beg_col, end_col):
    for col in data.columns[beg_col:end_col]:
        data[col] = data[col].apply(clean_currency_val)

def clean_currency_val(value):
    return float(value)

def employees_parser(file_path):
    data = read(file_path)

    #Ajustando dataframe para simplificar interação
    data = data[data['Unnamed: 0'].notna()]
    data = data.dropna()
    clean_currency(data,4,14)

    #Parsing data
    rows = data.to_numpy()
    employees = {}

    for row in rows:
        reg = str(row[0]) #Matrícula 
        name = row[1] #Nome
        role = row[2] #Cargo
        workplace = row[3] #Lotação
        remuneration = row[4] #Remuneração do cargo efetivo
        other_verbs =  row[5] #Outras Verbas Remuneratórias, Legais ou Judiciais   
        trust_pos = row[6] #Função de Confiança ou Cargo em Comissão 
        christmas_grati = row[7] #Gratificação Natalina
        terco_ferias = row[8] #Férias (1/3 constitucional)
        abono_permanencia = row[9] #Abono de Permanência
        temp_remu = row[10] #Outras Remunerações Temporárias
        idemnity = row[11] #Verbas Indenizatórias
        total = row[12] #Total de rendimentos brutos 
        prev_contrib = row[13] #Contribuição Previdenciária
        imposto_renda = row[14] #Imposto de Renda
        ceil_ret = row[15] #Retenção do Teto       

        employees[reg] = {
        'reg': reg,
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
                'total': trust_pos + christmas_grati + terco_ferias + abono_permanencia + temp_remu,
                'trust_position': trust_pos,
                'eventual_benefits': temp_remu,
                'others_total': christmas_grati + terco_ferias + abono_permanencia,
                'others': {
                    'Gratificação Natalina': christmas_grati,
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

def employees_idemnity(file_path, employees):
    data = read(file_path)

    #Ajustando dataframe para simplificar interação
    data = data[data['Unnamed: 4'].notna()]
    data = data[data['Ministério Público do Estado do Espírito Santo'].notna()]
    data = data[1:]
    clean_currency(data, 4,7)

    #Parsing Data
    rows = data.to_numpy()
    for row in rows:
        reg = str(row[0]) # Matrícula
        vacation = row[4] #ABONO  FÉR. IND. EX. ANT.
        aux_ali = row[5] #CARTÃO ALIMENTAÇÃO
        aux_saude = row[6] #AUXÍLIO SAÚDE
        plantao = row[7] #Plantao
        
        #Há funcionários não listados na lista de remunerações mas listados na lista de indenizações
        try:
            emp = employees[reg]
            exists = True
        except:
            exists = False

        if exists :    

            emp = employees[reg]

            emp['income']['perks'].update({
                'total': round( aux_ali + aux_saude, 2),
                'food': aux_ali ,
                'health': aux_saude,
            })
            emp['income']['other']['others'].update({
                'ABONO  FÉR. IND. EX. ANT': vacation,
                'Plantão': plantao,
            })
            emp['income']['other'].update({
                'others_total': round( emp['income']['other']['others_total'] + plantao, 2),
            })

            employees[reg] = emp 

    return employees

#Atende o formato de planilhas para meses anteriores á agosto/2019
def employees_parser_befago(file_path):
    data = read(file_path)
    
    #Ajustando dataframe 
    data = data[data['Unnamed: 0'].notna()]
    data = data.dropna()
    clean_currency(data,4,14)

    #Parsing data
    rows = data.to_numpy()
    employees = {}

    #Aqui funcionários não possuem matrículas para identificá-los, isto ocorre apenas pelo nome
    for row in rows:
        reg = str(row[0]) #A unica forma de identificação disponível é o nome do funcionário 
        name = row[0] #Nome
        role = row[1] #Cargo
        workplace = row[2] #Lotação
        remuneration = row[3] #Remuneração do cargo efetivo
        other_verbs =  row[4] #Outras Verbas Remuneratórias, Legais ou Judiciais   
        trust_pos = row[5] #Função de Confiança ou Cargo em Comissão 
        decimo = row[6] #013º VENCIMENTO
        terco_ferias = row[7] #Férias (1/3 constitucional)
        abono_permanencia = row[8] #Abono de Permanência
        total = row[9] #Total de rendimentos brutos 
        prev_contrib = row[10] #Contribuição Previdenciária
        imposto_renda = row[11] #Imposto de Renda
        ceil_ret = row[12] #Retenção do Teto       

        employees[reg] = {
        'reg': reg,
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
            },
            'other':
            { 
                'total': trust_pos,
                'trust_position': trust_pos,
                'others_total': decimo + terco_ferias + abono_permanencia,
                'others': {
                    '13º VENCIMENTO': decimo,
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

def employees_idemnity_befago(file_path, employees):
    data = read(file_path)

    #Ajustando dataframe para simplificar interação
    data = data[data['Unnamed: 4'].notna()]
    data = data[data['Ministério Público do Estado do Espírito Santo'].notna()]
    clean_currency(data,1,5)

    #Parsing data
    rows = data.to_numpy()

    for row in rows:
        reg = str(row[0]) # Matrícula
        verba1 = row[1] #VERBAS INDENIZATÓRIAS 1
        verba2 = row[2] #VERBAS INDENIZATÓRIAS 2
        other1 = row[3] #REMUNERAÇÃO TEMPORÁRIA 1
        other2 = row[4] #REMUNERAÇÃO TEMPORÁRIA 2
        
        #Há funcionários não listados na lista de remunerações mas listados na lista de indenizações
        try:
            emp = employees[reg]
            exists = True
        except:
            exists = False

        if exists :    

            emp = employees[reg]

            emp['income']['perks'].update({
                'total': 0.0,
            })
            emp['income']['other']['others'].update({
                'VERBAS INDENIZATÓRIAS 1': verba1,
                'VERBAS INDENIZATÓRIAS 2': verba2,
                'REMUNERAÇÃO TEMPORÁRIA 1': other1,
                'REMUNERAÇÃO TEMPORÁRIA 2': other2,

            })
            emp['income']['other'].update({
                'others_total': round( emp['income']['other']['others_total'] + verba1 + verba2 + other1 + other2, 2),
            })
            emp['income']['other'].update({
                'total': round(emp['income']['other']['total'] + emp['income']['other']['others_total'], 2)
            })
            emp['income'].update({
                'total': round( emp['income']['perks']['total'] + emp['income']['other']['total'] + emp['income']['wage'], 2),
            })

            employees[reg] = emp 

    return employees
         
def parse(file_names, year, month):
    employees = {} 

    for file_name in file_names:
        if 'vi' not in file_name:
            if(int(year) == 2019 and int(month) >= 8):
                employees.update(employees_parser(file_name))
            elif int(year) > 2019:
                employees.update(employees_parser(file_name))
            else:
                employees.update(employees_parser_befago(file_name))
        else:
            if (int(year) == 2019 and int(month) >= 8):
                employees.update(employees_idemnity(file_name, employees))
            elif int(year) > 2019:
                employees.update(employees_idemnity(file_name, employees))
            else:
                employees.update(employees_idemnity_befago(file_name, employees))
    
    return list(employees.values())