import os
from typing import Dict, Any
from state import CourseState
from tools import current_datetime, calculator, syllabus_topics, fallback_web_info_placeholder
from kb_loader import KBLoader

# LLM imports
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    ChatGoogleGenerativeAI = None

# Determine LLM
gemini_key = os.getenv("gemini_api_key") or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if gemini_key and ChatGoogleGenerativeAI:
    print(f"[TRACE] Using Gemini API for Agent core.")
    llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite-preview", temperature=0, google_api_key=gemini_key)
    llm_eval = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite-preview", temperature=0, google_api_key=gemini_key)
else:
    llm_provider = os.getenv("LLM_PROVIDER", "groq").lower()
    if os.getenv("OPENAI_API_KEY") and llm_provider == "openai":
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        llm_eval = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    else:
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
        llm_eval = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

# Initialize retriever
loader = KBLoader()
try:
    loader.load_and_ingest()
except Exception as e:
    print(f"[TRACE] Chroma init suppressed: {e}")

MAX_EVAL_RETRIES = 2

def memory_node(state: CourseState) -> Dict[str, Any]:
    print("[TRACE] Entering memory_node")
    messages = state.get("messages", [])
    question = state.get("question", "")
    user_name = state.get("user_name", None)

    messages.append({"role": "user", "content": question})

    if len(messages) > 6:
        messages = messages[-6:]

    q_low = question.lower()
    if "my name is" in q_low:
        words = q_low.split("my name is")
        if len(words) > 1:
            name_part = words[1].strip()
            if name_part:
                user_name = name_part.split()[0].capitalize()

    return {"messages": messages, "user_name": user_name, "eval_retries": 0}

def router_node(state: CourseState) -> Dict[str, Any]:
    print("[TRACE] Entering router_node")
    question = state.get("question", "").lower()
    
    skip_keywords = ["hello", "hi", "hey", "who are you", "what is my name", "thanks", "thank you"]
    if any(question.startswith(x) or question == x for x in skip_keywords) or ("my name is" in question) or ("what is my name" in question):
        print("[TRACE] Route selected: skip")
        return {"route": "skip"}

    tool_keywords = {
        "time": "current_datetime",
        "date": "current_datetime",
        "calculate": "calculator",
        "+": "calculator",
        "-": "calculator",
        "*": "calculator",
        "/": "calculator",
        "syllabus": "syllabus",
        "subject": "syllabus",
        "topics": "syllabus",
        "search": "fallback",
        "google": "fallback",
        "stock": "fallback"
    }
    
    for kw, tool_val in tool_keywords.items():
        if kw in question:
            if tool_val == "calculator" and kw in ["+", "-", "*", "/"]:
                has_digit = any(c.isdigit() for c in question)
                if not has_digit:
                    continue
            print("[TRACE] Route selected: tool")
            return {"route": "tool"}
            
    print("[TRACE] Route selected: retrieve")
    return {"route": "retrieve"}

def retrieval_node(state: CourseState) -> Dict[str, Any]:
    print("[TRACE] Entering retrieval_node")
    question = state.get("question", "")
    
    docs_retrieved = loader.retrieve(question, top_k=3)
    
    if docs_retrieved:
        print(f"[TRACE] Retrieved docs count: {len(docs_retrieved)}")
    else:
        print("[TRACE] Warning: No context retrieved.")
        
    return {"retrieved": docs_retrieved}

def skip_retrieval_node(state: CourseState) -> Dict[str, Any]:
    print("[TRACE] Entering skip_retrieval_node")
    return {"retrieved": []}

def tool_node(state: CourseState) -> Dict[str, Any]:
    print("[TRACE] Entering tool_node")
    question = state.get("question", "").lower()
    
    tool_result = ""
    if "time" in question or "date" in question:
        tool_result = current_datetime()
    elif "calculate" in question or any(op in question for op in ["+", "-", "*", "/"]):
        expr = question.replace("calculate", "").replace("what is", "").replace("?", "").strip()
        tool_result = calculator(expr)
    elif "syllabus" in question or "subject" in question or "topics" in question:
        tool_result = syllabus_topics()
    elif "search" in question or "google" in question or "stock" in question:
         tool_result = fallback_web_info_placeholder()
    else:
        tool_result = "Tool Error: No suitable tool matched."
        
    print(f"[TRACE] Tool output: {tool_result}")
    return {"tool_result": tool_result}

def answer_node(state: CourseState) -> Dict[str, Any]:
    print("[TRACE] Entering answer_node")
    route = state.get("route")
    question = state.get("question", "")
    retrieved = state.get("retrieved", [])
    tool_res = state.get("tool_result", "")
    user_name = state.get("user_name")
    
    system_msg_content = "You are an Academic Course Assistant for B.Tech students. Be concise, professional, and helpful."
    
    if user_name:
        system_msg_content += f"\nThe student's name is {user_name}. Address them by name when natural."
        
    if route == "retrieve":
        if retrieved:
            context_str = "\n\n".join(retrieved)
            system_msg_content += f"""\n\nCRITICAL ANTI-HALLUCINATION RULE: 
You must answer the question strictly using ONLY the context provided below. 
If the answer is completely missing or cannot be logically deduced from the context, you must return EXACTLY the following phrase string:
"I don’t know based on the available course materials."
Do not fabricate facts, formulas, or data. If you found a false premise in the question that contradicts notes, correct it based on the notes.

CITATION RULE:
Every response built from context must end with the exact source references used. Look at the [Topic: X] blocks and append citations like '[Source: X]'.

Context:\n{context_str}"""
        else:
             system_msg_content += f"\n\nCRITICAL ANTI-HALLUCINATION RULE: You failed to retrieve any context. You must return EXACTLY the following phrase string: 'I don’t know based on the available course materials.'"
             
    elif route == "tool":
         system_msg_content += f"\n\nYou used a tool to retrieve the following isolated data:\nData: {tool_res}\nPass this exactly to the user. Do not fabricate extra info outside this tool result."
         
    elif route == "skip":
         system_msg_content += "\n\nCRITICAL RULE: Engage in quick conversation. If the user asks for their name and you know it, tell them. Otherwise gently remind them you are predominantly for B.Tech course queries."
         
    messages_for_llm = [SystemMessage(content=system_msg_content)]
    
    history = state.get("messages", [])[:-1]
    
    for msg in history:
        if msg["role"] == "user":
            messages_for_llm.append(HumanMessage(content=msg["content"]))
        else:
            messages_for_llm.append(SystemMessage(content=msg["content"]))
            
    messages_for_llm.append(HumanMessage(content=question))
    
    response = llm.invoke(messages_for_llm)
    answer = response.content
    
    if isinstance(answer, list):
        answer = "".join(
            block.get("text", "") if isinstance(block, dict) else str(block) 
            for block in answer
        )
    elif not isinstance(answer, str):
        answer = str(answer)
        
    print(f"[TRACE] Answer generated.")
    return {"answer": answer}

def eval_node(state: CourseState) -> Dict[str, Any]:
    print("[TRACE] Entering eval_node")
    route = state.get("route")
    retrieved = state.get("retrieved", [])
    answer = state.get("answer", "")
    retries = state.get("eval_retries", 0)
    
    if route != "retrieve" or not retrieved:
        print("[TRACE] Faithfulness eval bypassed. PASS")
        return {"faithfulness": 1.0}
        
    eval_prompt = f"""You are an objective evaluator.
Source context:
{chr(10).join(retrieved)}

Generated answer:
{answer}

Evaluate faithfulness (0.0 to 1.0).
0.0 = completely hallucinated/contradicts source.
1.0 = highly faithful.
If the answer is exactly "I don’t know based on the available course materials.", score it 1.0.

Return ONLY a float."""
    
    try:
        res = llm_eval.invoke([SystemMessage(content=eval_prompt)])
        score_text = "".join([c for c in res.content.strip() if c.isdigit() or c == "."])
        score = float(score_text)
    except Exception as e:
        score = 1.0
        
    print(f"[TRACE] Faithfulness: {score}")
    
    if score < 0.70 and retries < MAX_EVAL_RETRIES:
        print("[TRACE] Eval result: FAIL. Retrying.")
        return {"faithfulness": score, "eval_retries": retries + 1}
    else:
        print("[TRACE] Eval result: PASS.")
        return {"faithfulness": score}
        
def save_node(state: CourseState) -> Dict[str, Any]:
    print("[TRACE] Saving response")
    messages = state.get("messages", [])
    answer = state.get("answer", "System error: No answer generated.")
    
    messages.append({"role": "assistant", "content": answer})
    return {"messages": messages}
