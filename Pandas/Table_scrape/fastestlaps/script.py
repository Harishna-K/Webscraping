import pandas as pd
from rich import print
df = pd.read_html('https://fastestlaps.com/tracks/le-mans-bugatti')

print(df[0])

df[0].to_excel('output.xlsx', index=False)