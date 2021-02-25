from datetime import datetime
import os
import csv

def build_crawler_result(month, year, employees, files):
    return {
        "aid": "mpba",
        "month": int(month),
        "year": int(year),
        "crawler": {
            "id": "mpba",
            "version": os.getenv("GIT_COMMIT"),
        },
        "files": files,
        "employees": employees,
        "timestamp": datetime.now().astimezone().replace(microsecond=0).isoformat(),
    }


def sum_up_from(values):
    return sum([
        value
        for key, value in values.items()
        if key != "total" and value is not None
    ])

# Retorna uma copia do csv em memória.
def read_roles():
    types = {}
    with open('./roles.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            types[row['role']] = row['type']
    return types
            
def parse(payload):
    employees = []
    types = read_roles()
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
            "personal_benefits": item["vlRendAbonoPerman"],
            "eventual_benefits": item["vlIdenizacoes"],
            "trust_position": item["vlRendCargoComissao"],
            "daily": None,
            "gratification": item["vlRendGratNatalina"],
            "origin_pos": item["vlRendTotalBruto"],
            "others_total": item["vlRendVerbas"],
            "others": item["vlOutrasRemun"],
        }
        funds["total"] = sum_up_from(funds)
        income = {
            "wage": item["vlRendCargoEfetivo"],
            "perks": perks,
            "other": funds,
        }
        income["total"] = income["wage"] + income["perks"]["total"] + income["other"]["total"]

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
            "type": types[item['dsCargo']],
            "workplace": item["dsLotacao"],
            "active": _status(item["dsLotacao"]),
            "income": income,
            "discounts": discounts,
        }
        employees.append(employee)
    return employees


def _status(workplace):
    return workplace.lower() != "inativo"
