import requests
import json

all_data = []
for i in range(0,94):
    url = 'https://reportcardsapi.ncqa.org/api/v1/CloudSearch/2013-01-01/search'   #https://reportcards.ncqa.org/health-plans

    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://reportcards.ncqa.org',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    params = {
        'q.parser': 'structured',
        'size': 20,
        'facet': '{"facet_statecoverage_la":{"sort":"count","size":200},"facet_insurancetype_l":{"sort":"count","size":200},"facet_producttype_l":{"sort":"count","size":200},"facet_all_statuses_la":{"sort":"count","size":200},"facet_distinctions_la":{"sort":"count","size":200},"facet_starrating_l":{"sort":"count","size":200},"facet_electronic_clinical_data_l":{"sort":"count","size":200}}',
        'fq': '(and type:\'Health Plan Accreditation\')',
        'sort': 'name_t asc',
        'start': i*20,
        'q': 'matchall'
    }
    proxies={
        "http": "http://ocapgizs-rotate:araohu409l9t@p.webshare.io:80/",
        "https": "http://ocapgizs-rotate:araohu409l9t@p.webshare.io:80/"
    }

    response = requests.get(url, headers=headers, params=params, proxies=proxies)
    if response.status_code == 200:
        data = response.json()
        all_data.append(data)
        print(f"page {i} scraped succesfully!")
    else:
        print(f"Failed to scrape page {i}. {response.status_code}")

with open("Data.json", 'w') as f:
    json.dump(all_data, f, indent=4)

