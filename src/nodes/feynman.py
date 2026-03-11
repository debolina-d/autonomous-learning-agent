"""Feynman Teaching Node - Provides simplified explanations for struggling learners"""
from src.state import LearningState
from src.utils import get_llm

def feynman_teaching_node(state: LearningState):
    """Generates Feynman-style simplified explanations based on learner's mistakes"""
    print(f"--- [FEYNMAN ADAPTIVE TEACHING] ---")
    
    llm = get_llm()
    
    prompt = f"""
    The learner scored {state['understanding_score']}% (Target: 70%).
    
    CONTEXT: {state['gathered_context']}
    QUESTIONS: {state['questions']}
    LEARNER ANSWERS: {state['learner_answers']}
    TOPIC: {state['topic']}
    OBJECTIVES: {state['objectives']}
    
    Create a Feynman Technique explanation with this EXACT structure:
    
    ## 🧠 Feynman Learning: {state['topic']}
    
    ### 🎯 Step 1: Simple Explanation
    [Explain as if teaching a 12-year-old. Use simple words, avoid jargon.]
    
    ### 🔍 Step 2: Identify Knowledge Gaps
    [Based on incorrect answers, identify specific areas of confusion:]
    - Gap 1: [specific misconception]
    - Gap 2: [another area of confusion]
    
    ### 🎨 Step 3: Use Analogies & Examples
    [Provide real-world analogies:]
    - **Analogy 1:** [simple comparison]
    - **Example:** [concrete example]
    
    ### 🔄 Step 4: Simplify & Review
    [Summarize key points in simplest terms:]
    1. [Key point 1]
    2. [Key point 2]
    3. [Key point 3]
    
    ### 📝 Step 5: Test Understanding
    [Provide a simple question or scenario to check comprehension]
    
    Focus on the learning objectives: {state['objectives']}
    """
    
    response = llm.invoke(prompt).content
    
    return {
        "questions": [f"FEYNMAN_PHASE|{response}"], 
        "learner_answers": "", 
        "understanding_score": state['understanding_score']
    }