import requests
import json
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

all_data = []
  
def download_json_data(i):
   
        url = f'https://smarthistory.org/wp-json/smthstapi/v1/objects?tag=938&page={i}'

        headers = {
            'accept': '*/*',
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
            print(f"Data from page {i} downloaded successfully!")
        else:
            print(f"Failed to download data from page {i}.Status code:{response.status_code}")

with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(download_json_data, range(1,43))
      
with open("test.json", "w") as fp:
    json.dump(all_data, fp, indent=4)
    


def scrape_data():
    
    with open('test.json', 'r') as fp:
        Data = json.load(fp)
    Output = []
    
    for item in Data:
        post = item.get('posts', [])
        for each_data in post:
            url = each_data.get('guid', {}).strip()
            title =each_data['title'].strip().replace('<em>', '')
            Description = each_data.get('excerpt', {}).strip().replace('<em>', '')
            details = {
                "url" : url,
                "Title":title,
                "Description":Description
            }
            Output.append(details)
    df = pd.DataFrame(Output)
    df.to_excel("output_data.xlsx", index=False)
    print(df.shape)       
scrape_data()