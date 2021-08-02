import json
import pathlib
import sys
import os


# Ler os arquivos json
def read_data(path):
    try:
        with open((pathlib.Path(path)), 'r') as arq:
            data = json.load(arq)
            return data
    except Exception as excep:
        sys.stderr.write("'Não foi possível ler o arquivo: " +
                         path + '. O seguinte erro foi gerado: ' + excep)
        os._exit(1)


# converte e remove os espaços em branco do incio e do fim da string
def conv(name):
    nome = str(name)
    return nome.strip()


def soma(*args):
    new_value = round(sum(args),2)
    return new_value


def parse(arq):
    employees = []
    data = read_data(arq)

    for item in data:
        # Identificação do membro (Nome), único identificador.
        name = item['Nome'] 
        # Cargo
        role = item['Cargo']  
        # Lotação
        workplace = item['Lotação']  
        # Remuneração do Cargo Efetivo
        remuneration = item['RemuneracaoCargoEfetivo'] 
        # Outras Verbas Remuneratórias Legais/Judiciais
        other_verbs = item['OutrasVerbasRemuneratoriasLegaisJudiciais']
        # Função de Confiança ou Cargo em Comissão
        trust_pos = item['FuncaoConfiancaCargoComissao']
        # Adicional de Férias
        ferias = item['Ferias']  
        # Abono de Permanência
        abono_permanencia = item['AbonoPermanencia']  
        # Outras Remunerações Temporárias
        temp_remu = soma(item['Insalubridade'], item['_RemuneracaoLei6773'], item['RemuneracaoLei6818'],
                         item['DifEntrancia'], item['RemuneracaoLei6773/Ato9/2012'],
                         item['Remuneracao/Ato9/112018'], item['CoordGruposTrabalho'], 
                         item['ParticComissaoProjetos'], item['RemunChefiaDirecaoAsses'],)  
        # Verbas Indenizatórias
        idemnity = soma(item['Aux_Alimentacao'], item['Aux_Transporte'], 
                        item['Aux_Moradia'], item['Aux_FeriasIndenizadas'], 
                        item['Aux_FeriasIndenizadasEstagio'])  
        # Total de rendimentos brutos
        total = item['TotalRendimentosBruto']  
        gratificao_natalina = item['GratificacaoNatalina']
        # Contribuição Previdenciária
        prev_contrib = item['ContribuicaoPrevidenciaria'] 
        # Imposto de Renda
        imposto_renda = item['ImpostoRenda']  
        # Retenção do Teto
        ceil_ret = item['RetencaoTetoConstitucional']  

        employees.append({
            'reg': '',
            'name': conv(name),
            'role': conv(role),
            'type': 'membro',
            'workplace': conv(workplace),
            'active': True,
            'income':{
                'total': total,
                'wage': round(remuneration + other_verbs, 2),
                'perks': {
                    'total': idemnity,
                    'vacation': ferias
                },
                'other':{
                    'total': round(trust_pos + ferias + abono_permanencia + temp_remu, 2),
                    'trust_position': trust_pos,
                    'others_total': round(ferias + abono_permanencia + gratificao_natalina + temp_remu, 2),
                    'others': {
                        'Gratigicação natalina': gratificao_natalina,
                        'Abono de permanência': abono_permanencia,
                        'Outras Remunerações Temporárias': temp_remu
                    }
                },
            },
            'discounts':{
                'total': round(prev_contrib + ceil_ret + imposto_renda, 2),
                'prev_contribution': prev_contrib,
                'ceil_retention': ceil_ret,
                'income_tax': imposto_renda
            }
        })

    return employees
