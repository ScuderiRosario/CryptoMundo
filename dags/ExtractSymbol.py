import pandas as pd

def ex_symb(data):
    List_crpyto=pd.DataFrame(data, columns=['symbol'])
    List_crpyto=list(List_crpyto["symbol"])
    print(List_crpyto)
    return List_crpyto[:10]