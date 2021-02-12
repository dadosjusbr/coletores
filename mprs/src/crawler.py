import requests
import pathlib
import os

# Os tipos descritos abaixo são: M = Membros, MI = Membros inativos,
# S = Servidores, SI = Servidores Inativos, P = Pensionistas
beneficiary_types = {1: 'M',
                     2: 'MI',
                     3: 'S',
                     4: 'SI',
                     5: 'P',
                     6: 'estagiarios/',
                     7: 'verbas_indenizatorias_temporarias/'
                    }

# Os tipos descritos abaixo são as folhas de pagamento, que podem ser: 
# Normal, Complementar e 13 (décimo terceiro salário).
payroll_types = {1: 'NORMAL',
                 2: 'COMPLEMENTAR',
                 3: '13'
                }

base_URL = 'https://transparencia.mprs.mp.br/contracheque/'

# Gera a url de acesso às informações referentes as remunerações do mês e ano de um tipo de funcionário
def generate_remuneration_url(year, month):
    links = {}
    link = ""

    for key, value in beneficiary_types.items():
        if key < 6:
            for value_payroll in payroll_types.values():
                if ((month != '12') & (value_payroll == '13')):
                    break
                link = base_URL + "api/folha/?ano=" + year + "&mes=" + month + "&tipo_folha=" + value_payroll + "&tipo_pessoa=" + value
                links[value + "-" + value_payroll] = link
        elif key == 6:
            link = base_URL + value + "?ano=" + year + "&mes=" + month.lstrip("0") + "&procurar=+Procurar+#"
            links[value] = link
        else:
            link = base_URL + value + year + "/" + month + "/#"
            links[value] = link

    return links

def download(url, file_path):
    response = requests.get(url, allow_redirects=True, verify = False)
    with open(file_path, "wb") as file:
        file.write(response.content)
    file.close()

def crawl(year, month, output_path):
    urls_remunerations  = generate_remuneration_url(year,month)
    files = []

    for key, value in urls_remunerations.items():
        pathlib.Path(output_path).mkdir(exist_ok=True)

        if "verbas_indenizatorias_temporarias/" in key or "estagiarios/" in key:
            file_name = key + "-" + month + '-' + year + '.html'
        else:
            file_name = key + "-" + month + '-' + year + '.json'

        file_path = output_path + "/" + file_name.replace("/", "")
        download(value, file_path)
        files.append(file_path)

    return files