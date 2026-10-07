import sys
import os

# -----------------------------------------
# Project paths
# -----------------------------------------

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

ANALYSIS_PATH = os.path.join(
    PROJECT_ROOT,
    "analysis"
)

sys.path.append(ANALYSIS_PATH)


# -----------------------------------------
# Import our modules
# -----------------------------------------

from llm import MockLLM

from tool_registry import execute_tool

from code_generator import generate_code

import code_generator

print("CODE GENERATOR FILE:")
print(code_generator.__file__)

from code_executor import execute_generated_code

from result_verifier import verify_result


class Agent:

    def __init__(self):

        self.name = "Proof-Carrying Data Analyst Agent"

        # Temporary mock LLM
        self.llm = MockLLM()


    def run(self, question):

        print("\n" + "=" * 60)
        print("DATA PROOF AI")
        print("=" * 60)

        print("\nUser Question:")
        print(question)


        # =========================================
        # STEP 1: LLM chooses a tool
        # =========================================

        decision = self.llm.choose_tool(question)

        tool_name = decision["tool"]
        parameters = decision["parameters"]

        print("\nLLM Decision:")
        print("Tool:", tool_name)
        print("Parameters:", parameters)


        # =========================================
        # STEP 2: Refuse unsupported questions
        # =========================================

        if tool_name is None:

            return {
                "status": "cannot_answer",
                "question": question,
                "message":
                    "I cannot determine the answer "
                    "from the available tools and data."
            }


        # =========================================
        # STEP 3: Execute trusted analytics tool
        # =========================================

        print("\nExecuting trusted tool...")

        try:

            analytics_result = execute_tool(
                tool_name,
                **parameters
            )

        except Exception as e:

            return {
                "status": "error",
                "question": question,
                "tool_used": tool_name,
                "message": str(e)
            }


        print("\nAnalytics Result:")
        print(analytics_result)


        # =========================================
        # STEP 4: Generate proof code
        # =========================================

        print("\nGenerating proof code...")

        try:

            generated_code = generate_code(question)

        except Exception as e:

            return {
                "status": "error",
                "question": question,
                "tool_used": tool_name,
                "tool_result": analytics_result,
                "message":
                    "Could not generate proof code: " + str(e)
            }


        print("\nGenerated Code:")
        print("-" * 50)
        print(generated_code)
        print("-" * 50)


        # =========================================
        # STEP 5: Execute generated code
        # =========================================

        print("\nExecuting generated proof code...")

        try:

            execution_result = execute_generated_code(
                generated_code
            )

        except Exception as e:

            return {
                "status": "error",
                "question": question,
                "tool_used": tool_name,
                "tool_result": analytics_result,
                "generated_code": generated_code,
                "message":
                    "Proof code execution failed: " + str(e)
            }


        print("\nExecution Result:")
        print(execution_result)


        # =========================================
        # STEP 6: Verify result
        # =========================================

        print("\nVerifying result...")

        try:

            verification_result = verify_result(
                analytics_result,
                execution_result
            )

        except Exception as e:

            verification_result = {
                "verified": False,
                "reason":
                    "Verification failed: " + str(e)
            }


        print("\nVerification:")
        print(verification_result)


        # =========================================
        # STEP 7: Final response
        # =========================================

        return {

            "status": "success",

            "question": question,

            "tool_used": tool_name,

            "tool_result": analytics_result,

            "generated_code": generated_code,

            "execution_result": execution_result,

            "verification": verification_result
        }


# =========================================
# TEST
# =========================================

if __name__ == "__main__":

    agent = Agent()


    questions = [

        "Which category has the highest revenue?",

        "Which state has the most orders?",

        "What is the average delivery time?",

        "How many orders took more than 30 days?",

        "What is the profit?"
    ]


    for question in questions:

        result = agent.run(question)

        print("\nFINAL RESULT:")
        print(result)