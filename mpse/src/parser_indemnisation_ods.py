import table


def update(remuneration, indemnsation, new=False):
    begin_row = table.get_begin_row(indemnsation, 'Matrícula')
    end_row = table.get_end_row(indemnsation, 'Total:')

    curr_row = 0

    for row in indemnsation:
        curr_row += 1
        if curr_row <= begin_row:
            continue

        if row[3] == 'INATIVOS':
            continue

        matricula = row[0]
        if type(matricula) != str:
            matricula = str(matricula)

        if matricula in remuneration.keys():
            # Verbas Indenizatorias
            auxilio_saude = table.clean_cell(row[4])
            dif_auxilio_saude = table.clean_cell(row[5])
            auxilio_alimentacao = table.clean_cell(row[6])
            dif_auxilio_alimentacao = table.clean_cell(row[7])
            auxilio_interiorizacao = table.clean_cell(row[8])
            dif_auxilio_interiorizacao = table.clean_cell(row[9])
            dif_auxilio_lei_8_625_93 = table.clean_cell(row[10])
            indenizacoes_ferias_licenca_premio = table.clean_cell(row[11])
            abono_pecuniario = table.clean_cell(row[12])
            dif_abono_pecuniario = table.clean_cell(row[13])
            ressarcimentos = table.clean_cell(row[14])

            # Remunerações Temporárias
            geo = table.clean_cell(row[16])
            dif_geo = table.clean_cell(row[17])
            insalubridade = table.clean_cell(row[18])
            dif_insalubridade = table.clean_cell(row[19])
            periculosidade = table.clean_cell(row[20])
            dif_periculosidade = table.clean_cell(row[21])
            adicional_trabalho_tecnico = table.clean_cell(row[22])
            dif_adicional_trabalho_tecnico = table.clean_cell(row[23])
            grat_atividade_ensino = table.clean_cell(row[24])
            substituicoes = table.clean_cell(row[25])
            dif_substituicoes = table.clean_cell(row[26])
            cumulacao = table.clean_cell(row[27])
            dif_cumulacao = table.clean_cell(row[28])
            representacao_de_direcao = table.clean_cell(row[29])
            dif_representacao_de_direcao = table.clean_cell(row[30])
            grat_turma_recursal = table.clean_cell(row[31])
            dif_grat_turma_recursal = table.clean_cell(row[32])
            grat_dificil_provimento = table.clean_cell(row[33])
            dif_grat_dificil_provimento = table.clean_cell(row[34])
            grat_assessor = table.clean_cell(row[35])
            dif_grat_assessor = table.clean_cell(row[36])
            representacao_gaego = table.clean_cell(row[37])
            dif_representacao_gaego = table.clean_cell(row[38])

            total_temporario = (auxilio_interiorizacao + dif_auxilio_interiorizacao + dif_auxilio_lei_8_625_93 +
                                indenizacoes_ferias_licenca_premio + abono_pecuniario + dif_abono_pecuniario +
                                ressarcimentos + geo + dif_geo + insalubridade + dif_insalubridade +
                                periculosidade + dif_periculosidade + adicional_trabalho_tecnico +
                                dif_adicional_trabalho_tecnico + grat_atividade_ensino + substituicoes +
                                dif_substituicoes + cumulacao + dif_cumulacao + representacao_de_direcao +
                                dif_representacao_de_direcao + grat_turma_recursal + dif_grat_turma_recursal +
                                grat_dificil_provimento + dif_grat_dificil_provimento + grat_assessor +
                                dif_grat_assessor + representacao_gaego + dif_representacao_gaego)

            emp = remuneration[matricula]

            emp["income"]["perks"].update(
                {
                    "food": auxilio_alimentacao + dif_auxilio_alimentacao,
                    "health": auxilio_saude + dif_auxilio_saude
                }
            )

            emp["income"]["other"]["others"].update(
                {
                    'Auxilio Interiorização': auxilio_interiorizacao + dif_auxilio_interiorizacao,
                    'Auxilio lei 8.625/93': dif_auxilio_lei_8_625_93,
                    'Indenizações Férias/Licença-Prêmio': indenizacoes_ferias_licenca_premio,
                    'Abono Pecuniário': abono_pecuniario + dif_abono_pecuniario,
                    'Ressarcimentos': ressarcimentos,

                    # Remuneraçoes
                    'GEO': geo + dif_geo,
                    'Insalubridade': insalubridade + dif_insalubridade,
                    'Periculosidade': periculosidade + dif_periculosidade,
                    'Adicional Trabalho Tecnico': adicional_trabalho_tecnico + dif_adicional_trabalho_tecnico,
                    'Grat. Atividade Ensino': grat_atividade_ensino,
                    'Substituições': substituicoes + dif_substituicoes,
                    'Cumulação': cumulacao + dif_cumulacao,
                    'Represetação de Direção': representacao_de_direcao + dif_representacao_de_direcao,
                    'Grat. Turma Recursal': grat_turma_recursal + dif_grat_turma_recursal,
                    'Grat. Dificil Provimento': grat_dificil_provimento + dif_grat_dificil_provimento,
                    'Grat. Acessor': grat_assessor + dif_grat_assessor,
                    'Representação GAEGO': representacao_gaego + dif_representacao_gaego
                }
            )

            # Para 2 de 2021 em diante
            if new:
                gratificacao_diretor_subsede = table.clean_cell(row[39])
                dif_gratificacao_diretor_subsede = table.clean_cell(row[40])

                total_temporario += gratificacao_diretor_subsede + dif_gratificacao_diretor_subsede

                emp["income"]["other"]["others"].update(
                    {
                        'Gratificação Diretor Subsede': gratificacao_diretor_subsede + dif_gratificacao_diretor_subsede
                    })

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

            if curr_row > end_row:
                break

    return remuneration
