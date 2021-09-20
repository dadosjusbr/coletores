import requests
import pathlib
import sys
import os

URL_REMUNERACOES = 'https://mpmt.mp.br/transparencia/gerar-plan-contracheque-r148.php?action=consultar&tipo=1'
URL_VERBAS_INDENIZATORIAS = 'https://mpmt.mp.br/transparencia/gerar-plan-indenizacoes-outras-remuneracoes-temporarias.php?action=consultar&tipo=8'


def generate_url(url, year, month):
    return f'{url}&mes={month}&ano={year}'


def generate_name(url, month, year):
    if url == URL_REMUNERACOES:
        return f'{month}-{year}-remuneracao-membros-ativos.ods'
    else:
        return f'{month}-{year}-verbas-indenizatorias-membros-ativos.ods'


def download(url, file_path):
    try:
        response = requests.get(url, allow_redirects=True)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        file.close()

    except Exception as excep:
        sys.exit(
            'Não foi possível fazer o download do arquivo: '
            + file_path
            + '. O seguinte erro foi gerado: '
            + str(excep)
        )


def crawl(year, month, output_path):
    # Quando um numero por ex.: 8 é passado para str ele fica '08',
    # mas a url só aceita o numero sem o '0' na frente.
    month = month.replace('0', '') if month != '10' else month
    # Cria a pasta output caso não exista.
    pathlib.Path(output_path).mkdir(exist_ok=True)
    files = []

    for url in [URL_REMUNERACOES, URL_VERBAS_INDENIZATORIAS]:
        url_generated = generate_url(
            url, year, month)
        file_name = generate_name(url, month, year)
        file_path = f'{output_path}/{file_name}'
        download(url_generated, file_path)
        files.append(file_path)

    return files
