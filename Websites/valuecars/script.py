import requests
from threading import Lock
import hashlib
from lxml import etree
import os
from concurrent.futures import ThreadPoolExecutor
from rich import print
import glob
import pandas
url = 'https://www.valuecarswarehouse.co.nz/vehicles?Page=1'

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
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
# base_url = 'https://www.valuecarswarehouse.co.nz'

# counter_lock = Lock()
# download_counter = 0

# def hash(text):
#     sha256_hash = hashlib.sha256(text.encode()).hexdigest()
#     return sha256_hash

# def download_page(page):
    
#     global download_counter
    
#     page_url = url.replace("Page=1", f"Page={page}")
#     response = requests.get(page_url, headers=headers)
    
#     print(f'Pagination: {page_url}')
    
#     tree = etree.HTML(response.content)
    
#     each_page_link = tree.xpath('//div[@class="small-10 columns"]//a//@href')

#     for link in each_page_link:
#         each_page_url = f'{base_url}{link}'
#         page_response = requests.get(each_page_url, headers=headers)
        
#         hash_filename = f'Storage/{hash(link)}.html'
        
#         with open(hash_filename, 'wb') as fp:
#             fp.write(page_response.content)
            
#         print(f"Downloaded: {hash_filename}")
        
#         with counter_lock:
#             download_counter +=1
            
# os.makedirs('Storage', exist_ok=True)
# with ThreadPoolExecutor(max_workers=10) as Executor:
#     Executor.map(download_page, range(1, 2))
# print(f"Total HTML files Downloaded : {download_counter}")

output = []

for each_file in glob.glob("Storage/*.html"):
    filename = os.path.basename(each_file)
    with open(each_file, 'r', encoding='utf-8') as fp:
        tree = etree.HTML(fp.read())
        data = {}
        urls = tree.xpath('//link[@rel="canonical"]//@href')[0].strip()
        Model = tree.xpath('//div[@class="title"]//h2//text()')[0].strip()
        Engine = tree.xpath('(//div[@class="small-7 columns"])[position()=1]//text()')[0].strip()
        Body = tree.xpath('//div[@class="small-7 columns "]//text()')[0].strip()
        Odometer = tree.xpath('(//div[@class="small-7 columns"])[position()=2]//text()')[0].strip()
        Ext_color = tree.xpath('(//div[@class="small-7 columns"])[position()=3]//text()')[0].strip()
        interior_list = tree.xpath('(//div[@class="small-7 columns"])[position()=4]//text()')
        if interior_list:
            interior_text = interior_list[0].strip()
            if '(' in interior_text:
                Interior = tree.xpath('normalize-space(substring-before((//div[@class="small-7 columns"])[position()=4]//text(), " ("))')
            elif '- (Cloth)' in interior_text:
                Interior = ""
            elif '-' in interior_text:
                Interior = ""
            else:
                Interior = interior_text
        Transmission = tree.xpath('(//div[@class="small-7 columns"])[position()=5]//text()')[0].strip()
        data = {
            "Url": urls,
            "Model" : Model,
            "Engine" : Engine,
            "Body" : Body,
            "Odometer" : Odometer,
            "Ext_color" : Ext_color,
            "Interior" : Interior,
            "Transmission" : Transmission 
        }
        output.append(data)
df = pandas.DataFrame(output)
df.to_excel("output.xlsx", index=False)
print(df.shape)
        


