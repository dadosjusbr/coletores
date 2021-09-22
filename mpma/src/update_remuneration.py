"""
Versão totalmente de demonstração haha
"""

from table import clean_cell
import pandas as pd

def update(remuneration, indemnization):
    df = pd.read_csv(indemnization)
    for i,row in df.iterrows():
        print(row)
        matricula = row['Matrícula']
        if type(matricula) != str:
            matricula = str(matricula)

        if matricula in remuneration.keys():

            # Verbas Indenizatorias
            # Nessa tabela juntaram vários valores em uma coluna
            try:
                ajuda_custo = clean_cell(row['Ajuda de custo'])
            except:
                ajuda_custo = 0.0
            
            try:
                auxilio_saude = clean_cell(row['Assistência médico-social (auxílio-saúde) Membro MP'])
            except:
                auxilio_saude = 0.0

            try:
                dif_auxilio_saude = clean_cell(row['Dif. Assistência médico-social (auxílio-saúde) Membro MP'])
            except:
                dif_auxilio_saude = 0.0

            try:
                grat_encargo_curso_concurso = clean_cell(row['Grat. por Encargo de Curso ou Concurso'])
            except:
                grat_encargo_curso_concurso = 0.0

            try:
                auxilio_alimentacao = clean_cell(row['Auxílio-alimentação Membro MP'])
            except:
                auxilio_alimentacao = 0.0

            try:
                dif_auxilio_alimentacao = clean_cell(row['Dif. Auxílio-alimentação Membro MP'])
            except:
                dif_auxilio_alimentacao = 0.0

            try:
                licenca_premio = clean_cell(row['Ind Licenca Premio/Espec Nao Gozada'])
            except:
                licenca_premio = 0.0

            try:
                auxilio_moradia = clean_cell(row['Auxilio-moradia Membro MP'])
            except:
                auxilio_moradia = 0.0

            try:
                ind_licenca_premio_espec_nao_gozada = clean_cell(row['Ind Licenca Premio/Espec Nao Gozada'])
            except:
                ind_licenca_premio_espec_nao_gozada = 0.0

            try:
                inden_conv_ferias_em_pecunia_com_1_3 = clean_cell(row['Inden. Conv. Férias em Pecúnia (com 1/3 Const)'])
            except:
                inden_conv_ferias_em_pecunia_com_1_3 = 0.0

            try:
                inden_conv_ferias_em_pecunia = clean_cell(row['Inden. Conv. Férias em Pecúnia'])
            except:
                inden_conv_ferias_em_pecunia = 0.0

            try:
                dif_terco_conv_ferias_pecunia = clean_cell(row['Dif. Terço Conv. Pecúnia Férias'])
            except:
                dif_terco_conv_ferias_pecunia = 0.0
            
            try:            
                inden_conv_pec_licensa_especial = clean_cell(row['Indenização - Conv. em Pec. da Licença Especial'])
            except:
                inden_conv_pec_licensa_especial = 0.0

            try:
                dif_pen_alimenticia = clean_cell(row['Dif. Pen. Aliment.-2'])
            except:
                dif_pen_alimenticia = 0.0

            try:
                dif_subs_cumulativa = clean_cell(row['Dif. Substituição Cumulativa Membro MP'])
            except:
                dif_subs_cumulativa = 0.0

            try:
                dif_inden_conv_pec_lic_comp_subs_cumul_membro = clean_cell(row['Dif. Inden. Conv. Pec. Lic. Comp. Subs. Cumul. Membro'])
            except:
                dif_inden_conv_pec_lic_comp_subs_cumul_membro = 0.0

            try:
                inden_conv_pec_lic_compensatoria_subs_cumul_membro = clean_cell(row['Inden. Conv. Pec. Lic. Compensatoria Subs. Cumul. Membro'])
            except:
                inden_conv_pec_lic_compensatoria_subs_cumul_membro = 0.0

            try:
                dif_ress_conv_mestrado_int_direito = clean_cell('Dif. RESS. Conv. Mestrado Int. Direito MINTER UNDB')
            except:
                dif_ress_conv_mestrado_int_direito = 0.0

            try:        
                ress_conv_mestrado_int_direito = clean_cell('RESS. Conv. Mestrado Int. Direito MINTER UNDB')
            except:
                ress_conv_mestrado_int_direito = 0.0

            # Remunerações Temporárias
            try:
                dif_subsidios = clean_cell(row['Dif. Subsídios'])
            except:
                dif_subsidios = 0.0

            try:
                dif_abono_permanencia = clean_cell(row['Dif. Abono de Permanência'])
            except:
                dif_abono_permanencia = 0.0

            try:
                direcao_promotoria = clean_cell(row['Direção de Promotoria'])
            except:
                direcao_promotoria = 0.0

            try:
                resp_direcao_promotoria = clean_cell(row['RESP. Direção de Promotorias'])
            except:
                resp_direcao_promotoria = 0.0

            try:
                subs_cumulativa = clean_cell(row['Substituição Cumulativa Membro MP'])
            except:
                subs_cumulativa = 0.0

            try:
                dif_gratificacao_por_funcao_ministerio_publico = clean_cell(row['Dif. Gratificação por Função Mininistério Público'])
            except:
                dif_gratificacao_por_funcao_ministerio_publico = 0.0

            try:
                dif_resp_direcao_promotoria = clean_cell(row['Dif. RESP. Direção de Promotorias'])
            except:
                dif_resp_direcao_promotoria = 0.0

            try:
                dif_direcao_promotoria = clean_cell(row['Dif. Direção de Promotoria'])
            except:
                dif_direcao_promotoria = 0.0

            try:
                subs_funcao_minis_pub = clean_cell(row['SUBS. Função Ministério Público'])
            except:
                subs_funcao_minis_pub = 0.0

            try:
                dif_terco_const_ferias =clean_cell(row['Dif. Terço Constitucional de Férias'])
            except:
                dif_terco_const_ferias = 0.0

            try:
                dif_13_salario = clean_cell(row['Dif. 13º Salário'])
            except:
                dif_13_salario = 0.0


            total_temporario = round(
                grat_encargo_curso_concurso
                + ind_licenca_premio_espec_nao_gozada
                + inden_conv_ferias_em_pecunia_com_1_3
                + dif_terco_conv_ferias_pecunia
                + inden_conv_pec_licensa_especial
                + dif_pen_alimenticia
                + dif_subs_cumulativa
                + dif_inden_conv_pec_lic_comp_subs_cumul_membro
                + inden_conv_pec_lic_compensatoria_subs_cumul_membro
                + dif_ress_conv_mestrado_int_direito
                + ress_conv_mestrado_int_direito
                + dif_subsidios
                + dif_abono_permanencia
                + resp_direcao_promotoria
                + subs_cumulativa
                + dif_gratificacao_por_funcao_ministerio_publico
                + dif_resp_direcao_promotoria
                + dif_direcao_promotoria
                + subs_funcao_minis_pub
                + dif_terco_const_ferias
                + dif_13_salario
                + direcao_promotoria, 2
            )

            emp = remuneration[matricula]

            emp["income"]["perks"].update(
                {
                    "Food": auxilio_alimentacao,
                    "Health": auxilio_saude,
                    "Subsistence": ajuda_custo,
                    "VacationPecuniary": inden_conv_ferias_em_pecunia,
                    "PremiumLicensePecuniary": licenca_premio,
                    "HousingAid": auxilio_moradia
                }
            )

            emp["income"]["other"]["others"].update(
                {
                    "grat_encargo_curso_concurso": grat_encargo_curso_concurso,
                    "ind_licenca_premio_espec_nao_gozada": ind_licenca_premio_espec_nao_gozada,
                    "inden_conv_ferias_em_pecunia_com_1_3": inden_conv_ferias_em_pecunia_com_1_3,
                    "dif_terco_conv_ferias_pecunia": dif_terco_conv_ferias_pecunia,
                    "inden_conv_pec_licensa_especial": inden_conv_pec_licensa_especial,
                    "dif_pen_alimenticia": dif_pen_alimenticia,
                    "dif_subs_cumulativa": dif_subs_cumulativa,
                    "dif_inden_conv_pec_lic_comp_subs_cumul_membro": dif_inden_conv_pec_lic_comp_subs_cumul_membro,
                    "inden_conv_pec_lic_compensatoria_subs_cumul_membro": inden_conv_pec_lic_compensatoria_subs_cumul_membro,
                    "dif_ress_conv_mestrado_int_direito": dif_ress_conv_mestrado_int_direito,
                    "ress_conv_mestrado_int_direito": ress_conv_mestrado_int_direito,
                    "dif_subsidios": dif_subsidios,
                    "dif_abono_permanencia": dif_abono_permanencia,
                    "resp_direcao_promotoria": resp_direcao_promotoria,
                    "subs_cumulativa": subs_cumulativa,
                    "dif_gratificacao_por_funcao_ministerio_publico": dif_gratificacao_por_funcao_ministerio_publico,
                    "dif_resp_direcao_promotoria": dif_resp_direcao_promotoria,
                    "dif_direcao_promotoria": dif_direcao_promotoria,
                    "subs_funcao_minis_pub": subs_funcao_minis_pub,
                    "dif_terco_const_ferias": dif_terco_const_ferias,
                    "dif_13_salario": dif_13_salario,
                    "direcao_promotoria": direcao_promotoria


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