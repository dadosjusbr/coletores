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

# Consulta se a planilha de indenizações está vazia. É necessário saber disso para saber por qual parser a planilha de remuneração vai passar
def isEmpty(file_name):
    data = pd.read_csv(file_name)
    if(len(data)) == 0:
        return True
    else:
        return False
        
# Checa se o valor é NaN
def isNaN(string):
    return string != string

# Parser para quando a tabela de remunerações e indenizações contém informações. Nesse caso, o valor das indenizações e remunerações temporárias é calculado através da soma de todos os beneficios recebidos
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
        if isNaN(workplace):
            workplace = "Não informado"
        remuneration = row[6] #Remuneração do cargo efetivo
        other_verbs = row[7] #Outras Verbas Remuneratórias
        trust_pos = row[8] #Função de Confiança ou Cargo em Comissão
        christmas_bonus = row[9] #Gratificação Natalina
        terco_ferias = row[10] #Férias (1/3 constitucional)
        abono_permanencia = row[11] #Abono de Permanência
        temp_remu = row[12] #Outras Remunerações Temporárias
        idemnity = row[13] #Verbas Indenizatórias
        prev_contrib = row[15] #Contribuição Previdenciária
        imposto_renda = row[16] #Imposto de Renda
        ceil_ret = row[17] #Retenção por Teto Constitucional
        total_descontos = prev_contrib + ceil_ret + imposto_renda
        total_gratificacoes = christmas_bonus + terco_ferias + abono_permanencia + trust_pos
        total = total_gratificacoes + remuneration + other_verbs
        #Evitando adição de colaboradores na planilha de membros
        if role != 'COLABORADOR':

            employees[reg] = {
            'reg': str(reg),
            'name': name,
            'role': role,
            'type': 'membro',
            'workplace': workplace,
            'active': True,
            "income":
            {
                'total': round(total, 2),
                'wage': round(remuneration + other_verbs, 2),
               
                'other':
                { 
                    'total': round(total_gratificacoes, 2),
                    'trust_position': trust_pos,
                    'others_total': round(christmas_bonus + terco_ferias + abono_permanencia, 2),
                    'others': {
                        'Gratificação Natalina': christmas_bonus,
                        'Férias (1/3 constitucional)': terco_ferias,
                        'Abono de permanência': abono_permanencia,
                    }
                },

            },
            'discounts':
            {
                'total': round(total_descontos, 2),
                'prev_contribution': prev_contrib,
                'ceil_retention': ceil_ret,
                'income_tax': imposto_renda
            }
        }
        
    return employees

# Parser para quando a planilha de indenizações está vazia. Neste caso, o valor das indenizações e remunerações temporárias utilizados é o valor que vem na tabela, pois como não há detalhamento dos beneficios não há como fazer a soma.  Então utilizamos o valor que vem pronto na tabela de remunerações
def employees_parser_without_indemnities(file_path):
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
        if isNaN(workplace):
            workplace = "Não informado"
        remuneration = row[6] #Remuneração do cargo efetivo
        other_verbs = row[7] #Outras Verbas Remuneratórias
        trust_pos = row[8] #Função de Confiança ou Cargo em Comissão
        christmas_bonus = row[9] #Gratificação Natalina
        terco_ferias = row[10] #Férias (1/3 constitucional)
        abono_permanencia = row[11] #Abono de Permanência
        temp_remu = row[12] #Outras Remunerações Temporárias
        idemnity = row[13] #Verbas Indenizatórias
        prev_contrib = row[15] #Contribuição Previdenciária
        imposto_renda = row[16] #Imposto de Renda
        ceil_ret = row[17] #Retenção por Teto Constitucional
        total_descontos = prev_contrib + ceil_ret + imposto_renda
        total_gratificacoes = christmas_bonus + terco_ferias + abono_permanencia + temp_remu + trust_pos
        total = total_gratificacoes + idemnity + remuneration + other_verbs
        #Evitando adição de colaboradores na planilha de membros
        if role != 'COLABORADOR':

            employees[reg] = {
            'reg': str(reg),
            'name': name,
            'role': role,
            'type': 'membro',
            'workplace': workplace,
            'active': True,
            "income":
            {
                'total': round(total, 2),
                'wage': round(remuneration + other_verbs, 2),
                'perks':{
                    'total': idemnity,
                },
                'other':
                { 
                    'total': round(total_gratificacoes, 2),
                    'trust_position': trust_pos,
                    'others_total': round(christmas_bonus + terco_ferias + abono_permanencia + temp_remu,2),
                    'others': {
                        'Gratificação Natalina': christmas_bonus,
                        'Férias (1/3 constitucional)': terco_ferias,
                        'Abono de permanência': abono_permanencia,
                        'Outras RemuneraçõesTemporárias': temp_remu,
                    }
                },

            },
            'discounts':
            {
                'total': round(total_descontos, 2),
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
        total_indenizacoes = aux_ali + pre_school + licenca
        total_remu_temp = verba_reci + abono_pecu + other_verbs + add_insa + gratification + esp_grati + sub + other_remu
        
        # Há funcionários nao listados na planilha de pagamento, porém listados na planilha de indenizações
        try:
            emp = employees[reg]
            exists = True
        except:
            exists = False

        if exists :    
            
            emp['income'].update({
                'perks':{
                    'total': round(total_indenizacoes, 2),
                    'food': aux_ali,
                    'pre_school': pre_school,
                    'premium_license_pecuniary':licenca
                },
            })
            emp['income']['other']['others'].update({
                'Verbas Rescisórias': verba_reci,
                'Abono Pecuniário': abono_pecu,
                'Outras Verbas Indenizatórias': other_verbs,
                'Adicional de Insalubridade/Periculosidade': add_insa,
                'Gratificação Exercício Cumulativo': gratification,
                'Gratificação Exercício Natureza Especial': esp_grati,
                "Substituição": sub,
                'Outras Remunerações Temporárias': other_remu,
            })
            emp['income']['other'].update({
                "total": round(emp["income"]["other"]["total"] + total_remu_temp, 2),
                'others_total': round(emp['income']['other']['others_total'] + total_remu_temp, 2)
            })

            emp["income"].update({
                "total": round(emp["income"]["total"] + total_indenizacoes + total_remu_temp, 2),
            })
    
    return employees

def parse(files):
    employees = {}
    table_indennity_empty = ''
    
    for fn in files:
         # Condicional para definir se a planilha de indenizações tá vazia ou não
        if 'vi' in fn:
            table_indennity_empty = isEmpty(fn)
    
    for file_name in files:
        
        if 'remu' in file_name:
            if(table_indennity_empty == True):
                employees.update(employees_parser_without_indemnities(file_name))
            else:
                employees.update(employees_parser(file_name))
        else:
            employees.update(employees_indemnity(file_name, employees))

    return list(employees.values()) 