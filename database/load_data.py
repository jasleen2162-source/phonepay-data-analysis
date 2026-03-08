import pandas as pd
from db_connection import engine

csv_table_map = {
    "aggregated_transaction.csv": "fact_aggregated_transaction",
    "aggregated_user.csv": "fact_aggregated_user",
    "aggregated_insurance.csv": "fact_aggregated_insurance",

    "map_transaction.csv": "fact_map_transaction",
    "map_user.csv": "fact_map_user",
    "map_insurance.csv": "fact_map_insurance",

    "top_transaction_district.csv": "fact_top_transaction_district",
    "top_transaction_pincode.csv": "fact_top_transaction_pincode",

    "top_insurance_district.csv": "fact_top_insurance_district",
    "top_insurance_pincode.csv": "fact_top_insurance_pincode",

    "top_user_district.csv": "fact_top_user_district",
    "top_user_pincode.csv": "fact_top_user_pincode"
}

for file, table in csv_table_map.items():
    print(f"Loading {file} into {table}...")
    
    df = pd.read_csv(f"./data/{file}")
    
    df.to_sql(
        name=table,
        con=engine,
        if_exists="append",
        index=False
    )

print("All files loaded successfully!")