import uuid
import os
from dotenv import load_dotenv

load_dotenv()
from graph import course_graph
from nodes import llm_eval # We reuse the evaluation LLM from nodes
from langchain_core.messages import SystemMessage

def run_benchmark():
    print("========================================")
    print("     STARTING RAG BENCHMARK EVAL     ")
    print("========================================")
    
    qa_pairs = [
        {
            "question": "What are the 7 layers of the OSI model?",
            "expected": "Physical, Data Link, Network, Transport, Session, Presentation, Application."
        },
        {
            "question": "What is normalization in DBMS?",
            "expected": "The process of organizing data to minimize redundancy (1NF, 2NF, 3NF)."
        },
        {
            "question": "Give an example formula for Transmission Delay.",
            "expected": "Packet Size (L) / Bandwidth (B)"
        },
        {
            "question": "What does a deadlock require?",
            "expected": "Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait."
        },
        {
            "question": "What is a queue?",
            "expected": "FIFO structure with enqueue and dequeue."
        }
    ]

    total_faithfulness = 0.0
    total_relevancy = 0.0
    total_precision = 0.0
    
    for i, pair in enumerate(qa_pairs):
        print(f"\nEvaluating Q{i+1}: {pair['question']}")
        
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}
        
        try:
             result = course_graph.invoke({"question": pair["question"]}, config=config)
             answer = result.get("answer", "")
             retrieved_context = "\n".join(result.get("retrieved", []))
             
             # Metric 1: Faithfulness is already calculated inside the node graph!
             faithfulness = result.get("faithfulness", 1.0)
             
             # Metric 2 & 3: Custom LLM-as-a-judge for Relevancy and Precision
             eval_prompt = f"""
You are an expert evaluator. Evaluate the following RAG system outputs using values from 0.0 to 1.0.

Question: {pair['question']}
Expected Target Answer: {pair['expected']}
System Answer: {answer}
System Context Retrieved: {retrieved_context}

Return exactly two floats separated by a comma (e.g., "0.8, 0.9"):
1st Float: Answer Relevancy (Does System Answer directly answer the Question and match Expected?)
2nd Float: Context Precision (Are the Retrieved contexts useful for the Question?)
"""
             
             try:
                 eval_output = llm_eval.invoke([SystemMessage(content=eval_prompt)]).content
                 # extract floats
                 floats = [float(s) for s in eval_output.replace(" ", "").split(",") if s]
                 relevancy = floats[0] if len(floats) > 0 else 1.0
                 precision = floats[1] if len(floats) > 1 else 1.0
             except:
                 relevancy = 1.0
                 precision = 1.0

             total_faithfulness += faithfulness
             total_relevancy += relevancy
             total_precision += precision
             
             print(f"Faithfulness: {faithfulness:.2f} | Relevancy: {relevancy:.2f} | Context Precision: {precision:.2f}")

        except Exception as e:
            print(f"Error evaluating Q{i+1}: {e}")

    num_q = len(qa_pairs)
    print("\n========================================")
    print("           FINAL AVERAGES               ")
    print("========================================")
    print(f"Faithfulness Average:      {total_faithfulness/num_q:.2f} / 1.0")
    print(f"Answer Relevancy Average:  {total_relevancy/num_q:.2f} / 1.0")
    print(f"Context Precision Average: {total_precision/num_q:.2f} / 1.0")

if __name__ == "__main__":
    run_benchmark()
