# ---------------------------------------------------
# DATA CAPABILITY CHECKER
# ---------------------------------------------------

def check_capability(question):

    question = question.lower()

    # Questions that require profit/cost information
    if "profit" in question or "profitability" in question:

        return {
            "can_answer": False,
            "reason": (
                "Profit cannot be determined because the available "
                "dataset does not contain cost or expense information."
            )
        }

    # Questions about employee information
    if (
        "employee" in question
        or "salary" in question
        or "employee salary" in question
    ):

        return {
            "can_answer": False,
            "reason": (
                "The available dataset does not contain employee "
                "or salary information."
            )
        }

    # Questions about years outside the dataset
    if "2020" in question or "2021" in question:
        return {
            "can_answer": False,
            "reason": (
                "The available Olist dataset does not contain "
                "data for the requested year."
            )
        }

    # If no known limitation is detected
    return {
        "can_answer": True,
        "reason": "The question appears to use available data."
    }


if __name__ == "__main__":

    questions = [
        "What is the profit?",
        "What is the average delivery time?",
        "What is the employee salary?",
        "What was the revenue in 2020?"
    ]

    print("CAPABILITY CHECKER TEST")
    print("-----------------------")

    for question in questions:

        result = check_capability(question)

        print("\nQuestion:", question)
        print("Can answer:", result["can_answer"])
        print("Reason:", result["reason"])