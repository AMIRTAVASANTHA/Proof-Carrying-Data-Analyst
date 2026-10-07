import pandas as pd

from data_loader import load_orders


def delivery_time_analysis():

    orders = load_orders()

    # Convert dates
    orders["order_purchase_timestamp"] = pd.to_datetime(
        orders["order_purchase_timestamp"]
    )

    orders["order_delivered_customer_date"] = pd.to_datetime(
        orders["order_delivered_customer_date"]
    )

    # Keep only orders with delivery date
    data = orders.dropna(
        subset=[
            "order_purchase_timestamp",
            "order_delivered_customer_date"
        ]
    ).copy()

    # Calculate delivery time in days
    data["delivery_days"] = (
        data["order_delivered_customer_date"]
        - data["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400

    return data

def late_orders(days=30):

    data = delivery_time_analysis()

    late = data[data["delivery_days"] > days]

    return late

if __name__ == "__main__":

    data = delivery_time_analysis()

    print("\nDelivery Analysis")

    print("Orders with delivery date:", len(data))

    print(
        "Average delivery time:",
        round(data["delivery_days"].mean(), 2),
        "days"
    )

    print(
        "Minimum delivery time:",
        data["delivery_days"].min(),
        "days"
    )

    print(
        "Maximum delivery time:",
        data["delivery_days"].max(),
        "days"
    )

    late = late_orders(30)

    print(
        "\nOrders delivered after 30 days:",
        len(late)
    )