

nan = float('nan')
# Strange way to check nan. Only I managed to make work
# Source: https://stackoverflow.com/a/944712/5822594
def is_nan(string):
    return string != string

def get_begin_row(rows, begin_string):
    begin_row = 0
    for row in rows:
        begin_row += 1
        if isinstance(row[0], str) and begin_string in row[0]:
            break
    # We need to continue interate until wee a value that is not
    # whitespace. That happen due to the spreadsheet formatting.
    while is_nan(rows[begin_row][0]):
        begin_row += 1
    return begin_row

def get_end_row(rows, begin_row, end_string):
    end_row = 0
    for row in rows:
        # First goes to begin_row.
        if end_row < begin_row:
            end_row += 1
            continue
        # Then keep moving until find a blank row.
        if isinstance(row[0], str) and end_string in row[0]:
            break
        if is_nan(row[0]):
            break
        end_row += 1
    return end_row

# After extracting the data, we need to delete the 'nan' fields, 
# resulting in lists with only valid data.
# Ex: [Maria, nan, nan, 29000] -> [Maria, 29000]
def treat_rows(rows): 
  emps_clean = []
  begin_string = "Matrícula"
  end_string = "TOTAL GERAL"
  begin_row = get_begin_row(rows, begin_string)
  end_row = get_end_row(rows, begin_row, end_string)
  for row in rows:
    emp_clean = [x for x in row if str(x) != 'nan']
    emps_clean.append(emp_clean)
  return emps_clean[begin_row:end_row]

def type_employee(fn):
    if 'membros' in fn:
        return 'membro'
    if 'servidores' in fn:
        return 'servidor'
    if 'pensionistas' in fn:
        return 'pensionista'
    if 'colaboradores' in fn:
        return 'colaborador'
    raise ValueError('Tipo de inválido de funcionário público: ' + fn)

#Metodo auxiliar responsável pela tradução do numero do mês em String
def get_month_name(month):
    months = { 1:'Janeiro' , 
               2:'Fevereiro' , 
               3:'Março', 
               4:'Abril', 
               5:'Maio', 
               6:'Junho', 
               7:'Julho', 
               8:'Agosto', 
               9:'Setembro', 
              10:'Outubro', 
              11:'Novembro', 
              12:'Dezembro'
            }
    return months[month]