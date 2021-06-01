import parser


def employees_idemnity_jan_to_mar_20(file_path, employees):
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
        ferias_indenizadas = row[4]
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
                'total': round( aux_ali + aux_saude + ferias_indenizadas, 2),
                'vocation': ferias_indenizadas,
                'food': aux_ali ,
                'health': aux_saude,
            })
            emp['income']['other']['others'].update({
                'Plantão': plantao,
            })
            emp['income']['other'].update({
                'others_total': round( emp['income']['other']['others_total'] + plantao, 2),
            })

            employees[reg] = emp 

    return employees

def employees_idemnity_abr_jun_jul20(file_path, employees):
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

            emp['income']['perks'].update({
                'total': round( aux_ali + aux_saude, 2),
                'food': aux_ali ,
                'health': aux_saude,
            })
            emp['income']['other']['others'].update({
                'Plantão': plantao,
            })
            emp['income']['other'].update({
                'others_total': round( emp['income']['other']['others_total'] + plantao, 2),
            })

            employees[reg] = emp 

    return employees

def employees_idemnity_aug20(file_path, employees):
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
                'total': round( aux_ali + aux_saude + ferias_indenizadas, 2),
                'vacation': ferias_indenizadas,
                'food': aux_ali ,
                'health': aux_saude,
            })
            emp['income']['other']['others'].update({
                'Plantão': plantao,
            })
            emp['income']['other'].update({
                'others_total': round( emp['income']['other']['others_total'] + plantao, 2),
            })

            employees[reg] = emp 

    return employees

def employees_idemnity_sept_nov_20(file_path, employees):
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

            emp['income']['perks'].update({
                'total': round( aux_ali + aux_saude + ferias_indenizadas + ferias_premio, 2),
                'vacation': round(ferias_indenizadas + ferias_premio,2),
                'food': aux_ali ,
                'health': aux_saude,
            })
            emp['income']['other']['others'].update({
                'Plantão': plantao,
            })
            emp['income']['other'].update({
                'others_total': round( emp['income']['other']['others_total'] + plantao, 2),
            })

            employees[reg] = emp 

    return employees

def employees_idemnity_oct_20(file_path, employees):
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
        aux_saude = row[8] #AUXÍLIO SAÚDE
        plantao = row[9] #Plantao
        
        #Há funcionários não listados na lista de remunerações mas listados na lista de indenizações
        try:
            emp = employees[reg]
            exists = True
        except:
            exists = False

        if exists :    

            emp = employees[reg]

            emp['income']['perks'].update({
                'total': round( aux_ali + aux_saude + ferias_indenizadas + ferias_premio + abono_ferias, 2),
                'vacation': round(ferias_indenizadas + ferias_premio + abono_ferias,2),
                'food': aux_ali ,
                'health': aux_saude,
            })
            emp['income']['other']['others'].update({
                'Plantão': plantao,
            })
            emp['income']['other'].update({
                'others_total': round( emp['income']['other']['others_total'] + plantao, 2),
            })

            employees[reg] = emp 

    return employees

def employees_idemnity_dec_20(file_path, employees):
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
        
        #Há funcionários não listados na lista de remunerações mas listados na lista de indenizações
        try:
            emp = employees[reg]
            exists = True
        except:
            exists = False

        if exists :    

            emp = employees[reg]

            emp['income']['perks'].update({
                'total': round( aux_ali + aux_saude + ferias_indenizadas + ferias_premio + abono_ferias + ajuda_de_custo, 2),
                'vacation': round(ferias_indenizadas + ferias_premio + abono_ferias,2),
                'food': aux_ali ,
                'health': aux_saude,
                'subsistence': ajuda_de_custo
            })
            emp['income']['other']['others'].update({
                'Plantão': plantao,
            })
            emp['income']['other'].update({
                'others_total': round( emp['income']['other']['others_total'] + plantao, 2),
            })

            employees[reg] = emp 

    return employees

