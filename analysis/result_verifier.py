def verify_result(analytics_result, execution_result):
    """
    Compare the trusted analytics result with the
    result produced by the generated proof code.
    """

    verification = {
        "verified": False,
        "reason": "",
        "analytics_value": None,
        "execution_output": None
    }

    # -----------------------------------------
    # Check analytics result
    # -----------------------------------------

    if not analytics_result:
        verification["reason"] = "Analytics result is empty."
        return verification

    # -----------------------------------------
    # Check execution result
    # -----------------------------------------

    if not execution_result:
        verification["reason"] = "Proof code produced no result."
        return verification

    if execution_result.get("status") != "success":
        verification["reason"] = "Proof code execution failed."
        return verification

    # -----------------------------------------
    # Get expected value
    # -----------------------------------------

    expected_value = analytics_result.get("value")

    execution_output = execution_result.get(
        "output",
        ""
    )

    verification["analytics_value"] = expected_value
    verification["execution_output"] = execution_output

    # -----------------------------------------
    # Make sure expected value exists
    # -----------------------------------------

    if expected_value is None:

        verification["reason"] = (
            "No numerical value available "
            "for verification."
        )

        return verification

    # -----------------------------------------
    # Compare result with execution output
    # -----------------------------------------

    expected_string = str(expected_value)

    if expected_string in execution_output:

        verification["verified"] = True

        verification["reason"] = (
            "The proof code executed successfully "
            "and produced the same value as the "
            "trusted analytics result."
        )

    else:

        verification["verified"] = False

        verification["reason"] = (
            "The proof code executed successfully, "
            "but its output does not match the "
            "trusted analytics result."
        )

    return verification