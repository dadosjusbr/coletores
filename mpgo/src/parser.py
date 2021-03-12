import pandas as pd
import sys
import os 

def read(path):
    try:
        data = pd.read_csv(path)
        return data
    except Exception as excep:
        sys.stderr.write("'Não foi possível ler o arquivo: " +
                         path + '. O seguinte erro foi gerado: ' + excep)
        os._exit(1)

def employees_parser(file_path):
    data =  read(file_path)
    #Removendo rows NaN
    data = data[data['Ano'].notna()]

    #Parsing Data
    rows = data.to_numpy()
    employees = {}

    for row in rows:
        reg = row[2] #Matricula
        name = row[3] #Nome
        role = row[4] #Cargo
        workplace = row[5] #Lotação
        remuneration = row[6] #Remuneração do cargo efetivo
        other_verbs = row[7] #Outras Verbas Remuneratórias
        trust_pos = row[8] #Função de Confiança ou Cargo em Comissão
        christmas_bonus = row[9] #Gratificação Natalina
        terco_ferias = row[10] #Férias (1/3 constitucional)
        abono_permanencia = row[11] #Abono de Permanência
        temp_remu = row[12] #Outras Remunerações Temporárias
        idemnity = row[13] #Verbas Indenizatórias
        total = row[14] #Rendimento Bruto
        prev_contrib = row[15] #Contribuição Previdenciária
        imposto_renda = row[16] #Imposto de Renda
        ceil_ret = row[17] #Retenção por Teto Constitucional

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

def employees_indemnity(file_path, employees):
    data = read(file_path)
    
    #Parsing Data
    rows = data.to_numpy()
    for row in rows:

        reg = int(row[0]) #Matrícula
        aux_ali = row[4] #Auxílio alimentação
        pre_school = row[5] #Auxílio creche
        verba_reci =  row[6] #Verbas Rescisórias
        licenca = row[7] #Licença-Prêmio
        abono_pecu = row[8] #Abono Pecuniário
        other_verbs = row[9] #Outras Verbas Indenizatórias
        add_insa = row[10] #Adicional de Insalubridade/Periculosidade
        gratification = row[11] #Gratificação Exercício Cumulativo
        esp_grati =  row[12] #Gratificação Exercício Natureza Especial
        sub = row[13] #Substituição
        other_remu = row[14] #Outras Remunerações Temporárias
        
        # Há funcionários nao listados na planilha de pagamento, porém listados na planilha de indenizações
        try:
            emp = employees[reg]
            exists = True
        except:
            exists = False

        if exists :    
            
            emp['income']['perks'].update({
                'total': round( aux_ali  + pre_school, 2),
                'food': aux_ali,
                'pre_school': pre_school,
            })
            emp['income']['other']['others'].update({
                'Verbas Rescisórias': verba_reci,
                'Licença-Prêmio': licenca,
                'Abono Pecuniário': abono_pecu,
                'Outras Verbas Indenizatórias': other_verbs,
                'Adicional de Insalubridade/Periculosidade': add_insa,
                'Gratificação Exercício Cumulativo': gratification,
                'Gratificação Exercício Natureza Especial': esp_grati,
                "Substituição": sub,
                'Outras Remunerações Temporárias': other_remu,
            })
            emp['income']['other'].update({
                'others_total': round(emp['income']['other']['others_total'] + verba_reci + licenca + abono_pecu + other_verbs
                + add_insa + gratification + esp_grati + sub + other_remu , 2)
            })
    
    return employees

def parse(files):
    employees = {}

    for file_name in files:
        if 'vi' not in file_name:
            employees.update(employees_parser(file_name))
        else:
            employees.update(employees_indemnity(file_name, employees))

    return list(employees.values()) 