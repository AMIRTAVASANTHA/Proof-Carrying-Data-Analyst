import pandas as pd
from data_loader import load_orders, load_order_items


def revenue_by_month():

    orders = load_orders()
    items = load_order_items()

    # Convert purchase date to datetime
    orders["order_purchase_timestamp"] = pd.to_datetime(
        orders["order_purchase_timestamp"]
    )

    # Join orders with order items
    data = orders.merge(
        items[["order_id", "price"]],
        on="order_id",
        how="inner"
    )

    # Extract month
    data["month"] = data["order_purchase_timestamp"].dt.to_period("M")

    # Calculate revenue
    result = (
        data.groupby("month")["price"]
        .sum()
    )

    return result


if __name__ == "__main__":

    result = revenue_by_month()

    print("\nMonthly revenue:")
    print(result)