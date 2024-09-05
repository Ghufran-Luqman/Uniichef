import pandas as pd
import sqlite3

conn = sqlite3.connect("recipes.db")

chunk_size = 10000
chunks = pd.read_csv("recipes.csv", chunksize=chunk_size)

for item in chunks:

    if 'Unnamed: 0' in item.columns:
        item = item.drop(columns=["Unnamed: 0"])
    item.to_sql("tableofrecipes", con=conn, if_exists='append', index=False)

conn.close()