import requests
import json
import pandas as pd
url = 'https://smarthistory.org/wp-json/smthstapi/v1/objects?tag=938&page={}'

headers = {
    "User-agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
}
all_data = []
page = 0
while True:
    response = requests.get(url.format(page), headers=headers)
    data = response.json()
    d = data['posts']
    if data.get('remaining') and int(data.get('remaining')) > 0:
        page +=1
    else:
        break;
    
    for i in d:
        URL = i.get('guid', {})  
        Title = i.get('title', {})
        Description=i.get('excerpt', {})
        details = {
            "URL":URL,
            "Title":Title,
            "Description":Description
        }
        all_data.append(details)
df = pd.DataFrame(all_data)
df.to_excel("output.xlsx", index=False)
print(df.shape)