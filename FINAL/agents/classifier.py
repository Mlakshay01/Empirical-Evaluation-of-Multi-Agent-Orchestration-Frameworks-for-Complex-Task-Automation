from llm.llama_wrapper import query_llama

TASK_TYPES = ["code", "summarize", "report", "research", "general"]

def classify_prompt(prompt: str) -> str:
    """
    Classify the user prompt into one of the supported task types using LLaMA.
    Returns: one of TASK_TYPES
    """
    system_instruction = (
        "You are a task classifier for an AI assistant. "
        "Classify the following user prompt into exactly one of the following task types:\n\n"
        "1. code - if the user wants to generate or test Python code\n"
        "2. summarize - if the user wants to summarize files or documents\n"
        "3. report - if the user wants a formal or structured report from the AI\n"
        "4. research - if the user asks to search the web or find current info\n"
        "5. general - if it doesn't clearly match any of the above\n\n"
        "Respond with only the task type (code / summarize / report / research / general), nothing else."
    )

    final_prompt = f"{system_instruction}\n\nUser Prompt:\n{prompt.strip()}\n\nTask Type:"
    raw_response = query_llama(final_prompt, stream=False).lower().strip()

    # Normalize response
    for task in TASK_TYPES:
        if task in raw_response:
            return task

    return "general"  # fallback
