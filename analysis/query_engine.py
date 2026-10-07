from question_parser import parse_question
from tool_registry import execute_tool
from code_generator import generate_code
from code_executor import execute_generated_code
from result_verifier import verify_result
from capability_checker import check_capability


def answer_question(question):

    # 1. Check whether the dataset can answer the question
    capability = check_capability(question)

    if not capability["can_answer"]:
        return {
            "status": "cannot_answer",
            "question": question,
            "answer": "I cannot determine the answer reliably.",
            "reason": capability["reason"],
            "verified": False
        }

    # 2. Understand the question
    tool_name = parse_question(question)

    # 3. Refuse if no analysis tool exists
    if tool_name is None:
        return {
            "status": "cannot_answer",
            "question": question,
            "answer": "I cannot determine the answer reliably.",
            "reason": "No suitable analysis tool was found.",
            "verified": False
        }

    # 4. Run analytics tool
    analytics_result = execute_tool(tool_name)

    # 5. Generate and execute reproducible code
    generated_code = generate_code(question)

    if not generated_code:
        return {
            "status": "partial_success",
            "question": question,
            "tool_used": tool_name,
            "answer": analytics_result.get("answer"),
            "value": analytics_result.get("value"),
            "unit": analytics_result.get("unit"),
            "rows_analyzed": analytics_result.get("rows_analyzed", 0),
            "tables_used": analytics_result.get("tables_used", []),
            "breakdown": analytics_result.get("breakdown", []),
            "generated_code": "# Proof code could not be generated for this query",
            "execution_output": "",
            "verified": False,
            "verification_reason": "Proof code template unavailable."
        }

    code_result = execute_generated_code(generated_code)

    if code_result.get("status") != "success":
        return {
            "status": "verification_failed",
            "question": question,
            "tool_used": tool_name,
            "answer": analytics_result.get("answer"),
            "value": analytics_result.get("value"),
            "unit": analytics_result.get("unit"),
            "rows_analyzed": analytics_result.get("rows_analyzed", 0),
            "tables_used": analytics_result.get("tables_used", []),
            "breakdown": analytics_result.get("breakdown", []),
            "generated_code": generated_code,
            "execution_output": code_result.get("output", ""),
            "error": code_result.get("message") or code_result.get("error"),
            "verified": False,
            "verification_reason": "Proof code execution failed."
        }

    # 6. Verify the result
    verification = verify_result(
        analytics_result,
        code_result
    )

    # 7. Return complete proof
    return {
        "status": "success",
        "question": question,
        "tool_used": tool_name,

        "answer": analytics_result.get("answer"),
        "value": analytics_result.get("value"),
        "unit": analytics_result.get("unit"),
        "rows_analyzed": analytics_result.get("rows_analyzed", 0),
        "tables_used": analytics_result.get("tables_used", []),
        "breakdown": analytics_result.get("breakdown", []),

        "generated_code": generated_code,
        "execution_output": code_result.get("output", ""),

        "verified": verification.get("verified", False),
        "verification_reason": verification.get("reason", "")
    }


if __name__ == "__main__":

    questions = [
        "Which category has the highest revenue?",
        "Which state has the most orders?",
        "What is the profit?",
        "What is the employee salary?",
        "What was the revenue in 2020?"
    ]

    for question in questions:

        print("\n================================")
        print("QUESTION:", question)
        print("================================")

        result = answer_question(question)

        print("\nSTATUS:")
        print(result["status"])

        print("\nANSWER:")
        print(result.get("answer"))

        print("\nVALUE:")
        print(result.get("value"))

        print("\nUNIT:")
        print(result.get("unit"))

        print("\nVERIFIED:")
        print(result.get("verified"))

        print("\nREASON:")
        print(
            result.get("verification_reason")
            or result.get("reason")
        )

        if result.get("execution_output"):
            print("\nEXECUTION OUTPUT:")
            print(result["execution_output"])

        if result.get("error"):
            print("\nERROR:")
            print(result["error"])