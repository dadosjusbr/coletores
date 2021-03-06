def parse(rows, employees):
    curr_row = 0
    begin_row = 1

    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue

        reg = float(row[0])
        aux_ali = float(row[4]) #AUXÍLIO-ALIMENTAÇÃO/VERBAS INDENIZATÒRIAS
        aux_ali_remu = float(row[10]) #AUXÌLIO-ALIMENTAÇÃO/OUTRAS REMUNERAÇÕES RETROATIVAS/TEMPORÁRIAS
        aux_edu = float(row[5]) #AUXÍLIO-EDUCAÇÃO/VERBAS_INDENIZATÒRIAS
        aux_edu_remu = float(row[11]) #AUXÌLIO-EDUCAÇÃO/OUTRAS REMUNERAÇÕES RETROATIVAS/TEMPORÁRIAS
        aux_saude = float(row[6]) #AUXÍLIO-SAUDE/VERBAS INDENIZATÓRIAS
        aux_saude_remu = float(row[12]) #AUXÌLIO-SAUDE/OUTRAS REMUNERAÇÕES RETROATIVAS/TEMPORÁRIAS
        devolucao_rra = float(row[7]) #DEVOLUÇÃO IR RRA

        indemnity_vacation = float(row[8]) #INDENIZAÇÃO DE FÉRIAS NÃO USUFRUÍDAS
        inde_license = float(row[9]) #INDENIZAÇÃO POR LICENÇA NÃO GOZADA
        found = float(row[13]) #DEVOLUÇÃO FUNDO DE RESERVA
        diff_aux =  float(row[14]) #DIFERENÇAS DE AUXÍLIOS
        gratification = float(row[15]) #GRATIFICAÇÕES EVENTUAIS
        parcelas_atraso = float(row[16]) #PARCELAS PAGAS EM ATRASO

        emp = employees[reg]
        emp['income']['perks'].update({
            'total': round( aux_ali + aux_ali_remu + aux_saude + aux_saude_remu , 2),
            'food':  aux_ali + aux_ali_remu ,
            'health': aux_saude + aux_saude_remu,
        })
        emp['income']['other']['others'].update({
            #Auxílio educação está disposto em 2 colunas diferentes
            'AUXÍLIO-EDUCAÇÃO': aux_edu + aux_edu_remu,
            'INDENIZAÇÃO DE FÉRIAS NÃO USUFRUÍDAS': indemnity_vacation,
            'INDENIZAÇÃO POR LICENÇA NÃO GOZADA': inde_license,
            'DEVOLUÇÃO IR RRA': devolucao_rra,
            'DEVOLUÇÃO FUNDO DE RESERVA': found,
            'DIFERENÇAS DE AUXÍLIOS': diff_aux,
            'PARCELAS PAGAS EM ATRASO': parcelas_atraso,
        })
        emp['income']['other'].update({
            'total': round(emp['income']['other']['total'] + aux_edu +
            aux_edu_remu  + indemnity_vacation + devolucao_rra + inde_license + found + parcelas_atraso
            + diff_aux + gratification, 2),
            'gratification': gratification,
            'others_total': round(emp['income']['other']['others_total'] + aux_edu +
            aux_edu_remu  + indemnity_vacation + devolucao_rra + inde_license + found + parcelas_atraso
            + diff_aux, 2),
        })
        emp['income'].update({
            'total': round(emp['income']['total']  + emp['income']['perks']['total'] + emp['income']['other']['total'], 2)
        })
        
        if (rows[curr_row] == rows[-1]).all():
            break
        curr_row += 1

    return employees
