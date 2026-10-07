from agent import Agent
from code_generator import generate_code
from tool_executor import execute_generated_code
from verifier import verify_result


def run_complete_test():

    print("=" * 50)
    print("PROOF-CARRYING DATA ANALYST")
    print("=" * 50)

    # 1. User request
    question = "How many customers are there?"

    print("\n1. USER REQUEST")
    print(question)

    # 2. Agent
    agent = Agent()

    print("\n2. AGENT DECISION")
    agent_result = agent.run(question)

    print(agent_result)

    # 3. Code generation
    print("\n3. CODE GENERATION")

    generated_code = generate_code(question)

    if generated_code is None:
        print("No suitable code generated.")
        return

    print(generated_code)

    # 4. Code execution
    print("\n4. CODE EXECUTION")

    execution_result = execute_generated_code(
        generated_code
    )

    print(execution_result)

    # 5. Verification
    print("\n5. VERIFICATION")

    verification_result = verify_result(
    execution_result
)

    print(verification_result)

    # 6. Final result
    print("\n6. FINAL RESULT")

    if verification_result["verified"]:
        print("✅ VERIFIED RESULT")
        print(execution_result["output"])
    else:
        print("❌ RESULT COULD NOT BE VERIFIED")


if __name__ == "__main__":
    run_complete_test()