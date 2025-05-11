import requests
import pandas as pd
from lxml import etree

Output = []
for i in range(0,66):
    url = f"https://www.austinisd.org/cp/conflict-of-interest-vendors/submitted-ciq-vendors?page={i}"
    response = requests.get(url)
    tree = etree.HTML(response.content)
    ventors = tree.xpath('//td[@class="views-field views-field-webform-submission-value is-active"]')
    for business in ventors:
        Ventor = business.xpath('.//a//text()')[0].strip()
        data = {
            "Ventors" : Ventor
        }
        Output.append(data)
df = pd.DataFrame(Output)
df = df.drop_duplicates(subset="Ventors")
df.to_excel("Output.xlsx", index=False)
print(df.shape)

