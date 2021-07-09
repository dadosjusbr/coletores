import requests
import pathlib
import sys
import os

base_url = 'https://sistemas.mpal.mp.br/transparencia/contracheque/index/'


def generate_remuneration_url(year, month):
    link = ''

    link = f"{base_url}'65?tipo=membrosativos&mes='{month}'&ano='{year}'&busca=&download=json'"

    return link


def download(url, file_path):
    try:
        response = requests.get(url, allow_redirects=True)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        file.close()

    except Exception as excep:
        sys.stderr.write(
            'Não foi possível fazer o download do arquivo: '
            + file_path
            + '. O seguinte erro foi gerado: '
            + excep
        )
        os._exit(1)


def crawl(year, month, output_path):
    urls_remunerations = generate_remuneration_url(year, month)

    pathlib.Path(output_path).mkdir(exist_ok=True)

    file_name = 'membros_ativos' + '-' + month + '-' + year + '.JSON'

    file_path = output_path + '/' + file_name.replace('/', '')
    download(urls_remunerations, file_path)
    file = file_path

    return file


