
import os
import json
import pandas as pd

path = "./pulse/data/aggregated/insurance/country/india/state/"

columns = {
    "state": [],
    "year": [],
    "quarter": [],
    "insurance_type": [],
    "insurance_count": [],
    "insurance_amount": []
}

# Safe state listing
state_list = [
    s for s in os.listdir(path)
    if os.path.isdir(os.path.join(path, s))
]

for state in state_list:
    state_path = os.path.join(path, state)

    years = [
        y for y in os.listdir(state_path)
        if os.path.isdir(os.path.join(state_path, y))
    ]

    for year in years:
        year_path = os.path.join(state_path, year)

        files = [
            f for f in os.listdir(year_path)
            if f.endswith(".json")
        ]

        for file in files:
            file_path = os.path.join(year_path, file)

            with open(file_path, "r") as f:
                data = json.load(f)

            # ✅ SAFE extraction
            transaction_data = data.get("data", {}).get("transactionData", [])

            if not transaction_data:
                continue

            for item in transaction_data:
                name = item.get("name")
                instruments = item.get("paymentInstruments", [])

                for inst in instruments:
                    columns["state"].append(state.replace("-", " ").title())
                    columns["year"].append(int(year))
                    columns["quarter"].append(int(file.replace(".json", "")))
                    columns["insurance_type"].append(name)
                    columns["insurance_count"].append(inst.get("count"))
                    columns["insurance_amount"].append(inst.get("amount"))

# Create DataFrame
agg_insurance = pd.DataFrame(columns)

# Export
agg_insurance.to_csv("aggregated_insurance.csv", index=False)

print("Rows:", len(agg_insurance))
print(agg_insurance.head())



















# What This Dataset Gives You
# 
# Now you can answer business questions like:
# 
# Adoption
# 
# Which states buy most insurance?
# 
# Is insurance growing year over year?
# 
# Premium Value
# 
# High value states vs high user states
# 
# Urban vs semi-urban adoption
# 
# Product Insights
# 
# Correlate insurance with transaction volume
# 
# Predict future financial product demand