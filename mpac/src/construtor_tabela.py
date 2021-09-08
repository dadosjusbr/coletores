def tabela(matricula, nome, cargo_efetivo, lotacao, remuneracao_cargo_efetivo,
        outras_verbas_remuneratorias, confianca_comissao, grat_natalina, ferias, permanencia,
        outras_remuneracoes_temporarias, total_indenizacao, previdencia, imp_renda,
        teto_constitucional, outros_descontos):
    total_desconto = round(previdencia + teto_constitucional + imp_renda + outros_descontos, 2)

    total_gratificacoes = round((
        grat_natalina
        + permanencia
        + confianca_comissao
        + ferias
        + outras_verbas_remuneratorias
    ), 2)

    total_bruto = round((remuneracao_cargo_efetivo + \
        outras_verbas_remuneratorias + outras_remuneracoes_temporarias \
        + total_indenizacao + total_gratificacoes), 2)

    employees = {
        "reg": matricula,
        "name": nome,
        "role": cargo_efetivo,
        "type": "membro",
        "workplace": lotacao,
        "active": True,
        "income": {
            "total": total_bruto,
            # REMUNERAÇÃO BÁSICA = Remuneração Cargo Efetivo + Outras Verbas Remuneratórias,
            # legais ou judiciais
            "wage": 
                round(remuneracao_cargo_efetivo + outras_verbas_remuneratorias,2),
            "perks": {
                "total": total_indenizacao,
            },
            "other": {  # Gratificações
                "total": total_gratificacoes,
                "trust_position": confianca_comissao,
                "eventual_benefits": outras_verbas_remuneratorias,
                "others_total": round(grat_natalina + ferias + permanencia,2),
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
            "total": total_desconto,
            "prev_contribution": previdencia,
            # Retenção por teto constitucional
            "ceil_retention": teto_constitucional,
            "income_tax": imp_renda,
            "others_total": outros_descontos,
            "others": {
                "Outros": outros_descontos
            },
        },
    }

    return employees