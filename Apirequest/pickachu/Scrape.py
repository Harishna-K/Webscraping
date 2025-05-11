import requests
import pandas as pd
from rich import print

baseurl = 'https://rickandmortyapi.com/api/'

endpoint = 'character'

def main_request(baseurl, endpoint, x):
    r = requests.get(baseurl + endpoint + f'?page={x}')
    return r.json()

def get_pages(response):
    return response['info']['pages']

def parse_json(response): 
    charlist = []
    for item in response['results']:
        char = {
            'id' : item['id'],
            'name' : item['name'], 
            'no_ep' : len(item['episode'])
        }
        charlist.append(char)
    return charlist

mainlist = []
data = main_request(baseurl, endpoint, 1)
for x in range(1,get_pages(data)+1):
    print(x)
    mainlist.extend(parse_json(main_request(baseurl, endpoint, x)))
df = pd.DataFrame(mainlist)
df.to_excel("data.xlsx", index=False)




