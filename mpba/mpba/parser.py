from datetime import datetime
import os
import csv

def build_crawler_result(month, year, employees, files):
    return {
        "agencyID": "mpba",
        "month": month,
        "year": year,
        "crawler": {
            "crawlerID": "mpba",
            "crawlerVersion": os.getenv("GIT_COMMIT"),
        },
        "files": files,
        "employees": employees,
        "timestamp": datetime.now().astimezone().replace(microsecond=0).isoformat(),
        "procInfo": None,
    }


def sum_up_from(values):
    return sum([
        value
        for key, value in values.items()
        if key != "total" and value is not None
    ])

#Infere o tipo de funcionário a partir do seu cargo.
def get_func_type(cargo):
    with open('./roles.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['role'] == cargo :
                return row['type']
            
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
        employee_type = get_func_type(item["dsCargo"])
        employee = {
            "reg": item["nuMatricula"],
            "name": item["nmServidor"],
            "role": item["dsCargo"],
            "type": employee_type,
            "workplace": item["dsLotacao"],
            "active": _status(item["dsLotacao"]),
            "income": income,
            "discounts": discounts,
        }
        employees.append(employee)
    return employees


def _status(workplace):
    return workplace.lower() != "inativo"
