import re


class MockLLM:
    """
    Temporary LLM used while API credits are unavailable.

    It simulates the LLM's job:
    understand the question and choose a tool.
    """

    def choose_tool(self, question):

        q = question.lower()

        # Highest revenue category
        if "category" in q and "revenue" in q:
            return {
                "tool": "top_category",
                "parameters": {}
            }

        # State with most orders
        if "state" in q and ("orders" in q or "order" in q):
            return {
                "tool": "top_state",
                "parameters": {}
            }

        # Average delivery
        if "average" in q and "delivery" in q:
            return {
                "tool": "average_delivery",
                "parameters": {}
            }

        # Late orders
        if ("late" in q or "more than" in q) and "order" in q:
            match = re.search(r"(\d+)\s*days?", q)

            days = int(match.group(1)) if match else 30

            return {
                "tool": "late_orders",
                "parameters": {
                    "days": days
                }
            }

        # Top product
        if "product" in q and "revenue" in q:
            return {
                "tool": "top_product",
                "parameters": {}
            }

        # Monthly revenue
        if "monthly" in q and "revenue" in q:
            return {
                "tool": "monthly_revenue",
                "parameters": {}
            }

        # No suitable tool
        return {
            "tool": None,
            "parameters": {}
        }


if __name__ == "__main__":

    llm = MockLLM()

    questions = [
        "Which category has the highest revenue?",
        "Which state has the most orders?",
        "What is the average delivery time?",
        "How many orders took more than 30 days?"
    ]

    for question in questions:

        result = llm.choose_tool(question)

        print("\nQuestion:", question)
        print("LLM decision:", result)