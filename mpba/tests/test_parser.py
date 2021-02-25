from datetime import datetime
from mpba.parser import build_crawler_result, parse, _status
import pytest


payload = [
    {
        "dsCargo": "DIGITADOR",
        "dsLotacao": "PJR DE PAULO AFONSO - APOIO TECNICO E ADMINISTRATIVO",
        "nmServidor": "IGOR ANDREYSON MENDES LOPES",
        "nuAnoReferencia": 2020,
        "nuMatricula": 904023,
        "nuMesReferencia": 1,
        "vlDescIR": 2428.29,
        "vlDescPrevidencia": 1952.1,
        "vlDescTeto": 0.0,
        "vlDescTotalBruto": 4380.39,
        "vlIdenizacoes": 1300.0,
        "vlOutrasRemun": 0.0,
        "vlRendAbonoPerman": 0.0,
        "vlRendCargoComissao": 7093.93,
        "vlRendCargoEfetivo": 6392.39,
        "vlRendFerias": 0.0,
        "vlRendGratNatalina": 0.0,
        "vlRendTotalBruto": 15243.57,
        "vlRendTotalLiquido": 10863.18,
        "vlRendVerbas": 457.25,
    }
]


def test_parse_payload_to_employee():
    expected_perks = {
        "total": 1300.0,
        "food": None,
        "vacation": 0.0,
        "transportation": None,
        "pre_school": None,
        "health": None,
        "birth_aid": None,
        "housing_aid": None,
        "subsistence": None,
        "compensatory_leave": None,
        "pecuniary": None,
        "vacation_pecuniary": None,
        "furniture_transport": None,
        "premium_license_pecuniary": None,
    }
    expected_funds = {
        "total": 24094.75,
        "personal_benefits": 0.0,
        "eventual_benefits": 1300.0,
        "trust_position": 7093.93,
        "daily": None,
        "gratification": 0.0,
        "origin_pos": 15243.57,
        "others_total": 457.25,
        "others": 0.0,
    }
    expected_discounts = {
        "total": 4380.39,
        "prev_contribution": 1952.1,
        "ceil_retention": 0.0,
        "income_tax": 2428.29,
        "others_total": None,
        "other": None,
    }
    expected_income = {
        "total": 31787.14,
        "wage": 6392.39,
        "perks": expected_perks,
        "other": expected_funds,
    }
    expected_employee = {
        "reg": 904023,
        "name": "IGOR ANDREYSON MENDES LOPES",
        "role": "DIGITADOR",
        "type": "servidor",
        "workplace": "PJR DE PAULO AFONSO - APOIO TECNICO E ADMINISTRATIVO",
        "active": True,
        "income": expected_income,
        "discounts": expected_discounts,
    }

    assert parse(payload) == [expected_employee]


def test_raise_exception_when_payload_is_invalid():
    with pytest.raises(Exception):
        parse(None)


@pytest.mark.parametrize(
    "workplace,expected_status",
    [
        ("PJR DE PAULO AFONSO - APOIO TECNICO E ADMINISTRATIVO", True),
        ("Inativo", False),
        ("NACRES - PERICIA", True),
        ("INATIVO", False),
    ],
)
def test_get_status(workplace, expected_status):
    assert _status(workplace) is expected_status


def test_crawler_result(monkeypatch):
    expected_git_commit = "a1b2c3"
    monkeypatch.setenv("GIT_COMMIT", expected_git_commit)
    employees = parse(payload)
    filepath = ["output/mpba-5-2020.json"]
    expected_crawler_result = {
        "aid": "mpba",
        "month": 1,
        "year": 2020,
        "crawler": {
            "id": "mpba",
            "version": expected_git_commit,
        },
        "files": filepath,
        "employees": employees,
        "timestamp": datetime.now().astimezone().replace(microsecond=0).isoformat(),
    }

    crawler_result = build_crawler_result(1, 2020, employees, filepath)
    assert crawler_result.keys() == expected_crawler_result.keys()
    assert crawler_result["aid"] == expected_crawler_result["aid"]
    assert crawler_result["month"] == expected_crawler_result["month"]
    assert crawler_result["year"] == expected_crawler_result["year"]
    assert crawler_result["employees"] == expected_crawler_result["employees"]
    assert crawler_result["timestamp"] == expected_crawler_result["timestamp"]
    assert (
        crawler_result["crawler"]["id"]
        == expected_crawler_result["crawler"]["id"]
    )
    assert (
        crawler_result["crawler"]["version"]
        == expected_crawler_result["crawler"]["version"]
    )
