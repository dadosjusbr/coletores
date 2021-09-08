import table
from construtor_tabela import tabela

def parse(file):
    employees = {}
 
    begin_row = table.get_begin_row(file, 'matrícula')
    curr_row = 0

    for row in file:
        curr_row += 1
        if curr_row <= begin_row:
            continue
        
        if str(row[1]).lower() == 'total geral':
                break
        matricula = row[0]
        if type(matricula) != str:
            matricula = str(matricula)

        nome = row[1]
        cargo_efetivo = table.this_nan(row[2])
        lotacao = table.this_nan(row[3])
        # grupo = row[4]
        remuneracao_cargo_efetivo = float(table.clean_cell(row[5]))
        outras_verbas_remuneratorias = table.clean_cell(row[6])
        # Função de Confiança ou Cargo em Comissão
        confianca_comissao = table.clean_cell(row[7])
        # Gratificação Natalina
        grat_natalina = table.clean_cell(row[8])
        ferias = table.clean_cell(row[9])
        permanencia = table.clean_cell(row[10])  # Abono de Permanência
        # Remunerações tempórarias
        outras_remuneracoes_temporarias = table.clean_cell(row[12])
        # Indenizações
        total_indenizacao = table.clean_cell(row[11])
        # Contribuição Previdenciária
        previdencia = table.clean_cell(row[14])
        # Imposto de Renda
        imp_renda = table.clean_cell(row[15])
        # Retenção por Teto Constitucional
        teto_constitucional = table.clean_cell(row[16])
        outros_descontos = table.clean_cell(row[17])

        employees[matricula] = tabela(matricula, nome, cargo_efetivo, lotacao, remuneracao_cargo_efetivo,
            outras_verbas_remuneratorias, confianca_comissao, grat_natalina, ferias, permanencia,
            outras_remuneracoes_temporarias, total_indenizacao, previdencia, imp_renda,
            teto_constitucional, outros_descontos)

    return employees