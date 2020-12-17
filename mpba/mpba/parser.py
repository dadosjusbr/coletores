from datetime import datetime
import os


def build_crawler_result(month, year, employees):
    return {
        "agencyID": "MP-BA",
        "month": month,
        "year": year,
        "crawler": {
            "crawlerID": "mpba",
            "crawlerVersion": os.getenv("GIT_COMMIT"),
        },
        "files": [],
        "employees": employees,
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "procInfo": None,
    }


def parse(payload):
    employees = []
    for item in payload:
        perks = {
            "total": item["vlIdenizacoes"],
            "food": None,
            "vacation": item["vlRendFerias"],
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
        funds = {
            "total": item["vlRendTotalLiquido"],
            "personal_benefits": item["vlRendAbonoPerman"],
            "eventual_benefits": item["vlIdenizacoes"],
            "trust_position": item["vlRendCargoComissao"],
            "daily": None,
            "gratification": item["vlRendGratNatalina"],
            "origin_pos": item["vlRendTotalBruto"],
            "others_total": item["vlRendVerbas"],
            "others": item["vlOutrasRemun"],
        }
        income = {
            "total": None,
            "wage": item["vlRendCargoEfetivo"],
            "perks": perks,
            "other": funds,
        }
        discounts = {
            "total": item["vlDescTotalBruto"],
            "prev_contribution": item["vlDescPrevidencia"],
            "ceil_retention": item["vlDescTeto"],
            "income_tax": item["vlDescIR"],
            "others_total": None,
            "other": None,
        }
        employee = {
            "reg": item["nuMatricula"],
            "name": item["nmServidor"],
            "role": item["dsCargo"],
            "type": None,
            "workplace": item["dsLotacao"],
            "active": _status(item["dsLotacao"]),
            "income": income,
            "discounts": discounts,
        }
        employees.append(employee)
    return employees


def _status(workplace):
    return workplace.lower() != "inativo"
