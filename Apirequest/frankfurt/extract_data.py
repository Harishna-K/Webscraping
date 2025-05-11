import json
import pandas as pd
with open("Data.json", "r") as fp:
    data = json.loads(fp)
all_data = []
for item in data:
    hits = item["result"]["hits"]
    for hit in hits:
        exhibitor = hit["exhibitor"]
        details = {
            "Name" : exhibitor["name"],
            "Phone" : exhibitor["address"]["tel"],
            "Email" : exhibitor["address"]["email"],
            "Street" : exhibitor["address"]["street"],
            "City" : exhibitor["address"]["city"],
            "Zip" : exhibitor["address"]["zip"],
            "Country" : exhibitor["address"]["country"]["label"]
        }
        all_data.append(details)
df = pd.DataFrame(all_data)
df.to_excel("output.xlsx", index=False)
print(df.shape)