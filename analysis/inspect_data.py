import pandas as pd
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = os.path.join(BASE_DIR, "data")

files = [
    "olist_customers_dataset.csv",
    "olist_orders_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "product_category_name_translation.csv"
]

for file in files:

    path = os.path.join(DATA_PATH, file)

    df = pd.read_csv(path)

    print("\n" + "=" * 60)
    print("FILE:", file)
    print("=" * 60)

    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate rows:", df.duplicated().sum())