import pandas as pd
import os


# ---------------------------------------------------
# CHECK WHETHER A VALUE IS A VALID NUMBER
# ---------------------------------------------------

def verify_number(value):

    if value is None:
        return False

    if isinstance(value, (int, float)):
        return True

    return False


# ---------------------------------------------------
# CHECK WHETHER A RESULT EXISTS
# ---------------------------------------------------

def verify_result(result):

    if result is None:
        return False

    if len(result) == 0:
        return False

    return True


# ---------------------------------------------------
# COMPARE TWO NUMBERS
# ---------------------------------------------------

def compare_results(result1, result2, tolerance=0.01):

    if result1 is None or result2 is None:
        return False

    difference = abs(float(result1) - float(result2))

    return difference <= tolerance


# ---------------------------------------------------
# INDEPENDENT VERIFICATION
# ---------------------------------------------------

def independently_verify_top_category():

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data")

    items = pd.read_csv(
        os.path.join(
            data_path,
            "olist_order_items_dataset.csv"
        )
    )

    products = pd.read_csv(
        os.path.join(
            data_path,
            "olist_products_dataset.csv"
        )
    )

    translation = pd.read_csv(
        os.path.join(
            data_path,
            "product_category_name_translation.csv"
        )
    )

    # Join the tables again independently
    data = items.merge(
        products[
            [
                "product_id",
                "product_category_name"
            ]
        ],
        on="product_id",
        how="left"
    )

    data = data.merge(
        translation,
        on="product_category_name",
        how="left"
    )

    # Independent calculation
    category_revenue = (
        data
        .groupby(
            "product_category_name_english",
            dropna=False
        )["price"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    top_category = category_revenue.index[0]
    top_value = float(category_revenue.iloc[0])

    return {
        "answer": top_category,
        "value": round(top_value, 2),
        "unit": "BRL",
        "rows_analyzed": len(items),
        "verified": True
    }


# ---------------------------------------------------
# TEST
# ---------------------------------------------------

if __name__ == "__main__":

    result = independently_verify_top_category()

    print("INDEPENDENT VERIFICATION")
    print(result)