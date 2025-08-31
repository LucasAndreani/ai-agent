import os
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write the content passed to the specified file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that is to be written in the file.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to write to, relative to the working directory.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)

    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(working_directory):
        try:
            os.makedirs(os.path.dirname(os.path.abspath(full_path)),  exist_ok=True)
        except Exception as e:
            return f'Error creating directory: {e}'

    try:
        with open(full_path, "w") as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error writing to file: {e}'
    
