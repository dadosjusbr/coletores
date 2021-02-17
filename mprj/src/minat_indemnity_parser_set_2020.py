def parse(rows, employees):
    curr_row = 0
    begin_row = 1

    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue

        reg = float(row[0])
        aux_edu = float(row[4]) #AUXÍLIO-ALIMENTAÇÃO/VERBAS INDENIZATÒRIAS
        aux_saude = float(row[5]) #AUXÍLIO-SAUDE/VERBAS INDENIZATÓRIAS
        aux_saude_remu = float(row[9]) #AUXÍLIO-SAUDE/OUTRAS REMUNERAÇÕES RETROATIVAS/TEMPORÁRIAS
        devolucao_rra = float(row[6]) #DEVOLUÇÃO IR RRA/VERBAS INDENIZATÓRIAS
        inde_vacation = float(row[7]) #INDENIZAÇÃO DE FÉRIAS NÃO USUFRUÍDAS
        inde_license = float(row[8]) #INDENIZAÇÃO DE LICENÇA ESPECIAL/PRÊMIO NÃO USUFRUÍDA
        found = float(row[10]) #DEVOLUÇÃO FUNDO DE RESERVA

        emp = employees[reg]
        emp['income']['perks'].update({
            'total': round( aux_saude + aux_saude_remu, 2),
            'health': aux_saude + aux_saude_remu,
        })
        emp['income']['other']['others'].update({
            'AUXÍLIO-EDUCAÇÃO': aux_edu,
            'DEVOLUÇÃO IR RRA': devolucao_rra,
            'INDENIZAÇÃO DE FÉRIAS NÃO USUFRUÍDAS': inde_vacation,
            'INDENIZAÇÃO DE LICENÇA ESPECIAL/PRÊMIO NÃO USUFRUÍDA': inde_license,
            'DEVOLUÇÃO FUNDO DE RESERVA': found,
        })
        emp['income']['other'].update({
            'total': round(emp['income']['other']['total'] + aux_edu + inde_vacation + devolucao_rra +
            inde_license + found, 2),
            'others_total': round(emp['income']['other']['others_total'] +  aux_edu + inde_vacation  +
            devolucao_rra + inde_license + found, 2),
        })
        emp['income'].update({
            'total': round(emp['income']['total']  + emp['income']['perks']['total'] + emp['income']['other']['total'], 2)
        })
        employees[row[0]] = emp
        if (rows[curr_row] == rows[-1]).all():
            break
        curr_row += 1

    return employees
