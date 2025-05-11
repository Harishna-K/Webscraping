import requests
from lxml import etree
import json
import pandas as pd
url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': '',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers)
with open("test.json", "r") as fp:
    data = json.load(fp)
movie_links = data["itemListElement"]

urls = []

for each_movie in movie_links:
    movie = each_movie.get("item")
    details = {
        "name" : movie.get("name"), 
        "movie url" :movie.get("url") , 
        "description" : movie.get("description"), 
        "rating count" : movie.get("aggregateRating")["ratingCount"], 
        "rating value" : movie.get("aggregateRating")["ratingValue"], 
        "content rating " : movie.get("contentRating"), 
        "duration" : movie.get("duration")
    }
    urls.append(details)
df = pd.DataFrame(urls)
df.to_excel("Task.xlsx", index=False)
print(df.shape)