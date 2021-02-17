def parse(rows, employees):
    curr_row = 0
    begin_row = 1

    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue

        reg = float(row[0])
        aux_adocao = float(row[4]) #AUXÍLIO-ADOÇÃO/VERBAS INDENIZATÓRIAS
        aux_saude =  float(row[5]) #AUXÍLIO-SAÚDE/VERBAS INDENIZATÒRIAS
        aux_saude_remu = float(row[8]) #AUXÍLIO-SAÚDE/OUTRAS REMUNERAÇÕES RETROATIVAS/TEMPORÁRIAS
        indemnity_vacation = float(row[6]) #INDENIZAÇÃO DE FÉRIAS NÃO USUFRUÍDAS
        licence =  float(row[7]) #INDENIZAÇÃO DE LICENÇA ESPECIAL/PRÊMIO NÃO USUFRUÍDA
        diff_aux = float(row[9]) #DIFERENÇAS DE AUXÍLIOS

        emp = employees[reg]
        emp['income']['perks'].update({
            'total': round(aux_saude + aux_saude_remu, 2),
            'health': aux_saude + aux_saude_remu,
        })
        emp['income']['other']['others'].update({
            #Auxílio educação está disposto em 2 colunas diferentes
            'AUXÍLIO-ADOÇÃO': aux_adocao,
            'INDENIZAÇÃO DE FÉRIAS NÃO USUFRUÍDAS': indemnity_vacation,
            'INDENIZAÇÃO DE LICENÇA ESPECIAL/PRÊMIO NÃO USUFRUÍDA': licence,
            'DIFERENÇAS DE AUXÍLIOS': diff_aux,
        })
        emp['income']['other'].update({
            'total': round(emp['income']['other']['total'] + aux_adocao +
             indemnity_vacation + licence + diff_aux, 2),
             'others_total': round(emp['income']['other']['others_total'] + aux_adocao +
             indemnity_vacation + licence + diff_aux, 2),
        })
        emp['income'].update({
            'total': round(emp['income']['total']  + emp['income']['perks']['total'] + emp['income']['other']['total'], 2)
        })
        employees[row[0]] = emp
        if (rows[curr_row] == rows[-1]).all():
            break
        curr_row += 1

    return employees
