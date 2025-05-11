import requests
from threading import Lock
import hashlib
from lxml import etree
import os
from concurrent.futures import ThreadPoolExecutor
from rich import print
import glob
import pandas as pd

url = 'https://directory.functionalmedicinecoaching.org/search_results?page=1&location_value=United%20States&country_sn=US&location_type=country&stateSearch=&swlat=15.7760139&nelat=72.7087158&swlng=-173.2992296&nelng=-66.3193754&lat=38.7945952&lng=-106.5348379&faddress=United%20States&place_id=ChIJCzYy5IS16lQRQrfeQ5K5Oxw&sort=name%20ASC'

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
}
proxies = {
    "http": "http://ocapgizs-rotate:araohu409l9t@p.webshare.io:80/",
    "https": "http://ocapgizs-rotate:araohu409l9t@p.webshare.io:80/"
}
Base_url = 'https://directory.functionalmedicinecoaching.org'

counter_lock = Lock()
download_counter = 0

def hash(text):
    sha256_hash = hashlib.sha256(text.encode()).hexdigest()
    return sha256_hash

def download_page(Page):
    global download_counter
    page_url = url.replace("page=1", f"page={Page}")
    response = requests.get(page_url, headers=headers, proxies=proxies)
    # print(f"Pagination: {page_url}")
    tree = etree.HTML(response.content)
    
    each_page_links = tree.xpath('//a[@class="center-block"]//@href')
    print(f'{Page}{len(each_page_links)}')
    for link in each_page_links:
        each_page_url = f"{Base_url}{link}"
        page_response = requests.get(each_page_url, headers=headers, proxies=proxies)
        
#         hash_filename = f"Storage/{hash(link)}.html"
        
#         # with open(hash_filename, 'wb') as fp:
#         #     fp.write(page_response.content)
            
        # print(f'Downloaded: {each_page_url}')
        
        with counter_lock:
            download_counter += 1
            
# os.makedirs("Storage", exist_ok=True)

with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(download_page, range(1, 130))
    
print(f"Total Downloaded HTML files: {download_counter}")

# output = []

# for each_file in glob.glob("Storage/*.html"):
#     with open(each_file, 'rb') as fp:
#         tree = etree.HTML(fp.read())    
#         data = {}
#         Name = tree.xpath('//h1[@class="bold inline-block"]//text()')
#         Description = tree.xpath('//div[@class=" clearfix table-display-about_me"]//text()')
#         Year = tree.xpath('//div[@class="col-sm-8"]/span[@class="years years-experience"]//text()')
#         forms_of_payments = tree.xpath('//span[@class="textarea textarea-affiliation"]//text()')
#         company_name = tree.xpath('//span[@class="textbox textbox-company"]//text()')
#         website = tree.xpath('//a[@class="weblink"]//text()')
#         Phone_number = tree.xpath('//div[@class="table-view-group clearfix"]//div[@class="col-sm-8"]/span//text()')
#         Location = tree.xpath('//div[@class="table-view-group clearfix overview-tab-the-member-address"]//div[@class="col-sm-8"]//text()')
#         data = {
#             "Name" : Name[0].strip() if Name else "",
#             "Description" : Description[0].strip() if Description else "",
#             "Year" : Year[0].strip() if Year else "",
#             "Payment" : forms_of_payments[0].strip() if forms_of_payments else "",
#             "Company Name" : company_name[0].strip() if company_name else "",
#             "Website" : website[0].strip() if website else "",
#             "Phone Number" : Phone_number[0].strip() if Phone_number else "",
#             "Location" : Location[0].strip() if Location else ""
#         }
#         output.append(data)
# df = pd.DataFrame(output)
# df.to_excel("Output.xlsx", index=False)
# print(df.shape)
        
    
    
