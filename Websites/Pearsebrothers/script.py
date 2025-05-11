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

url = 'https://www.pearcebrothers.co.nz/vehicles?Make=&Text=&PriceFrom=0&PriceTo=0&YearFrom=0&YearTo=0&Transmission=&BodyStyle=&Dealership=&SortOption=0&EngineSizeFrom=0&EngineSizeTo=0&OdometerFrom=0&OdometerTo=0&Model=&VehicleType=All&IgnoreContext=&FuelType1=&Colour=&Page=1'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

proxies = {
    "http": "http://ocapgizs-rotate:araohu409l9t@p.webshare.io:80/",
    "https": "http://ocapgizs-rotate:araohu409l9t@p.webshare.io:80/"
}
# base_url = "https://www.pearcebrothers.co.nz"
# counter_lock = Lock()
# download_counter = 0
# Failed_pages = []
# Less_data = []

# def hash_sha_256(text):
#     return hashlib.sha256(text.encode()).hexdigest()

# def download_html(page):
#     global download_counter
#     retries = 5  # Set retries to a reasonable number
    
#     # Retry logic for failed pages
#     for attempt in range(retries):
#         try:
#             page_url = url.replace('Page=1', f'Page={page}')
#             response = requests.get(page_url, headers=headers, proxies=proxies)
            
#             if response.status_code == 200:
#                 print(f"Pagination: {page_url}")
#                 tree = etree.HTML(response.content)
#                 each_page = tree.xpath('//div[@class="small-10 columns"]//a//@href')
                
#                 if len(each_page) < 20:  # Corrected comparison
#                     print(f"Less than 20 providers found: {page}, {len(each_page)} providers")
#                     Less_data.append(page)  # Append page number where the issue occurs

#                 # Check if we have valid links
#                 if not each_page:
#                     print(f"No provider links found on page {page}")
#                     continue
                
#                 for link in each_page:
#                     each_page_url = f'{base_url}{link}'
#                     page_response = requests.get(each_page_url, headers=headers, proxies=proxies)
                    
#                     if page_response.status_code == 200:
#                         tree = etree.HTML(page_response.content)
#                         file_name = f"Storage/{hash_sha_256(link)}.html"
                        
#                         # Save the downloaded page
#                         with open(file_name, 'wb') as fp:
#                             fp.write(page_response.content)
                        
#                         with counter_lock:
#                             download_counter += 1
#                             print(f"Downloaded: {link}")
#                     else:
#                         print(f"Failed to download link: {link}, status code: {page_response.status_code}")
#             else:
#                 print(f"Failed to download page: {page_url}, status code: {response.status_code}")
#             break  # Exit retry loop on success
        
#         except requests.RequestException as e:
#             print(f"Error while downloading page: {page}, attempt {attempt + 1}/{retries}")
            
#             # Append to failed pages after exhausting retries
#             if attempt == retries - 1:
#                 print(f"Giving up on page {page} after {retries} attempts.")
#                 Failed_pages.append(page)
            
#             time.sleep(5)

# # Create a folder for HTML files if it doesn't exist
# os.makedirs("Storage", exist_ok=True)

# # Use ThreadPoolExecutor for concurrent downloads
# with ThreadPoolExecutor(max_workers=10) as executor:
#     executor.map(download_html, range(1, 22))

# print(f"Total number of pages downloaded: {download_counter}")

# # Retry the failed pages if there are any
# if Failed_pages:
#     print(f"Retry Failed pages: {Failed_pages}")
#     for page in Failed_pages:
#         download_html(page)

# print("Download process completed!")
# print(f"Pages with less than 20 providers: {Less_data}")

Output = []
for each_file in glob.glob(f"Storage/*.html"):
    with open(each_file, 'r', encoding='utf-8') as fp:
        tree = etree.HTML(fp.read())
        data = {}
        provider_url = tree.xpath('//link[@rel="canonical"]//@href')[0].strip()

        Name = tree.xpath("//h2//text()")[0].strip()
        
        Engine = tree.xpath('//div[contains(text(), "Engine")]/following-sibling::div//text()')[0].strip()
        
        Body = tree.xpath('//div[contains(text(), "Body")]/following-sibling::div//text()')[0].strip()
        
        Odometer = tree.xpath("//div[contains(text(), 'Odometer')]/following-sibling::div//text()")[0].strip()
        
        Exterior = tree.xpath("//div[contains(text(), 'Ext Colour')]/following-sibling::div//text()")[0].strip()
        
        Interior = tree.xpath("//div[contains(text(), 'Interior')]/following-sibling::div//text()")
        
        Transmission = tree.xpath("//div[contains(text(), 'Transmission')]/following-sibling::div//text()")[0].strip()
        
        Nz_Owner = tree.xpath("//div[contains(text(), 'NZ Owners')]/following-sibling::div//text()")[0].strip()


        data = {
            "Url": provider_url,
            "Name": Name,
            "Engine": Engine,
            "Body": Body,
            "Odimeter": Odometer,
            "Exterior": Exterior,
            "Interior": Interior[0].strip() if Interior else None,
            "Transmission": Transmission,
            "Nz_Owner": Nz_Owner
        }
        Output.append(data)

# Create DataFrame and write to Excel
df = pd.DataFrame(Output)
df.to_excel("Output.xlsx", index=False)
print(f"Total number of records processed: {df.shape}")

        
        
