import requests
from lxml import etree
import os
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
import hashlib
import glob
import pandas as pd
url = 'https://www.ajmotors.co.nz/vehicles?Page=1'
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
}

proxies = {
    "http": "http://ocapgizs-rotate:araohu409l9t@p.webshare.io:80/",
    "https": "http://ocapgizs-rotate:araohu409l9t@p.webshare.io:80/"
}

base_url = 'https://www.ajmotors.co.nz'

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
    page_url = url.replace("Page=1", f"Page={page}")
    response = requests.get(page_url, headers=headers)  # , proxies=proxies to enable proxies if needed

    print(f"Pagination: {page_url}")
    
    # Parse the HTML content
    tree = etree.HTML(response.text)
    
    # Extract links
    each_page_links = tree.xpath('//div[@class="small-10 columns"]//a//@href')
    
    # Loop through the extracted URLs and save them
    for link in each_page_links:
        each_page_url = f'{base_url}{link}'
        print(f"Link: {each_page_url}")
        page_response = requests.get(each_page_url, headers=headers)  # , proxies=proxies to enable proxies if needed
        
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
with ThreadPoolExecutor(max_workers=10) as executor:
    # Submit tasks for each page to download and process
    executor.map(download_and_process_page, range(1, 54))  # Specify the page range

# After all tasks are complete, print the total number of downloaded files
print(f"Total HTML files downloaded: {download_counter}")

output = []

for each_file in glob.glob("Storage/*.html"):
    with open(each_file, "r", encoding='utf-8') as fp:
        tree =  etree.HTML(fp.read())
        data = {}
        Name = tree.xpath('//div[@class="title"]/h2//text()')[0].strip()
        Engine = tree.xpath('(//div[@class="small-7 columns"])[position()=1]//text()')[0].strip()
        Odometer = tree.xpath('(//div[@class="small-7 columns"])[position()=2]//text()')[0].strip()
        Ext_color = tree.xpath('(//div[@class="small-7 columns"])[position()=3]//text()')[0].strip()
        Interior = tree.xpath('(//div[@class="small-7 columns"])[position()=4]//text()')[0].strip()
        Transmission = tree.xpath('(//div[@class="small-7 columns"])[position()=5]//text()')[0].strip()   
        Emission_clean = ''.join(tree.xpath('(//div[@class="small-12 columns title ellipsis"])[position()=1]//text()')).strip()  
        Emission = Emission_clean.replace("Emissions", "").replace("(", "").replace(")", "")
        Mileage_clean = ''.join(tree.xpath('(//p[@class="mileage"])[position()=1]//text()')).strip()
        Mileage = Mileage_clean.replace("Fuel economy of ", "").replace("per 100km", "")
        data ={
            "Name" : Name if Name else None,
            "Engine" : Engine if Engine else None,
            "Odometer" : Odometer if Odometer else None,
            "Ext_color" : Ext_color if Ext_color else None,
            "Interior" : Interior if Interior else None,
            "Transmission" : Transmission if Transmission else None,
            "Emmission" : Emission if Emission else None,
            "Mileage" : Mileage if Mileage else None
        }
        output.append(data)
df = pd.DataFrame(output)
df.to_excel("output.xlsx", index=False)
print(df.shape)
