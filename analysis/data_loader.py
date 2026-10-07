import pandas as pd
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = os.path.join(BASE_DIR, "data")


def load_customers():
    return pd.read_csv(
        os.path.join(DATA_PATH, "olist_customers_dataset.csv")
    )


def load_orders():
    return pd.read_csv(
        os.path.join(DATA_PATH, "olist_orders_dataset.csv")
    )


def load_order_items():
    return pd.read_csv(
        os.path.join(DATA_PATH, "olist_order_items_dataset.csv")
    )


def load_products():
    return pd.read_csv(
        os.path.join(DATA_PATH, "olist_products_dataset.csv")
    )


def load_sellers():
    return pd.read_csv(
        os.path.join(DATA_PATH, "olist_sellers_dataset.csv")
    )


def load_payments():
    return pd.read_csv(
        os.path.join(DATA_PATH, "olist_order_payments_dataset.csv")
    )


def load_reviews():
    return pd.read_csv(
        os.path.join(DATA_PATH, "olist_order_reviews_dataset.csv")
    )


def load_category_translation():
    return pd.read_csv(
        os.path.join(DATA_PATH, "product_category_name_translation.csv")
    )