import pandas as pd
import json

with open("data.json", 'r') as fp:
    data = json.load(fp)
all_data = []

for item in data:
    hits = item['hits']['hit']        
    for field in hits:
        fields = field['fields']
        # import pdb; pdb.set_trace()
        # a = 1
        # b = 1

        details = {
            
            'Health Plan Name': fields['name_t'],
            'Insurance Type': fields['facet_insurancetype_l'],
            'Accreditation': fields['facet_accreditation_l'],
            'Product Type': fields['facet_producttype_l'],
            'State': fields['state_l'],
            'Organization id': fields['organizationid_l'],
            'Type': fields['type'],
            'Star Rating': fields['facet_starratingforsorting_i'],
            
        }
        for each_planrating in fields.get('planratings_ta', []):
            # import pdb; pdb.set_trace()
            # a = 1
            # b = 1
            # each_planrating = json.loads(each_planrating)
            level_name = each_planrating['levelname_l']
            
            level_rating = each_planrating.get('levelstarrating_l')
            details[level_name] = level_rating
        all_data.append(details)
df = pd. DataFrame(all_data)
df.to_excel('output.xlsx', index=False)
print(df.shape)

