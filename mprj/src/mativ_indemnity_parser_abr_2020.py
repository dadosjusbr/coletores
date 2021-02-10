def parse(rows, employees):
    curr_row = 0
    begin_row = 1

    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue

        reg = float(row[0])
        aux_ali = float(row[4]) #AUXÍLIO-ALIMENTAÇÃO/VERBAS INDENIZATÒRIAS
        aux_ali_remu = float(row[8]) #AUXÌLIO-ALIMENTAÇÃO/OUTRAS REMUNERAÇÕES RETROATIVAS/TEMPORÁRIAS
        aux_edu = float(row[5]) #AUXÍLIO-EDUCAÇÃO/VERBAS_INDENIZATÒRIAS
        aux_edu_remu = float(row[9]) #AUXÌLIO-EDUCAÇÃO/OUTRAS REMUNERAÇÕES RETROATIVAS/TEMPORÁRIAS
        aux_saude = float(row[6]) #AUXÍLIO-SAUDE/VERBAS INDENIZATÓRIAS
        aux_saude_remu = float(row[11]) #AUXÌLIO-SAUDE/OUTRAS REMUNERAÇÕES RETROATIVAS/TEMPORÁRIAS
        aux_moradia = float(row[10]) #AUXÍLIO-MORADIA/OUTRAS REMUNERAÇÕES RETROATIVAS/TEMPORÁRIAS
        inde_license = float(row[7]) #INDENIZAÇÃO POR LICENÇA NÃO GOZADA
        found = float(row[12]) #DEVOLUÇÃO FUNDO DE RESERVA
        diff_aux =  float(row[13]) #DIFERENÇAS DE AUXÍLIOS
        gratification = float(row[14]) #GRATIFICAÇÕES EVENTUAIS
        parcelas_atraso = float(row[15]) #PARCELAS PAGAS EM ATRASO

        emp = employees[reg]
        emp['income']['perks'].update({
            'total': round( aux_ali + aux_ali_remu + aux_saude + aux_saude_remu + aux_moradia, 2),
            'food':  aux_ali + aux_ali_remu ,
            'health': aux_saude + aux_saude_remu,
            'housing_aid': aux_moradia
        })
        emp['income']['other']['others'].update({
            #Auxílio educação está disposto em 2 colunas diferentes
            'AUXÍLIO-EDUCAÇÃO': aux_edu + aux_edu_remu,
            'INDENIZAÇÃO POR LICENÇA NÃO GOZADA': inde_license,
            'DEVOLUÇÃO FUNDO DE RESERVA': found,
            'DIFERENÇAS DE AUXÍLIOS': diff_aux,
            'PARCELAS PAGAS EM ATRASO': parcelas_atraso,
        })
        emp['income']['other'].update({
            'total': round(emp['income']['other']['total'] + aux_edu +
            aux_edu_remu  + inde_license + found + parcelas_atraso + diff_aux
            + gratification, 2),
            'gratification': gratification,
            'others_total': round(emp['income']['other']['others_total'] + aux_edu +
            aux_edu_remu  + inde_license + found + parcelas_atraso + diff_aux, 2),
        })
        emp['income'].update({
            'total': round(emp['income']['total']  + emp['income']['perks']['total'] + emp['income']['other']['total'], 2)
        })
        employees[row[0]] = emp
        if (rows[curr_row] == rows[-1]).all():
            break
        curr_row += 1

    return employees
