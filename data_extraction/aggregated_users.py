import os
import json
import pandas as pd

path = "./pulse/data/aggregated/user/country/india/state/"

columns = {
    "state": [],
    "year": [],
    "quarter": [],
    "registered_users": [],
    "app_opens": []
}

# Safe directory listing
state_list = [s for s in os.listdir(path) if not s.startswith(".")]

for state in state_list:
    state_path = os.path.join(path, state)

    if not os.path.isdir(state_path):
        continue

    years = [y for y in os.listdir(state_path) if not y.startswith(".")]

    for year in years:
        year_path = os.path.join(state_path, year)

        if not os.path.isdir(year_path):
            continue

        files = [f for f in os.listdir(year_path) if f.endswith(".json")]

        for file in files:
            file_path = os.path.join(year_path, file)

            with open(file_path, "r") as f:
                data = json.load(f)

            # ✅ SAFE EXTRACTION
            aggregated_data = data.get("data", {}).get("aggregated", {})

            users = aggregated_data.get("registeredUsers")
            opens = aggregated_data.get("appOpens")

            # Skip if missing
            if users is None or opens is None:
                continue

            columns["state"].append(state.replace("-", " ").title())
            columns["year"].append(int(year))
            columns["quarter"].append(int(file.replace(".json", "")))
            columns["registered_users"].append(users)
            columns["app_opens"].append(opens)

# Create DataFrame
agg_user = pd.DataFrame(columns)

# Export CSV
agg_user.to_csv("aggregated_user.csv", index=False)

print("Done ✅ Rows:", len(agg_user))
print(agg_user.head())





































# you can build insights like:
# 
# States with many users but low usage → awareness problem
# 
# States with high usage but low users → growth opportunity
# 
# User growth trend per year
# 
# Engagement ratio = app_opens / registered_users






















