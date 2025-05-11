import requests

all_data = []  # List to store all paginated data

# Loop through pages 1 to 71
for i in range(1, 72):
    url = 'https://api.messefrankfurt.com/service/esb_api/exhibitor-service/api/2.1/public/exhibitor/search'
    params = {
        'language': 'en-GB',
        'q': '',
        'orderBy': 'name',
        'pageNumber': i,  # Corrected this to pass as an integer
        'pageSize': 30,
        'orSearchFallback': 'false',
        'showJumpLabels': 'true',
        'findEventVariable': 'ISH'
    }
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://ish.messefrankfurt.com',
        'Referer': 'https://ish.messefrankfurt.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'apikey': 'LXnMWcYQhipLAS7rImEzmZ3CkrU033FMha9cwVSngG4vbufTsAOCQQ==',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        all_data.append(data)  # Append the response data to the list
        print(f"Page {i} scraped successfully.")
    else:
        print(f"Failed to scrape page {i}. Status code: {response.status_code}")

# Optionally, you can save the collected data to a file or process it further
# Example: Saving to a JSON file
import json
with open('exhibitor_data.json', 'w') as f:
    json.dump(all_data, f, indent=4)

print("Scraping complete. All data saved.")
