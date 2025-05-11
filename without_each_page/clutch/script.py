import requests
from requests.exceptions import RequestException
import hashlib
from lxml import etree
import os
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
import time
from rich import print

url = 'https://clutch.co/call-centers/appointment-setting?page=1'

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
}
proxies={
    "http": "http://ocapgizs-rotate:araohu409l9t@p.webshare.io:80/",
    "https": "http://ocapgizs-rotate:araohu409l9t@p.webshare.io:80/"
}
os.makedirs("Storage", exist_ok=True)
counter_lock = Lock()
Download_counter = 0
def hash(text):
    sha_256 = hashlib.sha256(text.encode()).hexdigest()
    return sha_256

from requests.exceptions import RequestException

def Download_htmls(page):
    global Download_counter
    try:
        page_url = url.replace("page=1", f"page={page}")
        response = requests.get(page_url, headers=headers, timeout=10)
        if response.status_code == 200:
            tree = etree.HTML(response.content)
            file_name = f"Storage/{hash(page_url)}.html"
            with open(file_name, "w", encoding="utf-8") as fp:
                fp.write(response.text)
                print(f"Downloading: {page_url}")
            with counter_lock:
                Download_counter += 1
        else:
            print(f"Failed to download {page_url} — Status: {response.status_code}")
    except RequestException as e:
        print(f"Error fetching {page_url}: {e}")

with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(Download_htmls, range(1,27))
print(f"Total number of htmls: {Download_counter}")
    

