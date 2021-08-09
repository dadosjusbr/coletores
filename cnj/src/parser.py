import pandas as pd
import sys
import os
import datetime

def read_data(path):
    try:
        data = pd.read_excel(path, engine='openpyxl')
    except Exception as excep:
        sys.stderr(
            "Não foi possível fazer a leitura do arquivo: " + path
            + ". O seguinte erro foi gerado:" + str(excep)
        )
        os._exit(1)

    return data

def parse_employees(fn):
    rows = read_data(fn).to_numpy()
    employees = {}

    for row in rows:
        name = row[1]
        if name != "0":
            subsidio = float(row[3])
            indenizacoes = float(row[5])
            previdencia = float(row[8])
            imposto_renda = float(row[9])
            descontos_diversos = float(row[10])
            retencao_teto = float(row[11])
            remuneracao_orgao_origem = float(row[14])
            diarias = float(row[15])

            total_descontos = previdencia + imposto_renda + descontos_diversos + retencao_teto
            total_bruto = (subsidio + remuneracao_orgao_origem + diarias)

            employees[name] = {
                "reg": "",
                "name": name,
                "role": "",
                "type": "membro",
                "workplace": "",
                "active": True, 
                "income": {
                    "total": round(total_bruto, 2),
                    "wage": round(subsidio + remuneracao_orgao_origem, 2),
                    "perks": {
                        "total": indenizacoes,
                    },
                    "other": {  # Gratificações
                        "total": diarias,
                        "daily": diarias,
                        "others_total": 0.0,
                        "others": {}
                    },
                },
                "discounts": {
                    "total": round(abs(total_descontos), 2),
                    "prev_contribution": abs(previdencia),
                    "ceil_retention": abs(retencao_teto),
                    "income_tax": abs(imposto_renda),
                    "others_total": abs(descontos_diversos),
                    "others": {
                        "Descontos Diversos": abs(descontos_diversos)
                    }
                },
            }
    return employees

def update_employees_indemnities(fn, employees):
    rows = read_data(fn).to_numpy()

    for row in rows:
        name = row[1]
        # Indenizações
        auxilio_alimentacao = round(float(row[3]), 2)
        auxilio_pre_escolar = round(float(row[4]), 2)
        auxilio_saude = round(float(row[5]), 2)
        auxilio_natalidade = round(float(row[6]), 2)
        auxilio_moradia = round(float(row[7]), 2)
        ajuda_de_custo = round(float(row[8]), 2)
        total = round(auxilio_alimentacao + auxilio_pre_escolar + auxilio_saude + auxilio_natalidade + auxilio_moradia + ajuda_de_custo, 2)
        # São dadas algumas colunas nomeadas "Outra" com um valor cuja descrição vem na coluna seguinte.
        # As colunas nomeadas "Detalhe" descrevem a origem do valor da coluna anterior.
        outra_1 = round(float(row[9]), 2)
        detalhe_outra_1 = row[10]
        outra_2 = round(float(row[11]), 2)
        detalhe_outra_2 = row[12]
        outra_3 = round(float(row[13]), 2)
        detalhe_outra_3 = row[14]
        
        # Atualização das indenizações
        if name in employees.keys():
            emp = employees[name]
            emp['income'].update({
                'total': round(emp['income']['total'] + total, 2)
            })
            emp['income']['perks'].update({
                'total': total,
                'food': auxilio_alimentacao,
                'pre_school': auxilio_pre_escolar,
                'health': auxilio_saude,
                'birth_aid': auxilio_natalidade,
                'housing_aid': auxilio_moradia,
                'subsistence': ajuda_de_custo
            })
            # Quando o valor em "Outra" é 0.0, o texto presente em "Detalhe" é sempre '0' ou '-'.
            if str(detalhe_outra_1) != '0' and str(detalhe_outra_1) != '-':
                emp['income']['other']['others'].update({
                    detalhe_outra_1: outra_1
                })
                emp['income']['other'].update({
                    'total': round(emp['income']['other']['total'] + outra_1, 2),
                    'others_total': round(emp['income']['other']['others_total'] + outra_1, 2)       
                })
                emp['income'].update({
                    'total': round(emp['income']['total'] + outra_1, 2)
                })
            if str(detalhe_outra_2) != '0' and str(detalhe_outra_2) != '-':
                emp['income']['other']['others'].update({
                    detalhe_outra_2: outra_2
                })
                emp['income']['other'].update({
                    'total': round(emp['income']['other']['total'] + outra_2, 2),
                    'others_total': round(emp['income']['other']['others_total'] + outra_2, 2)      
                })
                emp['income'].update({
                    'total': round(emp['income']['total'] + outra_2, 2)
                })
            if str(detalhe_outra_3) != '0' and str(detalhe_outra_3) != '-':
                emp['income']['other']['others'].update({
                    detalhe_outra_3: outra_3
                })
                emp['income']['other'].update({
                    'total': round(emp['income']['other']['total'] + outra_3, 2),
                    'others_total': round(emp['income']['other']['others_total'] + outra_3, 2)         
                })
                emp['income'].update({
                    'total': round(emp['income']['total'] + outra_3, 2)
                })

            employees[name] = emp

    return employees
def isNaN(string):
    return string != string

def format_value(element):
    # A value was found with incorrect formatting. (3,045.99 instead of 3045.99)
    if isNaN(element):
        return 0.0
    if type(element) == str:
        if "." in element and "," in element:
            element = element.replace(".", "").replace(",", ".")
        elif "," in element:
            element = element.replace(",", ".")
        elif "-" in element:
            element = 0.0

    return float(element)

def update_employees_eventual_gratifications(fn, employees):
    rows = read_data(fn).to_numpy()

    for row in rows:
        name = row[1]
        # Gratificações
        abono_constitucional = round(float(row[3]), 2)
        indenizacao_ferias = round(float(row[4]), 2)
        antecipacao_ferias = format_value(row[5])          
        gratificacao_natalina = round(float(row[6]), 2)
        antecipacao_grat_natal = round(float(str(row[7]).replace(",", ".")), 2)
        substituicao = round(float(row[8]), 2)
        gratificacao_exercicio_cumulativo = round(float(row[9]), 2)
        gratificacao_encargo = round(float(row[10]), 2)
        pagamentos_retroativos = round(float(row[11]), 2)
        jeton = round(float(row[12]), 2)
        total = abono_constitucional + gratificacao_natalina + antecipacao_grat_natal + substituicao + gratificacao_exercicio_cumulativo + gratificacao_encargo + pagamentos_retroativos + jeton
        # São dadas algumas colunas nomeadas "Outra" com um valor cuja descrição vem na coluna seguinte.
        # As colunas nomeadas "Detalhe" descrevem a origem do valor da coluna anterior.
        outra_1 = round(float(row[13]), 2)
        detalhe_outra_1 = row[14]
        outra_2 = round(float(row[15]), 2)
        detalhe_outra_2 = row[16]
        
        # Atualização das gratificações
        if name in employees.keys():
            emp = employees[name]

            emp['income'].update({
                'total': round(emp['income']['total'] + + indenizacao_ferias + antecipacao_ferias + total, 2)
            })
            emp['income']['perks'].update({
                'total': round(emp['income']['perks']['total'] + indenizacao_ferias + antecipacao_ferias, 2),
                'vacation': round(indenizacao_ferias + antecipacao_ferias, 2)
            })
            emp['income']['other'].update({
                'total':  round(emp['income']['other']['total'] + total, 2),
                'others_total': round(emp['income']['other']['others_total'] + total, 2)
            })
            emp['income']['other']['others'].update({
                'Abono constitucional de 1/3 de férias': abono_constitucional,
                'Gratificação natalina': gratificacao_natalina,
                'Antecipação de gratificação natalina': antecipacao_grat_natal,
                'Substituição': substituicao,
                'Gratificação por exercício cumulativo': gratificacao_exercicio_cumulativo,
                'Gratificação por encargo Curso/Concurso': gratificacao_encargo,
                'Pagamentos retroativos': pagamentos_retroativos,
                'JETON': jeton
            })
            # Quando o valor em "Outra" é 0.0, o texto presente em "Detalhe" é sempre '0' ou '-'.
            if str(detalhe_outra_1) != '0' and str(detalhe_outra_1) != '-':
                emp['income']['other']['others'].update({
                    detalhe_outra_1: outra_1
                })
                emp['income']['other'].update({
                    'total': round(emp['income']['other']['total'] + outra_1, 2),
                    'others_total': round(emp['income']['other']['others_total'] + outra_1, 2)       
                })
                emp['income'].update({
                    'total': round(emp['income']['total'] + outra_1, 2)
                })
            if str(detalhe_outra_2) != '0' and str(detalhe_outra_2) != '-':
                emp['income']['other']['others'].update({
                    detalhe_outra_2: outra_2
                })
                emp['income']['other'].update({
                    'total': round(emp['income']['other']['total'] + outra_2, 2),
                    'others_total': round(emp['income']['other']['others_total'] + outra_2, 2)      
                })
                emp['income'].update({
                    'total': round(emp['income']['total'] + outra_2, 2)
                })

            employees[name] = emp

    return employees

def update_employees_personal_gratifications(fn, employees):
    rows = read_data(fn).to_numpy()
    
    for row in rows:
        name = row[1]
        # Gratificações
        abono_permanencia  = round(float(row[3]), 2)
        # São dadas algumas colunas nomeadas "Outra" com um valor cuja descrição vem na coluna seguinte.
        # As colunas nomeadas "Detalhe" descrevem a origem do valor da coluna anterior.
        outra_1 = round(float(row[4]), 2)
        detalhe_outra_1 = row[5]
        outra_2 = round(float(row[6]), 2)
        detalhe_outra_2 = row[7]
        
        # Atualização das gratificações
        if name in employees.keys():
            emp = employees[name]

            emp['income'].update({
                'total': round(emp['income']['total'] + abono_permanencia, 2)
            })
            emp['income']['other'].update({
                'total':  round(emp['income']['other']['total'] + abono_permanencia, 2),
                'others_total': round(emp['income']['other']['others_total'] + abono_permanencia, 2)
            })
            emp['income']['other']['others'].update({
                'Abono de permanência' : abono_permanencia
            })
            # Quando o valor em "Outra" é 0.0, o texto presente em "Detalhe" é sempre '0' ou '-'.
            if str(detalhe_outra_1) != '0' and str(detalhe_outra_1) != '-':
                emp['income']['other']['others'].update({
                    detalhe_outra_1: outra_1
                })
                emp['income']['other'].update({
                    'total': round(emp['income']['other']['total'] + outra_1, 2),
                    'others_total': round(emp['income']['other']['others_total'] + outra_1, 2)       
                })
                emp['income'].update({
                    'total': round(emp['income']['total'] + outra_1, 2)
                })
            if str(detalhe_outra_2) != '0' and str(detalhe_outra_2) != '-':
                emp['income']['other']['others'].update({
                    detalhe_outra_2: outra_2
                })
                emp['income']['other'].update({
                    'total': round(emp['income']['other']['total'] + outra_2, 2),
                    'others_total': round(emp['income']['other']['others_total'] + outra_2, 2)      
                })
                emp['income'].update({
                'total': round(emp['income']['total'] + outra_2, 2)
                })
            
            employees[name] = emp

    return employees

def parse(file_names):
    employees = {}
    try:
        for fn in file_names:
            if "contracheque" in fn:
                # Puts all parsed employees in the big map
                employees.update(parse_employees(fn))
            elif "indenizações" in  fn:
                update_employees_indemnities(fn, employees)
            elif "direitos-eventuais" in fn:
                update_employees_eventual_gratifications(fn, employees)
            elif "-direitos-pessoais" in fn:
                update_employees_personal_gratifications(fn, employees)

    except KeyError as e:
        sys.stderr.write(
            "Registro inválido ao processar verbas indenizatórias: {}".format(e)
        )
        os._exit(1)

    return list(employees.values())

  