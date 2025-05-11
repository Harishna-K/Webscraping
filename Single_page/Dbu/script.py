from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from lxml import etree
import hashlib
import time
import os

# Setup headless Chrome
options = Options()
options.add_argument("--headless=new")  # use "new" mode for newer Chrome
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
os.makedirs("Storage", exist_ok=True)

def Hash(text):
    return hashlib.sha256(text.encode()).hexdigest()

# Step 1: Load main search result page
driver.get("https://www.dbu.dk/resultater/klubsoeg/?q=e")
time.sleep(3)  # wait for JS to load

# Step 2: Extract club links
tree = etree.HTML(driver.page_source)
club_links = tree.xpath('//td//a/@href')

# Step 3: Visit each klubinfo page
for link in club_links:
    if "/resultater/Klub/" in link:
        club_id = link.strip("/").split("/")[-1]
        klubinfo_url = f"https://www.dbu.dk/resultater/klub/{club_id}/klubinfo"

        print(f"Visiting: {klubinfo_url}")
        driver.get(klubinfo_url)
        time.sleep(3)  # allow page to load

        # Save fully rendered page
        with open(f"Storage/{Hash(klubinfo_url)}.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print(f"Saved klubinfo for club {club_id}")

driver.quit()
