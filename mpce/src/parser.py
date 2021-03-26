import sys
import os
import pandas as pd
def clean_currency_val(value):
    if isinstance(value, str):
        return float(value.replace('R$', '').replace('.', '').replace(',', '.').replace(' ', '').replace('"','').replace("'",''))
    return float(value)

def clean_currency(data, beg_col, end_col):
    for col in data.columns[beg_col:end_col]:
        data[col] = data[col].apply(clean_currency_val)

def read(path):
    try:
        data = pd.read_html(path)
        data = data[0]
        return data

    except Exception as excep:
        sys.stderr.write("'Não foi possível ler o arquivo: " + path + '. O seguinte erro foi gerado: ' + excep)
        os._exit(1)

def employees_parser(file_path):
    data = read(file_path)
    data = data[: -1]
    clean_currency(data, 4, 18)
    
    #Parsing data
    rows = data.to_numpy()
    employees = {}   
    for row in rows:
        
        reg = row[0] #Matrícula
        name = row[1] #Nome
        role = row[2] #Cargo
        workplace = row[3] #Lotação
        remuneration = row[4] #Remuneração do Cargo Efetivo
        other_verbs = row[5] #Outras Verbas Remuneratórias,Legais ou Judiciais	
        trust_pos = row[6] #Função de Confiança ou Cargo em Comissão	
        christmas_bonus = row[7] #Gratificação Natalina	
        terco_ferias = row[8] #Férias(1/3 constitucional)	
        abono_permanencia = row[9] #Abono de Permanência
        temp_remu = row[10] #Outras Remunerações Temporárias
        idemnity = row[11] #Verbas Indenizatórias	
        total = row[12] #Total de Rendimentos Brutos	
        prev_contrib = row[13] #Contribuição Previdenciária
        imposto_renda = row[14] #Imposto de Renda
        ceil_ret = row[15] #Retenção por Teto Constitucional

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
                    'total': trust_pos + christmas_bonus + terco_ferias + abono_permanencia,
                    'trust_position': trust_pos,
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
    print(employees)
    return employees

def employees_indemnity(file_path, employees):
    data = read(file_path)
    data = data[:-1]
    clean_currency(data, 4, 25)

    #Parsing Data
    rows = data.to_numpy()
    for row in rows:
        reg = row[0] #Matrícula
        ac_promocao =  row[4] # A.C. PROMOÇÃO
        ac_deslocamento = row[5] #A.C. DESLOCAMENTO	
        acf_ant_meses = row[6] #A.C.F MESES ANTERIORES	
        acf_mes = row[7] #A.C.F MÊS CORRENTE	
        aux_ali = row[8] #AUX.ALIMENTAÇÃO
        aux_ali_diff = row[9] #DIF. AUX. ALIMENTAÇÃO	
        hora_extra = row[10] #HORA EXTRA / SERVICO EXTRAORDINÁRIO	
        diff_sub = row[11] #DIF. DE SUBSÍDIO	
        diff_subs = row[12] #DIF. DE SUBSÍDIO POR SUBSTITUIÇÃO	
        diff_sub_ant = row[13] #DIF. DE SUBSÍDIO SUBSTITUIÇÃO (MESES ANT.)	
        diff_afas = row[14] #DIF. DE SUBSÍDIO AFASTAMENTO	
        gratification = row[15] #GRAT.DE REPRES. DE GABINETE
        gratifi_assessoramento = row[16] #GRAT.REP.GABINETE POR ASSESSORAMENTO	
        grati_ttr = row[17] #DIF.GRATIFICAÇÃO T.T.R	
        encargo_presi = row[18] #GRAT.POR ENCARGO DE LICITAÇÃO - Presidente comitê	
        encargo_prego = row[19] #GRAT.POR ENCARGO DE LICITAÇÃO - Pregoeiro	
        encargo_titu =  row[20] #GRAT.POR ENCARGO DE LICITAÇÃO - Membros Titular	
        encargo_apoio = row[21] #GRAT.POR ENCARGO DE LICITAÇÃO - Equipe de Apoio	
        trab_tec = row[22] #GRAT.TRAB.TEC./REL./CIENTIFICO - TTR	
        grat_gab = row[23] #DIF. DE GRAT.DE GABINETE	
        pre_school = row[24] #AUX. CRECHE

        # Há funcionários nao listados na planilha de pagamento, porém listados na planilha de indenizações
        try:
            emp = employees[reg]
            exists = True
        except:
            exists = False
        
        if exists:

            emp['income']['perks'].update({
                'total': round( aux_ali + pre_school, 2),
                'food': aux_ali,
                'pre_school': pre_school,
            })
            emp['income']['other']['others'].update({
                'A.C. PROMOÇÃO': ac_promocao,
                'A.C. DESLOCAMENTO': ac_deslocamento,
                'A.C.F MESES ANTERIORES': acf_ant_meses,
                'A.C.F MÊS CORRENTE': acf_mes,
                'DIF. AUX. ALIMENTAÇÃO': aux_ali_diff,
                'HORA EXTRA / SERVICO EXTRAORDINÁRIO': hora_extra,
                'DIF. DE SUBSÍDIO': diff_sub,
                'DIF. DE SUBSÍDIO POR SUBSTITUIÇÃO': diff_subs,
                'DIF. DE SUBSÍDIO SUBSTITUIÇÃO (MESES ANT.)': diff_sub_ant,
                'DIF. DE SUBSÍDIO AFASTAMENTO': diff_afas,
                'GRAT.DE REPRES. DE GABINETE': gratification,
                'GRAT.REP.GABINETE POR ASSESSORAMENTO': gratifi_assessoramento,
                'DIF.GRATIFICAÇÃO T.T.R': grati_ttr,
                'GRAT.POR ENCARGO DE LICITAÇÃO - Presidente comitê': encargo_presi,
                'GRAT.POR ENCARGO DE LICITAÇÃO - Pregoeiro': encargo_prego,
                'GRAT.POR ENCARGO DE LICITAÇÃO - Membros Titular': encargo_titu,
                'GRAT.POR ENCARGO DE LICITAÇÃO - Equipe de Apoio': encargo_apoio,
                'GRAT.TRAB.TEC./REL./CIENTIFICO - TTR': trab_tec,
                'DIF. DE GRAT.DE GABINETE': grat_gab,
            })
            emp['income']['other'].update({
            'others_total': round(emp['income']['other']['others_total'] + ac_promocao + ac_deslocamento + acf_ant_meses
            + acf_mes + aux_ali_diff + hora_extra + diff_sub + diff_subs + diff_sub_ant + diff_afas + gratification +
            gratifi_assessoramento + grati_ttr + encargo_presi + encargo_prego + encargo_titu + encargo_apoio + trab_tec +
            grat_gab , 2)
            })
    
    return employees

def parse(files):
    employees = {}

    for file_name in files:
        if 'vi' not in file_name:
            employees.update(employees_parser(file_name))
        else:
            employees_indemnity(file_name, employees)

    return list(employees.values())