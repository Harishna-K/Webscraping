import requests
import json
import os
import pandas as pd
from rich import print
import glob

base_url = "https://www.myschools.nyc/en/api/v2/schools/process/4/?page={}&"

headers = {
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "X-CSRFToken": "D6QAH5nzvTOHTd58iDrFTixJZSxKSWUq",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8, application/json",
}

proxies = {
    "http": "http://vwantbtc-rotate:igt0km7yu76c@p.webshare.io:80/",
    "https": "http://vwantbtc-rotate:igt0km7yu76c@p.webshare.io:80/"
}

os.makedirs("Storage", exist_ok=True)

def download_json():
    page = 1
    download_counter = 0

    while True:
        url = base_url.format(page)
        response = requests.get(url, headers=headers, proxies=proxies)

        if response.status_code == 200:
            data = response.json()

            if not data.get("results"):
                print(f"No more data on page {page}. Stopping...")
                break

            file_name = f"Storage/Page_{page}.json"

            with open(file_name, "w") as fp:
                json.dump(data, fp, indent=4)

            download_counter += 1
            print(f"Downloaded page {page}, saved as {file_name}")

        else:
            print(f"Failed to fetch data on page {page}. Status code: {response.status_code}")
            break

        page += 1

    print(f"Total {download_counter} JSON files downloaded.")

# download_json()

def Standardized_url(url):
    if not url:
        return ""
    url = url.lower().strip()
    if not url.startswith("http"):
        url = "https://" + url
    if "www" not in url and "." in url.split("//")[1]:
        url = url.replace("https://", "https://www.", 1).replace("http://", "http://www.", 1)
    return url
    
output = []

for each_file in glob.glob("Storage/*.json"):
    with open(each_file, "r") as fp:
        Data = json.load(fp)
        Results = Data["results"]
        
        for result in Results:
            school = result.get("school", {})
            website = Standardized_url(result.get("independent_website", {}))
            Details = {
            "Name" : school.get("name", {}),
            "address" : school.get("full_address", {}),
            "Email" : result.get("email", {}),
            "Telephone" : result.get("telephone", {}),
            "website" : website,
            }
            output.append(Details)
            
df = pd.DataFrame(output)
df.to_excel("Output.xlsx", index=False)
print(df.shape)