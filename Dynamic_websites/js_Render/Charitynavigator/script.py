import requests
from lxml import etree
from rich import print
import json
import re
from concurrent.futures import ThreadPoolExecutor
import os
import glob
import pandas as pd
# Base URL for pagination
base_url = "https://www.charitynavigator.org/search?causes=Arts+and+culture%2CEnvironment%2CReligion%2CHuman+rights&page={page}&rating=3%2B&sizes=large%2Csuper&pageSize=10"

# Headers for the request
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
}
proxies={
    "http": "http://vwantbtc-rotate:igt0km7yu76c@p.webshare.io:80/",
    "https": "http://vwantbtc-rotate:igt0km7yu76c@p.webshare.io:80/"
}
# Function to extract and save JSON data
def extract_json_data(page):
    url = base_url.format(page=page)
    response = requests.get(url, headers=headers,proxies=proxies)
    tree = etree.HTML(response.content)
    script_data = tree.xpath("//script//text()")[-1]
    json_data = re.sub(r'\\', '', script_data)
    match = re.search(r'{.*}', json_data, re.DOTALL)

    if match:
        json_string = match.group(0)
        try:
            json_obj = json.loads(json_string)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON on page {page}: {e}")
            return False

        # Save the JSON data to a file
        with open(f"Storage/Data_Page_{page}.json", 'w') as fp:
            json.dump(json_obj, fp, indent=4)

        print(f"Page {page} downloaded successfully.")
        return True
    else:
        print(f"No JSON data found on page {page}.")
        return False
os.makedirs("Storage", exist_ok=True)
# Main code to download the data concurrently and track the progress
def download_all_pages(max_pages=350):
    total_downloaded = 0
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(extract_json_data, range(1, max_pages)))

    total_downloaded = sum(results)
    print(f"Total JSON files downloaded: {total_downloaded} out of {max_pages} pages.")

# Run the download process
download_all_pages(350)


output = []

# Loop through each JSON file in the Storage directory
for each_file in glob.glob("Storage/*.json"):
    with open(each_file, 'r') as fp:
        data = json.load(fp)
        
        # Navigate through the nested structure based on the JSON provided
        children_list = data.get('children', [])
        for outer_list in children_list:
            if isinstance(outer_list, list):  # Check if outer_list is a list
                for middle_list in outer_list:
                    if isinstance(middle_list, dict):  # Ensure middle_list is a dict
                        inner_children = middle_list.get('children', [])
                        for inner_dict in inner_children:
                            if isinstance(inner_dict, dict) and 'results' in inner_dict:
                                results = inner_dict.get('results', [])
                                for result in results:
                                    details = {
                                        "URL":f'https://www.charitynavigator.org' + result.get('url', ''),
                                        "Name": result.get('name', ''),
                                        "EIN": result.get('ein', ''),
                                        "city":result.get('city', ''),
                                        "state":result.get('state', ''),
                                        "rating":result.get('rating', ''),
                                        "star_rating":result.get('star_rating', ''),
                                    }
                                    output.append(details)

# Convert the extracted data to a DataFrame
df = pd.DataFrame(output)

# Save the DataFrame to an Excel file
df.to_excel("Output.xlsx", index=False)

# Print the DataFrame
print(df)

                


        
        