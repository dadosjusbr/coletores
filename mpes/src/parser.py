import sys
import pandas as pd
import os
import parser_jan18_to_jul19
import parser_indenity_jun_to_aug_19
import parser_indenity_nov_dez_2019
import parser_indenity2020

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
    clean_currency(data,4,15)

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
        prev_contrib = row[13] #Contribuição Previdenciária
        imposto_renda = row[14] #Imposto de Renda
        ceil_ret = row[15] #Retenção do Teto       
        total_desconto = prev_contrib + imposto_renda + ceil_ret 
        total_gratificacoes = trust_pos + christmas_grati + terco_ferias + abono_permanencia + temp_remu
        total = total_gratificacoes + idemnity + remuneration + other_verbs

        employees[reg] = {
        'reg': reg,
        'name': name,
        'role': role,
        'type': 'membro',
        'workplace': workplace,
        'active': True,
        "income":
        {
            'total': round(total,2),
            'wage': round(remuneration + other_verbs, 2),
            'perks':{
                'total': idemnity,
            },
            'other':
            { 
                'total': round(total_gratificacoes, 2),
                'trust_position': trust_pos,
                'eventual_benefits': temp_remu,
                'others_total': round(christmas_grati + terco_ferias + abono_permanencia,2),
                'others': {
                    'Gratificação Natalina': christmas_grati,
                    'Férias (1/3 constitucional)': terco_ferias,
                    'Abono de permanência': abono_permanencia,
                }
            },

        },
        'discounts':
        {
            'total': round(total_desconto, 2),
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
        aux_ali = row[4] #CARTÃO ALIMENTAÇÃO
        aux_saude = row[5] #AUXÍLIO SAÚDE
        plantao = row[6] #Plantao
        
        #Há funcionários não listados na lista de remunerações mas listados na lista de indenizações
        try:
            emp = employees[reg]
            exists = True
        except:
            exists = False

        if exists :    

            emp = employees[reg]
            
            emp['income'].update({
                'total': round(emp['income']['total'] + plantao, 2),

            })

            emp['income']['perks'].update({
                'total': round( aux_ali + aux_saude, 2),
                'food': aux_ali ,
                'health': aux_saude,
            })
            emp['income']['other']['others'].update({
                'Plantão': plantao,
            })
            emp['income']['other'].update({
                'total': round( emp['income']['other']['total'] + plantao, 2),
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
            if year == '2018':
                employees.update(parser_jan18_to_jul19.employees_parser(file_name))
            elif(year == "2019" and int(month) < 8):
                employees.update(parser_jan18_to_jul19.employees_parser(file_name))
            elif(year == "2019" and  int(month) >= 8):
                employees.update(employees_parser(file_name))
            elif int(year) > 2019:
                employees.update(employees_parser(file_name))

        else:
            if year == "2018":
                employees.update(parser_jan18_to_jul19.employees_idemnity(file_name, employees))
            elif(year == "2019"):
                if month in ["01", "02", "03", "04", "05", "06", "07"]:
                    employees.update(parser_jan18_to_jul19.employees_idemnity(file_name, employees))
                elif month in ["08", "09", "10"]:
                    employees.update(parser_indenity_jun_to_aug_19.employees_idemnity(file_name, employees))
                elif month  == "11":
                    employees.update(parser_indenity_nov_dez_2019.employees_idemnity_nov19(file_name, employees))
                elif month  == "12":
                    employees.update(parser_indenity_nov_dez_2019.employees_idemnity_dez19(file_name, employees))
            elif year == "2020":
                if month in ["01", "02", "03"]:
                    employees.update(parser_indenity2020.employees_idemnity_jan_to_mar_20(file_name, employees))
                elif month in ["04", "06", "07"]:
                    employees.update(parser_indenity2020.employees_idemnity_abr_jun_jul20(file_name, employees))
                elif month == "08":
                    employees.update(parser_indenity2020.employees_idemnity_aug20(file_name, employees))
                elif month == "10":
                    employees.update(parser_indenity2020.employees_idemnity_oct_20(file_name, employees))
                elif month in ["09", "11"]:
                    employees.update(parser_indenity2020.employees_idemnity_sept_nov_20(file_name, employees))
                elif month == "12":
                    employees.update(parser_indenity2020.employees_idemnity_dec_20(file_name, employees))
    return list(employees.values())