import pandas as pd
import re
from rich import print
table = pd.read_html('https://en.wikipedia.org/wiki/Land_speed_record')

df = table[0]

df.columns = ['Date', 'Location', 'Driver', 'Vehicle', 'Power', '1 km(mph)', '1 km/h', '1 mile(mph)', '1 mile/h', 'Comments']
df['Comments'] = df['Comments'].apply(lambda x: re.sub(r'\[\d+\]', '', str(x)))
df['1 km(mph)'] = df['1 km(mph)'].replace('—', '')
df['1 km/h'] = df['1 km/h'].replace('—', '')
# df = df.drop(columns=['Comments'])
df.to_excel('output.xlsx', index=False)