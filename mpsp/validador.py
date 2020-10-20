# Tem como única função validar dados passados pelo usuário

def valida_data(mes, ano):
    meses = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    anos = ['2018', '2019', '2020']
    if mes not in meses:
        return "Mês inválido. Por favor, digite um mês entre Janeiro (01) e Dezembro (12)"
    elif ano not in anos:
        return "Ano inválido, tente um ano entre 2018 e 2020"