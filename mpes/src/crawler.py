import requests
import sys
import os 
import pathlib

url_formats = {
    "remu":'https://www.mpes.mp.br/transparencia/informacoes/Contracheque/Remuneracao_de_Todos_os_Membros_Ativos.asp?precommand=Download&folder={}%5C&file={}+%2D+Planilha+Lei+de+acesso+{}+informa%C3%A7%C3%A3o+%2D+{}%2Exlsx',
    "vi": 'https://www.mpes.mp.br/transparencia/informacoes/Contracheque/Verbas_Indenizatorias_e_Outras_Remuneracoes_Temporarias.asp?precommand=Download&folder={}%5CMembro+Ativo{}%5C&file={}+%2D+Planilha+Lei+de+acesso+{}+informa%C3%A7%C3%A3o+%2D+{}%2Exlsx'
}

#Falso indica que a coleta é referente á um mês anterior, á outubro de 2018
#Verdadeiro indica que a coleta é referente a um mês posterior ou igual á outubro de 2018
url_code = {
    False: 'a',
    True : "%C3%A0",
}

months = {
    1: 'Janeiro',
    2: 'Fevereiro',
    3: 'Março',
    4: 'Abril',
    5: 'Maio',
    6: 'Junho',
    7: 'Julho',
    8: 'Agosto',
    9: 'Setembro',
    10: 'outubro',
    11: 'novembro',
    12: 'dezembro'
}

def download(url, file_path):
    try:
      response = requests.get(url, allow_redirects=True, verify=False)
      with open(file_path, "wb") as file:
          file.write(response.content)
      file.close()
    except Exception as excep:
        sys.stderr.write("Não foi possível fazer o download do arquivo: " + file_path + '. O seguinte erro foi gerado: ' + excep )
        os._exit(1)


def crawl(year, month, output_path):
    files = [] 
    
    if (int(month) < 10) and (int(year) == 2018 ):
        after_2018_ot = False
    else:
        after_2018_ot = True
    
    for key in url_formats:
        pathlib.Path(output_path).mkdir(exist_ok=True)
        file_name = year + '_' + month + '_' + key
        file_path = output_path + '/' + file_name + '.xlsx'
        
        #A partir de 2019 não há letras maiúsculas no nome dos meses, e existe um sufixo associado á categoria de Membros
        if key == 'vi':
            if int(year) >= 2019:
                sufix = '%2Dvi'
                url = url_formats[key].format(year, sufix, month, url_code[after_2018_ot], months[int(month)].lower())
            else:
                sufix = ''
                url = url_formats[key].format(year, sufix, month, url_code[after_2018_ot], months[int(month)])
        else:
            url = url_formats[key].format(year, month, url_code[after_2018_ot], months[int(month)])
    
        download(url, file_path)
        files.append(file_path)
    
    return files
        