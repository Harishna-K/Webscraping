import glob
import json
import pandas as pd

def clean_website_url(url):
    url = url.strip()  # Remove any leading or trailing whitespace
    
    # If the URL is None or ends with a period, return an empty string
    if not url or url == 'https://www.' or url.endswith('.'):
        return ""  # Return an empty string for invalid URLs
    
    # Add "https://" if not present
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # If the URL doesn't contain "www.", add it after "https://"
    if 'www.' not in url:
        protocol, rest_of_url = url.split('//', 1)
        if not rest_of_url.startswith('www.') and '.' in rest_of_url:  # Ensure the domain part has a valid structure
            url = f'{protocol}//www.{rest_of_url}'
    
    return url.lower()  # Convert to lowercase for consistency

Output = []

for each_file in glob.glob("Exhibitors/*.json"):
    
    with open(each_file, 'r') as fp:
        Details = json.load(fp)
        
        directory = Details["EXHIBITOR"]["DIRECTORY"]
        company_name = directory.get("COMPANY_NAME", {})
        category = directory.get("CATEGORY", [])
        website = directory.get("WEBSITE", {})
        city = directory.get("CITY", {})
        state = directory.get("STATE", {})
        country = directory.get("COUNTRY", {})
        phone = directory.get("PHONE", {})
        Toll = directory.get("TOLL_FREE", {})
        Fax = directory.get("FAX", {})
        Zip = directory.get("ZIP_CODE", {})
        Address_1 = directory.get("ADDRESS1", {})
        Address_2 = directory.get("ADDRESS2", {})
        
        # Clean the website URL
        cleaned_website = clean_website_url(website)
        
        for cate in category:
            categories = cate.get("ANSWER_TITLE", {})
        
        Datas = {
            "Company Name": company_name,
            "Category": categories,
            "Website": cleaned_website,
            "Address 1": Address_1,
            "Address 2": Address_2,
            "City": city,
            "State": state,
            "Zip Code": Zip,
            "Country": country,
            "Phone": phone,
            "Toll Free": Toll,
            "Fax": Fax,
        }  
        Output.append(Datas)
        
df = pd.DataFrame(Output)
df.to_excel("Output_clean.xlsx", index=False)
print(df.shape)
