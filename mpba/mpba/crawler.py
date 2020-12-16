import requests


BASE_URL = "https://lai-app.sistemas.mpba.mp.br/api/quadroremuneratoriogeral/consultar?mes={}&ano={}&cargo=0"


def crawl(month, year):
    response = requests.get(BASE_URL.format(month, year))
    response.raise_for_status()
    return response.json()
