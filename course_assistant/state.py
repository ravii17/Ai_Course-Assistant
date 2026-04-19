from typing import TypedDict, List, Dict, Any, Optional

class CourseState(TypedDict):
    """
    State representing the context of a conversation in the Course Assistant agent.
    
    Fields:
    - question: The user's current question
    - messages: Thread history, including the current question and past context
    - route: Result of the router ("retrieve", "tool", "skip")
    - retrieved: List of context fragments retrieved from ChromaDB
    - sources: Source metadata/links for the retrieved context
    - tool_result: Result string from a successfully executed tool
    - answer: The generated response from the LLM
    - faithfulness: Float score between 0.0 and 1.0 evaluating hallucination
    - eval_retries: Counter to track loop breaking
    - user_name: Attempted memory extraction mechanism for personalization
    - thread_id: Used by LangGraph memory checkpointing
    """
    question: str
    messages: List[Dict[str, Any]]
    route: str
    retrieved: List[str]
    sources: List[str]
    tool_result: str
    answer: str
    faithfulness: float
    eval_retries: int
    user_name: Optional[str]
    thread_id: str
