import requests
from lxml import etree
import os
from threading import Lock
import glob
import hashlib
import pandas as pd

url = 'https://www.asterhospitals.ae/about-us/our-doctors'
base_url = 'https://www.asterhospitals.ae'

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
}
proxies={
    "http": "http://vwantbtc-rotate:igt0km7yu76c@p.webshare.io:80/",
    "https": "http://vwantbtc-rotate:igt0km7yu76c@p.webshare.io:80/"
}
# os.makedirs("Storage", exist_ok=True)

# counter_lock = Lock()
# Download_counter = 0

# def Hash(text):
#     return hashlib.sha256(text.encode()).hexdigest()

# response = requests.get(url, headers=headers, proxies=proxies)
# tree = etree.HTML(response.content)
# each_doctor = tree.xpath('//figure[@class="profile-card__image"]//a/@href')

# for link in each_doctor:
#     doctor_url = f"{base_url}{link}"
#     page_response = requests.get(doctor_url, headers=headers, proxies=proxies)
    
#     if page_response.status_code == 200:
#         tree = etree.HTML(page_response.content)
#         file_name = f"Storage/{Hash(link)}.html"
#         with open(file_name, "wb") as fp:
#             fp.write(page_response.content)
#         with counter_lock:
#             Download_counter += 1
#             print(f"Downloading: {doctor_url}")
#     else:
#         print(f"Failed to Download:{doctor_url}")
        
# print(f"Total HTMLS:{Download_counter}")

Output = []
for each_file in glob.glob("Storage/*.html"):
    with open(each_file, "r", encoding='utf-8') as fp:
        tree = etree.HTML(fp.read())
        Source_url = tree.xpath('//link[@rel="canonical"]/@href')[0].strip()
        Doctor_Name = tree.xpath('//h1/text()')[0].strip()
        Languages_raw = tree.xpath('//h3[contains(text(), "LANGUAGES")]/following-sibling::p[1]//text()')
        Languages = []

        for item in Languages_raw:
            # Split each line by commas (in case it's one big chunk)
            parts = item.split(',')
            for part in parts:
                clean = part.strip()
                if clean:
                    Languages.append(clean)

        languages_str = ",".join(Languages)

        
        Education_raw = tree.xpath('//h3[contains(text(), "Education")]/following-sibling::p[1]/text()')
        education = [edu.strip() for edu in Education_raw if edu.strip()]
        Education_text = ",".join(education)
        
        Specialization_raw = tree.xpath('//h3[contains(text(), "Specialization")]/following-sibling::p[1]/text()')
        specialization = [s.strip() for s in Specialization_raw if s.strip()]
        specialization_text = ",".join(specialization)
        
        Nationality = tree.xpath('//h3[contains(text(), "Nationality")]/following-sibling::p[1]/text()')
        Nationality = Nationality[0].strip() if Nationality else ""
        
        Grade = tree.xpath('//h3[contains(text(), "DOH License Grade")]/following-sibling::p[1]/text()')
        Grade = Grade[0].strip() if Grade else ""
        
        Type_of_physician = tree.xpath('//h3[contains(text(), "Type of Physician")]/following-sibling::p[1]/text()')
        Type_of_physician = Type_of_physician[0].strip() if Type_of_physician else ""
        
        Credentials_raw_1 = tree.xpath('//h3[contains(text(), "Credentials")]/following-sibling::ul//li/p/text()')
        Credentials_raw_2 = tree.xpath('//h3[contains(text(), "Credentials")]/following-sibling::ul//li/text()')
        Credentials_raw_3 = tree.xpath('//h3[contains(text(), "Credentials")]/following-sibling::ul//li/strong/text()')
        Credentials_raw_4 = tree.xpath('//h3[contains(text(), "Credentials")]/following-sibling::p/text()')
        Credentials_raw_5 = tree.xpath('//h3[contains(text(), "Credentials")]/following-sibling::p/strong/text()')
        all_credentials = Credentials_raw_1 + Credentials_raw_2 + Credentials_raw_3 + Credentials_raw_4 + Credentials_raw_5
        Credentials = [credential.strip() for credential in all_credentials if credential.strip()]
        Credentials_text = " ,".join(Credentials)
        
        # Extract data from all possible XPath patterns
        experience_raw_1 = tree.xpath('//h3[contains(text(), "Professional Experience")]/following-sibling::ul//li/text()')
        experience_raw_2 = tree.xpath('//h3[contains(text(), "Professional Experience")]/following-sibling::p/text()')
        experience_raw_3 = tree.xpath('//h3[contains(text(), "Professional Experience")]/following-sibling::ul//li//p//text()')
        experience_raw_4 = tree.xpath('//h3[contains(text(), "Professional Experience")]/following-sibling::ul//li/strong/text()')

        # Combine all results
        all_experiences_raw = experience_raw_1 + experience_raw_2 + experience_raw_3 + experience_raw_4

        # Clean and filter
        professional_experience = [exp.strip() for exp in all_experiences_raw if exp.strip()]

        # Join into a single string
        professionalexperience = " ,".join(professional_experience)

        
        Services_offered = tree.xpath('//h3[contains(text(), "Clinical Expertise & Services Offered")]/following-sibling::ul//li/text()')
        services = [service.strip() for service in Services_offered if service.strip()]
        services_text = ",".join(services)
        Data = {
            "Source Url" : Source_url,
            "Doctor Name" : Doctor_Name,
            "Languages" : languages_str,
            "Education" : Education_text,
            "Specialization" : specialization_text,
            "Nationality" : Nationality,
            "DOH License Grade" : Grade,
            "Type of physician" : Type_of_physician,
            "Credentials" : Credentials_text,
            "Professional Experience" : professionalexperience,
            "Clinical Expertise & Services Offered" : services_text
        }
        Output.append(Data)
df = pd.DataFrame(Output)
df.to_excel("Output.xlsx", index=False)
print(df.shape)