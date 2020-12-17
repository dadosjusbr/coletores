from mpba.crawler import crawl
from unittest.mock import patch


def test_crawl():
    expected_url = "https://lai-app.sistemas.mpba.mp.br/api/quadroremuneratoriogeral/consultar?mes=1&ano=2020&cargo=0"
    with patch("mpba.crawler.requests.get") as mock_method:
        mock_method.return_value.json.return_value = {}
        crawl(1, 2020)
    mock_method.assert_called_once_with(expected_url)
