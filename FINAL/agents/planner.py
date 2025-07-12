from llm.llama_wrapper import query_llama

def plan_steps(requirement: str) -> str:
    system_instruction = (
        "You are a planner. Break down the given software requirement into logical, sequential coding steps."
    )

    prompt = f"{system_instruction}\n\nRequirement:\n{requirement}\n\nStep-by-step Plan:"
    return query_llama(prompt, stream=False)
