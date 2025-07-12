import tempfile
import subprocess
import os
import sys
import re

def is_code_safe(code: str) -> bool:
    dangerous_keywords = [
        "eval", "exec", "compile", "__import__", "os.remove", "os.rmdir",
        "shutil.rmtree", "rm -rf", "subprocess.Popen", "subprocess.call"
    ]
    return not any(keyword in code for keyword in dangerous_keywords)

def test_generated_code(code: str) -> dict:
    temp_code_path = None
    dummy_input_path = None

    try:
        # Safety check first
        if not is_code_safe(code):
            return {
                "success": False,
                "stdout": "",
                "stderr": "🚨 Dangerous code detected (e.g., eval, exec, rm).",
                "reason": "unsafe_code",
                "time_taken_sec": 0.0
            }

        # Create temp file for the code
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as temp_code_file:
            temp_code_file.write(code)
            temp_code_path = temp_code_file.name

        # Create a dummy input file if the code expects a command-line input file
        dummy_input_path = temp_code_path.replace(".py", "_input.txt")
        with open(dummy_input_path, "w") as f:
            f.write("This is a dummy test file with repeated words. This is a dummy line.")

        # Prepare simulated args if required
        simulated_args = []
        if re.search(r"sys\.argv|argparse", code):
            simulated_args.append(dummy_input_path)

        # Simulate stdin input if needed
        input_data = "Simulated user input" if re.search(r"input\(\)", code) else None

        # Run the code using subprocess
        result = subprocess.run(
            [sys.executable, temp_code_path, *simulated_args],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=10
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "reason": "success" if result.returncode == 0 else "runtime_error",
            "time_taken_sec": round(result.stderr.count('\n') / 10, 3)
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": "Test timed out.",
            "reason": "timeout",
            "time_taken_sec": 10.0
        }

    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": str(e),
            "reason": "exception",
            "time_taken_sec": 0.0
        }

    finally:
        # Cleanup only if paths were assigned
        if temp_code_path and os.path.exists(temp_code_path):
            os.remove(temp_code_path)
        if dummy_input_path and os.path.exists(dummy_input_path):
            os.remove(dummy_input_path)
