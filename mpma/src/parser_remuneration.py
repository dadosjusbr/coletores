from table import clean_cell



def parse(data):
    employees = {}
    for row in data:

        matricula = row[0]

        if type(matricula) != str:
            matricula = str(matricula)

        nome = row[1]
        cargo_efetivo = row[2]
        lotacao = row[3]
        remuneracao_cargo_efetivo = clean_cell(
            row[4])
        outras_verbas_remuneratorias = clean_cell(
            row[5])
        # Função de Confiança ou Cargo em Comissão
        confianca_comissao = clean_cell(
            row[6])
        # Gratificação Natalina
        grat_natalina = abs(clean_cell(row[7]))
        ferias = clean_cell(row[8])
        # Abono de Permanência
        permanencia = clean_cell(row[9])
        # Remunerações tempórarias
        outras_remuneracoes_temporarias = clean_cell(
            row[11])
        # Indenizações
        total_indenizacao = clean_cell(row[10])
        # Contribuição Previdenciária
        previdencia = abs(clean_cell(row[13]))
        # Imposto de Renda
        imp_renda = abs(clean_cell(row[14]))
        # Retenção por Teto Constitucional
        teto_constitucional = abs(clean_cell(row[15]))
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

        campos = {
            'matricula': matricula,
            'nome': nome,
            'cargo_efetivo':cargo_efetivo,
            'lotacao': lotacao, 
            'remuneracao_cargo_efetivo': remuneracao_cargo_efetivo,
            'outras_verbas_remuneratorias': outras_verbas_remuneratorias, 
            'confianca_comissao': confianca_comissao, 
            'grat_natalina': grat_natalina, 
            'ferias': ferias, 
            'permanencia': permanencia,
            'outras_remuneracoes_temporarias': outras_remuneracoes_temporarias, 
            'total_indenizacao': total_indenizacao, 
            'previdencia': previdencia, 
            'imp_renda': imp_renda,
            'teto_constitucional': teto_constitucional, 
            'total_desconto': total_desconto, 
            'total_gratificacoes': total_gratificacoes, 
            'total_bruto': total_bruto
        }

        employees[matricula] = table(campos)

    return employees

def table(campos):
    employees = {
            "reg": campos['matricula'],
            "name": campos['nome'],
            "role": campos['cargo_efetivo'],
            "type": "membro",
            "workplace": campos['lotacao'],
            "active": True,
            "income": {
                "total": round(campos['total_bruto'], 2),
                # REMUNERAÇÃO BÁSICA = campos['Remuneração Cargo Efetivo'] + campos['Outras Verbas Remuneratórias'],
                # legais ou judiciais
                "wage": round(
                            campos['remuneracao_cargo_efetivo'] + 
                            campos['outras_verbas_remuneratorias'], 2
                        ),
                "perks": {
                    "total": round(campos['total_indenizacao'],2),
                },
                "other": {  # Gratificações
                    "total": campos['total_gratificacoes'],
                    "trust_position": campos['confianca_comissao'],
                    "others_total": round(
                                        campos['grat_natalina'] + 
                                        campos['ferias'] + campos['permanencia'], 2
                                    ),
                    "others": {
                        "Férias 1/3 constitucionais": campos['ferias'],
                        "Gratificação Natalina": campos['grat_natalina'],
                        "Abono de Permanência": campos['permanencia'],
                    },
                },
            },
            "discounts": {
                # Discounts Object. Using abs to garantee numbers are positive
                # (spreadsheet have negative discounts).
                "total": round(campos['total_desconto'], 2),
                "prev_contribution": campos['previdencia'],
                # Retenção por teto constitucional
                "ceil_retention": campos['teto_constitucional'],
                "income_tax": campos['imp_renda'],
            },
        }
    return employees
