import streamlit as st
import os
import json
import uuid
from dotenv import load_dotenv

load_dotenv()

try:
    from graph import course_graph
except Exception as e:
    course_graph = None
    st.error(f"Failed to load graph setup. Error: {str(e)}")

st.set_page_config(page_title="Academic Course Assistant", page_icon="🎓", layout="wide")

@st.cache_resource
def get_graph():
    return course_graph

def reset_thread():
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.chat_history = []
    st.session_state.question_count = 0
    
if "thread_id" not in st.session_state:
    reset_thread()

st.title("🎓 Academic Course Assistant")
st.markdown("*A LangGraph-powered Agentic RAG for B.Tech students (Capstone Edition).*")

# Demo questions
DEMO_QUESTIONS = [
    "Explain the OSI model.",
    "Why does TCP have 12 layers?",
    "What is the difference between TCP and UDP?",
    "What is deadlocks?",
    "What is my name?",
    "Calculate 125 * 4",
    "What is Tesla stock price?",
    "Give exact exam questions for tomorrow.",
    "Explain Testing in Software Engineering.",
    "What time is it?"
]

# Sidebar
with st.sidebar:
    st.header("Project Controls")
    
    # Status Badge Setup
    agent_status = "🟢 Ready" if course_graph else "🔴 Error"
    st.markdown(f"**Agent Status:** {agent_status}")
    st.markdown(f"**Questions Asked:** `{st.session_state.question_count}`")
    
    st.button("🔄 New Conversation", on_click=reset_thread, use_container_width=True)
    
    # Download Chat History
    if st.session_state.chat_history:
        chat_json = json.dumps(st.session_state.chat_history, indent=2)
        st.download_button(
            label="📥 Download Chat Log",
            data=chat_json,
            file_name=f"chat_log_{st.session_state.thread_id[:6]}.json",
            mime="application/json",
            use_container_width=True
        )

    st.markdown("---")
    
    # Demo Mode
    demo_mode = st.toggle("🧪 Enable Demo/Viva Mode")
    if demo_mode:
        st.subheader("Sample Viva Questions:")
        for q in DEMO_QUESTIONS:
            if st.button(q, use_container_width=True):
                # When clicked, we temporarily store this into session state to process below
                st.session_state.trigger_query = q

    st.markdown("---")
    st.caption(f"Thread ID: {st.session_state.thread_id[:8]}")

if not course_graph:
    st.stop()
    
# Display chat history with clean bubble rendering
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Identify user input (from direct chat or Demo sidebar button)
user_query = st.chat_input("Ask a syllabus question (e.g., 'What is deadlock?'):")
if "trigger_query" in st.session_state:
    user_query = st.session_state.trigger_query
    del st.session_state.trigger_query

if user_query:
    st.session_state.question_count += 1
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.status("🧠 Agent Thinking...", state="running") as status:
            config = {"configurable": {"thread_id": st.session_state.thread_id}}
            initial_state = {"question": user_query}
            
            try:
                result = course_graph.invoke(initial_state, config=config)
                final_answer = result.get("answer", "System error: No answer returned.")
                st.markdown(final_answer)
                st.session_state.chat_history.append({"role": "assistant", "content": final_answer})
                status.update(label="Response Generated!", state="complete", expanded=False)
            except Exception as e:
                status.update(label="Error Occurred", state="error", expanded=False)
                st.error(f"Execution Error: {str(e)}")
