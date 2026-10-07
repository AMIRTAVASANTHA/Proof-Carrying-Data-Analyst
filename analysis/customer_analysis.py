from data_loader import load_customers, load_orders


def orders_by_state():

    customers = load_customers()
    orders = load_orders()

    # Join customers and orders
    data = orders.merge(
        customers[["customer_id", "customer_state"]],
        on="customer_id",
        how="left"
    )

    # Count orders by state
    result = (
        data.groupby("customer_state")
        ["order_id"]
        .count()
        .sort_values(ascending=False)
    )

    return result


if __name__ == "__main__":

    result = orders_by_state()

    print("\nTop 10 states by number of orders:")
    print(result.head(10))