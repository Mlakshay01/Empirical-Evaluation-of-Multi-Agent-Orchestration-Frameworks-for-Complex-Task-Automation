This project benchmarks and evaluates the performance of three leading open-source multi-agent orchestration frameworks — LangChain, CrewAI, and AutoGen — in executing real-world complex AI tasks like multi-document summarization, report generation, web research, and code generation. The agents are powered by local LLaMA 3.2 via Ollama, without relying on paid OpenAI APIs.

🎯 Objectives
Design modular multi-agent systems for tasks like summarization, research, and code generation.

Orchestrate agent workflows using LangChain, CrewAI, and AutoGen frameworks.

Evaluate each framework on key dimensions: execution time, task success, coherence, and token cost.

Generate real-time visual and tabular comparison reports through a Streamlit dashboard.

🛠️ Tech Stack
| Component                 | Technology Used                            |
| ------------------------- | ------------------------------------------ |
| **LLM Backend**           | [LLaMA 3.2 via Ollama](https://ollama.com) |
| **Agent Frameworks**      | LangChain, CrewAI, AutoGen                 |
| **UI Framework**          | Streamlit                                  |
| **Document Parsing**      | PyPDF2, python-docx, python-pptx           |
| **Web Search (fallback)** | Serp API                        |
| **Evaluation**            | Coherence via LLM, token count             |
| **Visualization**         | Matplotlib, Pandas                         |

🧪 Benchmark Tasks
| Task                    | Example Roles                     |
| ----------------------- | --------------------------------- |
| Multi-Doc Summarization | Retriever, Summarizer, Evaluator  |
| Python Code Generation  | Analyst, Coder, Tester            |
| Web Research Agent      | Searcher, Ranker, Note-Taker      |
| Report Writing          | Data Collector, Writer, Formatter |

📊 Evaluation Metrics
| Metric              | Description                                      |
| ------------------- | ------------------------------------------------ |
| **Task Success**    | Boolean — did the framework produce valid output |
| **Execution Time**  | Total time for full orchestration                |
| **Coherence Score** | Evaluated using local LLaMA judging prompt       |
| **Token Estimate**  | Estimated tokens based on input + output         |

🚀 How It Works
User inputs a prompt and optional documents via the Streamlit interface.

Each orchestration framework independently executes the task using defined agents.

All outputs are collected and:

Compared by execution time

Scored for coherence using local LLaMA

Token usage estimated

Final results are visualized and tabulated.

📷 UI Preview
<img width="928" height="847" alt="image" src="https://github.com/user-attachments/assets/9fcdfc45-9b95-4552-aef3-b51330651564" />

🧩 Setup & Run
1. Clone Repo
   
git clone https://github.com/your-username/ai-multiagent-orchestration
cd ai-multiagent-orchestration

2. Set Up Environment

python -m venv venv
venv\Scripts\activate  # on Windows
pip install -r requirements.txt

3. Run App

streamlit run app.py

Ensure you have Ollama running with LLaMA 3.2 pulled:

ollama run llama3.2

🧠 Example Prompt
Give a Python code to count frequency of words in a text file. Also generate a report on the code.

📝 Acknowledgments
[LangChain.com](https://www.langchain.com/)

[CrewAI](https://docs.crewai.com/en/introduction)

[AutoGen](https://microsoft.github.io/autogen/stable/)

Ollama









