from datetime import datetime
import os
import csv

def build_crawler_result(month, year, employees, files):
    return {
        "aid": "mpba",
        "month": int(month),
        "year": int(year),
        "files": files,
        "crawler": {
            "id": "mpba",
            "version": os.getenv("GIT_COMMIT"),
        },
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
            "total": round(item["vlIdenizacoes"], 2),
            "vacation": item["vlRendFerias"],
        }
        funds = {
            "personal_benefits": item["vlRendAbonoPerman"],
            "eventual_benefits": item["vlIdenizacoes"],
            "trust_position": item["vlRendCargoComissao"],
            "gratification": item["vlRendGratNatalina"],
            "origin_pos": item["vlRendTotalBruto"],
            "others_total": item["vlRendVerbas"],
            "others": item["vlOutrasRemun"],
        }
        funds["total"] = round(sum_up_from(funds), 2)
        income = {
            "wage": item["vlRendCargoEfetivo"],
            "perks": perks,
            "other": funds,
        }
        income["total"] = round(income["wage"] + income["perks"]["total"] + income["other"]["total"], 2)

        discounts = {
            "total": round(item["vlDescTotalBruto"], 2),
            "prev_contribution": item["vlDescPrevidencia"],
            "ceil_retention": item["vlDescTeto"],
            "income_tax": item["vlDescIR"],
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
    return list(employees)


def _status(workplace):
    return workplace.lower() != "inativo"
