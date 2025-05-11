import requests
import os
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import hashlib
from threading import Lock
import glob
import pandas as pd

url = 'https://livingassistedguide.com/search-results/?layout=half_map&show_currencies=0&sort=featured&es_type%5B0%5D=917&state=17669Name&paged-1=1&sort-1=featured'

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

proxies = {
    "http": "http://ocapgizs-rotate:araohu409l9t@p.webshare.io:80/",
    "https": "http://ocapgizs-rotate:araohu409l9t@p.webshare.io:80/"
}

# Create a lock to ensure thread-safe counter increment
counter_lock = Lock()
download_counter = 0  # Variable to track the number of downloaded files

# Function to generate SHA-256 hash for a URL
def get_sha256_hash(text):
    sha256_hash = hashlib.sha256(text.encode()).hexdigest()
    return sha256_hash

# Function to download and process each page
def download_and_process_page(page):
    global download_counter
    page_url = url.replace("paged-1=1", f"paged-1={page}")
    response = requests.get(page_url, headers=headers, proxies=proxies)  # , proxies=proxies to enable proxies if needed

    print(f"Pagination: {page_url}")
    
    # Parse the HTML content
    tree = etree.HTML(response.text)
    
    # Extract links
    each_page_links = tree.xpath('//h3[@class="es-listing__title"]/a/@href')
    
    # Loop through the extracted URLs and save them
    for link in each_page_links:
        page_response = requests.get(link, headers=headers, proxies=proxies)  # , proxies=proxies to enable proxies if needed
        
        # Generate a SHA-256 hash for the link and use it as the filename
        hashed_filename = f"Storage/{get_sha256_hash(link)}.html"
        
        # Save the HTML content for each listing
        with open(hashed_filename, "wb") as fp:
            fp.write(page_response.content)
        
        print(f"Downloading: {link} -> Saved as {hashed_filename}")
        
        # Safely increment the download counter
        with counter_lock:
            download_counter += 1

# Create directory to store the downloaded pages
os.makedirs("Storage", exist_ok=True)

# Using ThreadPoolExecutor to download pages concurrently
# with ThreadPoolExecutor(max_workers=10) as executor:
#     # Submit tasks for each page to download and process
#     executor.map(download_and_process_page, range(1, 104))  # Specify the page range

# After all tasks are complete, print the total number of downloaded files
# print(f"Total HTML files downloaded: {download_counter}")

output = []
for each_file in glob.glob("Storage/*.html"):
    with open(each_file, "r", encoding="utf-8") as fp:
        tree = etree.HTML(fp.read())
        data = {}
        Urls = tree.xpath('//link[@rel="canonical"]//@href')
        Address = tree.xpath('//div[@class="es-single__header-left"]/span[@class="es-address"]//text()')
        Type_xpath = tree.xpath('//li[@class="es-entity-field es-entity-field--es_type es-property-field es-property-field--es_type es-property-field--default es-entity-field--full-width"]//span[@class="es-property-field__value es-entity-field__value"]/a//text()')
        Type = ', '.join(text.strip() for text in Type_xpath)
        Phone = tree.xpath('//li[@class="es-entity-field es-entity-field--phone-number es-property-field es-property-field--phone-number es-property-field--default es-entity-field--full-width"]/span[@class="es-property-field__value es-entity-field__value"]//text()')
        Email = tree.xpath('//li[@class="es-entity-field es-entity-field--Email-Address es-property-field es-property-field--Email-Address es-property-field--default"]/span[@class="es-property-field__value es-entity-field__value"]//text()')
        county = tree.xpath('//li[@class="es-entity-field es-entity-field--province es-property-field es-property-field--province es-property-field--province"]//span[@class="es-property-field__value es-entity-field__value"]/a//text()')
        print(Type)
        data = {
            "URL" : Urls[0].strip() if Urls else None,
            "Address" : Address[0].strip() if Address else None,
            "Type" : Type,
            "Phone" : Phone[0].strip() if Phone else None,
            "Email" : Email[0].strip() if Email else None,
            "County" : county[0].strip() if county else None
        }
        output.append(data)
df = pd.DataFrame(output)
df.to_excel("Data.xlsx", index=False)
print(df.shape)
        