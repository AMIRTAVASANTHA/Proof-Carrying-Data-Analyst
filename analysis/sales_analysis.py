from data_loader import (
    load_order_items,
    load_products,
    load_category_translation
)


def revenue_by_category():

    items = load_order_items()
    products = load_products()
    translation = load_category_translation()

    # Join order items with products
    data = items.merge(
        products[["product_id", "product_category_name"]],
        on="product_id",
        how="left"
    )

    # Translate category names
    data = data.merge(
        translation,
        on="product_category_name",
        how="left"
    )

    # Calculate revenue
    result = (
        data.groupby("product_category_name_english", dropna=False)
        ["price"]
        .sum()
        .sort_values(ascending=False)
    )

    return result


if __name__ == "__main__":

    result = revenue_by_category()

    print("\nTop 10 categories by revenue:")
    print(result.head(10))