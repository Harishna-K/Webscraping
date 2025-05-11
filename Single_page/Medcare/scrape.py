import json
import os
import re
import requests
from lxml import html
from time import sleep
from json import JSONDecoder

# Load doctors data from your JSON file
with open("Data.json", "r", encoding="utf-8") as f:
    doctors = json.load(f)["doc"]

# Create output directory
output_dir = "doctor_json_files"
os.makedirs(output_dir, exist_ok=True)

def sanitize_filename(name):
    # Replace problematic characters for filenames
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)

def extract_next_data_json(url):
    try:
        response = requests.get(url, timeout=10)
        tree = html.fromstring(response.content)

        # XPath to extract the first script tag under body
        script_texts = tree.xpath('//body[@class="responsive "]/script[1]/text()')

        if script_texts:
            raw = script_texts[0].strip()
            if raw.startswith("__NEXT_DATA__ ="):
                raw = raw.replace("__NEXT_DATA__ =", "").strip()
                if raw.endswith(";"):
                    raw = raw[:-1]

                # Safely parse only the first valid JSON object
                decoder = JSONDecoder()
                obj, _ = decoder.raw_decode(raw)
                return obj
            else:
                return {"error": "__NEXT_DATA__ variable not found"}
        else:
            return {"error": "Script tag not found"}

    except Exception as e:
        return {"error": str(e)}

# Loop through doctors and save JSON per doctor
for idx, doc in enumerate(doctors, 1):
    url = doc.get("booklink", "").strip()
    title = doc.get("title") or f"doctor_{doc.get('uid', idx)}"
    safe_title = sanitize_filename(title)

    if not url.startswith("http"):
        print(f"[{idx}] Skipping {title}: invalid URL")
        continue

    print(f"[{idx}/{len(doctors)}] Fetching: {title}")
    json_data = extract_next_data_json(url)

    # Save individual file
    file_path = os.path.join(output_dir, f"{safe_title}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    sleep(1)  # polite delay

print("✅ All JSON files saved in the 'doctor_json_files' directory.")
