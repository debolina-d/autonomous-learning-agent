import streamlit as st
from src.graph import create_graph
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Learning Assistant", page_icon="🎓", layout="wide")

# Initialize session state
if "agent" not in st.session_state:
    st.session_state.agent = create_graph()
if "checkpoint_idx" not in st.session_state:
    st.session_state.checkpoint_idx = 0
if "state" not in st.session_state:
    st.session_state.state = None

TOPICS = [
    {"topic": "Backpropagation", "obj": "Goal, Chain rule, Loss function, Weight updates, Vanishing gradient."},
    {"topic": "Gradient Descent", "obj": "SGD vs Batch, Learning rate, Convergence, Local minima, Momentum."},
    {"topic": "Activation Functions", "obj": "Non-linearity, ReLU, Sigmoid, Tanh, Softmax."},
    {"topic": "CNN Architectures", "obj": "Kernels, Stride, Padding, Max pooling, Flattening."},
    {"topic": "Regularization", "obj": "Overfitting, L1/L2, Dropout, Early stopping."}
]

def safe_invoke(input_state):
    try:
        with st.spinner("Processing..."):
            return st.session_state.agent.invoke(input_state)
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return input_state

# Header
st.title("🎓 AI Learning Assistant")
st.markdown("---")

# Check completion
if st.session_state.checkpoint_idx >= len(TOPICS):
    st.success("🎉 All topics completed!")
    st.balloons()
    st.stop()

current_topic = TOPICS[st.session_state.checkpoint_idx]

# Progress
progress = st.session_state.checkpoint_idx / len(TOPICS)
st.progress(progress)
st.write(f"Progress: {st.session_state.checkpoint_idx}/{len(TOPICS)} topics")

# Topic info
st.subheader(f"📚 {current_topic['topic']}")
st.info(f"**Objectives:** {current_topic['obj']}")

# Initialize state
if st.session_state.state is None:
    initial_input = {
        "topic": current_topic['topic'],
        "objectives": current_topic['obj'],
        "gathered_context": "",
        "relevance_score": 0,
        "questions": [],
        "learner_answers": "",
        "understanding_score": 0,
        "search_retry_count": 0
    }
    st.session_state.state = safe_invoke(initial_input)

state = st.session_state.state
score = state.get("understanding_score", 0)

# Show score if available
if score > 0:
    if score >= 70:
        st.success(f"✅ Score: {score}% - Mastery Achieved!")
    else:
        st.warning(f"📊 Score: {score}% - Need improvement")

# Study material - hide when score is below 70%
if not (score > 0 and score < 70):
    with st.expander("📖 Study Material", expanded=True):
        context = state.get('gathered_context', "Loading...")
        if context and context != "Loading...":
            if "Error gathering" in context:
                st.error("Failed to load study material. Please try again.")
            else:
                st.markdown(context)
        else:
            st.info("📚 Preparing personalized study material...")

# Main flow - define is_feynman first
questions = state.get("questions", [])
raw_q = str(questions[0]) if questions else ""
is_feynman = "FEYNMAN_PHASE|" in raw_q

if is_feynman:
    # Feynman mode
    st.markdown("### 🧠 Feynman Learning Mode")
    st.info("Let's learn with simple explanations!")
    
    explanation = raw_q.replace("FEYNMAN_PHASE|", "")
    st.markdown(explanation)
    
    if st.button("🚀 Try Assessment Again"):
        state["questions"] = []
        st.session_state.state = safe_invoke(state)
        st.rerun()

elif questions and not is_feynman:
    # Assessment mode
    st.markdown("### 📝 Assessment")
    
    with st.form("quiz"):
        st.markdown(questions[0])
        
        user_input = st.text_input("Your answers (e.g., 1.A, 2.B, 3.C, 4.D, 5.A):")
        submit = st.form_submit_button("Submit")
        
        if submit and user_input:
            state["learner_answers"] = user_input
            st.session_state.state = safe_invoke(state)
            st.rerun()
    
    # Show performance analysis right after MCQs if score is below 70%
    if score > 0 and score < 70:
        st.markdown("---")
        st.error(f"📊 Score: {score}% - Below Mastery Threshold")
        
        st.markdown("#### 🔍 Performance Analysis")
        st.warning("Your score is below the 70% mastery threshold. Let's review and improve!")
        
        if state.get("learner_answers"):
            st.markdown("**Your Answers:**")
            st.code(state["learner_answers"])
        
        st.info("💡 **Feynman Learning Mode will automatically start to help you understand better.**")
        
        # Auto-trigger Feynman mode after showing performance analysis
        if st.button("🧠 Continue to Feynman Learning"):
            # Manually trigger Feynman teaching
            from src.nodes.feynman import feynman_teaching_node
            feynman_result = feynman_teaching_node(state)
            # Update state with Feynman result
            st.session_state.state.update(feynman_result)
            st.rerun()

# Success handling
if score >= 70 and not is_feynman:
    st.balloons()
    if st.button("🎯 Next Topic"):
        st.session_state.checkpoint_idx += 1
        st.session_state.state = None
        st.rerun()