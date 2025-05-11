import requests
import json
import os
import glob
import pandas as pd

os.makedirs("Storage", exist_ok=True)
def download_json():
    page = 1
    download_count = 0
    while True:
        url = "https://secure.icimed.com/nx/portal/membership-directory/list"

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/json;charset=UTF-8",
            "Origin": "https://secure.icimed.com",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows"
        }
        proxies={
            "http": "http://vwantbtc-rotate:igt0km7yu76c@p.webshare.io:80/",
            "https": "http://vwantbtc-rotate:igt0km7yu76c@p.webshare.io:80/"
        }
        payload = {
            "pageNo": page,
            "pageSize": 24,
            "sortField": "lastName0",
            "sortOrder": "",
            "searchCriteria": {"directoryId": 2},
            "total": 0,
            "keyword": ""
        }
        response = requests.post(url, headers=headers,proxies=proxies, json=payload)

        if response.status_code == 200:
            data = response.json()
            if not data.get("rows", []):
                print(f"No more data on page {page}. Stopping...!")
                break
            
            filename = f"Storage/Page_{page}.json"
            with open(filename, "w") as fp:
                json.dump(data, fp, indent=4)
            print(f"Downloaded page {page}")
            download_count += 1
        else:
            print(f"Request failed with status code {response.status_code}")
        page += 1
    print(f"Total number of jsons Downloaded...{download_count}")

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
        rows = Data['rows']
        for row in rows:
            Details = {
                "Member Name" : row.get("memberName", {}),
                "First Name" : row.get("firstName0", {}),
                "Last Name" : row.get("lastName0", {}),
                "Company Name" :  row.get("companyName0",{}),
                "City" : row.get("city", {}),
                "State" : row.get("state", {}),
                "Phone" : row.get("phone1", {}),
                "Website" : Standardized_url(row.get("url", {}))
                
                
            }
            output.append(Details)
df = pd.DataFrame(output)
df.to_excel("Output.xlsx", index=False)
print(df.shape)
