from sqlalchemy import create_engine

import urllib.parse

username = "jasleenkaur"
password = urllib.parse.quote_plus("Sibaya@1")  # your real password
host = "localhost"
port = "5432"
database = "phonepe_analytics"

DATABASE_URL = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        print("✅ Connection Successful!")
except Exception as e:
    print("❌ Connection Failed")
    print(e)
