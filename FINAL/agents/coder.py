from llm.llama_wrapper import query_llama
import ast

def is_valid_python_code(code: str) -> bool:
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False

def clean_code_output(raw_output: str) -> str:
    if "```python" in raw_output:
        raw_output = raw_output.split("```python", 1)[1]
    if "```" in raw_output:
        raw_output = raw_output.split("```", 1)[0]
    return raw_output.strip()

def generate_code(coding_plan: str, max_retries: int = 2) -> str:
    system_instruction = (
        "You are a Python coding assistant. Based on the following plan, "
        "generate a complete and **runnable Python script**. "
        "Include all necessary imports (e.g., argparse, sys), and avoid using undefined variables or external inputs. "
        "If input files are required, simulate their handling safely. "
        "Return only the code. No explanations or markdown formatting."
    )

    prompt = f"{system_instruction}\n\nPlan:\n{coding_plan}\n\nPython Code:"

    for attempt in range(max_retries + 1):
        raw_output = query_llama(prompt, stream=False)
        code = clean_code_output(raw_output)

        if is_valid_python_code(code):
            return code
        elif attempt < max_retries:
            print(f"[⚠️ Retry {attempt+1}] Invalid code, retrying...")
        else:
            print("[❌ Failed] Could not generate valid code.")
            return code
