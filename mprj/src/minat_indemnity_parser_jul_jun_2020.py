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
        inde_vacation = float(row[6]) #INDENIZAÇÃO DE FÉRIAS NÃO USUFRUÍDAS
        inde_license = float(row[7]) #INDENIZAÇÃO DE LICENÇA ESPECIAL/PRÊMIO NÃO USUFRUÍDA
        found = float(row[8]) #DEVOLUÇÃO FUNDO DE RESERVA

        emp = employees[reg]
        emp['income']['perks'].update({
            'total': round( aux_saude, 2),
            'health': aux_saude,
        })
        emp['income']['other']['others'].update({
            'AUXÍLIO-EDUCAÇÃO': aux_edu,
            'INDENIZAÇÃO DE FÉRIAS NÃO USUFRUÍDAS': inde_vacation,
            'INDENIZAÇÃO DE LICENÇA ESPECIAL/PRÊMIO NÃO USUFRUÍDA': inde_license,
            'DEVOLUÇÃO FUNDO DE RESERVA': found,
        })
        emp['income']['other'].update({
            'total': round(emp['income']['other']['total'] + inde_vacation  +
            inde_license + found, 2),
            'others_total': round(emp['income']['other']['others_total'] + inde_vacation  +
             inde_license + found, 2),
        })
        emp['income'].update({
            'total': round(emp['income']['total']  + emp['income']['perks']['total'] + emp['income']['other']['total'], 2)
        })
        employees[row[0]] = emp
        if (rows[curr_row] == rows[-1]).all():
            break
        curr_row += 1

    return employees
