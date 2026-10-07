TOOLS = [

    {
        "name": "top_category",
        "description": "Find the product category with the highest revenue.",
        "parameters": {}
    },

    {
        "name": "top_state",
        "description": "Find the state with the highest number of orders.",
        "parameters": {}
    },

    {
        "name": "monthly_revenue",
        "description": "Calculate revenue for each month.",
        "parameters": {}
    },

    {
        "name": "average_delivery",
        "description": "Calculate the average delivery time in days.",
        "parameters": {}
    },

    {
        "name": "late_orders",
        "description": "Count orders delivered after a specified number of days.",
        "parameters": {
            "days": {
                "type": "integer",
                "description": "Number of days used as the threshold."
            }
        }
    },

    {
        "name": "top_product",
        "description": "Find the product with the highest revenue.",
        "parameters": {}
    }
]


def get_tools():
    return TOOLS