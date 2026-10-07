import pandas as pd
import subprocess
import sys
import tempfile
import os


def analyze_dataset(file_path, question):
    print("Analyzing dataset...")
    print("File:", file_path)
    print("Question:", question)

    try:
        data = pd.read_csv(file_path)

        print("\nDataset loaded successfully!")
        print("Rows:", len(data))
        print("Columns:", list(data.columns))

        return {
            "status": "success",
            "rows": len(data),
            "columns": list(data.columns)
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def execute_generated_code(code):
    print("\nExecuting generated code...")

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8"
        ) as file:

            file.write(code)
            temp_file = file.name

        result = subprocess.run(
            [sys.executable, temp_file],
            capture_output=True,
            text=True,
            timeout=10
        )

        os.remove(temp_file)

        if result.returncode == 0:

            print("Code executed successfully!")

            return {
                "status": "success",
                "output": result.stdout
            }

        return {
            "status": "error",
            "message": result.stderr
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


if __name__ == "__main__":

    from code_generator import generate_code

    question = "Analyze the customer data"

    generated_code = generate_code(question)

    print("Generated Code:")
    print(generated_code)

    result = execute_generated_code(generated_code)

    print("\nExecution Result:")
    print(result)