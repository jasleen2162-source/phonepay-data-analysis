import os
import json
import pandas as pd

path = "./pulse/data/map/insurance/country/india/state/"

columns = {
    "state": [],
    "year": [],
    "quarter": [],
    "district": [],
    "latitude": [],
    "longitude": [],
    "insurance_count": []
}

state_list = [
    s for s in os.listdir(path)
    if os.path.isdir(os.path.join(path, s))
]

for state in state_list:
    state_path = os.path.join(path, state)
    years = os.listdir(state_path)

    for year in years:
        year_path = os.path.join(state_path, year)
        files = os.listdir(year_path)

        for file in files:
            file_path = os.path.join(year_path, file)

            with open(file_path, "r") as f:
                data = json.load(f)

            if "data" in data and "data" in data["data"]:
                records = data["data"]["data"]["data"]

                for row in records:
                    lat = row[0]
                    lng = row[1]
                    metric = row[2]
                    label = row[3]

                    columns["state"].append(state.replace("-", " ").title())
                    columns["year"].append(int(year))
                    columns["quarter"].append(int(file.replace(".json", "")))
                    columns["district"].append(label.replace(" district", "").title())
                    columns["latitude"].append(lat)
                    columns["longitude"].append(lng)
                    columns["insurance_count"].append(metric)

map_insurance = pd.DataFrame(columns)

map_insurance.to_csv("map_insurance.csv", index=False)

print("Rows:", len(map_insurance))
print(map_insurance.head())



# aggregated_insurance → gives premium amount
# 
# map_insurance → gives district-level count only
# 
# 
# 
# You cannot get district premium amount — only transaction count.
# 
# 📊 Business Value of This Table
# 
# Now you can:
# 
# Identify insurance penetration hotspots
# 
# Compare rural vs urban districts
# 
# Create geo heatmaps in Streamlit
# 
# Detect fast-growing districts
