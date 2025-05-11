
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
url = 'https://www.bestcars4u.co.nz/vehicles.xhtml?page=1&'

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
    'sec-ch-ua-platform': '"Windows"'
}

proxies = {
    "http": "http://ocapgizs-rotate:araohu409l9t@p.webshare.io:80/",
    "https": "http://ocapgizs-rotate:araohu409l9t@p.webshare.io:80/"
}
base_url = 'https://www.bestcars4u.co.nz/'
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
            page_url = url.replace('page=1', f'page={page}')
            response = requests.get(page_url, headers=headers, proxies=proxies)
            
            if response.status_code == 200:
                print(f"Pagination: {page_url}")
                tree = etree.HTML(response.content)
                each_page = tree.xpath('//div[@class="col-sm-4 col-md-4 col-lg-4"]//div[@class="carsell_bx"]//div[@class="carsell_img"]//a//@href')
                
                # if len(each_page) < 12:  # Corrected comparison
                #     print(f"Less than 12 providers found: {page}, {len(each_page)} providers")
                #     Less_data.append(page)  # Append page number where the issue occurs

                # Check if we have valid links
                if not each_page:
                    print(f"No provider links found on page {page}")
                    continue
                
                for link in each_page:
                    each_page_url =f'{base_url}{link}'
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
# with ThreadPoolExecutor(max_workers=10) as executor:
#     executor.map(download_html, range(1, 4))

output = []
for each_file in glob.glob(f"Storage/*.html"):
    with open(each_file, 'rb') as fp:
        tree = etree.HTML(fp.read())
        data = {}
        urls = f'{base_url}{each_file.replace('Storage', '').replace('.html', '')}'
        Name = tree.xpath('//h2[@class="title_prodetail"]//text()')[0].strip()
        price = tree.xpath("//h5//text()")[0].strip()
        Engine = tree.xpath('//td[text()="Engine"]/following-sibling::td/text()')[0].strip()
        body = tree.xpath('//td[text()="Body"]/following-sibling::td/text()')[0].strip()
        Odometer = tree.xpath('//td[text()="Odometer"]/following-sibling::td/text()')[0].strip()
        Ext_color = tree.xpath('//td[text()="Ext Colour"]/following-sibling::td/text()')[0].strip()
        Interior = tree.xpath('//td[text()="Interior"]/following-sibling::td/text()')
        Interior = Interior[0].strip() if Interior else None
        Transmission = tree.xpath('//td[text()="Transmission"]/following-sibling::td/text()')[0].strip()   
        Address = tree.xpath('//div[@class="col-sm-3 col-md-3 col-lg-3"]//ul[@class="footer_addressL"]//li[1]/text()')
        Address = Address[0].strip()  if Address else None
        Phone = tree.xpath('//div[@class="col-sm-3 col-md-3 col-lg-3"]//ul[@class="footer_addressL"]//li[3]/text()')[0].strip()
        
        data ={
            "Url": urls,
            "Name" : Name if Name else None,
            "Price" : price if price else None,
            "Engine" : Engine if Engine else None,
            "Body": body if body else None,
            "Odometer" : Odometer if Odometer else None,
            "Ext_color" : Ext_color if Ext_color else None,
            "Interior" : Interior,
            "Transmission" : Transmission if Transmission else None,
            "Address" : Address,
            "Phone" : Phone if Phone else None
        }
        output.append(data)
df = pd.DataFrame(output)
df.to_excel("output.xlsx", index=False)
print(df.shape)
