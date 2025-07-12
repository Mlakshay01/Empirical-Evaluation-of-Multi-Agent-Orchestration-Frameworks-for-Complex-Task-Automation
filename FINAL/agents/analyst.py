from llm.llama_wrapper import query_llama

def analyze_requirement(user_prompt: str) -> str:
    system_instruction = (
        "You are a software analyst. Your task is to turn the user's prompt into a formal technical requirement "
        "for a developer. Make it clear, concise, and implementation-ready."
    )

    prompt = f"{system_instruction}\n\nUser Prompt:\n{user_prompt}\n\nFormal Requirement:"
    return query_llama(prompt, stream=False)
