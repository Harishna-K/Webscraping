import requests
from lxml import etree
from rich import print 
import pandas as pd
import hashlib
import os
import glob
# url = 'https://www.zulekhahospitals.com/best-doctors-in-uae'

# headers = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#     'Accept-Language': 'en-US,en;q=0.9',
#     'Cache-Control': 'no-cache',
#     'Connection': 'keep-alive',
#     'Pragma': 'no-cache',
#     'Sec-Fetch-Dest': 'document',
#     'Sec-Fetch-Mode': 'navigate',
#     'Sec-Fetch-Site': 'none',
#     'Sec-Fetch-User': '?1',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
#     'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
# }
# def Hash(text):
#     return hashlib.sha256(text.encode()).hexdigest()
# os.makedirs('Doctors', exist_ok=True)
# response = requests.get(url, headers=headers)
# tree = etree.HTML(response.content)
# Each_Doctor = tree.xpath('//a[@class="detail-btn"]/@href')
# for link in Each_Doctor:
#     page_response = requests.get(link, headers=headers)
#     tree = etree.HTML(page_response.content)
#     file_name = f"Doctors/{Hash(link)}.html"
#     with open(file_name, 'wb') as file:
#         file.write(page_response.content)
# Output = []
# for file in glob.glob('Doctors/*.html'):
#     with open(file, 'rb') as f:
#         tree = etree.HTML(f.read())
        
#         # Extracting data with XPath
#         Source_url = tree.xpath('//link[@rel="canonical"]/@href')  # Source URL
#         Name = tree.xpath('//div[@class="description-big"]//h3/text()')  # Doctor's Name
#         Qualifications = tree.xpath('//div[@class="description-big"]//h3/following-sibling::p[1]/text()')
#         Specialist = tree.xpath('//div[@class="description-big"]//h3/following-sibling::p[2]/text()')
#         work_experience = tree.xpath('//h2[contains(text(), "Work Experience")]/following-sibling::ul[1]//li/text()')  # Work Experience
#         experience = " ".join([item.strip() for item in work_experience if item.strip()])  # Clean and join experience
#         language = tree.xpath('//h2[contains(text(), "Languages Spoken")]/following-sibling::ul[1]//li/text()')  # Languages
#         languages = ", ".join(language)  # Join languages into a single string
#         interest = tree.xpath('//h2[contains(text(), "Special Interests")]/following-sibling::ul[1]//li/text()')  # Special Interests
#         interests = ", ".join(interest)  # Join interests into a single string
#         Research = tree.xpath('//h2[contains(text(), "Research") or contains(text(), "Publications")]/following-sibling::ul[1]//li/text()')  # Research/Publications
#         research = " | ".join([item.strip() for item in Research if item.strip()])  # Clean and join research
        
#         # Constructing the data dictionary
#         Data = {
#             "Source_url": Source_url[0] if Source_url else "",
#             "Name": Name[0].strip() if Name else "",
#             "Qualification": Qualifications[0].strip() if Qualifications else "",
#             "Specialist": Specialist[0].strip() if Specialist else "",
#             "Experience": experience,
#             "Languages": languages,
#             "Interests": interests,
#             "Research": research
#         }
#         Output.append(Data)
# import numpy as np
# df = pd.DataFrame(Output)
# df.replace("", np.nan, inplace=True)
# dfs = df.dropna(how='all')
# dfs.to_excel('Doctors.xlsx', index=False)
# print(df.shape)
    
import glob
from lxml import etree
import pandas as pd
import numpy as np

Output = []

for file in glob.glob('Doctors/*.html'):
    with open(file, 'rb') as f:
        tree = etree.HTML(f.read())
        
        Source_url = tree.xpath('//link[@rel="canonical"]/@href')
        Source_url = Source_url[0] if Source_url else ""

        for section in tree.xpath('//div[@class="description-big"]'):
            Name = section.xpath('.//h3[1]/text()')
            Name = Name[0].strip() if Name else ""

            # Safe extraction of the first two non-empty <p> tags after <h3>
            p_tags = section.xpath('.//h3[1]/following-sibling::p[normalize-space()]')
            Qualifications = ''.join(p_tags[0].itertext()).strip() if len(p_tags) > 0 else ""
            Specialist = ''.join(p_tags[1].itertext()).strip() if len(p_tags) > 1 else ""

            work_experience = section.xpath('.//h2[contains(text(), "Work Experience")]/following-sibling::ul[1]//li/text()')
            experience = " ".join([item.strip() for item in work_experience if item.strip()])

            language = section.xpath('.//h2[contains(text(), "Languages Spoken")]/following-sibling::ul[1]//li/text()')
            languages = ", ".join([lang.strip() for lang in language if lang.strip()])

            interest = section.xpath('.//h2[contains(text(), "Special Interests") or contains(text(), "Specialist Interests")]/following-sibling::ul[1]//li/text()')
            interests = ", ".join([item.strip() for item in interest if item.strip()])

            research = section.xpath('.//h2[contains(text(), "Research") or contains(text(), "Publications")]/following-sibling::ul[1]//li/text()')
            research_str = " | ".join([item.strip() for item in research if item.strip()])

            Data = {
                "Source_url": Source_url,
                "Name": Name,
                "Qualification": Qualifications,
                "Specialist": Specialist,
                "Experience": experience,
                "Languages": languages,
                "Interests": interests,
                "Research": research_str
            }

            Output.append(Data)

# Convert and clean DataFrame
df = pd.DataFrame(Output)
df.replace("", np.nan, inplace=True)
df.dropna(how='all', inplace=True)

# Save to Excel
df.to_excel('Doctors.xlsx', index=False)

print("Total entries extracted:", df.shape[0])
