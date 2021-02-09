#Servidores de Abril não possuem dados acerca de indenizações para transporte / locomoção
def parse(rows, employees):
    curr_row = 0
    begin_row = 1

    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue

        reg = float(row[0])
        aux_adocao = float(row[4]) #AUXÍLIO-ADOÇÃO/VERBAS INDENIZATÓRIAS
        aux_ali = float(row[5]) #AUXÍLIO-ALIMENTAÇÃO/VERBAS INDENIZATÒRIAS
        aux_ali_remu = float(row[9]) #AUXÌLIO-ALIMENTAÇÃO/OUTRAS REMUNERAÇÕES RETROATIVAS/TEMPORÁRIAS
        aux_edu = float(row[6]) #AUXÍLIO-EDUCAÇÃO/VERBAS_INDENIZATÒRIAS
        aux_edu_remu = float(row[10]) #AUXÌLIO-EDUCAÇÃO/OUTRAS REMUNERAÇÕES RETROATIVAS/TEMPORÁRIAS
        aux_saude = float(row[7]) #AUXÍLIO-SAUDE/VERBAS INDENIZATÓRIAS
        aux_saude_remu = float(row[11]) #AUXÌLIO-SAUDE/OUTRAS REMUNERAÇÕES RETROATIVAS/TEMPORÁRIAS
        indemnity_vacation = float(row[8]) #INDENIZAÇÃO DE FÉRIAS NÃO USUFRUÍDAS

        diff_aux =  float(row[12]) #DIFERENÇAS DE AUXÍLIOS
        gratification = float(row[13]) #GRATIFICAÇÕES EVENTUAIS
        parcelas_atraso = float(row[14]) #PARCELAS PAGAS EM ATRASO

        emp = employees[reg]
        emp['income']['perks'].update({
            'food':  aux_ali + aux_ali_remu ,
            'health': aux_saude + aux_saude_remu,
        })
        emp['income']['other']['others'].update({
            #Auxílio educação está disposto em 2 colunas diferentes
            'AUXÍLIO-ADOÇÃO': aux_adocao,
            'AUXÍLIO-EDUCAÇÃO': aux_edu + aux_edu_remu,
            'INDENIZAÇÃO DE FÉRIAS NÃO USUFRUÍDAS': indemnity_vacation,
            'DIFERENÇAS DE AUXÍLIOS': diff_aux,
            'PARCELAS PAGAS EM ATRASO': parcelas_atraso,
        })
        emp['income']['other'].update({
            'total': round(emp['income']['other']['total'] + aux_adocao + aux_edu +
            aux_edu_remu  + indemnity_vacation + diff_aux + parcelas_atraso
            + gratification, 2),
            'gratification': gratification,
            'others_total': round(emp['income']['other']['others_total'] + aux_adocao +
            aux_edu + aux_edu_remu + indemnity_vacation + diff_aux +
            parcelas_atraso , 2),
        })
        emp['income']['perks'].update({
            'total': round( aux_ali + aux_ali_remu + aux_saude + aux_saude_remu , 2)
        })
        emp['income'].update({
            'total': round(emp['income']['total']  + emp['income']['perks']['total'] + emp['income']['other']['total'], 2)
        })
        employees[row[0]] = emp
        if (rows[curr_row] == rows[-1]).all():
            break
        curr_row += 1

    return employees
