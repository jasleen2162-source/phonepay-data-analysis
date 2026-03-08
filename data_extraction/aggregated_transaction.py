import os
import json
import pandas as pd

path = "./pulse/data/aggregated/transaction/country/india/state/"

columns = {
    "state": [],
    "year": [],
    "quarter": [],
    "transaction_type": [],
    "transaction_count": [],
    "transaction_amount": []
}

# Safe state listing
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
                    columns["transaction_type"].append(name)
                    columns["transaction_count"].append(inst.get("count"))
                    columns["transaction_amount"].append(inst.get("amount"))

# Create dataframe
agg_transaction = pd.DataFrame(columns)

# Export
agg_transaction.to_csv("aggregated_transaction.csv", index=False)

print("Done ✅ Rows:", len(agg_transaction))
print(agg_transaction.head())