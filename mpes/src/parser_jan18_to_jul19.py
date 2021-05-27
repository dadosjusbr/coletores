import parser

def employees_parser(file_path):
    data = parser.read(file_path)
    
    #Ajustando dataframe 
    data = data[data['Unnamed: 0'].notna()]
    data = data.dropna()
    parser.clean_currency(data,4,14)

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
            'wage': round(remuneration + other_verbs, 2),
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

def employees_idemnity(file_path, employees):
    data = parser.read(file_path)

    #Ajustando dataframe para simplificar interação
    data = data[data['Unnamed: 4'].notna()]
    data = data[data['Ministério Público do Estado do Espírito Santo'].notna()]
    parser.clean_currency(data,1,5)

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