# Academic Course Assistant (Capstone Edition)

A complete, production-ready capstone submission for B.Tech students. This agentive assistant uses LangGraph to answer syllabus queries securely and robustly, utilizing ChromaDB document retrieval, dynamic agentic routing, and strict anti-hallucination nodes.

## 🌟 Features Implemented
1. **LangGraph Architected Engine**: Complete graph workflow with conditional routing (memory -> router -> [retrieve/skip/tool] -> answer -> eval -> [retry/save]).
2. **Robust ChromaDB RAG**: Built-in vectors loading standard B.Tech subjects context cleanly with strict markdown citations appended to assistant outputs.
3. **Session Persistence**: Complete conversation memory tracked across a Streamlit UI via Checkpointer logic.
4. **Self-Reflection Evaluation State**: Employs an LLM sub-agent. If `Faithfulness Score < 0.70`, the system automatically re-evaluates the prompt trace and tries again to prevent hallucinations.
5. **Custom Tool Framework**: Sandboxed Date/Time, Calculator, and Web-Fallback tools.
6. **Viva/Demo Ready Frontend**: Streamlit UI supports Dark/Light mode, Chat Log downloads, built-in Question Counters, and a pre-loaded Demo Menu toggle to show off agent responses instantly.

## ⚙️ Architecture

### How Memory Works
We use a sliding-window array of size limit `[-6:]` merged via `sqlite` (or LangGraph's native `MemorySaver`) locked to a unique `thread_id` UUID generated in the Streamlit Sidebar per conversation.

### How RAG Works
15 course documents are vectorized using Hugging Face model `all-MiniLM-L6-v2`. When a query arrives sequentially, cosine similarity selects `top_k=3`. The outputs contain explicit `[Source: doc_XXX.txt]` headers, forcefully included in the LLM final trace.

---

## 🛠 Usage & Testing Tools

### Running The Interface
```bash
pip install -r requirements.txt
# Populate .env file with your GROQ_API_KEY or OPENAI_API_KEY
streamlit run app.py
```

### Running the Red-Team Adversarial Test
We built an automated script (`red_team.py`) testing Prompt Injection, False Premises, and Hallucination Baits natively.
```bash
python red_team.py
```
**Results Example:**
- Prompt Injection: PASS (Refused)
- Hallucination Bait: PASS ("I don't know based on available course materials.")

### Running the RAG Benchmarks
We include an LLM-as-a-judge system (`eval_benchmark.py`) calculating Faithfulness, Relevancy, and Context Precision over standard syllabus questions.
```bash
python eval_benchmark.py
```

---

## 📋 Viva Questions & Answers
**Q1. Why did you use LangGraph instead of standard Langchain Chains?**  
*A1. LangGraph allows cyclical logic, giving us an `eval_node` to score faithfulness. A normal chain is linear and cannot loop back reliably if hallucination is detected.*

**Q2. How is hallucination prevented exactly?**  
*A2. Two steps. 1) Strict `answer_node` system prompting mandating adherence only to retrieved context. 2) A standalone `eval_node` calculating a 0-to-1 score. If it fails, it retries building the node dynamically.*

**Q3. What happens if a user asks a math question?**  
*A3. `router_node` identifies operational characters like `+,-,*,/` and parses it directly out of the RAG pipeline into the `tool_node`, allowing safe localized execution without vector noise.*

## 🚀 Future Scope
- Transition `MemorySaver` into persistent Postgres (PgVector).
- Upload PDF slide decks directly via Streamlit Dropzone handling natively into Chroma Collections.
- Add user-authentication loops and specific class profile loading.
