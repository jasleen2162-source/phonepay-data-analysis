# We Should Create TWO Tables
# 1️⃣ top_insurance_district
# 
# | state | year | quarter | district | insurance_count | insurance_amount |
# 
# 2️⃣ top_insurance_pincode
# 
# | state | year | quarter | pincode | insurance_count | insurance_amount |



import os
import json
import pandas as pd

path = "./pulse/data/top/insurance/country/india/state/"

district_columns = {
    "state": [],
    "year": [],
    "quarter": [],
    "district": [],
    "insurance_count": [],
    "insurance_amount": []
}

pincode_columns = {
    "state": [],
    "year": [],
    "quarter": [],
    "pincode": [],
    "insurance_count": [],
    "insurance_amount": []
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

            year_int = int(year)
            quarter_int = int(file.replace(".json", ""))

            # Districts
            if data["data"]["districts"]:
                for d in data["data"]["districts"]:
                    district_columns["state"].append(state.replace("-", " ").title())
                    district_columns["year"].append(year_int)
                    district_columns["quarter"].append(quarter_int)
                    district_columns["district"].append(d["entityName"].title())
                    district_columns["insurance_count"].append(d["metric"]["count"])
                    district_columns["insurance_amount"].append(d["metric"]["amount"])

            # Pincodes
            if data["data"]["pincodes"]:
                for p in data["data"]["pincodes"]:
                    pincode_columns["state"].append(state.replace("-", " ").title())
                    pincode_columns["year"].append(year_int)
                    pincode_columns["quarter"].append(quarter_int)
                    pincode_columns["pincode"].append(p["entityName"])
                    pincode_columns["insurance_count"].append(p["metric"]["count"])
                    pincode_columns["insurance_amount"].append(p["metric"]["amount"])

# DataFrames
top_insurance_district = pd.DataFrame(district_columns)
top_insurance_pincode = pd.DataFrame(pincode_columns)

# Export
top_insurance_district.to_csv("top_insurance_district.csv", index=False)
top_insurance_pincode.to_csv("top_insurance_pincode.csv", index=False)

print("District rows:", len(top_insurance_district))
print("Pincode rows:", len(top_insurance_pincode))

# Business Value
# 
# Now you can build:
# 
# 🏆 Leaderboards
# 
# Top insurance districts
# 
# Top insurance pincodes
# 
# 💰 High Premium Zones
# 
# Districts with high value but low count → expensive policies
# 
# High count but low value → micro-insurance adoption