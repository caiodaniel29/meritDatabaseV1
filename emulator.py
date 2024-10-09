import pandas as pd

path = r'C:\Users\caios\OneDrive\Documents\Merit Controls\Python\MC-AZA1-2100-0 IP Address Scheme.xlsx'

readfile = pd.read_excel(path, 'Inverters')

print(readfile.dropna())