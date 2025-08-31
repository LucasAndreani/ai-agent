from google.genai import types
from .get_file_content import get_file_content
from .get_files_info import get_files_info
from .write_file import write_file
from .run_python import run_python_file

def call_function(function_call_part, verbose=False):
    functions_dict = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "write_file": write_file,
        "run_python_file": run_python_file
    }
    

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    if not function_call_part.name in functions_dict:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    
    kwargs = dict(function_call_part.args)
    kwargs["working_directory"] = "./calculator"
    result = functions_dict[function_call_part.name](**kwargs)

    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={"result": result},
        )
    ],
)
    
