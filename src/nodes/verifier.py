import re
from src.state import LearningState
from src.utils import get_llm

def verify_understanding_node(state: LearningState):
    """
    Evaluates learner's answers against the context to calculate 
    a quantitative understanding score.
    """
    print(f"--- [VERIFYING ANSWERS] ---")
    llm = get_llm()
    
    # Grading Prompt for MCQs answered by the user
    prompt = f"""
    You are a strict academic grader. 
    
    CONTEXT: {state['gathered_context']}
    MCQ QUESTIONS: {state['questions']}
    LEARNER ANSWERS: {state['learner_answers']}

    TASK:
    1. There are EXACTLY 5 questions numbered 1-5.
    2. For each question, find the correct answer based ONLY on the provided CONTEXT.
    3. Compare the Learner's choice to the correct answer.
    4. Calculate score: (Number of correct answers / 5) * 100.
    5. Provide the result in the format below.

    FORMAT:
    FINAL_PERCENTAGE: [number]
    """
    
    response = llm.invoke(prompt).content
    
    try:
        match = re.search(r"FINAL_PERCENTAGE:\s*(\d+)", response)
        score = int(match.group(1)) if match else 0
    except Exception:
        score = 0
        
    return {"understanding_score": score}