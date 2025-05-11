import pandas as pd
import json
import glob
from rich import print

Output = []

for each_file in glob.glob("doctor_json_files/*.json"):
    with open(each_file, "r", encoding="utf-8") as fp:
        Data = json.load(fp)

        if "props" not in Data:
            print(f"[yellow]Skipping: {each_file} (no 'props')[/yellow]")
            continue

        try:
            Props = Data["props"]["pageProps"]
            partition = Props.get("practitioner", {})

            Doctor_Name = partition.get("title", "")
            gender = partition.get("gender", "")
            photo = partition.get("profilePicture", "")
            Title = partition.get("highlight", "")
            Experience =partition.get("years_of_experience", "")
            languages = partition.get("languages", "")
            locations = partition.get("locations", [])
            experience = partition.get("experiences", [])
            Education = partition.get("educations", [])
            expertise = partition["expertise"]["specialities"]
            awards = partition.get("awards",[])
            Hospital_website = partition.get("short_url", "")

            for location in locations:
                Address = location.get("address", "")
                phone = location.get("phone", "")
                availability = location.get("next_available", "")
                Hospital_name = location.get("name", "")
                Facility_type = location.get("clinicType", "")
                website = location.get("website", "")
            for exp in experience:
                Department = exp.get("medical_facility", "")
            for edu in Education:
                degree = edu.get("degree", "")      

                Output.append({
                    "Doctor Name": Doctor_Name,
                    "Profile photo": photo,
                    "Title" : Title,
                    "Gender": gender,
                    "Department" : Department,
                    "Years of experience" : Experience,
                    "languages" : languages,
                    "Qualifications & Certifications" : degree,
                    "Areas of Expertise" : expertise,
                    "Awards & Recognitions" : awards,
                    "Work Schedule" : availability,
                    "Healthcare Name" : Hospital_name,
                    "Branch Location": Address,
                    "Facility Type" : Facility_type,
                    "website" : website,
                    "Healthcare Website" : Hospital_website,
                    "Phone Number": phone
                })

        except Exception as e:
            print(f"[red]Error in {each_file}: {e}[/red]")

# Save to Excel
df = pd.DataFrame(Output)
df = df.drop_duplicates(subset = ["Doctor Name"])
df.to_excel("Output.xlsx", index=False)
print(f"[green]✅ Saved {df.shape} rows to Output.xlsx[/green]")
