import requests
from rich import print
import json
from lxml import etree
import pandas as pd

url = 'https://www.imdb.com/chart/top/'

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers)

tree = etree.HTML(response.content)

script_data = tree.xpath('//script[@type="application/ld+json"]/text()')[0].strip()
print(script_data)
data = json.loads(script_data)

json_data = data['itemListElement']
output = []
for item in json_data:
    Movie = item.get('item')
    data = {
    "Name" : Movie['name'],
    "url" : Movie['url'],
    "description" : Movie['description'],
    "RatingCount" : Movie['aggregateRating']['ratingCount'],
    "ratingValue" : Movie['aggregateRating']['ratingValue'],
    "contentRating" : Movie.get('contentRating'),
    "duration" : Movie['duration']  
    }
    output.append(data)
df = pd.DataFrame(output)
df.to_excel("OUTPUT.xlsx", index=False)
print(df.shape)