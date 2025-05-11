import pandas as pd
import json

with open('json_data.json', 'r') as f:
    data = json.load(f)

all_data = []

for item in data.get('pois', []):
    title = item.get('title', [])
    title_name = ''
    for t in title:
        if t.get('lang') == 'EN':
            title_name = t.get('value', '')

    phone = item.get('contact', {}).get('phone', '')
    Email = item.get('contact', {}).get('email', '')
    if title_name:
        details = {
            "title": title_name,
            "Phone" : phone,
            "Email" : Email
        }
        all_data.append(details) 
df = pd.DataFrame(all_data)
df.dropna(how='all', inplace=True)
df.drop_duplicates(inplace=True)
df.to_excel('Practice.xlsx', index=False)
print(df.shape)