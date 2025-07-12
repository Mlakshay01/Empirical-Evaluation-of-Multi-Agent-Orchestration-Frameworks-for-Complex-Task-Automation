from orchestrator.pipeline_runner import run_pipeline
import json

if __name__ == "__main__":
    print("📥 Multi-Agent AI Assistant")
    user_prompt = input("Enter your prompt: ").strip()

    file_input = input("Attach any file paths separated by commas (or press Enter to skip): ").strip()
    file_paths = [f.strip() for f in file_input.split(",")] if file_input else []

    results = run_pipeline(user_prompt, file_paths)

    print("\n✅ Final Output:\n")

    # Pretty print based on task
    task_type = results.get("task_type", "")
    if task_type == "code":
        print("🔧 Code Output:")
        print(results["code"])
        print("\n🧪 Test Result:")
        print(json.dumps(results["test_result"], indent=2))

    elif task_type == "summarize":
        print("📝 Summary:")
        print(results["summary"])

    elif task_type == "report":
        print("📊 Report:")
        print(results["report"])

    elif task_type == "research":
        print("🌐 Web Research:")
        print(results["web_results"])

    else:
        print("🤖 Response:")
        print(results.get("response", "No output."))

    # Optionally: dump everything
    # print("\n--- Full Raw Output ---")
    # print(json.dumps(results, indent=2))
