"""
Versão totalmente de demonstração haha
"""

from table import test_error
import pandas as pd
import sys


def generate_total(data):
    total_temporario = round(
            data['grat_encargo_curso_concurso']
            + data['ind_licenca_premio_espec_nao_gozada']
            + data['inden_conv_ferias_em_pecunia_com_1_3']
            + data['dif_terco_conv_ferias_pecunia']
            + data['inden_conv_pec_licensa_especial']
            + data['dif_pen_alimenticia']
            + data['dif_subs_cumulativa']
            + data['dif_inden_conv_pec_lic_comp_subs_cumul_membro']
            + data['inden_conv_pec_lic_compensatoria_subs_cumul_membro']
            + data['dif_ress_conv_mestrado_int_direito']
            + data['ress_conv_mestrado_int_direito']
            + data['dif_subsidios']
            + data['dif_abono_permanencia']
            + data['resp_direcao_promotoria']
            + data['subs_cumulativa']
            + data['dif_gratificacao_por_funcao_ministerio_publico']
            + data['dif_resp_direcao_promotoria']
            + data['dif_direcao_promotoria']
            + data['subs_funcao_minis_pub']
            + data['dif_terco_const_ferias']
            + data['dif_13_salario']
            + data['direcao_promotoria'], 2
        ),
    return total_temporario


def get_values_of_table_csv(row):
    # Nome das colunas, que vem nas tabelas
    data = {
        'ajuda_custo': test_error(row,'Ajuda de custo'),
        'auxilio_saude': test_error(row,'Assistência médico-social (auxílio-saúde) Membro MP'),
        'dif_auxilio_saude': test_error(row,'Dif. Assistência médico-social (auxílio-saúde) Membro MP'),
        'grat_encargo_curso_concurso': test_error(row,'Grat. por Encargo de Curso ou Concurso'),
        'auxilio_alimentacao': test_error(row, 'Auxílio-alimentação Membro MP'),
        'dif_auxilio_alimentacao': test_error(row,'Dif. Auxílio-alimentação Membro MP'),
        'licenca_premio': test_error(row,'Ind Licenca Premio/Espec Nao Gozada'),
        'auxilio_moradia': test_error(row,'Auxilio-moradia Membro MP'),
        'ind_licenca_premio_espec_nao_gozada': test_error(row,'Ind Licenca Premio/Espec Nao Gozada'),
        'inden_conv_ferias_em_pecunia_com_1_3': test_error(row,'Inden. Conv. Férias em Pecúnia (com 1/3 Const)'),
        'inden_conv_ferias_em_pecunia': test_error(row,'Inden. Conv. Férias em Pecúnia'),
        'dif_terco_conv_ferias_pecunia': test_error(row,'Dif. Terço Conv. Pecúnia Férias')           ,
        'inden_conv_pec_licensa_especial': test_error(row,'Indenização - Conv. em Pec. da Licença Especial'),
        'dif_pen_alimenticia': test_error(row,'Dif. Pen. Aliment.-2')            ,
        'dif_subs_cumulativa': test_error(row,'Dif. Substituição Cumulativa Membro MP'),
        'dif_inden_conv_pec_lic_comp_subs_cumul_membro': test_error(row,'Dif. Inden. Conv. Pec. Lic. Comp. Subs. Cumul. Membro'),
        'inden_conv_pec_lic_compensatoria_subs_cumul_membro': test_error(row,'Inden. Conv. Pec. Lic. Compensatoria Subs. Cumul. Membro'),
        'dif_ress_conv_mestrado_int_direito': test_error(row,'Dif. RESS. Conv. Mestrado Int. Direito MINTER UNDB'),
        'ress_conv_mestrado_int_direito': test_error(row, 'RESS. Conv. Mestrado Int. Direito MINTER UNDB'),
        'dif_subsidios': test_error(row,'Dif. Subsídios'),
        'dif_abono_permanencia': test_error(row,'Dif. Abono de Permanência'),
        'direcao_promotoria': test_error(row,'Direção de Promotoria'),
        'resp_direcao_promotoria': test_error(row,'RESP. Direção de Promotorias'),
        'subs_cumulativa': test_error(row,'Substituição Cumulativa Membro MP'),
        'dif_gratificacao_por_funcao_ministerio_publico': test_error(row,'Dif. Gratificação por Função Mininistério Público'),
        'dif_resp_direcao_promotoria': test_error(row,'Dif. RESP. Direção de Promotorias'),
        'dif_direcao_promotoria': test_error(row,'Dif. Direção de Promotoria'),
        'subs_funcao_minis_pub': test_error(row,'SUBS. Função Ministério Público'),
        'dif_terco_const_ferias': test_error(row,'Dif. Terço Constitucional de Férias'),
        'dif_13_salario': test_error(row,'Dif. 13º Salário')
        
    }

    total_temporario = generate_total(data)[0] # pego o valor de dentro da tupla
    data.update({'total_temporario': total_temporario})

    return data


def generate_json(emp, data):
    emp["income"]["perks"].update(
        {
            "Food": data['auxilio_alimentacao'],
            "Health": data['auxilio_saude'],
            "Subsistence": data['ajuda_custo'],
            "VacationPecuniary": data['inden_conv_ferias_em_pecunia'],
            "PremiumLicensePecuniary": data['licenca_premio'],
            "HousingAid": data['auxilio_moradia']
        }
    )

    emp["income"]["other"]["others"].update(
        {
            "grat_encargo_curso_concurso": data['grat_encargo_curso_concurso'],
            "ind_licenca_premio_espec_nao_gozada": data['ind_licenca_premio_espec_nao_gozada'],
            "inden_conv_ferias_em_pecunia_com_1_3": data['inden_conv_ferias_em_pecunia_com_1_3'],
            "dif_terco_conv_ferias_pecunia": data['dif_terco_conv_ferias_pecunia'],
            "inden_conv_pec_licensa_especial": data['inden_conv_pec_licensa_especial'],
            "dif_pen_alimenticia": data['dif_pen_alimenticia'],
            "dif_subs_cumulativa": data['dif_subs_cumulativa'],
            "dif_inden_conv_pec_lic_comp_subs_cumul_membro": data['dif_inden_conv_pec_lic_comp_subs_cumul_membro'],
            "inden_conv_pec_lic_compensatoria_subs_cumul_membro": data['inden_conv_pec_lic_compensatoria_subs_cumul_membro'],
            "dif_ress_conv_mestrado_int_direito": data['dif_ress_conv_mestrado_int_direito'],
            "ress_conv_mestrado_int_direito": data['ress_conv_mestrado_int_direito'],
            "dif_subsidios": data['dif_subsidios'],
            "dif_abono_permanencia": data['dif_abono_permanencia'],
            "resp_direcao_promotoria": data['resp_direcao_promotoria'],
            "subs_cumulativa": data['subs_cumulativa'],
            "dif_gratificacao_por_funcao_ministerio_publico": data['dif_gratificacao_por_funcao_ministerio_publico'],
            "dif_resp_direcao_promotoria": data['dif_resp_direcao_promotoria'],
            "dif_direcao_promotoria": data['dif_direcao_promotoria'],
            "subs_funcao_minis_pub": data['subs_funcao_minis_pub'],
            "dif_terco_const_ferias": data['dif_terco_const_ferias'],
            "dif_13_salario": data['dif_13_salario'],
            "direcao_promotoria": data['direcao_promotoria']
        }
    )

    emp["income"]["other"].update(
        {
            "others_total": round(
                emp["income"]["other"]["others_total"] +
                data['total_temporario'], 2
            ),
            "total": round(
                emp["income"]["other"]["total"] +
                data['total_temporario'], 2
            )
        }
    )  
    return emp


def update(remuneration, indemnization):

    try:
        df = pd.read_csv(indemnization)
    except Exception as excpt:
        sys.exit(str(excpt))

    for i, row in df.iterrows():
        matricula = row['Matrícula']
        if type(matricula) != str:
            matricula = str(matricula)

        if matricula in remuneration.keys():
            # Pega os valores da linha, e retorna já convertidos para float
            data = get_values_of_table_csv(row)
            emp = remuneration[matricula]
            # Atualiza o json de remunerações
            employer = generate_json(emp, data)
            remuneration[matricula] = employer

    return remuneration