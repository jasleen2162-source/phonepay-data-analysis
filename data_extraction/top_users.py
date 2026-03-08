import os
import json
import pandas as pd

path = "./pulse/data/top/user/country/india/state/"

district_columns = {
    "state": [],
    "year": [],
    "quarter": [],
    "district": [],
    "registered_users": []
}

pincode_columns = {
    "state": [],
    "year": [],
    "quarter": [],
    "pincode": [],
    "registered_users": []
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

            # DISTRICTS
            if data["data"]["districts"]:
                for d in data["data"]["districts"]:
                    district_columns["state"].append(state.replace("-", " ").title())
                    district_columns["year"].append(year_int)
                    district_columns["quarter"].append(quarter_int)
                    district_columns["district"].append(d["name"].title())
                    district_columns["registered_users"].append(d["registeredUsers"])

            # PINCODES
            if data["data"]["pincodes"]:
                for p in data["data"]["pincodes"]:
                    pincode_columns["state"].append(state.replace("-", " ").title())
                    pincode_columns["year"].append(year_int)
                    pincode_columns["quarter"].append(quarter_int)
                    pincode_columns["pincode"].append(p["name"])
                    pincode_columns["registered_users"].append(p["registeredUsers"])

# Create DataFrames
top_user_district = pd.DataFrame(district_columns)
top_user_pincode = pd.DataFrame(pincode_columns)

# Save
top_user_district.to_csv("top_user_district.csv", index=False)
top_user_pincode.to_csv("top_user_pincode.csv", index=False)

print("District rows:", len(top_user_district))
print("Pincode rows:", len(top_user_pincode))


# Business Value
# 
# Now you can create:
# 
# Adoption Leaderboards
# 
# Top districts by users
# 
# Top pincodes by users
# 
# Growth Strategy
# 
# High transaction but low users → onboarding opportunity
# 
# High users but low transactions → activation problem