import pandas as pd

output = []

for i in range(0,66):
    url = f"https://www.austinisd.org/cp/conflict-of-interest-vendors/submitted-ciq-vendors?page={i}"
    
    table = pd.read_html(url)
    
    df = table[0]
    output.append(df)

df = pd.concat(output)
df = df.dropna(how="all")
df = df.drop_duplicates(subset="Vendor Name")
df.to_excel("Table_output.xlsx", index=False)