import table


def parser(file):
    print('Dentro do parser 2018')
    begin_row = table.get_begin_row_nan(file, 'Matrícula')
    end_row = table.get_end_row_nan(file, 'TotalGeral')

    curr_row = 0
    employees = {}

    for row in file:
        curr_row += 1
        if curr_row <= begin_row:
            continue
            
        matricula = row[1]
        if type(matricula) != str:
            matricula = str(matricula)
        nome = row[2]
        cargo_efetivo = row[3]
        if table.is_nan(cargo_efetivo):
            cargo_efetivo = "Não informado"
        lotacao = row[4]
        if table.is_nan(lotacao):
            lotacao = "Não informado"
        remuneracao_cargo_efetivo = table.clean_cell(row[5])
        outras_verbas_remuneratorias = table.clean_cell(row[6])
        confianca_comissao = table.clean_cell(
            row[7]
        )  # Função de Confiança ou Cargo em Comissão
        grat_natalina = abs(table.clean_cell(row[8]))  # Gratificação Natalina
        ferias = table.clean_cell(row[9])
        permanencia = table.clean_cell(row[10])  # Abono de Permanência
        # Como esse valor é correspondente ao que vem descrito na planilha de verbas indenizatórias, não iremos utiliza-lo
        # outras_remuneracoes_temporarias = abs(table.clean_cell(row[12]))
        total_indenizacao = table.clean_cell(row[17])
        # Contribuição Previdenciária
        previdencia = abs(table.clean_cell(row[12]))
        imp_renda = abs(table.clean_cell(row[13]))  # Imposto de Renda
        teto_constitucional = abs(
            table.clean_cell(row[14])
        )  # Retenção por Teto Constitucional
        total_desconto = previdencia + teto_constitucional + imp_renda
        total_gratificacoes = (
            grat_natalina
            + ferias
            + permanencia
            + confianca_comissao
        )
        total_bruto = remuneracao_cargo_efetivo + \
            outras_verbas_remuneratorias + total_indenizacao + total_gratificacoes
        employees[matricula] = {
            "reg": matricula,
            "name": nome,
            "role": cargo_efetivo,
            "type": "membro",
            "workplace": lotacao,
            "active": True,
            "income": {
                "total": round(total_bruto, 2),
                # REMUNERAÇÃO BÁSICA = Remuneração Cargo Efetivo + Outras Verbas Remuneratórias, Legais ou Judiciais
                "wage": round(
                    remuneracao_cargo_efetivo + outras_verbas_remuneratorias, 2
                ),
                "perks": {"total": total_indenizacao},
                "other": {  # Gratificações
                    "total": round(total_gratificacoes, 2),
                    "trust_position": confianca_comissao,
                    "others_total": round(grat_natalina + ferias + permanencia, 2),
                    "others": {
                        "Gratificação Natalina": grat_natalina,
                        "Férias (1/3 constitucional)": ferias,
                        "Abono de Permanência": permanencia,
                    },
                },
            },
            "discounts": {  # Discounts Object. Using abs to garantee numbers are positive (spreadsheet have negative discounts).
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

    