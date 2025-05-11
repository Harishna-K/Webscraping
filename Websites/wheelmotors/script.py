import requests
import pandas as pd
from lxml import etree
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
import os
import glob
import hashlib


url = 'https://www.wheelermotors.co.nz/vehicles?Page=1'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': 'mc-cc=1; mc-st=; ai_user=+NeCV|2025-02-07T15:55:55.680Z; _gcl_au=1.1.215213399.1738943757; _hjSession_1536073=eyJpZCI6Ijk4MTUxOGYyLWFhYWYtNGQwNC04YmI2LTVhNjI5YzgyNjdjMSIsImMiOjE3Mzg5NDM3NTcxMzIsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MX0=; _fbp=fb.2.1738943757740.138608246579641050; _gid=GA1.3.1017631705.1738943758; _hjSessionUser_1536073=eyJpZCI6IjQ4NTJhNWNkLWUxNDAtNWMxOC04MTRjLWY0YmJkOWM3ZjQzMCIsImNyZWF0ZWQiOjE3Mzg5NDM3NTcxMzEsImV4aXN0aW5nIjp0cnVlfQ==; _ga=GA1.3.1347200327.1738943758; ai_session=hfpUe|1738943758356|1738943788277.3; _ga_X4VKGZD9J4=GS1.3.1738943760.1.1.1738943788.0.0.0; _ga_ZYRZXMYF7M=GS1.1.1738943758.1.1.1738943788.0.0.0; _ga_VZPVBFZ7S6=GS1.1.1738943758.1.1.1738943788.30.0.1769433526',
    'Referer': 'https://www.wheelermotors.co.nz/vehicles',
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
base_url = 'https://www.wheelermotors.co.nz'

counter_lock = Lock()
download_counter = 0

def hash(text):
    sha256_hash = hashlib.sha256(text.encode()).hexdigest()
    return sha256_hash

def download_page(page):
    
    global download_counter
    
    page_url = url.replace("Page=1", f"Page={page}")
    response = requests.get(page_url, headers=headers)
    
    print(f'Pagination: {page_url}')
    
    tree = etree.HTML(response.content)
    
    each_page_link = tree.xpath('//div[@class="small-10 columns"]//a//@href')

    for link in each_page_link:
        each_page_url = f'{base_url}{link}'
        page_response = requests.get(each_page_url, headers=headers)
        
        hash_filename = f'Storage/{hash(link)}.html'
        
        with open(hash_filename, 'wb') as fp:
            fp.write(page_response.content)
            
        print(f"Downloaded: {hash_filename}")
        
        with counter_lock:
            download_counter +=1
            
os.makedirs('Storage', exist_ok=True)
with ThreadPoolExecutor(max_workers=10) as Executor:
    Executor.map(download_page, range(1, 3))
print(f"Total HTML files Downloaded : {download_counter}")

output = []

for each_file in glob.glob("Storage/*.html"):
    filename = os.path.basename(each_file)
    with open(each_file, 'r', encoding='utf-8') as fp:
        tree = etree.HTML(fp.read())
        data = {}
        urls = f'{base_url}/{filename.replace(".html", "")}'
        Model = tree.xpath('//div[@class="title"]//h1//text()')[0].strip()
        Engine = tree.xpath('(//div[@class="small-7 columns"])[position()=1]//text()')
        Body = tree.xpath('//div[@class="small-7 columns "]//text()')
        Odometer = tree.xpath('(//div[@class="small-7 columns"])[position()=2]//text()')[0].strip()
        Ext_color = tree.xpath('(//div[@class="small-7 columns"])[position()=3]//text()')[0].strip()
        interior_list = tree.xpath('(//div[@class="small-7 columns"])[position()=4]//text()')
        
        data = {
            "Url": urls,
            "Model" : Model,
            "Engine" : Engine,
            "Body" : Body,
            "Odometer" : Odometer,
            "Ext_color" : Ext_color,
        }
        output.append(data)
df = pd.DataFrame(output)
df.to_excel("output.xlsx", index=False)
print(df.shape)
        


