import time
import math
from frameworks.crewai_runner import run_with_crewai
from frameworks.langchain_runner import run_with_langchain
from frameworks.autogen_runner import run_with_autogen
from llm.llama_wrapper import query_llama
from agents.summarizer import extract_text_from_file

# 🔍 Get coherence score from LLaMA locally
def get_llm_coherence_score(prompt: str, output: str, docs: list[str] = []) -> float:
    doc_text = "\n\n".join(docs) if docs else "[No document]"
    judge_prompt = f"""
You are a strict evaluator scoring how coherent and useful an AI output is for a given user prompt and its attached documents.
Rate between 0 (poor) and 1 (perfect), considering clarity, relevance, and completeness.

User Prompt:
{prompt}

Attached Document(s):
{doc_text[:2000]}

AI Output:
{output}

Score (just the number):
"""
    try:
        score_text = query_llama(judge_prompt, stream=False).strip()
        return float(score_text)
    except:
        return 0.0

# 💰 Estimate cost based on token usage
def estimate_token_cost(prompt: str, output: str, docs: list[str] = []) -> float:
    total_words = len(f"{prompt} {output} {' '.join(docs)}".split())
    return round(total_words / 4, 2)

# 📄 Extract text from uploaded files
def parse_uploaded_files(file_paths):
    texts = []
    for path in file_paths:
        try:
            text = extract_text_from_file(path)
            if text:
                texts.append(text.strip())
        except:
            pass
    return texts

def compare_frameworks(prompt: str, file_paths: list[str] = [], override_task: str = None) -> dict:
    results = {}
    doc_texts = parse_uploaded_files(file_paths)

    # Run CrewAI
    start = time.time()
    crewai_result = run_with_crewai(prompt, file_paths, override_task=override_task)
    crewai_result["time_taken"] = round(time.time() - start, 3)
    results["CrewAI"] = crewai_result

    # Run LangChain
    start = time.time()
    langchain_result = run_with_langchain(prompt, file_paths, override_task=override_task)
    langchain_result["time_taken"] = round(time.time() - start, 3)
    results["LangChain"] = langchain_result

    # Run AutoGen
    start = time.time()
    autogen_result = run_with_autogen(prompt, file_paths, override_task=override_task)
    autogen_result["time_taken"] = round(time.time() - start, 3)
    results["AutoGen"] = autogen_result

    # === Add Metrics (Success, Coherence, Cost) ===
    for fw_name, fw_result in results.items():
        test_result = fw_result.get("test_result", {})
        fw_result["task_success"] = test_result.get("success", True)

        output = fw_result.get("summary") or fw_result.get("report") or fw_result.get("code") or fw_result.get("response", "")
        fw_result["coherence_score"] = get_llm_coherence_score(prompt, output, doc_texts)
        fw_result["estimated_cost"] = estimate_token_cost(prompt, output, doc_texts)

    return results
