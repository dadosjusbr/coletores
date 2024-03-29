import table


def parser(file, no_budge_sheets=False):
    begin_row = table.get_begin_row(file, 'Matrícula')
    end_row = table.get_end_row(file, 'Total Geral')

    curr_row = 0
    employees = {}

    for row in file:
        curr_row += 1

        if curr_row <= begin_row:
            continue

        # Para não pegar os membros inativos
        if row[3] == 'INATIVOS':
            continue

        matricula = row[0]
        if type(matricula) != str:
            matricula = str(matricula)

        if matricula == 'nan':
            continue

        if row[0] == 'Total Geral':
            break

        nome = row[1]
        cargo_efetivo = row[2]
        lotacao = row[3]
        remuneracao_cargo_efetivo = table.clean_cell(row[4])
        outras_verbas_remuneratorias = table.clean_cell(row[5])
        # Função de Confiança ou Cargo em Comissão
        confianca_comissao = table.clean_cell(row[6])
        # Gratificação Natalina
        grat_natalina = abs(table.clean_cell(row[7]))
        ferias = table.clean_cell(row[8])
        permanencia = table.clean_cell(row[9])  # Abono de Permanência
        # Remunerações tempórarias
        outras_remuneracoes_temporarias = table.clean_cell(row[10])
        # Indenizações
        total_indenizacao = table.clean_cell(row[11])
        # Contribuição Previdenciária
        previdencia = abs(table.clean_cell(row[13]))
        # Imposto de Renda
        imp_renda = abs(table.clean_cell(row[14]))
        # Retenção por Teto Constitucional
        teto_constitucional = abs(table.clean_cell(row[15]))
        total_desconto = previdencia + teto_constitucional + imp_renda

        total_gratificacoes = (
            grat_natalina
            + permanencia
            + confianca_comissao
            + ferias
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
                # legais ou judiciais
                "wage": round(
                    remuneracao_cargo_efetivo + outras_verbas_remuneratorias, 2
                ),
                "perks": {
                    "total": total_indenizacao,
                },
                "other": {  # Gratificações
                    "total": total_gratificacoes,
                    "trust_position": confianca_comissao,
                    "others_total": round(grat_natalina + ferias + permanencia, 2),
                    "others": {
                        "Férias 1/3 constitucionais": ferias,
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

        if no_budge_sheets:
            employees[matricula]['income']['other'].update(
                {
                    "eventual_benefits": outras_remuneracoes_temporarias,
                }
            )
            employees[matricula]['income']['other'].update(
                {
                    'total': employees[matricula]['income']['other']['total'] + outras_remuneracoes_temporarias
                }
            )

        if curr_row > end_row:
            break

    return(employees)
