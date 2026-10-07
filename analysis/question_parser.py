# ---------------------------------------------------
# QUESTION PARSER
# ---------------------------------------------------

def parse_question(question):

    # Convert question to lowercase
    question = question.lower()

    # -----------------------------------------------
    # TOP CATEGORY
    # -----------------------------------------------

    if (
        ("category" in question or "categories" in question)
        and ("revenue" in question or "sales" in question)
    ):
        return "top_category"


    # -----------------------------------------------
    # TOP STATE
    # -----------------------------------------------

    if (
        ("state" in question or "states" in question)
        and ("order" in question or "orders" in question)
    ):
        return "top_state"


    # -----------------------------------------------
    # MONTHLY REVENUE
    # -----------------------------------------------

    if (
        ("monthly" in question or "month" in question)
        and ("revenue" in question or "sales" in question)
    ):
        return "monthly_revenue"


    # -----------------------------------------------
    # AVERAGE DELIVERY
    # -----------------------------------------------

    if (
        "average" in question
        and ("delivery" in question or "deliver" in question)
    ):
        return "average_delivery"


    # -----------------------------------------------
    # LATE ORDERS
    # -----------------------------------------------

    if (
        ("late" in question or "delayed" in question)
        and ("order" in question or "orders" in question)
    ):
        return "late_orders"


    # -----------------------------------------------
    # TOP PRODUCT
    # -----------------------------------------------

    if (
        ("product" in question or "products" in question)
        and ("revenue" in question or "sales" in question)
    ):
        return "top_product"


    # -----------------------------------------------
    # UNKNOWN QUESTION
    # -----------------------------------------------

    return None


# ---------------------------------------------------
# TEST
# ---------------------------------------------------

if __name__ == "__main__":

    questions = [
        "Which category has the highest revenue?",
        "Which state has the most orders?",
        "What is the monthly revenue?",
        "What is the average delivery time?",
        "How many late orders are there?",
        "Which product generated the most revenue?",
        "What is the profit?"
    ]

    for question in questions:

        tool = parse_question(question)

        print("\nQuestion:", question)
        print("Selected tool:", tool)