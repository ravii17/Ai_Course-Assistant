from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from state import CourseState
from nodes import (
    memory_node, router_node, retrieval_node, skip_retrieval_node,
    tool_node, answer_node, eval_node, save_node
)

def should_retry(state: CourseState) -> str:
    score = state.get("faithfulness", 1.0)
    retries = state.get("eval_retries", 0)
    
    if score < 0.70 and retries < 2:
        return "retry"
    return "pass"

def route_edge(state: CourseState) -> str:
    return state.get("route", "retrieve")

def build_graph():
    print("[TRACE] Building StateGraph...")
    builder = StateGraph(CourseState)
    
    builder.add_node("memory", memory_node)
    builder.add_node("router", router_node)
    builder.add_node("retrieve", retrieval_node)
    builder.add_node("skip", skip_retrieval_node)
    builder.add_node("tool", tool_node)
    builder.add_node("answer", answer_node)
    builder.add_node("eval", eval_node)
    builder.add_node("save", save_node)
    
    builder.set_entry_point("memory")
    builder.add_edge("memory", "router")
    
    builder.add_conditional_edges("router", route_edge, {"retrieve": "retrieve", "tool": "tool", "skip": "skip"})
    
    builder.add_edge("retrieve", "answer")
    builder.add_edge("tool", "answer")
    builder.add_edge("skip", "answer")
    
    builder.add_edge("answer", "eval")
    
    builder.add_conditional_edges("eval", should_retry, {"retry": "answer", "pass": "save"})
    builder.add_edge("save", END)
    
    memory = MemorySaver()
    app_graph = builder.compile(checkpointer=memory)
    print("[TRACE] Graph compilation successful.")
    return app_graph

course_graph = build_graph()
