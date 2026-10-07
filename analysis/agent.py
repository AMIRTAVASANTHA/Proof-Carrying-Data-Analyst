import sys
import os

# Allow Python to access the analysis folder
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANALYSIS_PATH = os.path.join(PROJECT_ROOT, "analysis")

sys.path.append(ANALYSIS_PATH)

from tool_registry import TOOLS, execute_tool
from capability_checker import check_capability


class DataProofAgent:

    def __init__(self):
        self.tools = TOOLS

    def understand_question(self, question):

        question_lower = question.lower()

        # Category revenue
        if (
            ("category" in question_lower
             or "categories" in question_lower)
            and
            ("revenue" in question_lower
             or "sales" in question_lower)
        ):
            return "top_category"

        # State orders
        if (
            ("state" in question_lower
             or "states" in question_lower)
            and
            ("order" in question_lower
             or "orders" in question_lower)
        ):
            return "top_state"

        # Monthly revenue
        if (
            ("monthly" in question_lower
             or "month" in question_lower)
            and
            ("revenue" in question_lower
             or "sales" in question_lower)
        ):
            return "monthly_revenue"

        # Delivery
        if (
            "average" in question_lower
            and
            ("delivery" in question_lower
             or "deliver" in question_lower)
        ):
            return "average_delivery"

        # Late orders
        if (
            ("late" in question_lower
             or "delayed" in question_lower)
            and
            ("order" in question_lower
             or "orders" in question_lower)
        ):
            return "late_orders"

        # Products
        if (
            ("product" in question_lower
             or "products" in question_lower)
            and
            ("revenue" in question_lower
             or "sales" in question_lower)
        ):
            return "top_product"

        return None

    def run(self, question):

        print("\n🤖 DATAPROOF AI AGENT")
        print("--------------------")

        print("\nUser question:")
        print(question)

        # Step 1: Check whether the data can answer
        capability = check_capability(question)

        print("\nCapability check:")
        print(capability)

        if not capability["can_answer"]:

            return {
                "status": "cannot_answer",
                "answer": "I cannot determine the answer reliably.",
                "reason": capability["reason"],
                "verified": False
            }

        # Step 2: Agent chooses a tool
        tool_name = self.understand_question(question)

        print("\nAgent selected tool:")
        print(tool_name)

        if tool_name is None:

            return {
                "status": "cannot_answer",
                "answer": "I cannot determine the answer reliably.",
                "reason": "The agent could not find a suitable tool.",
                "verified": False
            }

        # Step 3: Execute selected tool
        result = execute_tool(tool_name)

        print("\nTool result:")
        print(result)

        return {
            "status": "success",
            "tool_used": tool_name,
            "result": result,
            "verified": result.get("verified", False)
        }


if __name__ == "__main__":

    agent = DataProofAgent()

    questions = [
        "Which category has the highest revenue?",
        "Which state has the most orders?",
        "What is the profit?"
    ]

    for question in questions:

        result = agent.run(question)

        print("\nFINAL RESULT:")
        print(result)

        print("\n==============================")