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

url = 'https://www.eurocars.co.nz/vehicles?Page=1'

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
base_url = "https://www.eurocars.co.nz"
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
                each_page = tree.xpath('//div[@class="small-10 columns"]//a//@href')
                
                if len(each_page) < 20:  # Corrected comparison
                    print(f"Less than 20 providers found in page: {page}, {len(each_page)} providers")
                    Less_data.append(page)  # Append page number where the issue occurs

                # Check if we have valid links
                if not each_page:
                    print(f"No provider links found on page {page}")
                    continue
                
                for link in each_page:
                    each_page_url =f"{base_url}{link}"
                    page_response = requests.get(each_page_url, headers=headers, proxies=proxies)
                    
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
                        print(f"Failed to download link: {each_page_url}, status code: {page_response.status_code}")
            else:
                print(f"Failed to download page: {each_page_url}, status code: {response.status_code}")
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
# with ThreadPoolExecutor(max_workers=10) as executor:
#     executor.map(download_html, range(1, 4))

print(f"Total number of pages downloaded: {download_counter}")

# Retry the failed pages if there are any
if Failed_pages:
    print(f"Retry Failed pages: {Failed_pages}")
    for page in Failed_pages:
        download_html(page)

print("Download process completed!")
print(f"Pages with less than 20 providers: {Less_data}")

# Processing the downloaded HTML files
output = []
for each_file in glob.glob(f"Storage/*.html"):
    with open(each_file, 'rb') as fp:
        tree = etree.HTML(fp.read())
        data = {}
        urls = f'{base_url}{each_file.replace('Storage', '').replace('.html', '')}'
        Name = tree.xpath('//div[@class="title"]//h2//text()')
        Name = Name[0].strip() if Name else None
        price = tree.xpath('//div[@class="price-container"]//div[@class="price-container-content"]//span//span/span//text()')
        price = price[0].strip()  if price else None
        Engine = tree.xpath('//div[text()="Engine"]/following-sibling::div//text()')
        Engine= Engine[0].strip() if Engine else None
        body = tree.xpath('//div[text()="Body"]/following-sibling::div//text()')
        body = body[0].strip() if body else None
        Odometer = tree.xpath('//div[text()="Odometer"]/following-sibling::div/text()')
        Odometer = Odometer[0].strip()  if Odometer else None
        Ext_color = tree.xpath('//div[text()="Ext Colour"]/following-sibling::div/text()')
        Ext_color = Ext_color[0].strip() if Ext_color else None
        Interior = tree.xpath('//div[text()="Interior"]/following-sibling::div/text()')
        Interior = Interior[0].strip() if Interior else None
        Transmission = tree.xpath('//div[text()="Transmission"]/following-sibling::div/text()')
        Transmission = Transmission[0].strip() if Transmission else None
        Address = tree.xpath('//a//span[@class="dealership-info"]/text()')
        Address = Address[0].strip()  if Address else None
        Phone = tree.xpath('//span[@class="dealership-info hide-for-large"]/a//text()')
        Phone = Phone[0].strip() if Phone else None
        
        data ={
            "Url": urls,
            "Name" : Name ,
            "Price" : price,
            "Engine" : Engine ,
            "Body": body ,
            "Odometer" : Odometer,
            "Ext_color" : Ext_color,
            "Interior" : Interior,
            "Transmission" : Transmission,
            "Address" : Address,
            "Phone" : Phone
        }
        output.append(data)
df = pd.DataFrame(output)
df.replace("", "NaN")
df=df.dropna(how='all')
df.to_excel("output.xlsx", index=False)
print(df.shape)
