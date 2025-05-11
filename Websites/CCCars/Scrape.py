import requests
import pandas as pd
import hashlib
from threading import Lock
import os
import glob
from concurrent.futures import ThreadPoolExecutor
from rich import print
import time
from lxml import etree
url = 'https://www.cccars.co.nz/vehicles?Page=1'
base_url = 'https://www.cccars.co.nz'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
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
            page_url = url.replace('Page=1', f'Page={page}')
            response = requests.get(page_url, headers=headers, proxies=proxies)
            
            if response.status_code == 200:
                print(f"Pagination: {page_url}")
                tree = etree.HTML(response.content)
                each_page = tree.xpath('//div[@class="small-10 columns"]//a/@href')
                
                if len(each_page) < 20:  # Corrected comparison
                    print(f"Less than 20 providers found: {page}, {len(each_page)} providers")
                    Less_data.append(page)  # Append page number where the issue occurs

                # Check if we have valid links
                if not each_page:
                    print(f"No provider links found on page {page}")
                    continue
                
                for link in each_page:
                    page_link = f"{base_url}{link}"
                    page_response = requests.get(page_link, headers=headers, proxies=proxies)
                    
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
with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(download_html, range(1, 4))

print(f"Total number of pages downloaded: {download_counter}")

# Retry the failed pages if there are any
if Failed_pages:
    print(f"Retry Failed pages: {Failed_pages}")
    for page in Failed_pages:
        download_html(page)

print("Download process completed!")
print(f"Pages with less than 20 providers: {Less_data}")

output = []
for each_file in glob.glob(f"Storage/*.html"):
    with open(each_file, 'r', encoding='utf-8') as fp:
        tree = etree.HTML(fp.read())
        data = {}
        Source_url = tree.xpath('//link[@rel="canonical"]//@href')[0].strip()
        Name = tree.xpath('//div[@class="title"]//h2//text()')[0].strip()
        price = tree.xpath('//span[@class="retail"]/span[@class="amount"]/text()')[0].strip()
        Engine = tree.xpath('//div[contains(text(), "Engine")]/following-sibling::div/text()')[0].strip()
        Body = tree.xpath('//div[contains(text(), "Body")]/following-sibling::div/text()')[0].strip()
        Odometer = tree.xpath('//div[contains(text(), "Odometer")]/following-sibling::div/text()')[0].strip()
        Ext_color = tree.xpath('//div[contains(text(), "Ext Colour")]/following-sibling::div/text()')[0].strip()
        Interior = tree.xpath('//div[contains(text(), "Interior")]/following-sibling::div/text()')[0].strip()
        Transmission = tree.xpath('//div[contains(text(), "Transmission")]/following-sibling::div/text()')[0].strip()
        Nz_owners = tree.xpath('//div[contains(text(), "NZ Owners")]/following-sibling::div/text()')[0].strip()
        data = {
            "Source Url" : Source_url,
            "Name" : Name,
            "Price" : price,
            "Engine" :  Engine,
            "Body" : Body,
            "Odometer" : Odometer,
            "Exterior color" : Ext_color,
            "Interior" :  Interior,
            "Transmission" : Transmission,
            "NZ Owners" : Nz_owners
        }
        output.append(data)
df = pd.DataFrame(output)
df.to_excel("Output.xlsx", index=False)
print(df.shape)