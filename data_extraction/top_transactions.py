import os
import json
import pandas as pd

path = "./pulse/data/top/transaction/country/india/state/"

district_columns = {
    "state": [],
    "year": [],
    "quarter": [],
    "district": [],
    "transaction_count": [],
    "transaction_amount": []
}

pincode_columns = {
    "state": [],
    "year": [],
    "quarter": [],
    "pincode": [],
    "transaction_count": [],
    "transaction_amount": []
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

            # DISTRICT
            if data["data"]["districts"]:
                for d in data["data"]["districts"]:
                    district_columns["state"].append(state.replace("-", " ").title())
                    district_columns["year"].append(year_int)
                    district_columns["quarter"].append(quarter_int)
                    district_columns["district"].append(d["entityName"].title())
                    district_columns["transaction_count"].append(d["metric"]["count"])
                    district_columns["transaction_amount"].append(d["metric"]["amount"])

            # PINCODE
            if data["data"]["pincodes"]:
                for p in data["data"]["pincodes"]:
                    pincode_columns["state"].append(state.replace("-", " ").title())
                    pincode_columns["year"].append(year_int)
                    pincode_columns["quarter"].append(quarter_int)
                    pincode_columns["pincode"].append(p["entityName"])
                    pincode_columns["transaction_count"].append(p["metric"]["count"])
                    pincode_columns["transaction_amount"].append(p["metric"]["amount"])

# Create DataFrames
top_transaction_district = pd.DataFrame(district_columns)
top_transaction_pincode = pd.DataFrame(pincode_columns)

# Save
top_transaction_district.to_csv("top_transaction_district.csv", index=False)
top_transaction_pincode.to_csv("top_transaction_pincode.csv", index=False)

print("District rows:", len(top_transaction_district))
print("Pincode rows:", len(top_transaction_pincode))

# This drives your main dashboard visuals:
# 
# Leaderboards
# 
# Top 10 states
# 
# Top 10 districts
# 
# Top 10 pincodes
# 
# Business Insights
# 
# Merchant dense areas
# 
# Digital adoption hotspots
# 
# Rural vs metro payment penetration