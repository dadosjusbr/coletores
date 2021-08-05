import pandas as pd

# Quando se ler um documento odt, ele não fica no formato ods, 
# esse codigo transaforma ele no formato ods, para ficar mais facil de trabalhar
def together_array(file_odt):
    df = pd.read_excel(file_odt, engine='odf', sheet_name=None)
    new_array = []
    
    for i, e in df.items():
        for j in e.to_numpy():
            new_array.append(j)
            
    return new_array