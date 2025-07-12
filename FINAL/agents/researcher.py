import requests
from llm.llama_wrapper import query_llama

# 🔍 Use Brave Search API instead of DuckDuckGo
def brave_search(query: str, api_key: str, max_results=5):
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": api_key
    }
    params = {"q": query, "count": max_results}

    try:
        res = requests.get(url, headers=headers, params=params)
        res.raise_for_status()
        data = res.json()

        results = []
        for item in data.get("web", {}).get("results", []):
            results.append({
                "title": item.get("title", ""),
                "href": item.get("url", ""),
                "body": item.get("description", "")
            })
        return results

    except Exception as e:
        return [{"title": "[Error] Brave API failed", "href": "#", "body": str(e)}]

# 🧠 Format as markdown list
def format_markdown_links(results: list[dict]) -> str:
    markdown_links = []
    for r in results:
        markdown_links.append(
            f"#### 📘 **[{r['title']}]({r['href']})**\n{r['body']}\n"
        )
    return "\n".join(markdown_links)

# ✨ Summarize results always for research task
def summarize_if_requested(prompt: str, results: list[dict]) -> str:
    combined = "\n\n".join(
        f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}" for r in results
    )
    llama_prompt = f"""You are a research assistant. Based on the following search results, provide a concise summary.

User Query:
{prompt}

Search Results:
{combined}

Summary:"""
    return query_llama(llama_prompt, stream=False)

# 🔁 Research agent with Brave + LLaMA summary
def run_research_agent(prompt: str, brave_api_key: str = "your_api_key_here") -> dict:
    results = brave_search(prompt, brave_api_key)
    summary = summarize_if_requested(prompt, results)
    markdown_sources = format_markdown_links(results)

    return {
        "query": prompt,
        "summary": summary or "No summary requested.",
        "sources": markdown_sources
    }