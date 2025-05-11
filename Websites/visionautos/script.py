# import requests
# from lxml import etree
# import pandas as pd
# from threading import Lock
# import hashlib
# from concurrent.futures import ThreadPoolExecutor
# import os
# import glob
# import json
# import re

# url = 'https://www.visionautos.co.nz/vehicles?Page=1'

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
# proxies={
#     "http": "http://vwantbtc-rotate:igt0km7yu76c@p.webshare.io:80/",
#     "https": "http://vwantbtc-rotate:igt0km7yu76c@p.webshare.io:80/"
# }
# Counter_lock = Lock()
# Download_counter = 0
# base_url = "https://www.visionautos.co.nz"
# def Hash(text):
#     sha256 = hashlib.sha256(text.encode()).hexdigest()
#     return sha256

# def Download_html(Page):
#     global Download_counter
#     try:
#         page_url = url.replace("Page=1", f"Page={Page}")
#         response = requests.get(page_url, headers=headers, proxies=proxies)
#         if response.status_code == 200 :
#             tree = etree.HTML(response.content)
#             each_page = tree.xpath('//div[@class="small-10 columns"]//a//@href')
#             for link in each_page:
#                 each_page_url = f"{base_url}{link}"
#                 page_response = requests.get(each_page_url,headers=headers, proxies=proxies)
#                 if page_response.status_code == 200:
#                     # file_name = f"Storage/{Hash(link)}.html"
#                     file_name = f"Vehicles/{sanitize_filename(link)}.html"
#                     with open(file_name, "wb") as fp:
#                         fp.write(page_response.content)
#                     print(f"Downloaded: {link}")
                    
#                     with Counter_lock:
#                         Download_counter += 1
#                 else:
#                     print(f"Failed to Download: {link}")
        
#         else:
#             print(f"Failed to Download: {page_url}")
#     except Exception as e:
#         print(f"Error Fetched: {e} status: {response.status_code}")
# os.makedirs("Vehicles", exist_ok=True)               
# with ThreadPoolExecutor(max_workers=10) as executor:
#     executor.map(Download_html, range(1,9))
# print(f"Total Number of htmls Downloaded: {Download_counter}")

# Output = []
# for each_file in glob.glob("Storage/*.html"):
#     with open(each_file, "r") as fp:
#         tree = etree.HTML(fp.read())
#         Source_url = f""
#         Name = tree.xpath('//div[@class="title"]//h2//text()')[0].strip()
#         Price = tree.xpath('//span[@class="amount"]/text()')
#         Engine = tree.xpath('//div[contains(text(), "Engine")]/following-sibling::div//text()')[0].strip()
#         Body = tree.xpath('//div[contains(text(), "Body")]/following-sibling::div//text()')[0].strip()
#         Odometer = tree.xpath('//div[contains(text(), "Odometer")]/following-sibling::div//text()')[0].strip()
#         Ext_colour = tree.xpath('//div[contains(text(), "Ext Colour")]/following-sibling::div//text()')[0].strip()
#         Interior = tree.xpath('//div[contains(text(), "Interior")]/following-sibling::div//text()')[0].strip()
#         Transmission = tree.xpath('//div[contains(text(), "Transmission")]/following-sibling::div//text()')[0].strip()
#         Data = {
#             "Name" : Name,
#             "Price" : Price,
#             "Engine" : Engine,
#             "Body" : Body,
#             "Odometer" : Odometer,
#             "Ext Colour" : Ext_colour,
#             "Interior" : Interior,
#             "Transmission" : Transmission
#         }
#         Output.append(Data)
# df = pd.DataFrame(Output)
# df.to_excel("Output.xlsx", index=False)
# print(df.shape)
        
        
import requests
from lxml import etree
import pandas as pd
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
import os
import glob
import re

# Constants
url = 'https://www.visionautos.co.nz/vehicles?Page=1'
base_url = "https://www.visionautos.co.nz"
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
}
proxies = {
    "http": "http://vwantbtc-rotate:igt0km7yu76c@p.webshare.io:80/",
    "https": "http://vwantbtc-rotate:igt0km7yu76c@p.webshare.io:80/"
}

# Locks & Counters
Counter_lock = Lock()
Download_counter = 0

# Create output directory
os.makedirs("Vehicles", exist_ok=True)

# Helpers
def sanitize_filename(link):
    return re.sub(r'[\\/*?:"<>|]', '_', link.strip('/'))

def filename_to_url(file_path):
    filename = os.path.basename(file_path).replace('.html', '')
    original_path = filename.replace('_', '/')
    return f"https://www.visionautos.co.nz/{original_path}"

# HTML Downloader
def Download_html(Page):
    global Download_counter
    try:
        page_url = url.replace("Page=1", f"Page={Page}")
        response = requests.get(page_url, headers=headers, proxies=proxies)
        if response.status_code == 200:
            tree = etree.HTML(response.content)
            each_page = tree.xpath('//div[@class="small-10 columns"]//a//@href')
            for link in each_page:
                each_page_url = f"{base_url}{link}"
                try:
                    page_response = requests.get(each_page_url, headers=headers, proxies=proxies)
                    if page_response.status_code == 200:
                        file_name = f"Vehicles/{sanitize_filename(link)}.html"
                        with open(file_name, "wb") as fp:
                            fp.write(page_response.content)
                        print(f"Downloaded: {each_page_url}")
                        with Counter_lock:
                            Download_counter += 1
                    else:
                        print(f"Failed to download detail page: {each_page_url}")
                except Exception as inner_e:
                    print(f"Error downloading {each_page_url}: {inner_e}")
        else:
            print(f"Failed to fetch listing page: {page_url}")
    except Exception as e:
        print(f"Error on Page {Page}: {e}")

# Download all pages concurrently
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(Download_html, range(1, 9))

print(f"\n✅ Total Number of HTMLs Downloaded: {Download_counter}\n")

# Extract Data
Output = []
for each_file in glob.glob("Vehicles/*.html"):
    with open(each_file, "r", encoding="utf-8") as fp:
        try:
            tree = etree.HTML(fp.read())
            Source_url = filename_to_url(each_file)
            Name = tree.xpath('//div[@class="title"]//h2//text()')[0].strip()
            Price = tree.xpath('//span[@class="amount"]/text()')[0].strip()
            Engine = tree.xpath('//div[contains(text(), "Engine")]/following-sibling::div//text()')[0].strip()
            Body = tree.xpath('//div[contains(text(), "Body")]/following-sibling::div//text()')[0].strip()
            Odometer = tree.xpath('//div[contains(text(), "Odometer")]/following-sibling::div//text()')[0].strip()
            Ext_colour = tree.xpath('//div[contains(text(), "Ext Colour")]/following-sibling::div//text()')[0].strip()
            Interior = tree.xpath('//div[contains(text(), "Interior")]/following-sibling::div//text()')[0].strip()
            Transmission = tree.xpath('//div[contains(text(), "Transmission")]/following-sibling::div//text()')[0].strip()

            Data = {
                "Source URL": Source_url,
                "Name": Name,
                "Price": Price,
                "Engine": Engine,
                "Body": Body,
                "Odometer": Odometer,
                "Ext Colour": Ext_colour,
                "Interior": Interior,
                "Transmission": Transmission
            }
            Output.append(Data)
        except Exception as e:
            print(f"⚠️ Error parsing file {each_file}: {e}")

# Save to Excel
df = pd.DataFrame(Output)
df.to_excel("Output.xlsx", index=False)
print(f"\n✅ Data extracted and saved to 'Output.xlsx' | Total rows: {df.shape[0]}")
