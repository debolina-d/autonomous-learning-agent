from langgraph.graph import StateGraph, END
from src.state import LearningState
from src.nodes.gatherer import gather_context_node
from src.nodes.validator import validate_context_node
from src.nodes.question_generator import generate_questions_node
from src.nodes.verifier import verify_understanding_node
from src.nodes.feynman import feynman_teaching_node

def create_graph():
    workflow = StateGraph(LearningState)

   
    workflow.add_node("gather_context", gather_context_node)
    workflow.add_node("validate_context", validate_context_node)
    workflow.add_node("generate_questions", generate_questions_node)
    workflow.add_node("verify_understanding", verify_understanding_node)
    workflow.add_node("feynman_teaching", feynman_teaching_node) # Milestone 3 [cite: 101]

    workflow.set_entry_point("gather_context")
    workflow.add_edge("gather_context", "validate_context")

    def decide_path(state: LearningState):
        if state.get("learner_answers"):
            return "verify_understanding"
        if state["relevance_score"] >= 4 or state.get("search_retry_count", 0) >= 3:
            return "generate_questions"
        return "gather_context"

    workflow.add_conditional_edges("validate_context", decide_path)

    # Progression Logic
    def check_mastery(state: LearningState):
        # Feynman teaching if understanding score is below 70% and we have learner answers
        if state["understanding_score"] < 70 and state.get("learner_answers"):
            print(f"--- [UNDER-THRESHOLD] Score: {state['understanding_score']}% ---")
            return "feynman_teaching"
        return END

    workflow.add_conditional_edges("verify_understanding", check_mastery)
    
    workflow.add_edge("feynman_teaching", "generate_questions")
    
  
    workflow.add_edge("generate_questions", END)

    return workflow.compile()