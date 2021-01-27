import requests
import pathlib
import os

# Os tipos descritos abaixo são: M = Membros, MI = Membros inativos,
# S = Servidores, SI = Servidores Inativos, P = Pensionistas
beneficiary_types = {1: 'M/',
                     2: 'MI/',
                     3: 'S/',
                     4: 'SI/',
                     5: 'P/',
                     6: 'estagiarios/',
                     7: 'verbas_indenizatorias_temporarias/'
                    }

# Os tipos descritos abaixo são as folhas de pagamento, que podem ser: 
# Normal, Complementar e 13 (décimo terceiro salário).
payroll_types = {1: 'NORMAL/',
                 2: 'COMPLEMENTAR/',
                 3: '13/'
                }

base_URL = 'https://transparencia.mprs.mp.br/contracheque/'

# Gera a url de acesso às informações referentes as remunerações do mês e ano de um tipo de funcionário
def generate_remuneration_url(year, month):
    links = {}
    link = ""

    for key, value in beneficiary_types.items():
        if key < 6:
            for value_payroll in payroll_types.values():
                link = base_URL + "download/" + value + year + "/" + month + "/" + value_payroll
                links[value + value_payroll] = link
        elif key == 6:
            link = base_URL + value + "?ano=" + year + "&mes=" + month.lstrip("0") + "&procurar=+Procurar+#"
            links[value] = link
        else:
            link = base_URL + value + year + "/" + month + "/#"
            links[value] = link

    return links

def download(url, file_path, cwd):
    response = requests.get(url, allow_redirects=True, verify = False)
    with open(cwd + file_path, "wb") as file:
        file.write(response.content)
    file.close()

def crawl(year, month, output_path):
    urls_remunerations  = generate_remuneration_url(year,month)
    files = []
    cwd = os.getcwd()

    for key, value in urls_remunerations.items():
        pathlib.Path(cwd + output_path).mkdir(exist_ok=True)
        file_name = key + month + '-' + year + '.csv'
        file_path = output_path + "/" + file_name.replace("/", "-")
        download(value, file_path, cwd)
        files.append(file_path)

    return files