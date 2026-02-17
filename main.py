import os
from src.graph import create_graph

class LearningAgentOrchestrator:
    def __init__(self):
        """
        Initializes the orchestrator with the compiled LangGraph workflow.
        The LangGraph state graph acts as the core engine for the learning stages. [cite: 48]
        """
        self.app = create_graph()

    def run_checkpoint(self, topic, objectives):
        """
        Executes the mastery-based learning cycle for a single topic. [cite: 13, 15]
        Includes gathering, assessment, verification, and adaptive simplification. [cite: 11, 12]
        """
        print(f"\n{'='*25} STARTING CHECKPOINT: {topic} {'='*25}")
        
        # Initial State following the LearningState TypedDict structure
        current_state = {
            "topic": topic,
            "objectives": objectives,
            "gathered_context": "",
            "relevance_score": 0,
            "questions": [],
            "learner_answers": "",
            "understanding_score": 0,
            "search_retry_count": 0
        }

        while True:
            # Step 1: Execute Graph (Gather -> Validate -> Generate Questions)
            # The graph pauses at END if learner_answers is empty.
            current_state = self.app.invoke(current_state)

            # Step 2: Check for Mastery Achievement (>= 70%)
            # If the score is high enough, we exit the loop and proceed to the next topic. [cite: 25]
            if current_state.get("understanding_score", 0) >= 70:
                print(f"Mastery Achieved: {current_state['understanding_score']}% ✅")
                break

            # Step 3: Present Questions or Feynman Simplification
            # If questions exist and the user hasn't answered them yet, prompt for input. [cite: 22]
            if current_state.get("questions") and not current_state.get("learner_answers"):
                print(f"\n--- [ASSESSMENT] MCQs for {topic} ---")
                print(current_state["questions"][0]) 
                
                print("\n" + "-"*30)
                user_input = input("Enter your answers (e.g., 1.A, 2.C, 3.B): ")
                print("-" * 30)

                # Update the state with answers to trigger 'verify_understanding' in next invoke. [cite: 22]
                current_state["learner_answers"] = user_input
                
            # Step 4: Logic for Failures (< 70%)
            # If a score was generated but didn't pass, the graph automatically 
            # triggers Feynman teaching and loops back to question generation. 
            elif current_state.get("understanding_score", 0) > 0:
                print(f"--- Threshold Not Met ({current_state['understanding_score']}%). Triggering Feynman Pedagogy ---")
                # Reset learner_answers to allow the loop-back re-assessment. [cite: 110]
                current_state["learner_answers"] = ""
            
            else:
                # Safety break if no questions are generated or graph halts unexpectedly
                break

        return current_state

if __name__ == "__main__":
    agent = LearningAgentOrchestrator()
    
    # Milestone 4: Sequential Learning Pathway Simulation [cite: 121, 125]
    test_set = [
        {"topic": "Backpropagation", "obj": "Goal, Chain rule, Loss function, Weight updates, Vanishing gradient."},
        {"topic": "Gradient Descent", "obj": "SGD vs Batch, Learning rate, Convergence, Local minima, Momentum."},
        {"topic": "Activation Functions", "obj": "Non-linearity, ReLU, Sigmoid, Tanh, Softmax."},
        {"topic": "CNN Architectures", "obj": "Kernels, Stride, Padding, Max pooling, Flattening."},
        {"topic": "Regularization", "obj": "Overfitting, L1/L2, Dropout, Early stopping."}
    ]

    print("\n--- AUTONOMOUS LEARNING AGENT: MASTERY MODE ---")
    
    for item in test_set:
        final_state = agent.run_checkpoint(item['topic'], item['obj'])
        
        # Progress logic: Check if more checkpoints exist. [cite: 26, 27]
        print(f"\nCheckpoint '{item['topic']}' marked as COMPLETE. Proceeding...")

    print("--- ALL CHECKPOINTS COMPLETED: LEARNING PATH FINISHED --- [cite: 28]")