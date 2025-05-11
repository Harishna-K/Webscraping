import requests
import json
import pandas as pd
# Base URL for the API
url = 'https://xd0u5m6y4r-2.algolianet.com/1/indexes/evt-9e57c7b1-72b6-498a-bec2-07ea87a6be90-index/query?x-algolia-agent=Algolia%20for%20JavaScript%20(3.35.1)%3B%20Browser&x-algolia-application-id=XD0U5M6Y4R&x-algolia-api-key=d5cd7d4ec26134ff4a34d736a7f9ad47'

# Headers for the request
headers = {
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Origin': 'https://www.londonbookfair.co.uk',
    'Referer': 'https://www.londonbookfair.co.uk/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'accept': 'application/json',
    'content-type': 'application/json',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}
def scrape_all_pages():
    all_data = []
    page = 0  
    while True:
        payload = {
            'params': f'query=&page={page}&filters=recordType:exhibitor AND locale:en-gb AND eventEditionId:eve-b058582b-882a-4b01-a984-8cc4c75bc592&facetFilters=&optionalFilters=[]'
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            data = response.json()

            hits = data.get("hits", [])
            if not hits:
                print(f"No data on page {page}. Ending scrape.")
                break

            all_data.extend(hits)  # Add the data to the list
            print(f"Page {page} scraped. Number of records: {len(hits)}")

            # Check if there are more pages
            if page >= data.get('nbPages', 0) - 1:
                print("No more pages available.")
                break

            # Go to the next page
            page += 1
        else:
            print(f"Failed to retrieve data from page {page}. Status code: {response.status_code}")
            print("Response Text:", response.text)  # Print the error response for debugging
            break

    return all_data

all_exhibitor_data = scrape_all_pages()

print(f"Total records scraped: {len(all_exhibitor_data)}")

# Example: Save the data to a JSON file or process it further
with open("exhibitors_data.json", "w") as f:
    json.dump(all_exhibitor_data, f, indent=4)

def scrape_data():
    with open("exhibitors_data.json", "r") as fp:
        Data = json.load(fp)

    all_data = []

    for hit in Data:
        Website = hit.get('website', "").strip()
        Company_name = hit.get('companyName', "").strip()
        exhibitorname = hit.get('exhibitorName', "").strip()
        Description = hit.get('exhibitorDescription', "").strip()
        phone = hit.get('phone', "").strip()
        email = hit.get('email', "").strip()
        country = hit.get('countryName', "").strip()
        details = {
            
            "Company Name": Company_name,
            "Exhibitor Name": exhibitorname,
            "Description": Description,
            "Phone Number": phone,
            "Email": email,
            "Country": country,
            "Website": Website
        }
        all_data.append(details)
        
    df = pd.DataFrame(all_data)

    df.fillna('N/A', inplace=True)
    df.to_excel("Cleaned_Output.xlsx", index=False)
    print(f"Total cleaned records: {df.shape[0]}")
scrape_data()