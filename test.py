import pandas as pd
import matplotlib.pyplot as plt

xls = pd.ExcelFile('Zadanie projektowe_Lingaro_dane.xlsx')
df1 = pd.read_excel(xls, 'Dostawca1')
df2 = pd.read_excel(xls, 'Dostawca 2')
df3 = pd.read_excel(xls, 'Dostawca 3')
df4 = pd.read_excel(xls, 'Dostawca 4')
df5 = pd.read_excel(xls, 'Dostawca 5')

suppliers = [df1, df2, df3, df4, df5]
all_suppliers = pd.DataFrame()
for i, df in enumerate(suppliers):
    all_suppliers[f's{i+1}'] = df['brakująca ilość']

all_suppliers.index += 1
all_suppliers.describe()

