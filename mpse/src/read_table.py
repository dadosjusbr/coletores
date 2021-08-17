import pandas as pd

# Quando se ler um documento odt, ele não fica no formato ods, 
# esse codigo transaforma ele no formato ods, para ficar mais fácil de trabalhar
def read_odt(file_odt):
    df = pd.read_excel(file_odt, engine='odf', sheet_name=None, header=None)
    new_array = []
    
    for i, e in df.items():
        for j in e.to_numpy():
            new_array.append(j)
    return new_array

# Para ler ods
def read_ods(file_ods):
    df = pd.read_excel(file_ods, engine='odf').to_numpy()
    return df