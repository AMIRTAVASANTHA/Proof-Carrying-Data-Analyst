import textwrap
import re


def generate_code(question):

    q = question.lower()

    # -----------------------------------------
    # 1. HIGHEST REVENUE CATEGORY
    # -----------------------------------------
    if "category" in q and "revenue" in q:

        return textwrap.dedent("""
            import pandas as pd

            order_items = pd.read_csv(
                "data/olist_order_items_dataset.csv"
            )

            products = pd.read_csv(
                "data/olist_products_dataset.csv"
            )

            translation = pd.read_csv(
                "data/product_category_name_translation.csv"
            )

            data = order_items.merge(
                products[
                    ["product_id", "product_category_name"]
                ],
                on="product_id",
                how="left"
            )

            data = data.merge(
                translation,
                on="product_category_name",
                how="left"
            )

            revenue = (
                data
                .groupby("product_category_name_english")["price"]
                .sum()
                .sort_values(ascending=False)
            )

            print(revenue.head(1))
        """)

    # -----------------------------------------
    # 2. STATE WITH MOST ORDERS
    # -----------------------------------------
    if "state" in q and "order" in q:

        return textwrap.dedent("""
            import pandas as pd

            orders = pd.read_csv(
                "data/olist_orders_dataset.csv"
            )

            customers = pd.read_csv(
                "data/olist_customers_dataset.csv"
            )

            data = orders.merge(
                customers[
                    ["customer_id", "customer_state"]
                ],
                on="customer_id",
                how="left"
            )

            result = (
                data["customer_state"]
                .value_counts()
                .sort_values(ascending=False)
            )

            print(result.head(1))
        """)

    # -----------------------------------------
    # 3. AVERAGE DELIVERY TIME
    # -----------------------------------------
    if "average" in q and "delivery" in q:

        return textwrap.dedent("""
            import pandas as pd

            orders = pd.read_csv(
                "data/olist_orders_dataset.csv"
            )

            orders["order_purchase_timestamp"] = pd.to_datetime(
                orders["order_purchase_timestamp"]
            )

            orders["order_delivered_customer_date"] = pd.to_datetime(
                orders["order_delivered_customer_date"]
            )

            delivered = orders.dropna(
                subset=[
                    "order_purchase_timestamp",
                    "order_delivered_customer_date"
                ]
            ).copy()

            delivered["delivery_days"] = (
                delivered["order_delivered_customer_date"]
                - delivered["order_purchase_timestamp"]
            ).dt.total_seconds() / 86400

            average_delivery = delivered["delivery_days"].mean()

            print(round(average_delivery, 2))
        """)

    # -----------------------------------------
    # 4. LATE ORDERS
    # -----------------------------------------
    if "order" in q and (
        "late" in q or
        "more than" in q
    ):

        days = 30

        match = re.search(
            r"(\d+)\s*days?",
            q
        )

        if match:
            days = int(match.group(1))

        return textwrap.dedent(f"""
            import pandas as pd

            orders = pd.read_csv(
                "data/olist_orders_dataset.csv"
            )

            orders["order_purchase_timestamp"] = pd.to_datetime(
                orders["order_purchase_timestamp"]
            )

            orders["order_delivered_customer_date"] = pd.to_datetime(
                orders["order_delivered_customer_date"]
            )

            delivered = orders.dropna(
                subset=[
                    "order_purchase_timestamp",
                    "order_delivered_customer_date"
                ]
            ).copy()

            delivered["delivery_days"] = (
                delivered["order_delivered_customer_date"]
                - delivered["order_purchase_timestamp"]
            ).dt.total_seconds() / 86400

            late_orders = delivered[
                delivered["delivery_days"] > {days}
            ]

            print(len(late_orders))
        """)

    # -----------------------------------------
    # 5. HIGHEST REVENUE PRODUCT
    # -----------------------------------------
    if "product" in q and "revenue" in q:

        return textwrap.dedent("""
            import pandas as pd

            order_items = pd.read_csv(
                "data/olist_order_items_dataset.csv"
            )

            revenue = (
                order_items
                .groupby("product_id")["price"]
                .sum()
                .sort_values(ascending=False)
            )

            print(revenue.head(1))
        """)

    # -----------------------------------------
    # 6. MONTHLY REVENUE
    # -----------------------------------------
    if "monthly" in q and "revenue" in q:

        return textwrap.dedent("""
            import pandas as pd

            orders = pd.read_csv(
                "data/olist_orders_dataset.csv"
            )

            order_items = pd.read_csv(
                "data/olist_order_items_dataset.csv"
            )

            orders["order_purchase_timestamp"] = pd.to_datetime(
                orders["order_purchase_timestamp"]
            )

            data = orders.merge(
                order_items,
                on="order_id",
                how="inner"
            )

            data["month"] = (
                data["order_purchase_timestamp"]
                .dt.to_period("M")
            )

            revenue = (
                data
                .groupby("month")["price"]
                .sum()
            )

            print(revenue)
        """)

    # -----------------------------------------
    # QUESTION NOT SUPPORTED
    # -----------------------------------------
    return None