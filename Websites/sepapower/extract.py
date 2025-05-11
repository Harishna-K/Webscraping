import glob
import pandas as pd
from lxml import etree
Output = []
for each_file in glob.glob(f"Storage/*.html"):
    with open(each_file, "r", encoding='utf-8') as fp:
        tree = etree.HTML(fp.read())
        urls = tree.xpath('//head//link[@rel="canonical"]//@href')[0].strip()
        Title = tree.xpath('//div[@class="content"]/h1//text()')
        clean_title = ''.join(Title).strip()
        print(Title)
        details = {
            "Url" : urls,
            "Resource name" : clean_title
        }
        Output.append(details)
df = pd.DataFrame(Output)
df['Resource name'].replace('', pd.NA, inplace=True)
df = df.dropna(subset=['Resource name'])
df.to_excel("Output.xlsx", index=False)
print(df.shape)
        