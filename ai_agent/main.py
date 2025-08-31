import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.config import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python import schema_run_python
from functions.call_function import call_function


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python
    ]
)


def main():
    try:
        messages = [
        types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
        ]
    except IndexError as e:
        print("Error: Must provide a prompt")
        sys.exit(1)

    iterations_counts = 0

    while iterations_counts < 20:
        response = client.models.generate_content(
            model='gemini-2.0-flash-001', 
            contents= messages,
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
        )

        if "--verbose" in sys.argv:
            print(f"User prompt: {sys.argv[1]}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        for candidate in response.candidates:
            messages.append(candidate.content)
        
        if response.function_calls:
            function_responses = []

            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part)
                function_responses.append(function_call_result.parts[0])

                if not function_call_result.parts[0].function_response.response:
                    raise Exception("Fatal Error")
                elif "--verbose" in sys.argv:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

            messages.append(types.Content(role="user", parts=function_responses))


        else:
            print("Final Response:")
            print(response.text)
            return 
        
        iterations_counts += 1
        

if __name__ == "__main__":
    main()


