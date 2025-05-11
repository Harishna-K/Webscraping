import requests
import os
from tqdm import tqdm
from lxml import etree
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from rich import print

# URL for pagination
url = 'https://www.highpointmarket.org/exhibitordirectory?pageindex=1'

# Headers from the curl command
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

# Proxy details
proxies = {
    "http": "http://ocapgizs-rotate:araohu409l9t@p.webshare.io:80/",
    "https": "http://ocapgizs-rotate:araohu409l9t@p.webshare.io:80/"
}

# Base URL for exhibitor pages
base_url = 'https://www.highpointmarket.org'

# Function to download and extract details from each exhibitor page
def download_and_extract_exhibitor_data(exhibitor_url, page_num):
    try:
        response = requests.get(exhibitor_url, headers=headers, proxies=proxies)
        tree = etree.HTML(response.content)

        # Extract details using XPath
        company_name = tree.xpath('//div[@class="exhibitor-contain"]//h1//text()')
        address = tree.xpath('//div[@class="info-block"]//p//span/span//text()')
        shuttle_stop = tree.xpath('//div[@class="info-block"]//p/span[2]//text()')
        corporate_phone = tree.xpath('//div[@class="info-block"]//p/span[4]//text()')
        website = tree.xpath('//div[@class="info-block"]//p[2]/a//@href')
        # print(company_name, address, shuttle_stop, corporate_phone, website)

        # Clean up extracted data, remove prefixes from shuttle stop and phone
        clean_shuttle_stop = shuttle_stop[0].replace('Shuttle Stop: ', '') if shuttle_stop else None
        clean_corporate_phone = corporate_phone[0].replace('Corporate Phone: ', '') if corporate_phone else None

        data = {
            'Company Name': company_name[0] if company_name else None,
            'Address': ' '.join([addr.strip() for addr in address if addr.strip()]) if address else None,
            'Shuttle Stop': clean_shuttle_stop,
            'Corporate Phone': clean_corporate_phone,
            'Website': website[0] if website else None
        }

        return data

    except Exception as e:
        print(f"Error downloading or extracting exhibitor page {exhibitor_url}: {e}")
        return None

# Extract exhibitor URLs from each pagination page
def extract_exhibitor_links(page_html):
    tree = etree.HTML(page_html)
    links = tree.xpath('//div[@class="col-md-6"]//div//div//div[@class="col thumbnail"]//a/@href')
    return [base_url + link for link in links]

# Scrape all pages and store exhibitor data
def Scrape_pages():
    os.makedirs("Storage", exist_ok=True)
    exhibitor_data_list = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        for page in tqdm(range(1, 181)):
            response = requests.get(url.replace("pageindex=1", f"pageindex={page}"), headers=headers, proxies=proxies)
            page_url = url.replace("pageindex=1", f"pageindex={page}")
            print(f"Processing Page {page_url}")

            # Save pagination page HTML
            with open(f"Storage/Page_{page}.html", "wb") as fp:
                fp.write(response.content)

            # Extract exhibitor links
            exhibitor_links = extract_exhibitor_links(response.content)
            
            # Submit concurrent download tasks for each exhibitor
            future_results = [executor.submit(download_and_extract_exhibitor_data, link, page) for link in exhibitor_links]

            # Collect the results
            for future in future_results:
                exhibitor_data = future.result()
                if exhibitor_data:
                    exhibitor_data_list.append(exhibitor_data)

    # Save all the data to a DataFrame and write to Excel
    df = pd.DataFrame(exhibitor_data_list)
    df.to_excel('exhibitor_data.xlsx', index=False)
    print("Data scraping complete. Saved to exhibitor_data.xlsx")
    

# Call the scrape function
Scrape_pages()
