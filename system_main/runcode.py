import subprocess

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

        print(f'Process output: {output}')
        print(f'Process error: {error}')
        print(f'Process return code: {process.returncode}')
    except Exception as e:
        output = 'didnt catch thecode'
        error = str(e)

    return output, error