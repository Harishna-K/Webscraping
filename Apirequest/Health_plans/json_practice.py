import pandas as pd
import json

with open("Data.json", "r") as fp:
    data = json.load(fp)

all_data = []

for item in data:
    hits = item["hits"]["hit"]
    for hit in hits:
        field = hit["fields"]
        url = f"https://reportcards.ncqa.org/health-plan/Hp_{field['id']}"
        details = {
            "URL": url,
            "Name": field["name_t"],
            "Insurance type": field["facet_insurancetype_l"],
            "Accreditation / non Accreditation": field["facet_accreditation_l"],
            "Product type": field["facet_producttype_l"],
            "Website": field["website_t"],
            "City": field["city_t"],
            "State": field["state_l"],
        }
        for planrating in field.get("planratings_ta", []):

            planrating_data = json.loads(planrating)

            level_name = planrating_data["levelname_l"]
            level_star = planrating_data.get("levelstarrating_l", "")
            details[level_name] = level_star

        for project_type in field.get("projecttypes_ta", []):

            project_type_data = json.loads(project_type)

            for nextreview in project_type_data.get("details_ta", []):

                nextreview_date = nextreview.get("nextreviewdate_t", "")
                details["Next Review Date"] = (nextreview_date,)

                members_enrolled = nextreview.get("enrollment_i", "")
                details["Members Enrolled"] = members_enrolled

                Evaluation_Product = nextreview.get("ep_l", "")
                details["Evaluation Product"] = Evaluation_Product
        all_data.append(details)

df = pd.DataFrame(all_data)
df.drop_duplicates(subset="URL", inplace=True)
df.fillna(value="", inplace=True)
df.to_excel("Practice.xlsx", index=False)
print(df.shape)
print(df.columns)
