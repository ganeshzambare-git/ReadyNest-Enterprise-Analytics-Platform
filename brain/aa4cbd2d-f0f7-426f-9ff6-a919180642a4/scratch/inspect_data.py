import pandas as pd

try:
    df = pd.read_parquet('d:/Data Analytics Dashboard project/data_lake/curated/feature_store_customers.parquet')
    print("feature_store_customers.parquet:")
    print(df.columns.tolist())
    print(df.head())
except Exception as e:
    print(e)
