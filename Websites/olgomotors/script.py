import requests
from lxml import etree
from threading import Lock
import hashlib
import os
from concurrent.futures import ThreadPoolExecutor
import glob
import pandas as pd
url = 'https://www.olgomotors.co.nz/vehicles?Make=&Text=&PriceFrom=0&PriceTo=0&YearFrom=0&YearTo=0&Transmission=&BodyStyle=&Dealership=&SortOption=0&EngineSizeFrom=0&EngineSizeTo=0&OdometerFrom=0&OdometerTo=0&Model=&VehicleType=Used%2cUsed&IgnoreContext=&ExtColor1=&DoorNo=&FuelType1=&SearchType=&Page=1'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}
# base_url = 'https://www.olgomotors.co.nz/'

# counter_lock = Lock()
# download_counter = 0

# def hash(text):
#     sha256_hash = hashlib.sha256(text.encode()).hexdigest()
#     return sha256_hash

# def download_and_process_page(page):
#     global download_counter
#     page_url = url.replace("Page=1", f"Page={page}")
#     response = requests.get(page_url, headers=headers)
#     print(f"Pagination:{page_url}")
    
#     tree = etree.HTML(response.text)
    
#     each_page_links = tree.xpath('//li[@class="vehicle"]//div//div[@class="small-12 vehicle-specs specs-gallery columns"]//span[@class="spec-btn"]/a[@class="olbutton"]//@href')
    
#     for link in each_page_links:
#         each_page_url = f"{base_url}{link}"        
#         page_response = requests.get(each_page_url, headers=headers)
#         print(f'Link: {each_page_url}')
        
#         hash_filename = f"Storage/{hash(link)}.html"
        
#         with open(hash_filename, 'wb') as fp:
#             fp.write(page_response.content)
#         print(f"Downloaded: {link}")
            
#         with counter_lock:
#                 download_counter += 1
            
# os.makedirs("Storage", exist_ok=True)

# with ThreadPoolExecutor(max_workers=10) as Executor:
#     Executor.map(download_and_process_page, range(1, 15))
# print(f"Total downloaded files: {download_counter}")

output = []

for each_file in glob.glob("Storage/*.html"):
    with open(each_file, "r", encoding='utf-8') as fp:
        tree = etree.HTML(fp.read())
        data = {}
        Name = tree.xpath('//div[@class="title"]//h1//text()')[0].strip()
        Price = tree.xpath('//div[@class="price-wrapper"]//span//span[@class="price"]//text()')[0].strip()
        Body = tree.xpath('(//div[@class="small-7 columns "])[position()=1]//text()')[0].strip()
        Odometer = tree.xpath('(//div[@class="small-7 columns"])[position()=1]//text()')[0].strip()
        Ext_color = tree.xpath('(//div[@class="small-7 columns"])[position()=2]//text()')[0].strip()
        Int_color = tree.xpath('(//div[@class="small-7 columns"])[position()=3]//text()')[0].strip()
        Engine_size = tree.xpath('(//div[@class="small-7 columns"])[position()=4]//text()')[0].strip()
        Fuel_type = tree.xpath('(//div[@class="small-7 columns"])[position()=5]//text()')[0].strip()
        Transmission = tree.xpath('(//div[@class="small-7 columns"])[position()=6]//text()')[0].strip()
        Airbags = tree.xpath('(//div[@class="small-7 columns"])[position()=7]//text()')
        data = {
            "Name": Name,
            "Price" : Price,
            "Body" :Body,
            "Odometer" : Odometer,
            "Ext_color" : Ext_color,
            "Int_color" : Int_color,
            "Engine Size" : Engine_size,
            "Fuel Type" : Fuel_type,
            "Transmission" : Transmission,
            "Airbags" : Airbags[0].strip() if Airbags else None
        }
        output.append(data)
df = pd.DataFrame(output)
df.to_excel("olgomotors.xlsx", index=False)
print(df.shape)       
