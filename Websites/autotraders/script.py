import requests
from threading import Lock
import hashlib
import os
import glob
import pandas as pd
from rich import print
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import time

url = 'https://www.autotrader.co.uk/cars/leasing/deals?pageNumber=1'

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"134.0.6998.178"',
    'sec-ch-ua-full-version-list': '"Chromium";v="134.0.6998.178", "Not:A-Brand";v="24.0.0.0", "Google Chrome";v="134.0.6998.178"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"19.0.0"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
}
proxies = {
    "http": "http://ocapgizs-rotate:araohu409l9t@p.webshare.io:80/",
    "https": "http://ocapgizs-rotate:araohu409l9t@p.webshare.io:80/"
}
# base_url = "https://www.autotrader.co.uk/"
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
#             page_url = url.replace('pageNumber=1', f'pageNumber={page}')
#             response = requests.get(page_url, headers=headers, proxies=proxies)
            
#             if response.status_code == 200:
#                 print(f"Pagination: {page_url}")
#                 tree = etree.HTML(response.content)
#                 each_page = tree.xpath('//div[@class="at__sc-ii80w-4 drsALN"]//a//@href')
                
#                 if len(each_page) < 12:  # Corrected comparison
#                     print(f"Less than 12 providers found: {page}, {len(each_page)} providers")
#                     Less_data.append(page)  # Append page number where the issue occurs

#                 # Check if we have valid links
#                 if not each_page:
#                     print(f"No provider links found on page {page}")
#                     continue
                
#                 for link in each_page:
#                     each_page_link = f"{base_url}{link}"
#                     page_response = requests.get(each_page_link, headers=headers, proxies=proxies)
                    
#                     if page_response.status_code == 200:
#                         tree = etree.HTML(page_response.content)
#                         file_name = f"Storage/{hash_sha_256(each_page_link)}.html"
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
#     executor.map(download_html, range(1, 10))

# print(f"Total number of pages downloaded: {download_counter}")

# # Retry the failed pages if there are any
# if Failed_pages:
#     print(f"Retry Failed pages: {Failed_pages}")
#     for page in Failed_pages:
#         download_html(page)

# print("Download process completed!")
# print(f"Pages with less than 12 providers: {Less_data}")

Output = []

for each_file in glob.glob("Storage/*.html"):
    
    with open(each_file, "r") as fp:
        tree = etree.HTML(fp.read())
        Web_url = tree.xpath('//link[@rel="canonical"]//@href')
        Web_url = Web_url[0].strip() if Web_url else ""
        Name = tree.xpath('//h2[@class="at__sc-1n64n0d-3 at__sc-14s6se5-6 imRloa cCDigX"]/text()')
        Name = " ".join([x.strip() for x in Name if x.strip()])
        print(Name)
        Description = tree.xpath('//span[@class="at__sc-1n64n0d-8 at__sc-14s6se5-7 fepBps duEsxu"]//text()')
        Description = Description[0].strip() if Description else ""
        price = tree.xpath('//span[@class="at__sc-1n64n0d-2 at__sc-1tjq3r2-3 eTJtTe ddWYov"]//text()')
        price = price[0].strip() if price else ""
        price = price.replace("Â£", "")
        Fuel_type = tree.xpath('//span[contains(text(), "Fuel type")]/following-sibling::span//text()')
        Fuel_type = Fuel_type[0].strip() if Fuel_type else ""
        Gearbox = tree.xpath('//span[contains(text(), "Gearbox")]/following-sibling::span//text()')
        Gearbox = Gearbox[0].strip() if Gearbox else ""
        Bodytype = tree.xpath('//span[contains(text(), "Bodytype")]/following-sibling::span//text()')
        Bodytype = Bodytype[0].strip() if Bodytype else ""
        Range = tree.xpath('//span[contains(text(), "Range")]/following-sibling::span//text()')
        Range = Range[0].strip() if Range else ""
        Doors = tree.xpath('//span[contains(text(), "Doors")]/following-sibling::span//text()')
        Doors = Doors[0].strip() if Doors else ""
        Seats = tree.xpath('//span[contains(text(), "Seats")]/following-sibling::span//text()')
        Seats = Seats[0].strip() if Seats else ""
        
        Details = {
            "Url" : Web_url,
            "Name":Name,
            "Description" : Description,
            "Price" :  price,
            "Fuel Type" : Fuel_type,
            "GearBox" : Gearbox,
            "Body Type" : Bodytype,
            "Range" :  Range,
            "Doors" : Doors,
            "Seats" : Seats
        }
        Output.append(Details)
df = pd.DataFrame(Output)
df.to_excel("Output.xlsx", index=False)
print(df.shape)
