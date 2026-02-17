from src.state import LearningState
from src.utils import get_llm

def feynman_teaching_node(state: LearningState):
    """
    Identifies gaps and provides simplified teaching using Feynman Technique.
    """
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
    [Explain the concept as if teaching a 12-year-old child. Use simple words and avoid jargon.]
    
    ### 🔍 Step 2: Identify Knowledge Gaps
    [Based on the learner's incorrect answers, identify specific areas of confusion:]
    - Gap 1: [specific misconception]
    - Gap 2: [another area of confusion]
    
    ### 🎨 Step 3: Use Analogies & Examples
    [Provide real-world analogies to make complex concepts understandable:]
    - **Analogy 1:** [simple comparison]
    - **Example:** [concrete example]
    
    ### 🔄 Step 4: Simplify & Review
    [Summarize the key points in the simplest possible terms:]
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