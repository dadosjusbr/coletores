def parse(rows, employees):
    curr_row = 0
    begin_row = 1

    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue

        reg = float(row[0])
        aux_adocao = float(row[4]) #AUXÍLIO-ADOÇÃO/VERBAS INDENIZATÓRIAS
        aux_ali = float(row[5]) #AUXÍLIO-ALIMENTAÇÃO/VERBAS INDENIZATÓRIAS
        aux_saude =  float(row[6]) #AUXÍLIO-SAÚDE/VERBAS INDENIZATÒRIAS
        aux_saude_remu = float(row[9]) #AUXÍLIO-SAÚDE/OUTRAS REMUNERAÇÕES RETROATIVAS/TEMPORÁRIAS
        indemnity_vacation = float(row[7]) #INDENIZAÇÃO DE FÉRIAS NÃO USUFRUÍDAS
        licence =  float(row[8]) #INDENIZAÇÃO DE LICENÇA ESPECIAL/PRÊMIO NÃO USUFRUÍDA
        diff_aux = float(row[10]) #DIFERENÇAS DE AUXÍLIOS
        parcelas_atraso = float(row[11]) #PARCELAS PAGAS EM ATRASO

        emp = employees[reg]
        emp['income']['perks'].update({
            'total': round(aux_saude + aux_saude_remu + aux_ali, 2),
            'food': aux_ali,
            'health': aux_saude + aux_saude_remu,
        })
        emp['income']['other']['others'].update({
            #Auxílio educação está disposto em 2 colunas diferentes
            'AUXÍLIO-ADOÇÃO': aux_adocao,
            'INDENIZAÇÃO DE FÉRIAS NÃO USUFRUÍDAS': indemnity_vacation,
            'INDENIZAÇÃO DE LICENÇA ESPECIAL/PRÊMIO NÃO USUFRUÍDA': licence,
            'DIFERENÇAS DE AUXÍLIOS': diff_aux,
            'PARCELAS PAGAS EM ATRASO': parcelas_atraso,
        })
        emp['income']['other'].update({
            'total': round(emp['income']['other']['total'] + aux_adocao +
             indemnity_vacation + licence + diff_aux + parcelas_atraso, 2),
             'others_total': round(emp['income']['other']['others_total'] + aux_adocao +
             indemnity_vacation + licence + diff_aux + parcelas_atraso , 2),
        })
        emp['income'].update({
            'total': round(emp['income']['total']  + emp['income']['perks']['total'] + emp['income']['other']['total'], 2)
        })
        
        if (rows[curr_row] == rows[-1]).all():
            break
        curr_row += 1

    return employees
