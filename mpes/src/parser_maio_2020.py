import parser

# Source: https://stackoverflow.com/a/944712/5822594
def isNaN(string):
    return string != string


def format_value(element):
    if(isNaN(element)):
        return 0.0
    if type(element) == str:
        if("." in element and "," in element):
            element = element.replace(".", "").replace(",", ".")
        elif("," in element):
            element = element.replace(",", ".")

    return float(element)

def employees_parser(file_path):
    data = parser.read(file_path)
    #Ajustando dataframe para simplificar interação
    data = data[data['Unnamed: 0'].notna()]
    del data['Unnamed: 18']
    data = data.dropna() 
    parser.clean_currency(data,4,15)

    #Parsing data
    rows = data.to_numpy()
    employees = {}

    for row in rows:
        reg = str(row[0]) #Matrícula 
        name = row[1] #Nome
        role = row[2] #Cargo
        workplace = row[3] #Lotação
        remuneration = format_value(row[4]) #Remuneração do cargo efetivo
        other_verbs =  format_value(row[5]) #Outras Verbas Remuneratórias, Legais ou Judiciais   
        trust_pos = format_value(row[6]) #Função de Confiança ou Cargo em Comissão 
        christmas_grati = format_value(row[7]) #Gratificação Natalina
        terco_ferias = format_value(row[8]) #Férias (1/3 constitucional)
        abono_permanencia = format_value(row[9]) #Abono de Permanência
        temp_remu = format_value(row[10]) #Outras Remunerações Temporárias
        idemnity = format_value(row[11]) #Verbas Indenizatórias
        prev_contrib = format_value(row[13]) #Contribuição Previdenciária
        imposto_renda = format_value(row[14]) #Imposto de Renda
        ceil_ret = format_value(row[15]) #Retenção do Teto       
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