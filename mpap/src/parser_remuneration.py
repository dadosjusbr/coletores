from table import clean_cell


class Remuneration:
    def __init__(self, data):
        self.data = data

    def parser(self):
        employees = {}
        for i, row in self.data.iterrows():

            matricula = row['MATRÍCULA']

            if type(matricula) != str:
                matricula = str(matricula)

            if matricula == 'TOTAL GERAL':
                break

            nome = row['NOME']
            cargo_efetivo = row['CARGO']
            lotacao = row['LOTAÇÃO']
            remuneracao_cargo_efetivo = clean_cell(
                row['REMUNERAÇÃO_DO_CARGO_EFETIVO'])
            outras_verbas_remuneratorias = clean_cell(
                row['OUTRAS_VERBAS_REMUNERATÓRIAS_LEGAIS_OU_JUDICIAIS'])
            # Função de Confiança ou Cargo em Comissão
            confianca_comissao = clean_cell(
                row['FUNÇÃO_DE_CONFIANÇA_OU_CARGO_EM_COMISSÃO'])
            # Gratificação Natalina
            grat_natalina = abs(clean_cell(row['GRATIFICAÇÃO_NATALINA']))
            ferias = clean_cell(row['FÉRIAS(1/3_CONSTITUCIONAL)'])
            # Abono de Permanência
            permanencia = clean_cell(row['ABONO_PERMANÊNCIA'])
            # Remunerações tempórarias
            outras_remuneracoes_temporarias = clean_cell(
                row['OUTRAS_REMUNERAÇÕES_TEMPORÁRIAS'])
            # Indenizações
            total_indenizacao = clean_cell(row['VERBAS_INDENIZATÓRIAS'])
            # Contribuição Previdenciária
            previdencia = abs(clean_cell(row['CONTRIBUIÇÃO_PREVIDENCIÁRIA']))
            # Imposto de Renda
            imp_renda = abs(clean_cell(row['IMPOSTO_DE_RENDA']))
            # Retenção por Teto Constitucional
            teto_constitucional = abs(clean_cell(row['RETENÇÃO_TETO']))
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

            employees[matricula] = self.table(campos)

        return employees

    def table(self,campos):
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
