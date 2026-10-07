import subprocess
import sys
import tempfile
import os


def execute_generated_code(code):

    print("\nExecuting generated code...")

    project_root = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

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

            timeout=30,

            cwd=project_root
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


    except subprocess.TimeoutExpired:

        return {
            "status": "error",
            "message": "Code execution timed out."
        }


    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }