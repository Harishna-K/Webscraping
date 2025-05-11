import requests
import hashlib
from lxml import etree
import pandas as pd
import os
import glob
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
import time
from rich import print

url = 'https://www.autopride.co.nz/vehicles.php?&pageNum=1'
base_url = 'https://www.autopride.co.nz/'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
}
proxies = {
    "http": "http://vwantbtc-rotate:igt0km7yu76c@p.webshare.io:80/",
    "https": "http://vwantbtc-rotate:igt0km7yu76c@p.webshare.io:80/"
}

counter_lock = Lock()
download_counter = 0
Failed_pages = []
Less_data = []
downloaded_links = set()

def hash_sha_256(text):
    return hashlib.sha256(text.encode()).hexdigest()

def download_html(page):
    global download_counter
    retries = 7

    for attempt in range(retries):
        try:
            page_url = url.replace('pageNum=1', f'pageNum={page}')
            response = requests.get(page_url, headers=headers, proxies=proxies)

            if response.status_code == 200:
                print(f"[bold green]Pagination:[/] {page_url}")
                tree = etree.HTML(response.content)
                each_page = tree.xpath('//div[@class="fea"]/a/@href')

                if len(each_page) < 18:
                    print(f"[yellow]Less than 18 providers found:[/] Page {page}, Found: {len(each_page)}")
                    Less_data.append(page)

                if not each_page:
                    print(f"[red]No provider links found on page {page}[/]")
                    continue

                for link in each_page:
                    if link in downloaded_links:
                        continue
                    downloaded_links.add(link)

                    each_page_url = f"{base_url}{link}"
                    page_response = requests.get(each_page_url, headers=headers, proxies=proxies)

                    if page_response.status_code == 200:
                        tree = etree.HTML(page_response.content)
                        file_name = f"Storage/{page}_{hash_sha_256(link)}.html"

                        with open(file_name, 'wb') as fp:
                            fp.write(page_response.content)

                        with counter_lock:
                            download_counter += 1
                            print(f"[blue]Downloaded:[/] {link}")
                    else:
                        print(f"[red]Failed to download link:[/] {link}, status code: {page_response.status_code}")
            else:
                print(f"[red]Failed to download page:[/] {page_url}, status code: {response.status_code}")
            break

        except requests.RequestException as e:
            print(f"[red]Error while downloading page {page}, attempt {attempt + 1}/{retries}[/]")
            if attempt == retries - 1:
                print(f"[bold red]Giving up on page {page} after {retries} attempts.[/]")
                Failed_pages.append(page)
            time.sleep(5 * (attempt + 1))

# Create folder if it doesn't exist
os.makedirs("Storage", exist_ok=True)

# Run with multithreading
with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(download_html, range(1, 26))

print(f"[bold cyan]Total downloaded:[/] {download_counter}")
if Failed_pages:
    print(f"[bold yellow]Retrying failed pages:[/] {Failed_pages}")
    for page in Failed_pages:
        time.sleep(2)
        download_html(page)

print(f"[bold green]All done![/]")
print(f"[bold magenta]Less than 18 providers pages:[/] {Less_data}")

# -------------------------------
# Parsing section
# -------------------------------
Output = []

for each_file in glob.glob("Storage/*.html"):
    with open(each_file, "r", encoding="utf-8") as fp:
        tree = etree.HTML(fp.read())

        try:
            Source_url = tree.xpath('//meta[@property="og:url"]/@content')[0].strip()
            Name = tree.xpath('//div[@class="col-md-9"]//h3/text()')[0].strip()
            Make = tree.xpath('//span[contains(text(), "Make")]/following-sibling::strong/text()')[0].strip()
            Model = tree.xpath('//span[contains(text(), "Model")]/following-sibling::strong/text()')
            model = Model[0].strip() if Model else " "
            Year = tree.xpath('//span[contains(text(), "Year")]/following-sibling::strong/text()')[0].strip()
            Body = tree.xpath('//span[contains(text(), "Body")]/following-sibling::strong/text()')[0].strip()
            Milege = tree.xpath('//span[contains(text(), "Mileage")]/following-sibling::strong/text()')[0].strip()
            Transmission = tree.xpath('//span[contains(text(), "Transmission")]/following-sibling::strong/text()')[0].strip()
            Fuel = tree.xpath('//span[contains(text(), "Fuel")]/following-sibling::strong/text()')[0].strip()
            Exterior_color = tree.xpath('//span[contains(text(), "Exterior Color")]/following-sibling::strong/text()')[0].strip()
            Interior_color = tree.xpath('//span[contains(text(), "Interior Color")]/following-sibling::strong/text()')
            Int_clr = Interior_color[0].strip() if Interior_color else " "
            Engine = tree.xpath('//span[contains(text(), "Engine")]/following-sibling::strong/text()')[0].strip()
            Doors = tree.xpath('//span[contains(text(), "Doors")]/following-sibling::strong/text()')[0].strip()
            Seats = tree.xpath('//span[contains(text(), "Seats")]/following-sibling::strong/text()')[0].strip()
            Dealership = tree.xpath('//span[contains(text(), "Dealership")]/following-sibling::strong/text()')[0].strip()
            Stock_no = tree.xpath('//span[contains(text(), "Stock No")]/following-sibling::strong/text()')[0].strip()

            Data = {
                "Source url": Source_url,
                "Name": Name,
                "Make": Make,
                "Model": model,
                "Year": Year,
                "Body": Body,
                "Milege": Milege,
                "Transmission": Transmission,
                "Fuel": Fuel,
                "Exterior color": Exterior_color,
                "Interior color": Int_clr,
                "Engine": Engine,
                "Doors": Doors,
                "Seats": Seats,
                "Dealership": Dealership,
                "Stock Number": Stock_no
            }
            Output.append(Data)

        except Exception as e:
            print(f"[red]Failed to parse:[/] {each_file} - {e}")

df = pd.DataFrame(Output)
df.to_excel("Output.xlsx", index=False)
print(f"[bold green]{df.shape}[/] rows saved to Output.xlsx")
