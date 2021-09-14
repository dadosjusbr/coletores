from table import clean_cell


class UpdateRemuneration:
    def __init__(self, remuneration, indemnization):
        self.remuneration = remuneration
        self.indemnization = indemnization

    def update(self):
        for i,row in self.indemnization.iterrows():
            matricula = row['Matrícula']
            if type(matricula) != str:
                matricula = str(matricula)

            if matricula in self.remuneration.keys():

                # Verbas Indenizatorias
                auxilio_saude = clean_cell(row['Auxílio_Saúde'])
                auxilio_doenca = clean_cell(row['Auxílio_Doença'])
                auxilio_moradia= clean_cell(row['Auxílio_Moradia'])
                auxilio_alimentacao = clean_cell(row['Auxílio_Alimentação'])
                licenca_premio = clean_cell(row['Licença_Prêmio'])
                ferias_indenizadas = clean_cell(row['Indenização_de_Férias'])

                abono_pecuniario = clean_cell(row['Abono_Pecuniário'])
                resseco_administrativo = clean_cell(row['Recesso_Administrativo'])
                dif_indenizada = clean_cell(row['Diferença_Indenizada'])
                plantao_indenizado = clean_cell(row['Plantão_indenizado'])

                # Remunerações Temporárias
                substituicao = clean_cell(row['Substituição'])
                hora_extra = clean_cell(row['Hora-Extra'])
                plantao = clean_cell(row['Plantão'])
                dif_recebimentos = clean_cell(row['Diferença_de_Recebimentos'])
                cumulacao = clean_cell(row['Cumulação'])
                devolucoes_descontos = clean_cell(row['Devoluções_de_Desconto'])

                gratificacoes = clean_cell(row['Gratificações'])
                
                total_temporario = (  
                    auxilio_doenca
                    + abono_pecuniario
                    + resseco_administrativo
                    + dif_indenizada
                    + plantao_indenizado
                    + substituicao
                    + hora_extra
                    + plantao
                    + dif_recebimentos
                    + cumulacao
                    + devolucoes_descontos
                )

                emp = self.remuneration[matricula]

                emp["income"]["perks"].update(
                    {
                        "Food": auxilio_alimentacao,
                        "Health": auxilio_saude,
                        "Vacation": ferias_indenizadas,
                        "HousingAid": auxilio_moradia,
                        "PremiumLicensePecuniary": licenca_premio,
                    }
                )

                emp["income"]["other"]["others"].update(
                    {
                        "Abono Pecuniário": abono_pecuniario,
                        "Auxílio Doença": auxilio_doenca,
                        "Recesso Administrativo": resseco_administrativo,
                        "Diferença Indenizada": dif_indenizada,
                        "Plantão indenizado": plantao_indenizado,
                        "Substituição": substituicao,
                        "Hora-Extra": hora_extra,
                        "Plantão": plantao,
                        "Diferença de Recebimentos": dif_recebimentos,
                        "Cumulação": cumulacao,
                        "Devoluções de Descontos": devolucoes_descontos,
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

                self.remuneration[matricula] = emp

        return self.remuneration