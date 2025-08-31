import os
from google.genai import types


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


def get_files_info(working_directory, directory="."):

    full_path = os.path.join(working_directory, directory)
    results = f"Result for {directory} directory:\n"

    
    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)): 
        results += f' Error: Cannot list "{directory}" as it is outside the permitted working directory'
        return results
    
    if not os.path.isdir(full_path):
        results += f' Error: "{directory}" is not a directory'
        return results

    try:    
        for file in os.listdir(full_path):
            f = os.path.join(full_path, file)
            results += (f" - {file}: file_size={os.path.getsize(f)} bytes, is_dir={os.path.isdir(f)}\n")

        return results
    except Exception as e:
        return f'Error listing files: {e}'