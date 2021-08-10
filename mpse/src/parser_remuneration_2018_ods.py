import table


def parser(file):
    begin_row = table.get_begin_row_nan(file, 'Matrícula')
    end_row = table.get_end_row_nan(file, 'TotalGeral')

    curr_row = 0
    employees = {}

    for row in file:
        curr_row += 1
        if curr_row <= begin_row:
            continue

        if row[4] == 'INATIVO':
            continue
            
        matricula = row[1]
        if type(matricula) != str:
            matricula = str(matricula)

        nome = row[2]
        # Remuneração cargo efetivo
        cargo_efetivo = row[3]
        lotacao = row[4]
        remuneracao_cargo_efetivo = table.clean_cell(row[5])
        outras_verbas_remuneratorias = table.clean_cell(row[6])
        # Função de Confiança ou Cargo em Comissão
        confianca_comissao = table.clean_cell(row[7])
        # Gratificação Natalina
        grat_natalina = abs(table.clean_cell(row[8]))
        ferias = table.clean_cell(row[9])
        # Abono de Permanência
        permanencia = table.clean_cell(row[10])
        # Contribuição Previdenciária
        previdencia = abs(table.clean_cell(row[12]))
        # Imposto de Renda
        imp_renda = abs(table.clean_cell(row[13])) 
        # Retenção por Teto Constitucional
        teto_constitucional = abs(table.clean_cell(row[14]))  
        total_desconto = previdencia + teto_constitucional + imp_renda
        total_indenizacao = table.clean_cell(row[17])
        outras_remuneracoes_temporarias = abs(table.clean_cell(row[18]))
        
        total_gratificacoes = (
            grat_natalina
            + permanencia
            + confianca_comissao
        )
        total_bruto = remuneracao_cargo_efetivo + \
            outras_verbas_remuneratorias + outras_remuneracoes_temporarias \
                + total_indenizacao + total_gratificacoes

        employees[matricula] = {
            "reg": matricula,
            "name": nome,
            "role": cargo_efetivo,
            "type": "membro",
            "workplace": lotacao,
            "active": True,
            "income": {
                "total": round(total_bruto, 2),
                # REMUNERAÇÃO BÁSICA = Remuneração Cargo Efetivo + Outras Verbas Remuneratórias,
                # Legais ou Judiciais
                "wage": round(
                    remuneracao_cargo_efetivo + outras_verbas_remuneratorias, 2
                ),
                "perks": {
                    "total": total_indenizacao,
                    "vacation": ferias
                },
                "other": {  
                    # Gratificações
                    "total": round(total_gratificacoes, 2),
                    "trust_position": confianca_comissao,
                    "others_total": round(grat_natalina + ferias + permanencia, 2),
                    "others": {
                        
                        "Gratificação Natalina": grat_natalina,
                        "Abono de Permanência": permanencia,
                    },
                },
            },
            "discounts": {  
                # Discounts Object. Using abs to garantee numbers are positive 
                # (spreadsheet have negative discounts).
                "total": round(total_desconto, 2),
                "prev_contribution": previdencia,
                # Retenção por teto constitucional
                "ceil_retention": teto_constitucional,
                "income_tax": imp_renda,
            },
        }

        if curr_row > end_row:
            break

    return(employees)

    