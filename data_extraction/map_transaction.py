import os
import json
import pandas as pd

path = "./pulse/data/map/transaction/hover/country/india/state/"

columns = {
    "state": [],
    "year": [],
    "quarter": [],
    "district": [],
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

            hover_list = data["data"]["hoverDataList"]

            for item in hover_list:
                district = item["name"]

                for metric in item["metric"]:
                    columns["state"].append(state.replace("-", " ").title())
                    columns["year"].append(int(year))
                    columns["quarter"].append(int(file.replace(".json", "")))
                    columns["district"].append(district.replace(" district","").title())
                    columns["transaction_count"].append(metric["count"])
                    columns["transaction_amount"].append(metric["amount"])

map_transaction = pd.DataFrame(columns)

map_transaction.to_csv("map_transaction.csv", index=False)

print("Rows:", len(map_transaction))
print(map_transaction.head())


# 
# it is what actually powers the state map tooltip in the dashboard.
# Geography Questions
# 
# Which district uses UPI the most?
# 
# High value vs high volume districts
# 
# Urban vs rural digital adoption
# 
# Business KPIs
# 
# Payment penetration
# 
# Financial inclusion
# 
# Cashless economy hotspots