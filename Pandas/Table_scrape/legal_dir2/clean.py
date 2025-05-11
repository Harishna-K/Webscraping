import pandas as pd

df = pd.read_excel("output.xlsx")

df = df.drop_duplicates()

df.to_excel("clean_data.xlsx", index=False)

print(df.shape)