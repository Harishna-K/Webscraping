import requests
from threading import Lock
import hashlib
import os
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import time

base_url = 'https://doctor.webmd.com/providers/specialty/plastic-surgery/?pagenumber={}'

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
}
proxies = {
    "http": "http://ocapgizs-rotate:araohu409l9t@p.webshare.io:80/",
    "https": "http://ocapgizs-rotate:araohu409l9t@p.webshare.io:80/"
}

counter_lock = Lock()
download_counter = 0

def hash(text):
    sha_256 = hashlib.sha256(text.encode()).hexdigest()
    return sha_256

def download_page(page_number):
    global download_counter
    retries = 3
    for attempt in range(retries):
        try:
            page_url = base_url.format(page_number)
            response = requests.get(page_url, headers=headers, proxies=proxies)
            print(f"Pagination: {page_number}")
            if response.status_code == 200:
                tree = etree.HTML(response.text)
                each_page_links = tree.xpath('//h2/a[@class="prov-name"]//@href')
                for link in each_page_links:
                    print(f"Downloading: {link}")
                    page_response = requests.get(link, headers=headers, proxies=proxies)
                    if page_response.status_code == 200:
                        file_name = f"Storage/{hash(link)}.html"
                        with open(file_name, "w", encoding="utf-8") as fp:
                            fp.write(page_response.text)
                        with counter_lock:
                            download_counter += 1
                            print(f"Downloaded: {download_counter}")
                    else:
                        print(f"Failed to download: {link} (Status Code: {page_response.status_code})")
            else:
                print(f"Failed to download pagination: {page_number} (Status Code: {response.status_code})")
                break
        except requests.RequestException as e:
            print(f"Error while downloading page {page_number}, attempt {attempt +1}/retries: {e}")
            if attempt == retries - 1:
                print(f"Giving up on page {page_number} after {retries} attempts.")
            time.sleep(3)

os.makedirs("Storage", exist_ok=True)

with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(download_page, range(1, 251))

print(f"The total number of pages downloaded: {download_counter}")
