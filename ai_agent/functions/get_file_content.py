import os
from .config import MAX_CHARS
from google.genai import types


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Return the file contents as a string, or perhaps an error string if something went wrong.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to read from, relative to the working directory.",
            ),
        },
    ),
)



def get_file_content(working_directory, file_path):

    full_path = os.path.join(working_directory, file_path)


    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)): 
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(full_path, "r") as file:
            file_content_string = file.read(MAX_CHARS + 1)

            if len(file_content_string) > MAX_CHARS:
                file_content_string = file_content_string[:-1]
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            
            return file_content_string
    except Exception as e:
            return f'Error reading file "{file_path}": {e}'
