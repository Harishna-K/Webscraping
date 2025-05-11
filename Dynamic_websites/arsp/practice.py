import pandas as pd

table = pd.read_html('new.html')
df = table[0]
df = df.dropna(how="all")
print(df) 