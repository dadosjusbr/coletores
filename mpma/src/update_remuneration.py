from table import clean_cell


def update(remuneration, indemnization):
    for row in indemnization:
        matricula = row[0]
        if type(matricula) != str:
            matricula = str(matricula)

        if matricula in remuneration.keys():

            # Verbas Indenizatorias
            # Nessa tabela juntaram vários valores em uma coluna
            ajuda_custo = clean_cell(row[4])
            auxilio_saude = clean_cell(row[5])
            auxilio_alimentacao = clean_cell(row[6])
            licenca_premio = clean_cell(row[8])
            inden_conv_ferias_em_pecunia = clean_cell(row[9])

            dif_inden_conv_pec_lic_comp_subs_cumul_membro = clean_cell(row[7])
            inden_conv_pec_lic_compensatoria_subs_cumul_membro = clean_cell(row[10])

            # Remunerações Temporárias
            dif_abono_permanencia = clean_cell(row[13])
            dif_direcao_promotoria = clean_cell(row[14])

            try:
                dif_gratificacao_por_funcao_ministerio_publico = clean_cell(row[15])
            except:
                dif_gratificacao_por_funcao_ministerio_publico = 0.0

            try:
                dif_resp_direcao_promotoria = clean_cell(row[16])
            except:
                dif_resp_direcao_promotoria =  0.0

            try:
                direcao_promotoria = clean_cell(row[17])
            except:
                direcao_promotoria = 0.0
            
            try:
                resp_direcao_promotoria = clean_cell(row[18])
            except:
                resp_direcao_promotoria = 0.0
                
            total_temporario = round(
                dif_inden_conv_pec_lic_comp_subs_cumul_membro
                + inden_conv_pec_lic_compensatoria_subs_cumul_membro
                + dif_abono_permanencia 
                + dif_direcao_promotoria
                + dif_gratificacao_por_funcao_ministerio_publico 
                + dif_resp_direcao_promotoria 
                + direcao_promotoria 
                + resp_direcao_promotoria, 2
            )

            emp = remuneration[matricula]

            emp["income"]["perks"].update(
                {
                    "Food": auxilio_alimentacao,
                    "Health": auxilio_saude,
                    "Subsistence": ajuda_custo,
                    "VacationPecuniary": inden_conv_ferias_em_pecunia,
                    "PremiumLicensePecuniary": licenca_premio,
                }
            )

            emp["income"]["other"]["others"].update(
                {
                    "Dif. Inden. Conv. Pec. Lic. Comp. Subs. Cumul. Membro": dif_inden_conv_pec_lic_comp_subs_cumul_membro,
                    "Inden. Conv. Pec. Lic. Compensatoria Subs. Cumul. Membro": inden_conv_pec_lic_compensatoria_subs_cumul_membro,
                    "Dif. Abono de Permanência": dif_abono_permanencia,
                    "Dif. Direção de Promotoria": dif_direcao_promotoria,
                    "Dif. Gratificação por Função Mininistério Público": dif_gratificacao_por_funcao_ministerio_publico,
                    "Dif. RESP. Direção de Promotorias": dif_resp_direcao_promotoria,
                    "Direção de Promotoria": direcao_promotoria,
                    "RESP. Direção de Promotorias": resp_direcao_promotoria,
                }
            )

            emp["income"]["other"].update(
                {
                    "others_total": round(
                        emp["income"]["other"]["others_total"] +
                        total_temporario, 2
                    ),
                    "total": round(
                        emp["income"]["other"]["total"] +
                        total_temporario, 2
                    )
                }
            )

            remuneration[matricula] = emp

    return remuneration
