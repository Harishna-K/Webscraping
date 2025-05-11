import requests
import json
from rich import print
import os
import time
import glob
import pandas as pd

url = "https://us-east-1-renderer-read.knack.com/v1/scenes/scene_20/views/view_104/records"

page = 1
all_pages = []

os.makedirs("Storage", exist_ok=True)

while True:
    
    params = {
        "format": "both",
        "page": {page},
        "rows_per_page": "50",
        "sort_field": "field_1",
        "sort_order": "asc",
        "_": "1746167157805"
    }

    headers = {
        "accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-fetch-storage-access": "active",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "x-knack-application-id": "60991a70e3ac80001ca1ff5e",
        "x-knack-new-builder": "true",
        "x-knack-rest-api-key": "renderer",
        "x-requested-with": "XMLHttpRequest"
    }

    response = requests.get(url, headers=headers, params=params)

    Data = response.json()

    Records = Data.get("records", [])
    
    if not Records:
        break
    
    with open(f"Storage/Page_{page}.json", "w") as fp:
        json.dump(Data, fp, indent=4)
        
    all_pages.extend(Records)
    page += 1
    time.sleep(1)

print(f"Total pages Downloaded:{len(all_pages)}")

Output = []

for each_file in glob.glob("Storage/*.json"):
    
    with open(each_file, "r", encoding='utf-8') as fp:
        Data = json.load(fp)
        
        Records = Data.get("records", [])
        
        for record in Records:
            Source_url = f"https://schsl.org/schsl-directory#schsl-directory/school-details5/{record.get("id",{})}"
            School_Name = record.get("field_1", {})
            
            Directory_administrator = record["field_25_raw"]
            for directory in Directory_administrator:
                Administrator = directory.get("identifier",{})
            
            # School_type = record.get("field_32", {})
            classification = record.get("field_44", {})
            Region = record.get("field_45", {})
            
            Mail_Address = record.get("field_34_raw", {})
            if isinstance(Mail_Address,str):
                try:
                    Mail_Address = json.loads(Mail_Address)
                except json.JSONDecodeError:
                    Mail_Address = {}
            mail = Mail_Address.get("full", {})
            
            Phone = record["field_35_raw"]["formatted"]
            mascot =record.get("field_37",{})
            school_colors = record.get("field_38", {})
            Date_Modified = record.get("field_47",{})
            Details = {
                "Source url":Source_url,
                "School Name":School_Name,
                # "School Type":School_type,
                "Classification":classification,
                "Region":Region,
                "Mail Address":mail,
                "Phone":Phone,
                "Mascot":mascot,
                "School colors":school_colors,
                "Directory Administrator":Administrator,
                "Date modified":Date_Modified
            }
            Output.append(Details)
df =pd.DataFrame(Output)
df.to_excel("Output.xlsx", index=False)
print(df.shape)        
