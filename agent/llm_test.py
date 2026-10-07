import pandas as pd
df = pd.read_csv("data/olist_orders_dataset.csv")
print(df.head())
print(df.columns)
print(df.shape)
print("Total number of orders:", len(df))
print("Order statuses:", df["order_status"].unique())
print("Delivered orders:", (df["order_status"] == "delivered").sum())
print("Delivery percentage:", (df["order_status"] == "delivered").mean() * 100)