TOOLS = [
    {
        "name": "analyze_dataset",
        "description": "Analyze a CSV dataset and answer questions about it.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the CSV dataset."
                },
                "question": {
                    "type": "string",
                    "description": "Question that needs to be answered."
                }
            },
            "required": ["file_path", "question"]
        }
    }
]


def get_tools():
    return TOOLS


if __name__ == "__main__":
    print("Available tools:")
    
    for tool in TOOLS:
        print("-", tool["name"])