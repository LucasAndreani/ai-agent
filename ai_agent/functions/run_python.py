import os
import subprocess
import sys
from google.genai import types


schema_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description="Run the given .py file, pass the arguments if needed",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the file that will be run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="The arguments passed to the file, if needed.",
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)

    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(
            [sys.executable, file_path,] + args,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=os.path.abspath(working_directory)
        )
    except Exception as e:
        return f'Error running Python file: {e}'

    result_string = f'STDOUT:{result.stdout}\nSTDERR:{result.stderr}'

    if not result.stdout and not result.stderr:
        return "No output produced."
    
    if result.returncode != 0:
        result_string += f"\nProcess exited with code {result.returncode}"
    
    
    return result_string