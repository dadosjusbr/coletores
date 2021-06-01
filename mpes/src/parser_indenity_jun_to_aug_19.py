import parser

def employees_idemnity(file_path, employees):
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