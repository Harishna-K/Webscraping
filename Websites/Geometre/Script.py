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
# url = 'https://www.geometre-expert.fr/trouver-un-geometre-expert/page/1/'

# headers = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#     'Accept-Language': 'en-US,en;q=0.9',
#     'Cache-Control': 'no-cache',
#     'Connection': 'keep-alive',
#     'Pragma': 'no-cache',
#     'Sec-Fetch-Dest': 'document',
#     'Sec-Fetch-Mode': 'navigate',
#     'Sec-Fetch-Site': 'same-origin',
#     'Sec-Fetch-User': '?1',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
#     'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
# }
# proxies = {
#     "http": "http://ocapgizs-rotate:araohu409l9t@p.webshare.io:80/",
#     "https": "http://ocapgizs-rotate:araohu409l9t@p.webshare.io:80/"
# }

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
#             page_url = f"https://www.geometre-expert.fr/trouver-un-geometre-expert/page/{page}/"
#             response = requests.get(page_url, headers=headers, proxies=proxies)
            
#             if response.status_code == 200:
#                 print(f"Pagination: {page_url}")
#                 tree = etree.HTML(response.content)
#                 each_page = tree.xpath('//div[@class="card-footer"]//a[1]/@href')
                
#                 if len(each_page) < 20:  # Corrected comparison
#                     print(f"Less than 20 providers found: {page}, {len(each_page)} providers")
#                     Less_data.append(page)  # Append page number where the issue occurs

#                 # Check if we have valid links
#                 if not each_page:
#                     print(f"No provider links found on page {page}")
#                     continue
                
#                 for link in each_page:
#                     page_response = requests.get(link, headers=headers, proxies=proxies)
                    
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
#     executor.map(download_html, range(1, 96))

# print(f"Total number of pages downloaded: {download_counter}")

# # Retry the failed pages if there are any
# if Failed_pages:
#     print(f"Retry Failed pages: {Failed_pages}")
#     for page in Failed_pages:
#         download_html(page)

# print("Download process completed!")
# print(f"Pages with less than 20 providers: {Less_data}")

Output = []

for each_file in glob.glob("Storage/*.html"):
    with open(each_file, 'rb') as file:
        content = file.read()
        tree = etree.HTML(content)
        Source_url = tree.xpath('//link[@rel="canonical"]/@href')
        name = tree.xpath("//h1/text()")
        Expert = tree.xpath("//dt[span[text()='Cabinet']]/following-sibling::dd[1]/text()")
        phone = tree.xpath('//dd/a[contains(@href, "tel")]/text()')
        email = tree.xpath("//dl//dt[span[text()='Email']]/following-sibling::dd/a/@title")
        website = tree.xpath('//dd[4]//font/font/text()')
        Location = tree.xpath("//dl//dt[span[text()='Ville']]/following-sibling::dd[1]/text()")
        
        Output.append({
            "Source url": Source_url[0] if Source_url else None,
            "Name": name[0] if name else None,
            "Expert": Expert[0] if Expert else None,
            "Phone": phone[0] if phone else None,
            "Email": email[0] if email else None,
            # "Website": website,
            "Location": Location[0] if Location else None,
        })
df = pd.DataFrame(Output)
df.to_excel("output.xlsx", index=False)
print(df.shape)