import requests
from lxml import etree
import pandas as pd

url = 'https://arsp.cd/registre-des-entreprises-enregistrees/'

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
}

response = requests.get(url, headers=headers)
parser = etree.HTMLParser()
tree = etree.HTML(response.content, parser)
html_string = etree.tostring(tree, pretty_print=True, encoding='unicode')

# with open("test.html", "w", encoding="utf-8") as fp:
#     fp.write(html_string)
    
tables = pd.read_html('test.html')
df = tables[0]

df = df.dropna(how="all")
df =df.drop(["Date de publication", "Voir plus"], axis=1)

df.to_excel("new.xlsx", index=False)
print(df.shape)
