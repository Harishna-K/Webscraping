import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
import pandas as pd
import os
import glob
import hashlib
from rich import print
import time

url = 'https://www.autocourt.net.nz/vehicles?Page=1'
base_url = 'https://www.autocourt.net.nz'

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
    "http": "http://vwantbtc-rotate:igt0km7yu76c@p.webshare.io:80/",
    "https": "http://vwantbtc-rotate:igt0km7yu76c@p.webshare.io:80/"
}
# Counter_lock = Lock()
# Download_counter = 0
# Less_page = []
# Failed_pages = []

# def Hash(text):
#     return hashlib.sha256(text.encode()).hexdigest()

# def Download_htmls(page):
#     global Download_counter
#     Retries = 5
#     for attempt in range(Retries):
#         try:
#             page_url = url.replace("Page=1", f"Page={page}")
#             response = requests.get(page_url, headers=headers, proxies=proxies)
#             if response.status_code == 200:
#                 print(f"Pagination:{page_url}")
#                 tree = etree.HTML(response.content)
#                 each_page = tree.xpath('//div[@class="small-10 columns"]//a/@href')
#                 if len(each_page) < 20:
#                     print(f"Less than 20 pages in page:{page}")
#                     Less_page.append(page)
                
#                 if not each_page:
#                     print(f"No more pages in page:{page}")
#                     continue
                
#                 for link in each_page:
#                     Each_page_url = f"{base_url}{link}"
#                     page_response = requests.get(Each_page_url, headers=headers, proxies=proxies)
#                     if page_response.status_code == 200:
#                         tree = etree.HTML(page_response.content)
#                         file_name = f"Storage/{page}_{Hash(link)}.html"
#                         with open(file_name, "wb") as fp:
#                             fp.write(page_response.content)
#                         with Counter_lock:
#                             Download_counter += 1
#                             print(f"Downloading:{link}")
#                     else:
#                         print(f"Failed to Download:{link}")
#             else:
#                 print(f"Failed to Download page:{page}")
#             break
#         except Exception as e:
#             print(f"Error while Downloading page:{page}")
#             if attempt == Retries - 1:
#                 print(f"Giving upon page:{page}, attempts{attempt + 1}/{Retries} attempts.")
#                 Failed_pages.append(page)
#             time.sleep(1)
# os.makedirs("Storage", exist_ok=True)
# with ThreadPoolExecutor(max_workers=10) as executor:
#     executor.map(Download_htmls, range(1,4))
# print(f"Total Htmls:{Download_counter}")
# if Failed_pages:
#     print(f"Retrying pages:{Failed_pages}")
#     for page in Failed_pages:
#         Download_htmls(page)
# print(f"Less than 20 count pages are{Less_page}")
# print("All Done")
                
Output = []
for each_file in glob.glob("Storage/*.html"):
     with open(each_file, "r") as fp:
        tree = etree.HTML(fp.read())
        data = {}
        Source = tree.xpath('//link[@rel="canonical"]/@href')[0].strip()
        Title = tree.xpath('//div[@class="title"]//h2/text()')[0].strip()
        price = tree.xpath('//div[@class="price-container-content"]//span//span/span[@class="amount"]/text()')[0].strip()
        Engine = tree.xpath('//div[contains(text(), "Engine")]/following-sibling::div/text()')[0].strip()
        Body = tree.xpath('//div[contains(text(), "Body")]/following-sibling::div/text()')[0].strip()
        Odometer = tree.xpath('//div[contains(text(), "Odometer")]/following-sibling::div/text()')[0].strip()
        Ext_color = tree.xpath('//div[contains(text(), "Ext Colour")]/following-sibling::div/text()')[0].strip()
        Interior = tree.xpath('//div[contains(text(), "Interior")]/following-sibling::div/text()')[0].strip()
        Transmission = tree.xpath('//div[contains(text(), "Transmission")]/following-sibling::div/text()')[0].strip()
        data = {
            "Source url" : Source,
            "Title" : Title,
            "Price" : price,
            "Engine" : Engine,
            "Body" : Body,
            "Odometer" : Odometer,
            "Exterior color" :  Ext_color,
            "Interior" : Interior,
            "Transmission" : Transmission
        }
        Output.append(data)
df = pd.DataFrame(Output)
df.to_excel("Output.xlsx", index=False)
print(df.shape)                
            
            

