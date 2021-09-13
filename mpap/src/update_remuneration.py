from table import clean_cell


class UpdateRemuneration:
    def __init__(self, remuneration, indemnization):
        self.remuneration = remuneration
        self.indemnization = indemnization

    def update(self):
        for row in self.indemnization:
            matricula = row[0]
            if type(matricula) != str:
                matricula = str(matricula)

            if matricula in self.remuneration.keys():

                # Verbas Indenizatorias
                auxilio_saude = clean_cell(row[4])
                auxilio_doenca = clean_cell(row[5])
                auxilio_moradia= clean_cell(row[6])
                auxilio_alimentacao = clean_cell(row[7])
                licenca_premio = clean_cell(row[8])
                ferias_indenizadas = clean_cell(row[9])

                abono_pecuniario = clean_cell(row[10])
                resseco_administrativo = clean_cell(row[11])
                dif_indenizada = clean_cell(row[12])
                plantao_indenizado = clean_cell(row[13])

                # Remunerações Temporárias
                substituicao = clean_cell(row[15])
                hora_extra = clean_cell(row[16])
                plantao = clean_cell(row[17])
                dif_recebimentos = clean_cell(row[18])
                cumulacao = clean_cell(row[19])
                devolucoes_descontos = clean_cell(row[20])

                gratificacoes = clean_cell(row[21])
                
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