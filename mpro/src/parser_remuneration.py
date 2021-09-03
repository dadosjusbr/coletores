from table import clean_cell 

def parse(data):
    employees = {}
    for i, row in data.iterrows():


        matricula = row['MATRICULA']
        
        if type(matricula) != str:
            matricula = str(matricula)

        nome = row['NOME']
        cargo_efetivo = row['DESCRICAO']
        lotacao = row['LOTACAO']
        remuneracao_cargo_efetivo = clean_cell(row['COL01'])
        outras_verbas_remuneratorias = clean_cell(row['COL02'])
        # Função de Confiança ou Cargo em Comissão
        confianca_comissao = clean_cell(row['COL03'])
        # Gratificação Natalina
        grat_natalina = abs(clean_cell(row['COL04']))
        ferias = clean_cell(row['COL05'])
        permanencia = clean_cell(row['COL06'])  # Abono de Permanência
        # Remunerações tempórarias
        outras_remuneracoes_temporarias = clean_cell(row['COL14'])
        # Indenizações
        total_indenizacao = clean_cell(row['COL13'])
        # Contribuição Previdenciária
        previdencia = abs(clean_cell(row['COL08']))
        # Imposto de Renda
        imp_renda = abs(clean_cell(row['COL09']))
        # Retenção por Teto Constitucional
        teto_constitucional = abs(clean_cell(row['COL10']))
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



    return employees
