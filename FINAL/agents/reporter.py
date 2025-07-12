import os
from PyPDF2 import PdfReader
from llm.llama_wrapper import query_llama

def extract_text_from_pdf(file_path: str) -> str:
    try:
        reader = PdfReader(file_path)
        text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
        return text.strip()
    except Exception as e:
        return f"[Error reading PDF {file_path}: {e}]"

def create_combined_context(
    plan: str = "", 
    code: str = "", 
    test_result: dict = None, 
    summary: str = "", 
    pdf_paths: list[str] = None
) -> str:
    test_result = test_result if isinstance(test_result, dict) else {}

    context_parts = [
        "## Planning Steps",
        plan.strip() or "[Not Applicable]",
        "",
        "## Generated Code",
        code.strip() or "[Not Applicable]",
        "",
        "## Test Result",
        f"Success: {test_result.get('success', 'N/A')}",
        f"Reason: {test_result.get('reason', 'N/A')}",
        f"Output: {test_result.get('stdout', 'N/A')}",
        f"Errors: {test_result.get('stderr', 'N/A')}",
        ""
    ]

    if summary:
        context_parts.append("## Summary")
        context_parts.append(summary.strip())
        context_parts.append("")

    if pdf_paths:
        context_parts.append("## Attached PDF Summaries")
        for pdf_path in pdf_paths:
            file_name = os.path.basename(pdf_path)
            pdf_text = extract_text_from_pdf(pdf_path)

            if isinstance(pdf_text, str) and not pdf_text.startswith("[Error") and pdf_text.strip():
                try:
                    short_summary = query_llama(f"Summarize this document:\n\n{pdf_text[:4000]}", stream=False)
                    context_parts.append(f"**{file_name}**:\n{short_summary.strip()}\n")
                except Exception as e:
                    context_parts.append(f"**{file_name}**: [Error summarizing: {e}]")
            else:
                context_parts.append(f"**{file_name}**: {pdf_text or '[No extractable text]'}")
        context_parts.append("")

    return "\n".join(context_parts)

def generate_final_report(
    user_prompt: str, 
    requirement: str = "", 
    plan: str = "", 
    code: str = "", 
    test_result: dict = None, 
    summary: str = "", 
    pdf_paths: list[str] = None
) -> str:
    context = create_combined_context(plan, code, test_result or {}, summary, pdf_paths)

    prompt = f"""You are a technical writer. Based on the following AI outputs, generate a clear and professional report for submission. Include appropriate headings, structure, and technical clarity.

## User Prompt
{user_prompt.strip() or '[Missing]'}

## Technical Requirement
{requirement.strip() or '[Not Applicable]'}

{context}

Final Report:"""

    return query_llama(prompt, stream=False)
