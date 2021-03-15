import pandas as pd 
import sys
import os

def clean_currency_val(value):
    if isinstance(value, str):
        return float(value.replace('.', '').replace(',', '.').replace(' ', '').replace('"','').replace("'",''))
    return float(value)

def clean_currency(data, beg_col, end_col):
    for col in data.columns[beg_col:end_col]:
        data[col] = data[col].apply(clean_currency_val)

def read(path):
    try:
        data = pd.read_excel(path, engine='odf')
        #Remove linhas de valor NAN
        data = data[data['Unnamed: 0'].notna()]
        return data
    except Exception as excep:
        sys.stderr.write("'Não foi possível ler o arquivo: " +
                         path + '. O seguinte erro foi gerado: ' + excep)
        os._exit(1)
        
def employees_parser(file_path):
    data =  read(file_path)
    data = data[data['Unnamed: 17'].notna()]
    data = data[:-1]
    data = data.drop(data.index[0])
    clean_currency(data, 4,17)
    
    #Parsing data
    rows = data.to_numpy()
    employees = {} 
    
    for row in rows:
        # A unica identificação disponível é por meio do nome 
        reg = row[0] # Identificação do membro (Nome)
        role = row[1] #Cargo
        workplace = row[2] #Lotação
        remuneration = row[4] #Remuneração do Cargo Efetivo
        other_verbs = row[5] #Outras Verbas Remuneratórias Legais/Judiciais
        trust_pos = row[6]  #Função de Confiança ou Cargo em Comissão 
        decimo = row[7] #13o. Salário 
        ferias = row[8] #Adicional de Férias
        abono_permanencia = row[9] #Abono de Permanência
        temp_remu = row[10] #Outras Remunerações Temporárias
        idemnity = row[11] #Verbas Indenizatórias
        total = row[12] #Total de rendimentos brutos 
        prev_contrib = row[13] #Contribuição Previdenciária
        imposto_renda = row[14] #Imposto de Renda
        ceil_ret = row[15] #Retenção do Teto       
        
        employees[reg] = {
                'reg': reg,
                'name': row[0],
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
                        'total': trust_pos + decimo + ferias + abono_permanencia + temp_remu,
                        'trust_position': trust_pos,
                        'eventual_benefits': temp_remu,
                        'others_total': decimo + ferias + abono_permanencia,
                        'others': {
                            '13o. Salário': decimo,
                            'Adicional de Férias': ferias,
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

def employees_indemnity(file_path, employees):
    data = read(file_path)
    #Ajustando o dataframe para facilitar a interação
    data = data[data['Unnamed: 13'].notna()]
    data = data[:-1]
    data = data.drop(data.index[0])
    clean_currency(data, 4,13)
    
    rows = data.to_numpy()
    for row in rows:

        reg = row[0] # O membro é identificado apenas pelo nome
        aux_ali = row[4] # Auxílio alimentação
        aux_saude = row[5]  #Auxílio saúde
        pre_school = row[6] #Auxílio Pré Escolar
        aux_curso =  row[7] #Auxílio Cursos
        aux_moradia = row[8] #Auxílio Moradia
        add_noturno =  row[9] #Adicional Noturno
        extra_serv =  row[10] #Serviço Extraor.
        sub_func = row[11] #Substituição de Função
        cumula = row[12] #Cumulações
        
        # Há funcionários nao listados na planilha de pagamento, porém listados na planilha de indenizações
        try:
            emp = employees[reg]
            exists = True
        except:
            exists = False

        if exists :    
            emp['income']['perks'].update({
                'total': round( aux_ali + aux_saude + pre_school + aux_moradia, 2),
                'food': aux_ali ,
                'health': aux_saude,
                'pre_school': pre_school,
                'housing_aid': aux_moradia,
            })
            emp['income']['other']['others'].update({
                'Adicional Noturno': add_noturno,
                'Cursos': aux_curso,
                'Serviço Extraor': extra_serv,
                'Substituição de Função': sub_func,
                'Cumulações': cumula
            })
            emp['income']['other'].update({
                'others_total': round( emp['income']['other']['others_total'] + extra_serv + sub_func + cumula + aux_curso + add_noturno, 2),
            })
            employees[reg] = emp

    return employees

def employee_parser_2019(file_path):
    data =  read(file_path)
    data = data[data['Unnamed: 16'].notna()]
    data = data[:-1]
    data = data.drop(data.index[0])
    clean_currency(data, 4,16)
    
    #Parsing data
    rows = data.to_numpy()
    employees = {} 
    
    for row in rows:
        # A unica identificação disponível é por meio do nome 
        reg = row[0] # Identificação do membro (Nome)
        role = row[1] #Cargo
        workplace = row[2] #Lotação
        remuneration = row[4] #Remuneração do Cargo Efetivo
        other_verbs = row[5] #Outras Verbas Remuneratórias Legais/Judiciais
        trust_pos = row[6]  #Função de Confiança ou Cargo em Comissão 
        decimo = row[7] #13o. Salário 
        ferias = row[8] #Adicional de Férias
        abono_permanencia = row[9] #Abono de Permanência
        temp_remu = row[10] #Outras Remunerações Temporárias
        total = row[11] #Total de rendimentos brutos 
        prev_contrib = row[12] #Contribuição Previdenciária
        imposto_renda = row[13] #Imposto de Renda
        ceil_ret = row[14] #Retenção do Teto       
        
        employees[reg] = {
                'reg': reg,
                'name': row[0],
                'role': role,
                'type': 'membro',
                'workplace': workplace,
                'active': True,
                "income":
                {
                    'total': total,
                    'wage': remuneration + other_verbs,
                    # Em 2019 nenhuma coluna express o total de perks, este é calculado nas indenizações
                    'perks':{
                    },
                    'other':
                    { 
                        'total': trust_pos + decimo + ferias + abono_permanencia + temp_remu,
                        'trust_position': trust_pos,
                        'eventual_benefits': temp_remu,
                        'others_total': decimo + ferias + abono_permanencia,
                        'others': {
                            '13o. Salário': decimo,
                            'Adicional de Férias': ferias,
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
            if ('2019' in file_name) or ('2018' in file_name):
                employees.update(employee_parser_2019(file_name))
            else:
                employees.update(employees_parser(file_name))
        else: 
             employees.update(employees_indemnity(file_name, employees))
      
    return list(employees.values())  