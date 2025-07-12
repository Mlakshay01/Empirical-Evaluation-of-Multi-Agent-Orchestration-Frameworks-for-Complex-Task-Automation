import streamlit as st
import os
import pandas as pd
from frameworks.compare_frameworks import compare_frameworks
from frameworks.langchain_runner import visualize_framework_comparison
import matplotlib.pyplot as plt

st.set_page_config(page_title="Multi-Agent AI Framework Comparison", layout="wide")
st.title("🤖 Multi-Agent AI Framework Comparison")

# Prompt input
user_prompt = st.text_area("📥 Enter your prompt:", height=150)

# File uploader
uploaded_files = st.file_uploader(
    "📎 Upload supporting files (PDF, DOCX, PPTX, TXT, JSON):",
    type=["pdf", "docx", "pptx", "txt", "json"],
    accept_multiple_files=True
)

# Manual override dropdown
task_override = st.selectbox(
    "🔧 Optional: Manually select task type (or leave as 'auto')",
    options=["auto", "code", "summarize", "report", "research", "general"]
)

# Run button
if st.button("🚀 Run All Frameworks"):
    if not user_prompt.strip():
        st.error("Please enter a valid prompt.")
    else:
        # Save uploaded files
        file_paths = []
        os.makedirs("data/uploads", exist_ok=True)
        for uploaded_file in uploaded_files:
            temp_path = os.path.join("data/uploads", uploaded_file.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            file_paths.append(temp_path)

        override = None if task_override == "auto" else task_override

        with st.spinner("🔄 Running all orchestration frameworks..."):
            all_results = compare_frameworks(user_prompt, file_paths, override_task=override)

        st.success("✅ Task completed across all frameworks.")

        # Show visual comparison
        st.header("📊 Framework Evaluation Metrics")
        try:
            visualize_framework_comparison(all_results)
            st.image(
                "data/outputs/framework_comparison.png",
                caption="Execution Time Comparison",
                use_container_width=True
            )
        except Exception as e:
            st.warning(f"⚠️ Could not load comparison chart: {e}")

        # 🔍 Expanded metrics table
        st.subheader("📋 Detailed Evaluation Table")
        metrics_data = []
        for name, res in all_results.items():
            metrics_data.append({
                "Framework": name,
                "Success ✅": "Yes" if res.get("task_success") else "No",
                "Coherence Score": res.get("coherence_score", 0),
                "Time Taken (s)": res.get("time_taken", 0),
                "Estimated Cost (tokens)": res.get("estimated_cost", 0),
            })

        df_metrics = pd.DataFrame(metrics_data)
        st.dataframe(df_metrics, use_container_width=True)

        # Show individual framework outputs
        for fw_name, results in all_results.items():
            with st.expander(f"🔧 {fw_name} Output (Task: {results.get('task_type', 'Unknown')})", expanded=True):
                task_type = results.get("task_type", "")

                if task_type == "code":
                    st.subheader("💻 Generated Code")
                    st.code(results.get("code", ""), language="python")

                elif task_type == "summarize":
                    st.subheader("📝 File Summary")
                    st.markdown(results.get("summary", ""), unsafe_allow_html=True)

                elif task_type == "report":
                    st.subheader("📄 Report Summary")
                    st.markdown(results.get("summary", ""), unsafe_allow_html=True)
                    st.subheader("📊 Final Report")
                    st.markdown(results.get("report", ""), unsafe_allow_html=True)

                elif task_type == "research":
                    st.subheader("🧠 Research Summary")
                    st.markdown(results.get("summary", ""), unsafe_allow_html=True)

                    st.subheader("🔗 Sources")
                    for src in results.get("sources", []):
                        try:
                            st.markdown(f"- [{src.get('title', 'Source')}]({src.get('href', '#')})")
                        except:
                            st.markdown("- [⚠️ Invalid source entry]")

                elif task_type == "general":
                    st.subheader("🤖 LLM Response")
                    st.markdown(results.get("response", "No response returned."))

                # Show test result (only if available)
                if "test_result" in results:
                    st.subheader("🧪 Test Result")
                    st.json(results["test_result"])

        # Cleanup uploaded files
        for path in file_paths:
            if os.path.exists(path):
                os.remove(path)
