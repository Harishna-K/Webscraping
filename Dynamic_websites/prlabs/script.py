import requests
import pandas as pd
from bs4 import BeautifulSoup

# Define the URL with pagination
base_url = "https://prlabs.com/prlocator/index/ajax/?p="

# Headers to mimic a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
proxies={
    "http": "http://vwantbtc-rotate:igt0km7yu76c@p.webshare.io:80/",
    "https": "http://vwantbtc-rotate:igt0km7yu76c@p.webshare.io:80/"
}
all_data = []

# Loop through pages (change range as needed)
for page in range(1, 20):
    url = f"{base_url}{page}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        
        for item in data['items']:
            lat = item.get("lat", "")
            lng = item.get("lng", "")
            marker_url = item.get("marker_url", "")
            popup_html = item.get("popup_html", "")

            # Parse HTML using BeautifulSoup
            soup = BeautifulSoup(popup_html, "html.parser")
            
            # Extract Name
            name_elem = soup.select_one(".prlocator-title .address-txt")
            name = name_elem.text.strip() if name_elem else ""

            # Extract Address
            address_elem = soup.select_one(".address-info")
            address = address_elem.text.strip().replace("\n", " ") if address_elem else ""

            # Extract Phone
            phone_elem = soup.select_one("a[href^='tel:']")
            phone = phone_elem.text.replace("Phone:", "").strip() if phone_elem else ""

            # Extract Email
            email_elem = soup.select_one("a[href^='mailto:']")
            email = email_elem.get("href", "").replace("mailto:", "") if email_elem else ""

            # Append extracted data
            all_data.append({
                "Name": name,
                "Address": address,
                "Latitude": lat,
                "Longitude": lng,
                "Phone": phone,
                "Email": email,
                "Marker URL": marker_url
            })

    else:
        print(f"Failed to fetch page {page}")

# Save data to CSV
df = pd.DataFrame(all_data)
df = df.drop_duplicates()
df.to_csv("prlabs_data.csv", index=False)

df.to_excel("prlabs_data.xlsx", index=False)


print("Data saved to prlabs_data.csv")
