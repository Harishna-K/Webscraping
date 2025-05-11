# import requests
# from lxml import etree
# from rich import print
# import json
# import re

# url = "https://csh.ae/"

# headers = {
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#     "Accept-Language": "en-US,en;q=0.9",
#     "Cache-Control": "no-cache",
#     "Connection": "keep-alive",
#     "Pragma": "no-cache",
#     "Sec-Fetch-Dest": "document",
#     "Sec-Fetch-Mode": "navigate",
#     "Sec-Fetch-Site": "none",
#     "Sec-Fetch-User": "?1",
#     "Upgrade-Insecure-Requests": "1",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
#     "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": '"Windows"'
# }
# proxies={
#     "http": "http://vwantbtc-rotate:igt0km7yu76c@p.webshare.io:80/",
#     "https": "http://vwantbtc-rotate:igt0km7yu76c@p.webshare.io:80/"
# }
# response = requests.get(url, headers=headers, proxies=proxies)
# tree = etree.HTML(response.content)

# script_tag = tree.xpath('(//script[contains(text(), "specialties")])[last()]/text()')[-1]
# json_data = re.sub(r"\\", "", script_tag)
# match = re.search(r'{.*}', json_data, re.DOTALL)


# if match:
#     json_string = match.group(0)


#     # Convert the string to a dictionary
#     try:
#         json_obj = json.loads(json_string)
#     except json.JSONDecodeError as e:
#         print(f"Error decoding JSON: {e}")
#         json_obj = {}


#     # Save the cleaned JSON to a file
#     with open("Data.json", 'w') as fp:
#         json.dump(json_obj, fp, indent=4)


# else:
#     print("No JSON data found in the script tag.")
import requests
from lxml import etree
import re
import json

def extract_json_block(text: str) -> str:
    """Extract the first JSON-like block starting with '{' and ending with the matching '}'."""
    start = text.find('{')
    if start == -1:
        return None

    open_braces = 0
    for i in range(start, len(text)):
        if text[i] == '{':
            open_braces += 1
        elif text[i] == '}':
            open_braces -= 1
            if open_braces == 0:
                return text[start:i + 1]

    return None  # Not balanced

# Step 1: Setup
url = "https://csh.ae/"
headers = {
    "User-Agent": "Mozilla/5.0"
}
proxies = {
    "http": "http://vwantbtc-rotate:igt0km7yu76c@p.webshare.io:80/",
    "https": "http://vwantbtc-rotate:igt0km7yu76c@p.webshare.io:80/"
}

# Step 2: Download and parse HTML
response = requests.get(url, headers=headers, proxies=proxies)
tree = etree.HTML(response.content)

# Step 3: Extract script containing JSON
script_tags = tree.xpath('(//script[contains(text(), "specialties")])[last()]/text()')
if not script_tags:
    print("[-] No script tag with 'specialties' found.")
    exit()

script_text = script_tags[0].replace("\\", "")

# Step 4: Extract the JSON block
json_str = extract_json_block(script_text)

if json_str:
    # Step 5: Clean common JSON issues
    cleaned_str = re.sub(r'\$[a-zA-Z0-9_]+', '""', json_str)         # Remove $vars
    cleaned_str = re.sub(r',\s*([}\]])', r'\1', cleaned_str)         # Remove trailing commas

    try:
        data = json.loads(cleaned_str)
        with open("Data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print("[+] JSON successfully extracted and saved to Data.json.")
    except json.JSONDecodeError as e:
        print(f"[!] JSON decoding error: {e}")
        with open("raw_json_failed.txt", "w", encoding="utf-8") as f:
            f.write(cleaned_str)
        print("[!] Raw JSON saved to raw_json_failed.txt for debugging.")
else:
    print("[-] Could not find balanced JSON block.")
