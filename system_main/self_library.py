import django
from django.conf import settings
from .models import File,AskAIRecord
import subprocess
import difflib
import sys
import tempfile
import selectors
import os
from code import InteractiveInterpreter
from io import StringIO

from subprocess import Popen, PIPE

def initialize_django():
    """Ensure Django is initialized properly in each process."""
    if not settings.configured:
        django.setup()

def run_code(code):
    try:
        # Execute the code
        process = subprocess.run(
            ['python', '-c', code],
            text=True,
            capture_output=True,
            timeout=20  # Limit the execution time
        )
        
        output = process.stdout
        error = process.stderr

        print(f'Process output:\n{output}\n')
        print(f'Process error: {error}\n')
        print(f'Process return code: {process.returncode}\n')
    except Exception as e:
        output = 'didnt catch the code'
        error = str(e)

    return output, error


    
def debug_code_with_file(server_data,main_file):
    """
    Debug Python code by running it from a temporary file.
    Includes additional library files if provided.

    Args:
        code (str): The Python code to execute.
        lib_files (dict): A dictionary of filenames and their content 
                          for additional library files.

    Returns:
        tuple: (output, error)
    """

    # Separate main file and library files
    # Filter out the main_file

    lib_file = [file for file in server_data if file['id'] != main_file['id']]
    print("lib_file",lib_file)
    print("main_file",main_file)
    print("server_data",server_data)
    try:
        # Create a temporary directory to store files
        with tempfile.TemporaryDirectory() as temp_dir:
            print("tempfile")
           # Write the main file
            main_file_path = os.path.join(temp_dir, f"{main_file['FileName']}")
            with open(main_file_path, "w") as f:
                # Use rstrip() to remove any trailing whitespace from lines
                cleaned_code = "\n".join(line.rstrip() for line in main_file['Code'].splitlines())
                f.write(cleaned_code)

            # Write library files
            for lib in lib_file:
                lib_file_path = os.path.join(temp_dir, f"{lib['FileName']}")
                with open(lib_file_path, "w") as f:
                    cleaned_code = "\n".join(line.rstrip() for line in lib['Code'].splitlines())
                    f.write(cleaned_code)
            
             # List and display the contents of temp_dir
            files_in_temp_dir = os.listdir(temp_dir)
            print("Contents of temporary directory:")
            for file_name in files_in_temp_dir:
                file_path = os.path.join(temp_dir, file_name)
                # Read the file content to print the code
                with open(file_path, "r") as f:
                    file_code = f.read()
                    print(f"File: {file_name}\nCode:\n{file_code}\n")

            # Run the main file using subprocess
            process = subprocess.run(
                ['python', main_file_path],
                text=True,
                capture_output=True,
                timeout=20  # Limit execution time
            )

            # Capture output and errors
            output = process.stdout
            error = process.stderr

            print(f'Process output:\n{output}\n')
            print(f'Process error:\n{error}\n')
            print(f'Process return code: {process.returncode}\n')

            return output, error

    except Exception as e:
        print(f"An error occurred: {e}")
        return "", str(e)


# Compare the code by User with the code by ChatGPT
def compare_code(original_code,compare_code):
    original_code_lines = original_code.strip().split('\n')
    compare_code_line = compare_code.strip().split('\n')
    diff = list(difflib.unified_diff(original_code_lines, compare_code_line, lineterm=''))
    print(f'original={original_code_lines}')
    print(f'feedback={compare_code_line}')
    print (diff)
    return diff

#CanAskAI is the permission to run the API
def CanAskAI():
    """
    if option == "only_code":
        return not only_code
    elif option == "without_code":
        return not without_code
    else :
        return True
    """
    return True
        
