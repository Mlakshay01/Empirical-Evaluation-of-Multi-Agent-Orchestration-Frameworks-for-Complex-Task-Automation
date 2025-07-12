# /orchestrator/pipeline_runner.py

from agents.classifier import classify_prompt
from agents.analyst import analyze_requirement
from agents.planner import plan_steps
from agents.coder import generate_code
from agents.tester import test_generated_code
from agents.summarizer import summarize_files
from agents.reporter import generate_final_report
from agents.researcher import run_research_agent

def run_pipeline(user_prompt: str, file_paths: list[str] = []) -> dict:
    task_type = classify_prompt(user_prompt)
    print(f"\n🧠 Detected task type: {task_type}")

    result = {"task_type": task_type, "prompt": user_prompt}

    if task_type == "code":
        requirement = analyze_requirement(user_prompt)
        plan = plan_steps(requirement)
        code = generate_code(plan)
        test_result = test_generated_code(code)

        result.update({
            "requirement": requirement,
            "plan": plan,
            "code": code,
            "test_result": test_result
        })

    elif task_type == "summarize":
        summary = summarize_files(file_paths)
        result["summary"] = summary

    elif task_type == "report":
        summary = summarize_files(file_paths) if file_paths else ""
        report = generate_final_report(user_prompt, "", "", "", {}, summary)
        result.update({
            "summary": summary,
            "report": report
        })

    elif task_type == "research":
        research_result = run_research_agent(user_prompt)
        result.update(research_result)

    else:  # fallback
        result["response"] = f"🤖 I'm not sure what to do. Please clarify your prompt."

    return result
