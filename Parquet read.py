import pandas as pd
import json
# Path to your Parquet file
file_path = ("/Users/reubenharuray/Downloads/part-00000-f2cb3f12-6795-4985-88bb-11c75801ae04.c000.snappy.parquet"
             "")

# Read the Parquet file using pyarrow
df = pd.read_parquet(file_path, engine="pyarrow")

print(df.columns)

# Peek inside the first row of a column
print(df["ticketingCorrelations"].iloc[0])  # or try 'events', 'meta', etc.