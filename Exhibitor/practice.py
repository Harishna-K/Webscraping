# import requests
# from rich import print
# from lxml import etree
# import os
# from tqdm import tqdm
# import pandas as pd
# from concurrent.futures import ThreadPoolExecutor
# url = 'https://www.highpointmarket.org/exhibitordirectory?pageindex=1'

# headers = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#     'Accept-Language': 'en-US,en;q=0.9',
#     'Cache-Control': 'max-age=0',
#     'Connection': 'keep-alive',
#     'Sec-Fetch-Dest': 'document',
#     'Sec-Fetch-Mode': 'navigate',
#     'Sec-Fetch-Site': 'none',
#     'Sec-Fetch-User': '?1',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
#     'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
# }

# base_url = "https://www.highpointmarket.org/exhibitordirectory"

# def download_and_process_page(page):
#     page_url = url.replace("pageindex=1", f"pageindex={page}")
#     response = requests.get(page_url, headers=headers)
    
#     with open(f"Database/Page_{page}", "wb") as fp:
#         fp.write(response.content)
#     print(f"processing : {page_url}")
    
#     tree = etree.HTML(response.text)
    
#     each_page_links = tree.xpath('//div[@class="col-md-6"]//div//div//div[@class="col thumbnail"]//a//@href')
    
#     for link in each_page_links:
#         each_page_url = f"{base_url}{link}"
#         page_response = requests.get(each_page_url, headers=headers)
        
#         with open(f"Database/{link.split('/')[-1]}_{page}.html", "wb") as fp:
#             fp.write(page_response.content)
#         print(f"Downloading: {each_page_url}")
        
# os.makedirs("Database", exist_ok=True)
   
# with ThreadPoolExecutor(max_workers=10) as Executor:
#     Executor.map(download_and_process_page, range(1,5))   

import requests
from rich import print
from lxml import etree
import os
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

url = 'https://www.highpointmarket.org/exhibitordirectory?pageindex=1'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

base_url = "https://www.highpointmarket.org/exhibitordirectory"
total_htmls = 0  # To track the total number of HTMLs downloaded

def download_and_process_page(page):
    global total_htmls  # To modify the total_htmls variable
    page_url = url.replace("pageindex=1", f"pageindex={page}")
    response = requests.get(page_url, headers=headers)
    
    os.makedirs(f"Database", exist_ok=True)  # Create directory if it doesn't exist
    
    # Save the main page content
    with open(f"Database/Page_{page}.html", "wb") as fp:
        fp.write(response.content)
    
    print(f"Processing page: {page_url}")
    
    tree = etree.HTML(response.text)
    each_page_links = tree.xpath('//div[@class="col-md-6"]//div//div//div[@class="col thumbnail"]//a//@href')
    
    # Count the total HTMLs in this page (main page + each page links)
    page_html_count = 1  # For the main page itself
    for link in each_page_links:
        each_page_url = f"{base_url}{link}"
        page_response = requests.get(each_page_url, headers=headers)
        
        # Save each link's HTML
        with open(f"Database/{link.split('/')[-1]}_{page}.html", "wb") as fp:
            fp.write(page_response.content)
        
        print(f"Downloading: {each_page_url}")
        page_html_count += 1  # Increase count for each link page downloaded
    
    print(f"Page {page} has {page_html_count} HTMLs downloaded")
    return page_html_count  # Return the number of HTMLs downloaded for this page

total_htmls_per_page = []  # List to store the count of HTMLs per page

# Use ThreadPoolExecutor to download pages concurrently
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(download_and_process_page, page) for page in range(1, 5)]
    
    # Collect results from each page
    for future in futures:
        total_htmls_per_page.append(future.result())

# Sum up total HTMLs from all pages
total_htmls = sum(total_htmls_per_page)

# Print the results
print(f"\nTotal pages processed: {len(total_htmls_per_page)}")
print(f"Total HTMLs downloaded: {total_htmls}")
