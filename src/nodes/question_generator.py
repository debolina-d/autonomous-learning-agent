from src.state import LearningState
from src.utils import get_llm

def generate_questions_node(state: LearningState):
    print(f"--- [GENERATING MCQs] {state['topic']} ---")
    
    llm = get_llm() 
    
    prompt = f"""
    Context: {state['gathered_context']}
    Create EXACTLY 5 Multiple Choice Questions (MCQs) for the topic: {state['topic']}.
    
    STRICT RULES:
    1. Generate EXACTLY 5 questions, no more, no less.
    2. Do NOT include correct answers, keys, or explanations in the generated text.
    3. Provide only the questions and options A, B, C, and D.
    4. Ensure questions assess the following objectives: {state['objectives']}
    5. Number each question clearly (1, 2, 3, 4, 5).
    
    FORMAT:
    1. [Question]
       A) [Option]
       B) [Option]
       C) [Option]
       D) [Option]
    
    2. [Question]
       A) [Option]
       B) [Option]
       C) [Option]
       D) [Option]
    
    [Continue for exactly 5 questions]
    """
    
    response = llm.invoke(prompt).content
    
    return {"questions": [response]}