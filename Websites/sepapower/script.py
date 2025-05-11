import requests
from threading import Lock
import hashlib
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import os

url = 'https://sepapower.org/knowledge/?_type=case-study&_publication_period=last-5-years&_paged=1'

# Headers to mimic a real browser
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
}


# Proxy configuration (make sure this is working as expected)
proxies = {
    "http": "http://ocapgizs-rotate:araohu409l9t@p.webshare.io:80/",
    "https": "http://ocapgizs-rotate:araohu409l9t@p.webshare.io:80/"
}

# Lock for thread safety
counter_lock = Lock()
download_counter = 0

# Function to hash a string (for filenames)
def hash_text(text):
    sha256_hash = hashlib.sha256(text.encode()).hexdigest()
    return sha256_hash
publication_type = ['case-study', 'report', 'white-paper']
# Function to download pages and save them
def download_page(page_number, pub_type):
    global download_counter
    page_url = f'https://sepapower.org/knowledge/?_type={pub_type}&_publication_period=last-5-years&_paged={page_number}'
    response = requests.get(page_url, headers=headers, proxies=proxies)

    if response.status_code == 200:
        print(f"Pagination: {page_url}")
        tree = etree.HTML(response.content)

        # Extract each article's URL
        each_page_url = tree.xpath('//main[@class="card-content"]//a//@href')

        for link in each_page_url:
            page_response = requests.get(link, headers=headers, proxies=proxies)
            
            if page_response.status_code == 200:
                print(f"Link: {link}")
                hash_filename = f"Storage/{hash_text(link)}.html"
                
                # Save the page content to file
                with open(hash_filename, "w", encoding='utf-8') as fp:
                    fp.write(page_response.text)
                
                print(f"Downloaded: {link} -> saved as {hash_filename}")
                
                # Safely update the download counter
                with counter_lock:
                    download_counter += 1
            else:
                print(f"Failed to download: {link}, status code: {page_response.status_code}")
    else:
        print(f"Failed to fetch page: {page_url}, status code: {response.status_code}")

# Create a storage directory if it doesn't exist
os.makedirs("Storage", exist_ok=True)

# Use ThreadPoolExecutor to download pages concurrently
with ThreadPoolExecutor(max_workers=10) as executor:
    for pub_type in publication_type:
        executor.map(download_page, range(1, 8), [pub_type] *7)

print(f"Total HTML Files Downloaded: {download_counter}")
