# import requests
# from threading import Lock
# import hashlib
# from lxml import etree
# from concurrent.futures import ThreadPoolExecutor
# import os

# # Constants
# base_url = 'https://www.sgdi.gov.sg/'
# headers = {
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
#     'accept-language': 'en-US,en;q=0.9',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
# }
# proxies = {
#     "http": "http://ocapgizs-rotate:araohu409l9t@p.webshare.io:80/",
#     "https": "http://ocapgizs-rotate:araohu409l9t@p.webshare.io:80/"
# }

# os.makedirs("downloaded_pages", exist_ok=True)

# # XPath rules per directory
# xpaths = {
#     "ministries": '//ul[@class="ministries"]//li//a/@href',
#     "statutory-boards": '//ul[@class="ministries"]//li//a/@href',
#     "organs-of-state": '//ul[@class="ministries"]//li//a/@href',
#     "other-organisations": '//ul[@class="ministries"]//li//a/@href',
#     "spokespersons": '//ul[@class="contact-list"]//li//a/@href',
# }

# # All directory names
# Directories = [
#     "ministries",
#     "statutory-boards",
#     "organs-of-state",
#     "other-organisations",
#     "public-services",
#     "spokespersons"
# ]

# # Helper: hash a URL to create filename
# def hash_text(text):
#     return hashlib.sha256(text.encode()).hexdigest()

# # Save HTML to file
# def save_html(content, url):
#     filename = hash_text(url) + ".html"
#     filepath = os.path.join("downloaded_pages", filename)
#     with open(filepath, "wb") as f:
#         f.write(content)

# # Download individual detail page
# def download_detail_page(link):
#     try:
#         if not link.startswith("http"):
#             link = base_url.rstrip('/') + link
#         response = requests.get(link, headers=headers, proxies=proxies, timeout=20)
#         if response.status_code == 200:
#             save_html(response.content, link)
#             print(f"Downloaded: {link}")
#     except Exception as e:
#         print(f"Failed to download {link}: {e}")

# # Process each directory
# def process_directory(directory):
#     urls_to_download = []

#     # Special case: public-services
#     if directory == "public-services":
#         url = f"{base_url}{directory}?char=all"
#         try:
#             response = requests.get(url, headers=headers, proxies=proxies, timeout=20)
#             if response.status_code == 200:
#                 save_html(response.content, url)
#                 print(f"Saved full public-services page: {url}")
#         except Exception as e:
#             print(f"Error fetching public-services: {e}")
#         return

#     # Other directories with respective xpaths
#     url = f"{base_url}{directory}"
#     try:
#         response = requests.get(url, headers=headers, proxies=proxies, timeout=20)
#         if response.status_code == 200:
#             tree = etree.HTML(response.content)
#             links = tree.xpath(xpaths[directory])
#             urls_to_download.extend(links)
#             print(f"Collected {len(links)} links from {directory}")
#         else:
#             print(f"Failed to load: {url}")
#     except Exception as e:
#         print(f"Error fetching {directory}: {e}")

#     # Download all detail pages using threads
#     with ThreadPoolExecutor(max_workers=10) as executor:
#         executor.map(download_detail_page, urls_to_download)

# # Main runner
# if __name__ == "__main__":
#     for directory in Directories:
#         process_directory(directory)

import os
from lxml import etree
import pandas as pd

# Folder containing the downloaded HTML pages
html_folder = "downloaded_pages"

# Output list
data = []

# Loop through each HTML file
for filename in os.listdir(html_folder):
    if filename.endswith(".html"):
        filepath = os.path.join(html_folder, filename)
        with open(filepath, 'rb') as f:
            content = f.read()

        tree = etree.HTML(content)

        # Extract data using robust XPaths
        title = tree.xpath('//div[@class="agency-title no-margin"]/h1//text()')
        tel = tree.xpath('//p[@class="tel" and contains(text(), "Tel")]/following-sibling::p[@class="tel-info"][1]/text()')
        fax = tree.xpath('//p[@class="tel" and contains(text(), "Fax")]/following-sibling::p[@class="tel-info"][1]/text()')
        website = tree.xpath('//p[@class="website"]/a/@href')

        # Extract address across multiple lines, stopping before "Tel"
        address_lines = tree.xpath('//address/p[@class="street-address"]/following-sibling::p[preceding-sibling::p[@class="street-address"] and following-sibling::p[@class="tel"]]/text()')
        address = " ".join([line.strip() for line in address_lines if line.strip()])

        # Append the cleaned results
        data.append({
            "File": filename,
            "Title": title[0].strip() if title else "",
            "Address": address,
            "Telephone": tel[0].strip() if tel else "",
            "Fax": fax[0].strip() if fax else "",
            "Website": website[0].strip() if website else ""
        })

# Convert to DataFrame and save
df = pd.DataFrame(data)
df.to_excel("sgdi_cleaned_data.xlsx", index=False)

print("✅ Data extraction complete. Saved to sgdi_cleaned_data.xlsx.")
