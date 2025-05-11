import json
import glob
import requests
import pandas as pd
import time
from lxml import etree
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
}

Output = []

for each_file in glob.glob("Storage/*.json"):
    with open(each_file, "r", encoding="utf-8") as fp:
        data = json.load(fp)

    docs = data.get("response", {}).get("docs", [])
    for doc in docs:
        school_name = doc.get("school_name_s", "")
        slug = doc.get("slug_s", "")

        detail_url = f"https://www.moe.gov.sg/schoolfinder/schooldetail?schoolname={slug}"

        try:
            res = requests.get(detail_url, headers=headers, timeout=10)
            tree = etree.HTML(res.content)

            contact_section = tree.xpath('//div[@class="moe-main__content"]//div[@class="p-x:xl m-b:2xl"]//div[@class="wrap:m m-x:a g:12"]')
            if contact_section:
                section = contact_section[0]

                school_name = section.xpath('.//div/h1//text()')
                Address = section.xpath('.//div[@class="d:f fld:c"]//div/a//text()')
                mode = section.xpath('//span[contains(text(), "School mode:")]/following-sibling::span//text()')
                category = section.xpath('.//span[contains(text(), "School nature:")]/following-sibling::span[1]//text()')
                Type = section.xpath('.//span[contains(text(), "School type:")]/following-sibling::span//text()')
                email = section.xpath('.//span[contains(text(), "Email:")]/following-sibling::a[1]//text()')
                phone = section.xpath('.//span[contains(text(), "Phone:")]/following-sibling::span[1]//text()')
                website = section.xpath('.//span[contains(text(), "Website:")]/following-sibling::a[1]//text()')
                # print(phone)
                Output.append({
                    "URL": detail_url,
                    "School Name": " ".join(school_name).strip(),
                    "Address": " ".join(Address).strip(),
                    "School Mode": " ".join(mode).strip(),
                    "School Nature": " ".join(category).strip(),
                    "School Type": " ".join(Type).strip(),
                    "Email": ", ".join(email).strip(),
                    "Phone": " ".join(phone).strip(),  # ✅ cleaned here
                    "Website": ", ".join(website).strip(),
                })
                print(f"Done: {school_name}")
            else:
                print(f"Contact section not found for: {school_name}")

        except Exception as e:
            print(f"Failed for {school_name}: {e}")

        time.sleep(1)

df = pd.DataFrame(Output)
df.to_excel("Output_clean.xlsx", index=False)
print("Saved to Output_clean.xlsx")
print(df.shape)
