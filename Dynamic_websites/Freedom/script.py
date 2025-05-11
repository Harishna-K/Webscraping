import requests
import pandas as pd
import json
from concurrent.futures import ThreadPoolExecutor
from rich import print

all_data = []

def Download_json(page):
    
    url = f'https://www.freedomunited.org/wp-json/u1/v2/speak-free?page={page}&_=1740421570406'

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    
    proxies={
    "http": "http://vwantbtc-rotate:igt0km7yu76c@p.webshare.io:80/",
    "https": "http://vwantbtc-rotate:igt0km7yu76c@p.webshare.io:80/"
    }
    
    response = requests.get(url, headers=headers, proxies=proxies)
    
    if response.status_code == 200:
        data = response.json()
        all_data.append(data)
        print(f'Page {page} Downloaded successfully...!')
    else:
        print(f"Failed to Download page:{page}. Status code:{response.status_code}")
        
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(Download_json, range(1,17))
    
with open("test.json", "w") as fp:
    json.dump(all_data, fp, indent=4)
    
def scrape_data():
    with open('test.json', 'r') as fp:
        Data = json.load(fp)
    output = []
    for item in Data:
        for subitem in item:
            URL = subitem.get('permalink', {})
            Title = subitem.get('title', {})
            PostDate = subitem.get('postdate', {})
            details = {
                "URL":URL,
                'TITLE':Title,
                "POST DATE" : PostDate
            }
            output.append(details)
            
    df = pd.DataFrame(output) 
    df.drop_duplicates()
    df.to_excel('Output_file.xlsx', index=False)
    print(df.shape)
scrape_data()