import requests
import time
import os
from lxml import etree
import pandas as pd
import glob
from rich import print
from threading import Lock

base_url = "https://www.mediclinic.ae/en/corporate/hospitals-and-clinics/find-a-doctor/_jcr_content/content/doctors.filter.html"
headers = {
    'accept': 'text/html, */*; q=0.01',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'referer': 'https://www.mediclinic.ae/en/corporate/hospitals-and-clinics/find-a-doctor.html'
}

# os.makedirs("Storage", exist_ok=True)

# step = 10
# max_empty_pages = 3
# empty_pages = 0
# i = 0

# while True:
#     url = f"{base_url}/{i}/{i + step - 1}.html"
#     print(f"Fetching: {url}")

#     try:
#         response = requests.get(url, headers=headers)
#         if response.status_code != 200:
#             print(f"Non-200 response: {response.status_code}")
#             empty_pages += 1
#             if empty_pages >= max_empty_pages:
#                 print("Stopping: too many consecutive non-200 responses.")
#                 break
#             i += step
#             continue

#         if not response.text.strip():
#             print("Empty response content.")
#             empty_pages += 1
#             if empty_pages >= max_empty_pages:
#                 print("Stopping: too many consecutive empty pages.")
#                 break
#             i += step
#             continue

#         tree = etree.HTML(response.content)
#         names = tree.xpath('//h3')

#         if not names:
#             print("No <h3> tags found (likely no doctor names). Stopping.")
#             break

#         # Save file only if <h3> tags are found
#         file_name = f"Storage/doctor_page_{i}_{i + step - 1}.html"
#         with open(file_name, "w", encoding="utf-8") as f:
#             f.write(response.text)
#         print(f"Saved: {file_name}")

#         empty_pages = 0  # Reset because content was valid

#     except requests.exceptions.RequestException as e:
#         print(f"Request failed: {e}")
#         break

#     i += step
#     time.sleep(1)

# Each doctor page download



# counter_lock = Lock()
# Download_counter = 0

# Output = []

# os.makedirs("Doctors", exist_ok=True)

# for each_file in glob.glob("Storage/*.html"):
    
#     with open(each_file, "r", encoding="utf-8") as fp:
#         tree = etree.HTML(fp.read())
#         doctors = tree.xpath('//li[@data-anchor]')
        
#         for doctor in doctors:
            
#             relative_url = doctor.xpath(".//a/@href")[0].strip()
#             base_url = "https://www.mediclinic.ae"
            
#             page_url = f"{base_url}{relative_url}"
#             page_response = requests.get(page_url, headers=headers)
#             tree = etree.HTML(page_response.content)
            
#             file_path = relative_url.strip('/').replace('/', '_').replace('en_corporate_doctors_', '')
#             File_name = f"Doctors/{file_path}"
            
#             with open(File_name, "wb") as fp:
#                 fp.write(page_response.content)
#                 print(f"Downloaded:{File_name}")
#             with counter_lock:
#                 Download_counter += 1
# print(f"Total HTMLS Downloaded:{Download_counter}")


Output = []

for each_file in glob.glob("Doctors/*.html"):
    with open(each_file, 'r', encoding='utf-8') as fp:
        tree = etree.HTML(fp.read())
        Source_url = tree.xpath('//link[@rel="canonical"]/@href')
        Doctor_name = tree.xpath('//h1/text()')
        Speciality = tree.xpath('//dd/a/text()')
        Specialities = ",".join(s.strip() for s in Speciality)
        Languages = tree.xpath('//dt[contains(text(), "Languages")]/following-sibling::dd/text()')
        practices_at = tree.xpath('//div[@class="mc-doctor-practices-list section"]//ul//li/a/text()')
        practices = ",".join(p.strip() for p in practices_at)
        Nationality = tree.xpath('//dt[contains(text(), "Nationality")]/following-sibling::dd[1]/text()')
        Summary = tree.xpath('//dt[contains(text(), "Summary")]/following-sibling::dd[1]/text()')
        Qualification = tree.xpath('//h2[text()="Qualification"]/ancestor::div[contains(@class, "section-box")][1]//dd/text()')
        Qualification = [q.strip() for q in Qualification]
        Qualifications = ",".join(Qualification)
        Facebook = tree.xpath('//a[contains(@href, "facebook.com")]/@href')
        Twitter = tree.xpath('//a[contains(@href, "twitter.com")]/@href')
        Linkedin = tree.xpath('//a[contains(@href, "linkedin.com")]/@href')
        Youtube = tree.xpath('//a[contains(@href, "youtube.com")]/@href')
        instagram = tree.xpath('//a[contains(@href, "instagram.com")]/@href')
        Details = {
            "Source url":Source_url[0].strip() if Source_url else "",
            "Doctor Name":Doctor_name[0].strip() if Doctor_name else "",
            "Specialities":Specialities.strip() if Specialities else "",
            "Languages":Languages[0].strip() if Languages else "",
            "Practices At":practices.strip() if practices else "",
            "Nationality":Nationality[0].strip() if Nationality else "",
            "Summary":Summary[0].strip() if Summary else "",
            "Qualification":Qualifications.strip() if Qualifications else "",
            "FaceBook":Facebook[0].strip() if Facebook else "",
            "Twitter":Twitter[0].strip() if Twitter else "",
            "LinkedIn":Linkedin[0].strip() if Linkedin else "",
            "Youtube":Youtube[0].strip() if Youtube else "",
            "Instagram":instagram[0].strip() if instagram else "",
        }
        Output.append(Details)
df = pd.DataFrame(Output)
df.to_excel("Doctors_data.xlsx", index=False)
print(df.shape)
