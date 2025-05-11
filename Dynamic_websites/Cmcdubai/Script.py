import requests
from lxml import html
import os
import time
import glob
import pandas as pd

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
# }

# base_url = "https://cmcdubai.ae/find-a-doctor/"
# output_dir = "doctor_pages"
# os.makedirs(output_dir, exist_ok=True)

# page = 1
# while True:
#     url = f"{base_url}{page}/"
#     print(f"Checking page {page}: {url}")
#     response = requests.get(url, headers=headers)
#     tree = html.fromstring(response.content)

#     # Check if <script type="application/ld+json"> is present
#     json_ld = tree.xpath('//script[@type="application/ld+json"]')
#     if not json_ld:
#         print("No <script type='application/ld+json'> found. Stopping.")
#         break

#     # Extract doctor URLs
#     doctor_links = tree.xpath('//h2[@class="elementor-heading-title elementor-size-default"]/a/@href')
#     print(f"Found {len(doctor_links)} doctor profile(s).")
#     if not doctor_links:
#         print("No doctor links found. Stopping.")
#         break
#     for doctor_url in doctor_links:
#         try:
#             doctor_filename = doctor_url.rstrip('/').split('/')[-1] + ".html"
#             doctor_filepath = os.path.join(output_dir, doctor_filename)
#             if not os.path.exists(doctor_filepath):
#                 print(f"Downloading: {doctor_url}")
#                 doctor_resp = requests.get(doctor_url, headers=headers)
#                 with open(doctor_filepath, 'w', encoding='utf-8') as f:
#                     f.write(doctor_resp.text)
#                 time.sleep(1)  # polite delay
#             else:
#                 print(f"Already downloaded: {doctor_filename}")
#         except Exception as e:
#             print(f"Error downloading {doctor_url}: {e}")

#     page += 1
#     time.sleep(1)  # polite delay between pages

Output = []

for each_file in glob.glob("doctor_pages/*.html"):
    with open(each_file, 'r', encoding='utf-8') as file:
        content = file.read()
        tree = html.fromstring(content)
        Source_url = tree.xpath('//link[@rel="alternate"]/@href')
        name = tree.xpath('//h3[@class="doctor-title"]/text()')
        Category = tree.xpath('//div[@class="doctor-category"]/a/text()')
        Category = [cat.strip() for cat in Category if cat.strip()]
        Category = ', '.join(Category) if Category else " "
        Speacialist = tree.xpath('//p[@class="description"]/text()')
        Languages = tree.xpath('//span[@class="elementor-post-info__terms-list"]/span/text()')
        Languages = [lang.strip() for lang in Languages if lang.strip()]
        Languages = ', '.join(Languages) if Languages else " "
        Telephone = tree.xpath('//h3[@class="elementor-heading-title elementor-size-default"]/a/text()')
        Location = tree.xpath('//div[@class="dr-location"]/div[@class="locatoins"]/text()')
        Output.append({
            "Source_url": Source_url[0] if Source_url else " ",
            "Name": name[0] if name else " ",
            "Category": Category,
            "Specialist": Speacialist[0] if Speacialist else " ",
            "Languages": Languages,
            "Telephone": Telephone[0] if Telephone else " ",
            "Location": Location[0] if Location else " "
        })
df = pd.DataFrame(Output)
df.to_excel("doctor_data.xlsx", index=False)
print(df.shape)