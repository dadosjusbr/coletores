import table


def update(remuneration, indemnsation):

    for row in indemnsation:

        matricula = row[0]
        if type(matricula) != str:
            matricula = str(matricula)

        if matricula == 'nan':
            continue

        if row[0] == 'Total':
            break

        if matricula in remuneration.keys():
            # Verbas Indenizatorias
            auxilio_alimentacao = table.clean_cell(row[4])
            assistencia_medico_social = table.clean_cell(row[5])
            auxilio_moradia= table.clean_cell(row[6])
            auxilio_transporte = table.clean_cell(row[7])
            auxilio_pre_escolar = table.clean_cell(row[8])
            ajuda_custo = table.clean_cell(row[9])
            licenca_premio = table.clean_cell(row[10])
            indenizaao_substituicao = table.clean_cell(row[11])
            abono_pecuniario_ferias = table.clean_cell(row[12])
            ferias_indenizadas = table.clean_cell(abs(row[13]))
            compensacao_platao = table.clean_cell(row[14])

            # Remunerações Temporárias
            cumulacao = table.clean_cell(row[15])
            
            total_temporario = (  
                indenizaao_substituicao
                + compensacao_platao
                + cumulacao)

            emp = remuneration[matricula]

            emp["income"]["perks"].update(
                {
                    "Food": auxilio_alimentacao,
                    "Health": assistencia_medico_social,
                    "Vacation": ferias_indenizadas,
                    "Transportation": auxilio_transporte,
                    "Subsistence": ajuda_custo,
                    "PremiumLicensePecuniary": licenca_premio,
                    "VacationPecuniary": abono_pecuniario_ferias,
                    "PreSchool": auxilio_pre_escolar,
                    "HousingAid": auxilio_moradia,
                }
            )

            emp["income"]["other"]["others"].update(
                {
                    "Indenização de Substituição": indenizaao_substituicao,
                    "Compensação de Plantão": compensacao_platao,
                    "Cumulações": cumulacao,
                }
            )

            emp["income"]["other"].update(
                {
                    "others_total": round(
                        emp["income"]["other"]["others_total"] +
                        total_temporario, 2
                    ),
                    "total": round(
                        emp["income"]["other"]["total"] + total_temporario, 2
                    )
                }
            )

            remuneration[matricula] = emp

    return remuneration
