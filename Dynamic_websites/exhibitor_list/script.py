import requests
import json
import os
from concurrent.futures import ThreadPoolExecutor
import glob
import pandas as pd
import time
from rich import print

download_count = 0
def download_exhibitor_data(exhibitors):
    global download_count
    ex_key = exhibitors.get("EXHIBITOR_KEY", {})
    url = f'https://s2.goeshow.com/webservices/eshow/floor_space.cfc?method=getExhibitor&exhibitor_key={ex_key}'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': 'Bearer /mdna/xpo/2025/exhibitor_list',
        'origin': 'https://maps.goeshow.com',
        'priority': 'u=1, i',
        'referer': 'https://maps.goeshow.com/',
        'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
    }
    proxies = {
        "http": "http://vwantbtc-rotate:igt0km7yu76c@p.webshare.io:80/",
        "https": "http://vwantbtc-rotate:igt0km7yu76c@p.webshare.io:80/"
    }
    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        
        if response.status_code == 200:
            data = response.json()  
            file_path = f"Exhibitors/{ex_key}.json"
            with open(file_path, 'w') as fp: 
                json.dump(data, fp, indent=4) 
            print(f"Saved data for {ex_key} to {file_path}")
            download_count += 1
        else:
            print(f"Failed to download data for {ex_key}. Status code: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error occurred for {ex_key}: {e}")

with open("data.json", 'r', encoding='utf-8') as fp:
    Data = json.load(fp)
    exhibitors = Data.get("EXHIBITORS", [])

os.makedirs("Exhibitors", exist_ok=True)

with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(download_exhibitor_data, exhibitors)

print(f"Total number of files downloaded successfully: {download_count}")

Output = []

for each_file in glob.glob("Exhibitors/*.json"):
    
    with open(each_file, 'r') as fp:
        Details = json.load(fp)
        
        Datas = {}
        directory = Details["EXHIBITOR"]["DIRECTORY"]
        company_name = directory.get("COMPANY_NAME", {})
        category = directory.get("CATEGORY", [])
        website = directory.get("WEBSITE", {})
        city = directory.get("CITY", {})
        state = directory.get("STATE", {})
        country = directory.get("COUNTRY", {})
        phone = directory.get("PHONE", {})
        Toll = directory.get("TOLL_FREE", {})
        Fax = directory.get("FAX", {})
        Zip = directory.get("ZIP_CODE", {})
        Address_1 = directory.get("ADDRESS1", {})
        Address_2 = directory.get("ADDRESS2", {})
        for cate in category:
            categories = cate.get("ANSWER_TITLE", {})
        
        Datas = {
            "Company Name" : company_name,
            "Category" : categories,
            "Website" : website,
            "Address 1" : Address_1,
            "Address 2" : Address_2,
            "City" : city,
            "State" : state,
            "Zip Code" : Zip,
            "Country" : country,
            "Phone" : phone,
            "Toll Free" : Toll,
            "Fax" : Fax,
            
        }  
        Output.append(Datas)
        
df = pd.DataFrame(Output)
df.to_excel("Output.xlsx", index=False)
print(df.shape)     
                
            
        
    