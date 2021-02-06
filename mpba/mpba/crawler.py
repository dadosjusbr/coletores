import json
import pathlib
import requests


BASE_URL = "https://lai-app.sistemas.mpba.mp.br/api/quadroremuneratoriogeral/consultar?mes={}&ano={}&cargo=0"


def crawl(month, year):
    response = requests.get(BASE_URL.format(month, year))
    response.raise_for_status()
    return response.json()


def save(filename, payload, output_path):
    pathlib.Path(output_path).mkdir(exist_ok=True)
    file_path = f"{output_path}/{filename}"
    file_path = file_path.replace("//", "/")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=4)
    return file_path
