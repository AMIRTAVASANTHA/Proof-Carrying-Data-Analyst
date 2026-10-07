def verify_result(result, code):

    print("\nVerifying result...")

    proof = {
        "execution_successful": False,
        "output_present": False,
        "dataset_used": False,
        "verified": False
    }

    # Check 1: Execution successful
    if result and result.get("status") == "success":
        proof["execution_successful"] = True

    # Check 2: Output exists
    output = result.get("output", "") if result else ""

    if output.strip():
        proof["output_present"] = True

    # Check 3: Dataset was used
    if "read_csv" in code:
        proof["dataset_used"] = True

    # Final verification
    if (
        proof["execution_successful"]
        and proof["output_present"]
        and proof["dataset_used"]
    ):
        proof["verified"] = True

    return proof


if __name__ == "__main__":

    test_code = """
import pandas as pd

data = pd.read_csv("data/olist_customers_dataset.csv")

print("Total Customers:", len(data))
"""

    test_result = {
        "status": "success",
        "output": "Total Customers: 99441"
    }

    verification = verify_result(
        test_result,
        test_code
    )

    print("\nPROOF CERTIFICATE")
    print("-----------------")

    for key, value in verification.items():
        print(key, ":", value)