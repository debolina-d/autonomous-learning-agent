from src.state import LearningState
from src.utils import get_llm
import re

def validate_context_node(state: LearningState):
    print(f"--- [VALIDATING CONTEXT] ---")
    llm = get_llm()
    
    current_retries = state.get("search_retry_count", 0) + 1
    
    prompt = f"""
    Topic: {state['topic']}
    Objectives: {state['objectives']}
    Context: {state['gathered_context']}

    TASK:
    1. Check if the context covers all objectives.
    2. Provide a FINAL_SCORE from 1-5 (4+ is passing).
    """
    
    response = llm.invoke(prompt).content
    
  
    try:
        score_match = re.search(r'FINAL_SCORE:\s*(\d)', response)
        score = int(score_match.group(1)) if score_match else 1
    except:
        score = 1
        
    print(f"Context Relevance Score: {score}/5")
    return {"relevance_score": score, "search_retry_count": current_retries}