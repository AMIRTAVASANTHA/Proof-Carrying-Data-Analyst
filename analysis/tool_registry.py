from analytics_tools import (
    get_top_categories,
    get_top_states,
    get_monthly_revenue,
    get_delivery_summary,
    get_late_orders,
    get_top_products
)


# ---------------------------------------------------
# AVAILABLE TOOLS
# ---------------------------------------------------

TOOLS = {
    "top_category": {
        "description": "Find the product category with the highest revenue",
        "function": get_top_categories
    },

    "top_state": {
        "description": "Find the state with the highest number of orders",
        "function": get_top_states
    },

    "monthly_revenue": {
        "description": "Calculate revenue for each month",
        "function": get_monthly_revenue
    },

    "average_delivery": {
        "description": "Calculate the average delivery time",
        "function": get_delivery_summary
    },

    "late_orders": {
        "description": "Count orders delivered after a given number of days",
        "function": get_late_orders
    },

    "top_product": {
        "description": "Find the product with the highest revenue",
        "function": get_top_products
    }
}


# ---------------------------------------------------
# TOOL EXECUTOR
# ---------------------------------------------------

def execute_tool(tool_name, **parameters):

    if tool_name not in TOOLS:
        return {
            "error": "Tool not found",
            "tool": tool_name
        }

    tool_function = TOOLS[tool_name]["function"]

    result = tool_function(**parameters)

    return result


# ---------------------------------------------------
# TEST
# ---------------------------------------------------

if __name__ == "__main__":

    print("AVAILABLE TOOLS:\n")

    for name, tool in TOOLS.items():
        print(name, "->", tool["description"])

    print("\n-----------------------------")
    print("TESTING TOOL EXECUTOR")
    print("-----------------------------")

    result = execute_tool("top_state")

    print("\nTOP STATE RESULT:")
    print(result)