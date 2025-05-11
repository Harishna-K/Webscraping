import pandas as pd
from lxml import etree
import glob
output = []
for each_file in glob.glob("Storage/*.html"):
    with open(each_file, "r", encoding='utf-8') as fp:
        tree = etree.HTML(fp.read())
        Url = tree.xpath('//link[@rel="canonical"]//@href')[0].strip()
        Name = tree.xpath('//h1[@class="provider-full-name loc-co-fname"]//text()')[0].strip()
        Rating = tree.xpath('//span/span[@class="avg-ratings"]//text()')
        clean_rating = ''.join(Rating).strip()
        Rating_count = tree.xpath('///button[@class="webmd-button webmd-button--text webmd-button--medium active-review-count"]//span//text()')
        clean_rating_count = Rating_count[0].split("with")[0].strip()
        Experience =tree.xpath('//div[@class="years-of-exp"]/span//text()')
        clean_experience = ''.join(Experience).strip()
        location_name =  tree.xpath('//div[@class="prov-location-name loc-co-tplcnm"]//text()')[0].strip()
        Address = tree.xpath('//p[@class="prov-address-text loc-co-tplcadd"]//text()')[0].strip()
        Phone = tree.xpath('//div[@class="btn-holder"]//a//span/span//text()')
        clean_phone = ''.join(Phone).strip()
        # print(f"Name:{Name}", f"Experience:{Experience}")
        data = {
            "Url" : Url,
            "Name": Name,
            "Rating": clean_rating,
            "Rating_count": clean_rating_count,
            "location_name": location_name,
            "Address": Address,
            "Experience" : clean_experience,
            "Phone": clean_phone
        }
        output.append(data)
df = pd.DataFrame(output)
df.to_excel("Output.xlsx", index=False)
print(df.shape)