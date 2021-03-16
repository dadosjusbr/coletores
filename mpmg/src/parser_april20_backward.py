import parser


def format_value(element):
    # A value was found with incorrect formatting. (3,045.99 instead of 3045.99)
    if(parser.isNaN(element)):
        return 0.0
    if type(element) == str:
        if("." in element and "," in element):
            element = element.replace(".", "").replace(",", ".")
        elif("," in element):
            element = element.replace(",", ".")

    return float(element)


def parse_employees(file_name):
    rows = parser.read_data(file_name).to_numpy()
    begin_string = "Matrícula"
    end_string = "TOTAL"
    begin_row = parser.get_begin_row(rows, begin_string)
    end_row = parser.get_end_row(rows, begin_row, end_string)

    employees = {}
    curr_row = 0
    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue
        
        matricula = row[1]
        if(type(matricula) != str):
            matricula = str(matricula)
        nome = row[2]
        cargo_efetivo = row[3]
        unidade_administrativa = row[5]
        remuneracao_cargo_efetivo = format_value(row[6])
        outras_verbas_remuneratorias = format_value(row[7])
        confianca_comissao = format_value(
            row[8]
        )  # Função de Confiança ou Cargo em Comissão
        grat_natalina = format_value(row[9])  # Gratificação Natalina
        ferias = format_value(row[10])
        permanencia = format_value(row[11])  # Abono de Permanência
        previdencia = format_value(row[13])  # Contribuição Previdenciária
        imp_renda = format_value(row[14])  # Imposto de Renda
        teto_constitucional = format_value(row[15])  # Retenção por Teto Constitucional
        total_desconto = previdencia + imp_renda + teto_constitucional
        outras_remuneracoes_temporarias = format_value(row[19])
        total_gratificacoes = (
            grat_natalina
            + ferias
            + permanencia
            + confianca_comissao
            + outras_remuneracoes_temporarias
        )
        total_bruto = (
            remuneracao_cargo_efetivo
            + outras_verbas_remuneratorias
            + total_gratificacoes
        )
        employees[matricula] = {
            "reg": matricula,
            "name": nome,
            "role": cargo_efetivo,
            "type": "membro",
            "workplace": unidade_administrativa,
            "active": True,
            "income": {
                "total": total_bruto,
                # REMUNERAÇÃO BÁSICA = Remuneração Cargo Efetivo + Outras Verbas Remuneratórias, Legais ou Judiciais
                "wage": remuneracao_cargo_efetivo + outras_verbas_remuneratorias,
                "other": {  # Gratificações
                    "total": total_gratificacoes,
                    "trust_position": confianca_comissao,
                    "others_total": grat_natalina
                    + ferias
                    + permanencia
                    + outras_remuneracoes_temporarias,
                    "others": {
                        "Gratificação Natalina": grat_natalina,
                        "Férias (1/3 constitucional)": ferias,
                        "Abono de Permanência": permanencia,
                        "Outras Remunerações Temporárias": outras_remuneracoes_temporarias,
                    },
                },
            },
            "discounts": {  # Discounts Object. Using abs to garantee numbers are positivo (spreadsheet have negative discounts).
                "total": round(total_desconto, 2),
                "prev_contribution": previdencia,
                # Retenção por teto constitucional
                "ceil_retention": teto_constitucional,
                "income_tax": imp_renda,
            },
        }

        curr_row += 1
        if curr_row > end_row:
            break
    
    return employees


def update_employee_indemnity(file_name, employees):
    rows = parser.read_data(file_name).to_numpy()
    begin_string = "Matrícula"  # word before starting data
    end_string = "TOTAL"
    begin_row = parser.get_begin_row(rows, begin_string)
    end_row = parser.get_end_row(rows, begin_row, end_string)
    curr_row = 0

    for row in rows:
        if curr_row < begin_row:
            curr_row += 1
            continue
        matricula = row[1]

        if(type(matricula) != str):
            matricula = str(matricula)
        if matricula in employees.keys():
            vale_alimentacao = format_value(row[5])
            auxilio_alimentacao = format_value(row[6])
            auxilio_creche = format_value(row[7])
            transporte = format_value(row[8])
            saude = format_value(row[9])
            moradia = format_value(row[10])
            total_indenizacoes = (
                vale_alimentacao
                + auxilio_alimentacao
                + auxilio_creche
                + transporte
                + moradia
                + saude
            )
            emp = employees[matricula]

            emp["income"].update(
                {
                    "total": round(emp["income"]["total"] + total_indenizacoes, 2),
                }
            )

            emp["income"].update(
                {
                    "perks": {
                        "total": round(total_indenizacoes,2),
                        "food": vale_alimentacao + auxilio_alimentacao,
                        "pre_school": auxilio_creche,
                        "transportation": transporte,
                        "housing_aid": moradia,
                        "health": saude,
                    }
                }
            )

            employees[matricula] = emp

            curr_row += 1
            if curr_row > end_row:
                break
    return employees
