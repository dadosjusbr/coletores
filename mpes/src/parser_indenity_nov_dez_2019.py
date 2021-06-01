import parser

# Strange way to check nan. Only I managed to make work
# Source: https://stackoverflow.com/a/944712/5822594
def isNaN(string):
    return string != string

def employees_idemnity_nov19(file_path, employees):
    data = parser.read(file_path)

    #Ajustando dataframe para simplificar interação
    data = data[data['Unnamed: 4'].notna()]
    data = data[data['Ministério Público do Estado do Espírito Santo'].notna()]
    data = data[1:]
    parser.clean_currency(data, 4,7)

    #Parsing Data
    rows = data.to_numpy()
    for row in rows:
        reg = str(row[0]) # Matrícula
        aux_ali = row[4] #CARTÃO ALIMENTAÇÃO
        ferias_indenizadas = row[5]
        ferias_premio = row[6]
        aux_saude = row[7] #AUXÍLIO SAÚDE
        plantao = row[8] #Plantao
        
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
                'total': round( aux_ali + aux_saude + ferias_indenizadas + ferias_premio, 2),
                'vacation': round(ferias_indenizadas + ferias_premio, 2),
                'food': round(aux_ali,2),
                'health': round(aux_saude, 2),
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

def employees_idemnity_dez19(file_path, employees):
    data = parser.read(file_path)

    #Ajustando dataframe para simplificar interação
    data = data[data['Unnamed: 4'].notna()]
    data = data[data['Ministério Público do Estado do Espírito Santo'].notna()]
    data = data[1:]
    parser.clean_currency(data, 4,7)

    #Parsing Data
    rows = data.to_numpy()
    for row in rows:
        reg = str(row[0]) # Matrícula
        aux_ali = row[4] #CARTÃO ALIMENTAÇÃO
        ferias_indenizadas = row[5]
        abono_ferias = row[6]
        ferias_premio = row[7]
        ajuda_de_custo = row[8]
        aux_saude = row[9] #AUXÍLIO SAÚDE
        plantao = row[10] #Plantao
        if isNaN(plantao):
            plantao = 0.0
        
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
                'total': round( aux_ali + aux_saude + ferias_indenizadas + ferias_premio + abono_ferias + ajuda_de_custo, 2),
                'vacation': round(ferias_indenizadas + ferias_premio + abono_ferias, 2),
                'food': round(aux_ali,2),
                'health': round(aux_saude, 2),
                'subsistence': ajuda_de_custo
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