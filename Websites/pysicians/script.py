import requests
import hashlib
from threading import Lock
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import os
import pandas as pd
import time
import glob
from rich import print

url = 'https://physicians.umassmemorial.org/results?Affiliations=111&Index=1'

headers = {
    'Referer': 'https://physicians.umassmemorial.org/results?',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}
proxies = {
    "http": "http://ocapgizs-rotate:araohu409l9t@p.webshare.io:80/",
    "https": "http://ocapgizs-rotate:araohu409l9t@p.webshare.io:80/"
}

counter_lock = Lock()
download_counter = 0
Failed_pages = []
Less_data = []

def hash_sha_256(text):
    return hashlib.sha256(text.encode()).hexdigest()

def download_html(page):
    global download_counter
    retries = 5  # Set retries to a reasonable number
    
    # Retry logic for failed pages
    for attempt in range(retries):
        try:
            page_url = url.replace('Index=1', f'Index={page}')
            response = requests.get(page_url, headers=headers, proxies=proxies)
            
            if response.status_code == 200:
                print(f"Pagination: {page_url}")
                tree = etree.HTML(response.content)
                each_page = tree.xpath('//h2[@class="nameHead"]/a//@href')
                
                if len(each_page) < 12:  # Corrected comparison
                    print(f"Less than 12 providers found: {page}, {len(each_page)} providers")
                    Less_data.append(page)  # Append page number where the issue occurs

                # Check if we have valid links
                if not each_page:
                    print(f"No provider links found on page {page}")
                    continue
                
                for link in each_page:
                    page_response = requests.get(link, headers=headers, proxies=proxies)
                    
                    if page_response.status_code == 200:
                        tree = etree.HTML(page_response.content)
                        file_name = f"Storage/{hash_sha_256(link)}.html"
                        
                        # Save the downloaded page
                        with open(file_name, 'wb') as fp:
                            fp.write(page_response.content)
                        
                        with counter_lock:
                            download_counter += 1
                            print(f"Downloaded: {link}")
                    else:
                        print(f"Failed to download link: {link}, status code: {page_response.status_code}")
            else:
                print(f"Failed to download page: {page_url}, status code: {response.status_code}")
            break  # Exit retry loop on success
        
        except requests.RequestException as e:
            print(f"Error while downloading page: {page}, attempt {attempt + 1}/{retries}")
            
            # Append to failed pages after exhausting retries
            if attempt == retries - 1:
                print(f"Giving up on page {page} after {retries} attempts.")
                Failed_pages.append(page)
            
            time.sleep(5)

# Create a folder for HTML files if it doesn't exist
os.makedirs("Storage", exist_ok=True)

# Use ThreadPoolExecutor for concurrent downloads
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(download_html, range(1, 208))

print(f"Total number of pages downloaded: {download_counter}")

# Retry the failed pages if there are any
if Failed_pages:
    print(f"Retry Failed pages: {Failed_pages}")
    for page in Failed_pages:
        download_html(page)

print("Download process completed!")
print(f"Pages with less than 12 providers: {Less_data}")

# Processing the downloaded HTML files
output = []
for each_file in glob.glob(f"Storage/*.html"):
    with open(each_file, 'r', encoding='utf-8') as fp:
        tree = etree.HTML(fp.read())
        data = {}
        
        provider_url = tree.xpath('//link[@rel="canonical"]//@href')[0].strip()
        # Extract the required fields from the HTML, with checks for missing data
        Name = tree.xpath('//h1[@class="providerName"]/span//text()')
        Name = Name[0].strip() if Name else 'Unknown'
        
        practice_name = tree.xpath('//div[@class="profileLabel" and contains(text(), "Interests")]/following-sibling::div//div/span//text()')
        practice_data = ','.join([practice.strip() for practice in practice_name] if practice_name else ' ')
        
        Specialties = tree.xpath('//div[@class="profileLabel" and contains(text(), "Specialties")]/following-sibling::div/span//text()')
        each_specialities = ','.join([speciality.strip() for speciality in Specialties] if Specialties else ' ')
        
        Academic_Titles = tree.xpath("//div[@class='profileLabel' and contains(text(),'Academic Titles')]/following-sibling::div//span/text()")
        Academic_data = ','.join([Academic.strip() for Academic in Academic_Titles] if Academic_Titles else ' ')
        
        Affiliation = tree.xpath('(//div[@class="profileDisplayData profileBlockNoBreak"])[position()=2]//div//div//text()')
        Affiliation_data = ','.join([affiliation.strip() for affiliation in Affiliation] if Affiliation else '')
        
        Npi_no_list = tree.xpath('//div[@id="person_npi"]//div/span//text()')
        Npi_no = Npi_no_list[0].strip() if Npi_no_list else ''
        
        Languages = tree.xpath('//div[@id="person_languages"]//div/span//text()')
        Languages_spoken = ','.join([Language.strip() for Language in Languages] if Languages else '')
        
        address = tree.xpath('concat(//div[@itemprop="streetAddress"]/text(), ", ", //div[@class="profileDataNoLabel"]//span[@itemprop="addressLocality"]/text(), ", ", //div[@class="profileDataNoLabel"]//span[@itemprop="addressRegion"]/text(), " ", //div[@class="profileDataNoLabel"]//span[@itemprop="postalCode"]/text())')
        address = address if address else ' '
        
        phone_list = tree.xpath('//span[@class="profileData"]/a//text()')
        phone = phone_list[0].strip() if phone_list else 'Unknown'
        
        Fax = tree.xpath('//span/b//text()')
        Fax_no = Fax[0].strip() if Fax else ' '

        data = {
            "Url": provider_url,
            "NAME": Name,
            "Practice Name": practice_data,
            "Specialities": each_specialities,
            "Academic Titles": Academic_data,
            "Affiliation": Affiliation_data,
            "NPI Number": Npi_no,
            "Languages Spoken": Languages_spoken,
            "Address": address,
            "Phone": phone,
            "Fax": Fax_no
        }
        output.append(data)

# Create DataFrame and write to Excel
df = pd.DataFrame(output)
df.to_excel("Output.xlsx", index=False)
print(f"Total number of records processed: {df.shape}")


