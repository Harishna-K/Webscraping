import requests
from lxml import etree
import pandas as pd
import time
import os
from rich import print
import glob
import hashlib

# Create storage folder if it doesn't exist
os.makedirs("Storage", exist_ok=True)

url = 'https://www.fairview.co.nz/stock/results/load'

headers = {
    'accept': '*/*',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://www.fairview.co.nz',
    'referer': 'https://www.fairview.co.nz/stock',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'x-requested-with': 'XMLHttpRequest'
}

base_data = {
    'filters': '{"dealer":[],"location":[],"state":[],"suburb":[],"condition":[],"make":{},"series":{},"model":[],"badge":[],"year":"","budget":"","finance":"","keywords":[],"kilometers":"","body_type":[],"transmission":[],"drive_type":[],"fuel_type":[],"consumption":[],"promotions":[],"sleeps":[],"seats":[],"doors":[],"category_name":[],"featured":[],"colour":[],"more_filters":[],"sort_by":[],"age":[],"variant":[]}',
    'sortby': 'JustArrived',
    'append': 'true'
}

all_vehicles = []
page = 1

def Hash(text):
    sha_256 = hashlib.sha256(text.encode()).hexdigest()
    return sha_256

while True:
    print(f"Scraping page {page}...")
    data = base_data.copy()
    data['page'] = str(page)

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    result = response.json()

    html_content = result.get("html", "")
    if not html_content.strip():
        print("No more data. Stopping.")
        break

    parser = etree.HTMLParser()
    tree = etree.fromstring(html_content, parser)

    items = tree.xpath('//div[contains(@class, "stock-item")]')
    if not items:
        print("No stock items found. Ending.")
        break

    for item in items:
        hrefs = item.xpath('.//a[@class="si-title"]/@href')
        if not hrefs:
            continue
        relative_url = hrefs[0]
        full_url = f"https://www.fairview.co.nz{relative_url}"
        try:
            page_response = requests.get(full_url, headers=headers)
            if page_response.status_code == 200:
                
                file_path = f"Storage/{Hash(full_url)}.html"
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(page_response.text)
                print(f"[green]Saved:[/green] {file_path}")
            else:
                print(f"[red]Failed:[/red] {full_url} (Status {page_response.status_code})")
        except Exception as e:
            print(f"[red]Error downloading {full_url}:[/red] {e}")

    page += 1
    time.sleep(1)

Output = []
for each_file in glob.glob("Storage/*.html"):
    with open(each_file, "r", encoding="utf-8") as fp:
        tree = etree.HTML(fp.read())
        source_url = tree.xpath('//link[@rel="canonical"]/@href')[0].strip()
        Car = tree.xpath('//h1/span//text()')
        Car_name = ' '.join(C.strip() for C in Car if C[0].strip())
        price_1 = tree.xpath('//span[@class="price-value sl-highlight"]/text()')
        price_2 = tree.xpath('//span[@class="price-value sl-highlight price-special"]/text()')
        all_price = price_1 + price_2
        cleaned_price = [price.strip() for price in all_price if price.strip()]
        interest = tree.xpath('//div[@id="sdf-interest"]/text()')[0].strip()
        km = tree.xpath('//span[contains(text(),"Kilometres:")]/following-sibling::span/text()')[0].strip()
        Fuel = tree.xpath('//span[contains(text(),"Fuel Consumption:")]/following-sibling::span/text()')
        Fuel = Fuel[0].strip() if Fuel else " "
        Body = tree.xpath('//span[contains(text(),"Body Type:")]/following-sibling::span/text()')[0].strip()
        type = tree.xpath('//span[contains(text(),"Fuel Type:")]/following-sibling::span/text()')
        type = type[0].strip() if type else ""
        ex_color = tree.xpath('//span[contains(text(),"Exterior Colour:")]/following-sibling::span/text()')
        ex_color = ex_color[0].strip() if ex_color else ""
        Reg_plate = tree.xpath('//span[contains(text(),"Reg Plate:")]/following-sibling::span/text()')
        Reg_plate = Reg_plate[0].strip() if Reg_plate else ""
        Reg_exp = tree.xpath('//div[@class="v_reg_exp"]/text()')
        Reg_exp = Reg_exp[0].strip() if Reg_exp else ""
        stock = tree.xpath('//div[@class="v_stock_no"]/span/text()')[0].strip()
        Vin = tree.xpath('//span[contains(text(),"VIN:")]/following-sibling::span/text()')[0].strip()
        Data = {
            "Source url":source_url,
            "Car Name":Car_name,
            "Price":cleaned_price[0].strip(),
            "Interest Rate":interest,
            "Kilometers":km,
            "Fuel Consumption":Fuel,
            "Body Type":Body,
            "Fuel Type":type,
            "Exterior colour":ex_color,
            "Reg Plate":Reg_plate,
            "Reg Expiry":Reg_exp,
            "Stock":stock,
            "VIN":Vin
            
        }
        Output.append(Data)
        # print(Output)
        
df = pd.DataFrame(Output)
df.to_excel("Output.xlsx", index=False)
print(df.shape)