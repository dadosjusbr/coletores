import json
import pathlib
import sys
import os

def read_data(path):
    try:
        with open((pathlib.Path(path)), 'r') as arq:
            data = json.load(arq)
            return data
    except Exception as excep:
        sys.stderr.write("'Não foi possível ler o arquivo: " +
                        path + '. O seguinte erro foi gerado: ' + excep)
        os._exit(1)

def conv(name):
    nome = str(name)
    return nome.strip()

def parse(arq):
    employees = []
    caminho = read_data(arq)

    for item in caminho:
        reg = item['Nome'] # Identificação do membro (Nome)
        role = item['Cargo'] #Cargo
        workplace = item['Lotação'] #Lotação
        remuneration = item['RemuneracaoCargoEfetivo'] #Remuneração do Cargo Efetivo
        other_verbs = item['OutrasVerbasRemuneratoriasLegaisJudiciais'] #Outras Verbas Remuneratórias Legais/Judiciais
        trust_pos = item['FuncaoConfiancaCargoComissao']  #Função de Confiança ou Cargo em Comissão 
        decimo = 0 #13o. Salário 
        ferias = item['Ferias'] #Adicional de Férias
        abono_permanencia = item['AbonoPermanencia'] #Abono de Permanência
        temp_remu = 0 #Outras Remunerações Temporárias
        idemnity = 0 #Verbas Indenizatórias
        total = item['TotalRendimentosBruto'] #Total de rendimentos brutos 
        prev_contrib = item['ContribuicaoPrevidenciaria'] #Contribuição Previdenciária
        imposto_renda = item['ImpostoRenda'] #Imposto de Renda
        ceil_ret = item['RetencaoTetoConstitucional'] #Retenção do Teto      

        employees.append({
                'reg': conv(reg),
                'name': conv(reg),
                'role': conv(role),
                'type': 'membro',
                'workplace': conv(workplace),
                'active': True,
                "income":
                {
                    'total': total,
                    'wage': remuneration + other_verbs,
                    'perks':{
                        'total': idemnity,
                    },
                    'other':
                    { 
                        'total': trust_pos + decimo + ferias + abono_permanencia + temp_remu,
                        'trust_position': trust_pos,
                        'eventual_benefits': temp_remu,
                        'others_total': decimo + ferias + abono_permanencia,
                        'others': {
                            '13o. Salário': decimo,
                            'Adicional de Férias': ferias,
                            'Abono de permanência': abono_permanencia,
                        }
                    },

                },
                'discounts':
                {
                    'total': round(prev_contrib + ceil_ret + imposto_renda, 2),
                    'prev_contribution': prev_contrib,
                    'ceil_retention': ceil_ret,
                    'income_tax': imposto_renda
                }
            })

    return employees
