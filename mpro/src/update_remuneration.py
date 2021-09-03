import table


def update(remuneration, indemnization):

    for i, row in indemnization.iterrows():

        matricula = row['MATRICULA']
        if type(matricula) != str:
            matricula = str(matricula)

        if matricula in remuneration.keys():

            # Verbas Indenizatorias
            auxilio_alimentacao = table.clean_cell(row['AUX_ALIMENTACAO'])
            assistencia_medico_social = table.clean_cell(row['AUX_SAUDE'])
            auxilio_moradia= table.clean_cell(row['AUX_MORADIA'])
            auxilio_transporte = table.clean_cell(row['AUX_TRANSPORTE'])
            auxilio_pre_escolar = table.clean_cell(row['AUX_CRECHE'])
            ajuda_custo = table.clean_cell(row['AJUDA_CUSTO'])

            aux_escolar = table.clean_cell(row['AUX_ESCOLA'])
            aux_odonto = table.clean_cell(row['AUX_ODONTO'])
            outros_aux = table.clean_cell(row['OUTROS_AUX'])

            # Remunerações Temporárias
            abonos = table.clean_cell(row['ABONOS'])
            adicionais = table.clean_cell(row['ADICIONAIS'])
            comissoes = table.clean_cell(row['COMISSOES'])
            diferencas = table.clean_cell(row['DIFERENCAS'])
            indenizacoes = table.clean_cell(row['INDENIZACOES'])
            outras_remuneracoes = table.clean_cell(row['OUTRAS_REMUNERACOES'])

            gratificacoes = table.clean_cell(row['GRATIFICACOES'])
            
            total_temporario = (  
                aux_escolar
                + aux_odonto
                + outros_aux
                + abonos
                + adicionais
                + comissoes
                + diferencas
                + indenizacoes
                + outras_remuneracoes)

            emp = remuneration[matricula]

            emp["income"]["perks"].update(
                {
                    "Food": auxilio_alimentacao,
                    "Health": assistencia_medico_social,
                    "Transportation": auxilio_transporte,
                    "Subsistence": ajuda_custo,
                    "PreSchool": auxilio_pre_escolar,
                    "HousingAid": auxilio_moradia,
                }
            )

            emp["income"]["other"]["others"].update(
                {
                    "Auxílio-Escola": aux_escolar,
                    "Auxílio-Odontológico": aux_odonto,
                    "Outros Auxílios": outros_aux,

                    "Abonos": abonos,
                    "Adicionais": adicionais,
                    "Comissões": comissoes,
                    "Diferenças": diferencas,
                    "Indenizações": indenizacoes,
                    "Outras Remunerações": outras_remuneracoes
                }
            )

            emp["income"]["other"].update(
                {
                    "others_total": round(
                        emp["income"]["other"]["others_total"] +
                        total_temporario, 2
                    ),
                    "gratification": gratificacoes,
                    "total": round(
                        emp["income"]["other"]["total"] + total_temporario + gratificacoes, 2
                    )
                }
            )

            remuneration[matricula] = emp

    return remuneration
