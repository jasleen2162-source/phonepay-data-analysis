import os
import json
import pandas as pd

path = "./pulse/data/map/user/hover/country/india/state/"

columns = {
    "state": [],
    "year": [],
    "quarter": [],
    "district": [],
    "registered_users": [],
    "app_opens": []
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

            hover_data = data["data"]["hoverData"]

            for district, values in hover_data.items():

                columns["state"].append(state.replace("-", " ").title())
                columns["year"].append(int(year))
                columns["quarter"].append(int(file.replace(".json", "")))
                columns["district"].append(district.replace(" district","").title())
                columns["registered_users"].append(values["registeredUsers"])
                columns["app_opens"].append(values["appOpens"])

map_user = pd.DataFrame(columns)

map_user.to_csv("map_user.csv", index=False)

print("Rows:", len(map_user))
print(map_user.head())


# This table will help:
# 
# user penetration maps
# 
# engagement heatmaps
# 
# retention analysis