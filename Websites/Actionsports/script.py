import requests
import hashlib
from rich import print
import glob 
import pandas as pd
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
import os
from lxml import etree

url = 'https://actionsportsdirect.co.nz/collections/all-products?page=1'

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
}
proxies={
    "http": "http://vwantbtc-rotate:igt0km7yu76c@p.webshare.io:80/",
    "https": "http://vwantbtc-rotate:igt0km7yu76c@p.webshare.io:80/"
}
def Hash(text):
    sha_256 = hashlib.sha256(text.encode()).hexdigest()
    return sha_256
Counter_lock = Lock()
Download_counter = 0
def Download_htmls(page):
    global Download_counter
    Page_url = url.replace("page=1", f"page={page}")
    response = requests.get(Page_url, headers=headers, proxies=proxies)
    print(f"Pagination:{Page_url}")
    if response.status_code == 200:
        try:
            tree = etree.HTML(response.content)
            Each_page = tree.xpath('//a[@class="card-link text-current js-prod-link"]/@href')
            for link in Each_page:
                base_url = "https://actionsportsdirect.co.nz"
                Each_page_url = f"{base_url}{link}"
                page_response = requests.get(Each_page_url, headers=headers, proxies=proxies)
                if page_response.status_code == 200:
                    try:
                        file_name = f"Storage/{Hash(link)}.html"
                        with open(file_name, "w", encoding="utf-8") as f:
                            f.write(page_response.text)
                        print(f'Downloaded:{link}')
                        
                        with Counter_lock:
                            Download_counter += 1
                    except:
                        print(f"Error Downloading file:{link} status:{page_response.status_code}")
                else:
                    print(f"Failed to Fetch:{link}")
        except:
            print(f"Error Downloading page:{page}")
    else:
        print(f"Failed to Fetch page:{page}")

os.makedirs("Storage", exist_ok=True)
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(Download_htmls, range(1,23))
print(f"Total HTMLS Downloaded:{Download_counter}")

Output = []

for each_file in glob.glob("Storage/*.html"):
    with open(each_file, "r", encoding='utf-8') as fp:
        tree = etree.HTML(fp.read())
        Source_url = tree.xpath('//link[@rel="canonical"]/@href')[0].strip()
        SKU = tree.xpath('//span[contains(text(), "SKU:")]/following-sibling::span/text()')
        SKU = [S.strip() for S in SKU if S]
        Title = tree.xpath('//h1/text()')[0].strip()
        price = tree.xpath('//div[@class="price__default"]/strong[@class="price__current"]/text()')[0].strip()
        Data = {
            "Source Url":Source_url,
            "SKU":SKU[0] if SKU else None,
            "Title":Title,
            "Price":price,
        }
        Output.append(Data)
df = pd.DataFrame(Output)
df.to_excel("Output.xlsx", index=False)
print(df.shape)

