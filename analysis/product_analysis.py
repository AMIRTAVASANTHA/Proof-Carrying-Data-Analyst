from data_loader import load_order_items, load_products


def top_products():

    items = load_order_items()
    products = load_products()

    # Join items with products
    data = items.merge(
        products[["product_id", "product_category_name"]],
        on="product_id",
        how="left"
    )

    # Calculate revenue for each product
    result = (
        data.groupby("product_id")["price"]
        .sum()
        .sort_values(ascending=False)
    )

    return result


if __name__ == "__main__":

    result = top_products()

    print("\nTop 10 products by revenue:")
    print(result.head(10))