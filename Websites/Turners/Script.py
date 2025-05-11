import requests
from lxml import etree
import os
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
import hashlib
import glob
import pandas as pd

# Constants
BASE_URL = "https://www.turners.co.nz"
PAGE_TEMPLATE = "https://www.turners.co.nz/Cars/Used-Cars-for-Sale/?sortorder=7&pagesize=20&pageno={page}&issearchsimilar=true"
STORAGE_DIR = "Storage"
TOTAL_PAGES = 53  # Adjust if more pages exist

# Headers for requests
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}

# Optional proxy
# proxies = {
#     "http": "http://user:pass@proxy:port",
#     "https": "http://user:pass@proxy:port"
# }

# Thread-safe download counter
counter_lock = Lock()
download_counter = 0

# Ensure storage directory exists
os.makedirs(STORAGE_DIR, exist_ok=True)

# Generate SHA-256 hash for URL to use as filename
def get_sha256_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()

# Download and process a single page of listings
def download_and_process_page(page):
    global download_counter
    page_url = PAGE_TEMPLATE.format(page=page)
    print(f"[+] Scraping Page: {page_url}")
    try:
        response = requests.get(page_url, headers=headers, timeout=10)
        tree = etree.HTML(response.text)
        links = tree.xpath('//a[@class="product-summary-title"]/@href')
        
        for link in links:
            full_url = BASE_URL + link
            print(f"    [-] Downloading Detail Page: {full_url}")
            try:
                detail_resp = requests.get(full_url, headers=headers, timeout=10)
                hashed_filename = os.path.join(STORAGE_DIR, f"{get_sha256_hash(link)}.html")
                with open(hashed_filename, "wb") as fp:
                    fp.write(detail_resp.content)
                with counter_lock:
                    download_counter += 1
            except Exception as e:
                print(f"    [!] Failed to download detail page: {full_url} - {e}")
    except Exception as e:
        print(f"[!] Failed to load listing page: {page_url} - {e}")

# Step 1: Download all vehicle HTML files
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(download_and_process_page, range(1, TOTAL_PAGES + 1))

print(f"[✔] Total HTML files downloaded: {download_counter}")

# Step 2: Parse downloaded HTML files and extract data
output = []

for filepath in glob.glob(os.path.join(STORAGE_DIR, "*.html")):
    try:
        with open(filepath, "r", encoding="utf-8") as fp:
            tree = etree.HTML(fp.read())
            data = {
                "Name": tree.xpath('//div[@class="title"]/h2//text()')[0].strip() if tree.xpath('//div[@class="title"]/h2//text()') else None,
                "Engine": tree.xpath('(//div[@class="small-7 columns"])[1]//text()')[0].strip() if tree.xpath('(//div[@class="small-7 columns"])[1]//text()') else None,
                "Odometer": tree.xpath('(//div[@class="small-7 columns"])[2]//text()')[0].strip() if tree.xpath('(//div[@class="small-7 columns"])[2]//text()') else None,
                "Ext_color": tree.xpath('(//div[@class="small-7 columns"])[3]//text()')[0].strip() if tree.xpath('(//div[@class="small-7 columns"])[3]//text()') else None,
                "Interior": tree.xpath('(//div[@class="small-7 columns"])[4]//text()')[0].strip() if tree.xpath('(//div[@class="small-7 columns"])[4]//text()') else None,
                "Transmission": tree.xpath('(//div[@class="small-7 columns"])[5]//text()')[0].strip() if tree.xpath('(//div[@class="small-7 columns"])[5]//text()') else None,
                "Emission": ''.join(tree.xpath('(//div[@class="small-12 columns title ellipsis"])[1]//text()')).strip().replace("Emissions", "").replace("(", "").replace(")", "") if tree.xpath('(//div[@class="small-12 columns title ellipsis"])[1]//text()') else None,
                "Mileage": ''.join(tree.xpath('(//p[@class="mileage"])[1]//text()')).strip().replace("Fuel economy of ", "").replace("per 100km", "") if tree.xpath('(//p[@class="mileage"])[1]//text()') else None
            }
            output.append(data)
    except Exception as e:
        print(f"[!] Error parsing {filepath}: {e}")

# Step 3: Save data to Excel
df = pd.DataFrame(output)
df.to_excel("output.xlsx", index=False)
print(f"[✔] Data saved to output.xlsx — {df.shape[0]} rows.")
