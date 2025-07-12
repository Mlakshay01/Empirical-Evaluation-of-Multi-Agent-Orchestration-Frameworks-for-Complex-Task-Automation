import requests
import json

def query_llama(prompt: str, model="llama3.2", temperature=0.7, stream=False):
    print(f"\n📤 Prompt sent to LLaMA:\n{prompt[:400]}...\n")

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "temperature": temperature},
            stream=stream
        )

        result = ""

        if stream:
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line.decode("utf-8").replace("data: ", ""))
                        print("[🧠 CHUNK]", chunk.get("response", "").strip())
                        result += chunk.get("response", "")
                    except Exception as e:
                        print("[❌ PARSE ERROR]", e)
        else:
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line.decode("utf-8").replace("data: ", ""))
                        result += chunk.get("response", "")
                    except Exception as e:
                        print("[❌ PARSE ERROR]", e)

        return result.strip()

    except requests.exceptions.RequestException as e:
        print("[❌ LLaMA Request Error]", e)
        return "[LLaMA connection failed]"
