# langchain_runner.py
from agents.analyst import analyze_requirement
from agents.planner import plan_steps
from agents.coder import generate_code
from agents.tester import test_generated_code
from agents.summarizer import summarize_files
from agents.reporter import generate_final_report
from agents.researcher import run_research_agent
from llm.llama_wrapper import query_llama
import matplotlib.pyplot as plt

def run_with_langchain(prompt: str, file_paths: list[str] = [], override_task: str = None) -> dict:
    from agents.classifier import classify_prompt

    task_type = override_task or classify_prompt(prompt)
    result = {"framework": "LangChain", "prompt": prompt, "task_type": task_type}

    if task_type == "code":
        requirement = analyze_requirement(prompt)
        plan = plan_steps(requirement)
        code = generate_code(plan)
        test_result = test_generated_code(code)
        result.update({"requirement": requirement, "plan": plan, "code": code, "test_result": test_result})

    elif task_type == "summarize":
        summary = summarize_files(file_paths)
        result.update({"summary": summary})

    elif task_type == "report":
        summary = summarize_files(file_paths) if file_paths else ""
        report = generate_final_report(prompt, "", "", "", {}, summary)
        result.update({"summary": summary, "report": report})

    elif task_type == "research":
        research_result = run_research_agent(prompt)
        result.update(research_result)

    else:
        fallback = query_llama(prompt)
        result.update({"response": fallback})

    return result



def visualize_framework_comparison(comparison_results):
    import matplotlib.pyplot as plt

    labels = list(comparison_results.keys())
    times = [res.get("time_taken", 0) for res in comparison_results.values()]

    plt.figure(figsize=(6, 4))
    bars = plt.bar(labels, times, color=["#6a5acd", "#ff8c00", "#3cb371"])
    plt.xlabel("Framework")
    plt.ylabel("Time Taken (seconds)")
    plt.title("Framework Execution Time Comparison")
    plt.ylim(0, max(times) * 1.2)

    for bar, time_taken in zip(bars, times):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02, f"{time_taken:.2f}s", ha="center", fontsize=9)

    plt.tight_layout()
    plt.savefig("data/outputs/framework_comparison.png")
    plt.close()
