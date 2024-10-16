from .models import CodeSnippet,CodeRecord
import subprocess
import difflib

def run_code(code):
    try:
        # Execute the code
        process = subprocess.run(
            ['python', '-c', code],
            text=True,
            capture_output=True,
            timeout=10  # Limit the execution time
        )
        output = process.stdout
        error = process.stderr

        print(f'Process output: {output}\n')
        print(f'Process error: {error}\n')
        print(f'Process return code: {process.returncode}\n')
    except Exception as e:
        output = 'didnt catch thecode'
        error = str(e)

    return output, error


# Compare the instant code and the lastest Code Record
def IsSameCode(snippet):
    # CodeRecord if it exists(if the code debuged before),
    if CodeRecord.objects.filter(CodeSnippet=snippet).exists:
        lastest_code_record = CodeRecord.objects.filter(CodeSnippet=snippet).order_by('-created_at').first()
        
        #If the CodeRecord is exits ,checked the code is the same with the lastest CodeRecord
        if lastest_code_record and lastest_code_record.original_code == snippet.code :
            print("Block Debug because Same Code with the lastest")
            return True
        #False if code different with lastest CodeRecord
        else:
            #print("Different Code with the Lastest")
            return False
    #False if the lastest Record not exits(This is the first code)
    else:
        #print("The First code")
        return False
    

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
def CanAskAI(only_code,without_code,option):
    if option == "only_code":
        return not only_code
    elif option == "without_code":
        return not without_code
    else :
        return True

        
