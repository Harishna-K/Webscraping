import requests
import pandas as pd

url = 'https://map.abuzz.tech/api/medias/site/TDM_/map/cache/data.json?v=1739972607490'
headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Referer': 'https://map.abuzz.tech/amap/embedex.php?site=TDM_&apiKey=AC6B0D339940194AB7E2BC8E1967A4AE&searchUI=false&servicesList=false&baseui=false&poiUI=false&pathUI=false&hover=true&lazyld=false&mobile=true&node=TDM-FF-295',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}

response = requests.get(url, headers=headers)
datas = response.json()


details = datas['pois']
output = []

for item in details:
    
    titles = item.get('title', [])
    store_title = ''
    
    if len(titles) > 1:
        store_title = titles[1].get('value', '')  
    
    contact = item.get('contact', {})

    data = {
        "Store Name": store_title, 
        "Phone Number": contact.get('phone', ''),
        "Email Address": contact.get('email', '')
    }
    
    output.append(data)

df = pd.DataFrame(output)
df_cleaned = df.dropna(how="all")
df_cleaned = df.drop_duplicates()

df_cleaned.to_excel('contacts_cleaned.xlsx', index=False)

print(df_cleaned.shape)
