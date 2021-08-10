import requests
import pathlib
import sys
import os

# Keys usadas para baixar as planilhas, cada uma corresponde a um ano mês
# Formatos em ods e odt
keys_remuneration = {
    # Aqui é formarto ods
    '2018': {
        '1': 56421,
        '2': 56423,
        '3': 56425,
        '4': 56894,
        '5': 56897,
        '6': 57398,
        '7': 57910,
        '8': 58383,
        '9': 58865,
        '10': 60307,
        '11': 60308,
        '12': 61432
    },
    # Aqui é formato odt
    '2019': {
        '1': 61431,
        '2': 61479,
        '3': 64797,
        '4': 64798,
        '5': 64799,
        '6': 64800,
        '7': 64801,
        '8': 64802,
        '9': 65280,
        '10': 65629,
        '11': 66225,
        '12': 66458
    },
    '2020': {
        '1': 67041,
        '2': 67489,
        '3': 67736,
        '4': 67987,
        '5': 68221,
        '6': 68469,
        '7': 68889,
        '8': 69309,
        '9': 69650,
        '10': 70347,
        '11': 70892,
        '12': 71278
    },
    '2021': {
        '1': 71898,
        '2': 72385,
        '3': 72635,
        '4': 73091,
        '5': 73484,
        '6': 73802
    }
}

# Tudo em ods
keys_indemnisation = {
    '2019': {
        '7': 64806,
        '8': 64807,
        '9': 65281,
        '10': 65281,
        '11': 66226,
        '12': 66459
    },
    '2020': {
        '1': 67042,
        '2': 67576,
        '3': 67737,
        '4': 67988, 
        '5': 68220,
        '6': 68471,
        '7': 68894,
        '8': 69314,
        '9': 69656,
        '10': 70352,
        '11': 70936,
        '12': 71287
    }, 
    '2021': {
        '1': 71905,
        '2': 72390,
        '3': 72640,
        '4': 73097,
        '5': 73490,
        '6': 73811
    }
}

def return_base():
    return 'https://sistemas.mpse.mp.br/2.0/PublicDoc/PublicacaoDocumento/AbrirDocumento.aspx?cd_documento={}'


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


def generate_url_remuneration(year, month):
    for years, months in keys_remuneration.items():
        if str(year) == years:
            for y, m in months.items():
                # Pegando as keys se os meses forem iguais
                if str(month) == y:
                    url = return_base().format(m)
                    return url


def generate_url_indemnisation(year, month):
    for years, months in keys_indemnisation.items():
        if str(year) == years:
            for y, m in months.items():
                # Pegando as keys se os meses forem iguais
                if str(month) == y:
                    url = return_base().format(m)
                    return url


def file_dowload_ods(year, month, output_path, url_remuneration, indemnisation = False):
    name = ''
    pathlib.Path(output_path).mkdir(exist_ok=True)

    if indemnisation: 
        name = 'indenizacao-membros-ativos'
    else:
        name = 'remuneracao-membros-ativos' 
    
    file_name = name + '-' + month + '-' + year + '.ods'
    file_path = output_path + '/' + file_name
    download(url_remuneration, file_path)
    return file_path


def file_dowload_odt(year, month, output_path, url_remuneration):
    pathlib.Path(output_path).mkdir(exist_ok=True)
    file_name = 'remuneracao-membros-ativos' + '-' + month + '-' + year + '.odt'
    file_path = output_path + '/' + file_name
    download(url_remuneration, file_path)
    return file_path


def crawl(year, month, output_path):
    url_remuneration = generate_url_remuneration(year, month)
    files = []

    if int(year) == 2018:
        # Para pegar os documentos em ods
        file_path = file_dowload_ods(year, month, output_path, url_remuneration)
        files.append(file_path)

    else:
        if int(year) == 2019 and int(month) >= 7 or int(year)>= 2020:
            print('aqui')
            url_indemnisation = generate_url_indemnisation(year, month)
            # Para pegar os que são dois arquivos juntos remuneração e indenização
            # vai ser uma lista:

            file_path = file_dowload_ods(year, month, output_path, url_indemnisation, True)
            files.append(file_path)
            
            file_path = file_dowload_odt(year, month, output_path, url_remuneration)
            files.append(file_path)
            
        else:
            # aqui vai pega só do mês 1 ao 6 de 2019
            file_path = file_dowload_odt(year, month, output_path, url_remuneration)
            files.append(file_path)

    return files
