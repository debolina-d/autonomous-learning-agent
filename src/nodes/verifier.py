"""Answer Verification Node - Grades learner responses"""
import re
from src.state import LearningState
from src.utils import get_llm

def verify_understanding_node(state: LearningState):
    """Evaluates learner answers and calculates understanding score"""
    print(f"--- [VERIFYING ANSWERS] ---")
    
    llm = get_llm()
    
    prompt = f"""
    You are a strict academic grader. 
    
    CONTEXT: {state['gathered_context']}
    MCQ QUESTIONS: {state['questions']}
    LEARNER ANSWERS: {state['learner_answers']}

    TASK:
    1. There are EXACTLY 5 questions numbered 1-5.
    2. Find the correct answer for each question based ONLY on the CONTEXT.
    3. Compare learner's answers to correct answers.
    4. Calculate score: (Correct answers / 5) * 100.
    5. Provide result in format: FINAL_PERCENTAGE: [number]
    """
    
    response = llm.invoke(prompt).content
    
    # Extract percentage from response
    try:
        match = re.search(r"FINAL_PERCENTAGE:\s*(\d+)", response)
        score = int(match.group(1)) if match else 0
    except Exception:
        score = 0
        
    return {"understanding_score": score}