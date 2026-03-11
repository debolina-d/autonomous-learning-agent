import streamlit as st
from src.graph import create_graph
import os
from dotenv import load_dotenv
from src.utils import get_llm

load_dotenv()

st.set_page_config(page_title="AI Learning Assistant", page_icon="🎓", layout="wide")

# Check for required API key
if not os.getenv("GROQ_API_KEY"):
    st.error("⚠️ GROQ_API_KEY not found in environment variables")
    st.stop()

# Initialize session state
if "agent" not in st.session_state:
    st.session_state.agent = create_graph()
if "topic" not in st.session_state:
    st.session_state.topic = None
if "checkpoints" not in st.session_state:
    st.session_state.checkpoints = []
if "checkpoint_idx" not in st.session_state:
    st.session_state.checkpoint_idx = 0
if "state" not in st.session_state:
    st.session_state.state = None

def generate_checkpoints(topic):
    """Generate learning checkpoints using LLM"""
    llm = get_llm()
    
    prompt = f"""
    You are an expert learning path designer. Create a structured learning path for the topic: "{topic}"
    
    Generate EXACTLY 5 learning checkpoints that progressively build understanding.
    Each checkpoint should have:
    1. A clear, concise checkpoint name (2-4 words)
    2. Specific learning objectives (comma-separated, 5 key concepts)
    
    FORMAT (follow exactly):
    CHECKPOINT_1: [Name]
    OBJECTIVES_1: [Objective1, Objective2, Objective3, Objective4, Objective5]
    
    CHECKPOINT_2: [Name]
    OBJECTIVES_2: [Objective1, Objective2, Objective3, Objective4, Objective5]
    
    [Continue for all 5 checkpoints]
    
    Make checkpoints logical, progressive, and comprehensive.
    """
    
    try:
        response = llm.invoke(prompt).content
        checkpoints = []
        
        # Parse the response
        lines = response.strip().split('\n')
        current_checkpoint = {}
        
        for line in lines:
            line = line.strip()
            if line.startswith('CHECKPOINT_'):
                if current_checkpoint:
                    checkpoints.append(current_checkpoint)
                current_checkpoint = {'topic': line.split(':', 1)[1].strip()}
            elif line.startswith('OBJECTIVES_'):
                current_checkpoint['obj'] = line.split(':', 1)[1].strip()
        
        if current_checkpoint:
            checkpoints.append(current_checkpoint)
        
        # Ensure we have exactly 5 checkpoints
        if len(checkpoints) < 5:
            # Fallback to basic checkpoints
            return [
                {"topic": f"{topic} - Fundamentals", "obj": "Basic concepts, Core principles, Key terminology, Foundation, Overview"},
                {"topic": f"{topic} - Core Concepts", "obj": "Main ideas, Essential components, Key mechanisms, Structure, Function"},
                {"topic": f"{topic} - Advanced Topics", "obj": "Complex concepts, Advanced techniques, Optimization, Best practices, Edge cases"},
                {"topic": f"{topic} - Applications", "obj": "Real-world use, Practical examples, Implementation, Case studies, Problem solving"},
                {"topic": f"{topic} - Mastery", "obj": "Integration, Advanced applications, Troubleshooting, Performance, Expert level"}
            ]
        
        return checkpoints[:5]
    
    except Exception as e:
        st.error(f"Error generating checkpoints: {str(e)}")
        return []

def safe_invoke(input_state):
    try:
        with st.spinner("Processing..."):
            return st.session_state.agent.invoke(input_state)
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return input_state

# Header
st.title("🎓 AI Learning Assistant")
st.markdown("### Personalized Learning Powered by AI")
st.markdown("---")

# Topic Input Section
if st.session_state.topic is None:
    st.markdown("## 📚 Start Your Learning Journey")
    st.info("Enter any topic you want to learn, and AI will create a personalized learning path for you!")
    
    with st.form("topic_form"):
        user_topic = st.text_input(
            "What do you want to learn?",
            placeholder="e.g., Machine Learning, Python Programming, Data Structures, etc.",
            help="Enter any topic - the AI will break it down into manageable checkpoints"
        )
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submit_topic = st.form_submit_button("🚀 Generate Learning Path", use_container_width=True)
        
        if submit_topic and user_topic:
            with st.spinner("🤖 AI is creating your personalized learning path..."):
                checkpoints = generate_checkpoints(user_topic)
                
                if checkpoints:
                    st.session_state.topic = user_topic
                    st.session_state.checkpoints = checkpoints
                    st.session_state.checkpoint_idx = 0
                    st.session_state.state = None
                    st.success(f"✅ Learning path created with {len(checkpoints)} checkpoints!")
                    st.rerun()
                else:
                    st.error("Failed to generate learning path. Please try again.")
    
    st.stop()

# Learning Path Display
st.markdown(f"## 🎯 Learning: {st.session_state.topic}")

# Check completion
if st.session_state.checkpoint_idx >= len(st.session_state.checkpoints):
    st.success("🎉 Congratulations! You've completed the entire learning path!")
    st.balloons()
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Start New Topic", use_container_width=True):
            st.session_state.topic = None
            st.session_state.checkpoints = []
            st.session_state.checkpoint_idx = 0
            st.session_state.state = None
            st.rerun()
    st.stop()

# Progress tracking
progress = st.session_state.checkpoint_idx / len(st.session_state.checkpoints)
st.progress(progress)
st.caption(f"Progress: {st.session_state.checkpoint_idx}/{len(st.session_state.checkpoints)} checkpoints completed")

# Sidebar - Learning Path
with st.sidebar:
    st.markdown("### 📋 Learning Path")
    st.markdown(f"**Topic:** {st.session_state.topic}")
    st.markdown("---")
    
    for i, checkpoint in enumerate(st.session_state.checkpoints):
        if i < st.session_state.checkpoint_idx:
            st.markdown(f"✅ **{i+1}. {checkpoint['topic']}**")
        elif i == st.session_state.checkpoint_idx:
            st.markdown(f"🎯 **{i+1}. {checkpoint['topic']}** *(Current)*")
        else:
            st.markdown(f"🔒 {i+1}. {checkpoint['topic']}")
    
    st.markdown("---")
    if st.button("🔄 Change Topic"):
        st.session_state.topic = None
        st.session_state.checkpoints = []
        st.session_state.checkpoint_idx = 0
        st.session_state.state = None
        st.rerun()

current_checkpoint = st.session_state.checkpoints[st.session_state.checkpoint_idx]

# Current checkpoint info
st.markdown(f"### 📚 Checkpoint {st.session_state.checkpoint_idx + 1}: {current_checkpoint['topic']}")
st.info(f"**Learning Objectives:** {current_checkpoint['obj']}")
st.markdown("---")

# Initialize state for current checkpoint
if st.session_state.state is None:
    initial_input = {
        "topic": current_checkpoint['topic'],
        "objectives": current_checkpoint['obj'],
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

# Study material - always show first before assessment
with st.expander("📖 Study Material", expanded=True):
    context = state.get('gathered_context', "Loading...")
    if context and context != "Loading...":
        if "Error gathering" in context:
            st.error("Failed to load study material. Please try again.")
        else:
            st.markdown(context)
    else:
        st.info("📚 Preparing personalized study material...")

st.markdown("---")

# Main flow
questions = state.get("questions", [])
raw_q = str(questions[0]) if questions else ""
is_feynman = "FEYNMAN_PHASE|" in raw_q

# Show score and next actions if assessment was submitted
if score > 0 and not is_feynman:
    st.markdown("---")
    
    if score >= 70:
        # Success - proceed to next checkpoint
        st.balloons()
        st.success(f"🎉 Excellent! Score: {score}% - Checkpoint Mastered!")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🎯 Next Checkpoint", use_container_width=True):
                st.session_state.checkpoint_idx += 1
                st.session_state.state = None
                st.rerun()
    
    else:
        # Failed - show analysis and trigger Feynman
        st.error(f"📊 Score: {score}% - Below Mastery Threshold (70%)")
        
        st.markdown("#### 🔍 Performance Analysis")
        st.warning("You need more practice on this checkpoint. Let's review the concepts!")
        
        if state.get("learner_answers"):
            st.markdown("**Your Answers:**")
            st.code(state["learner_answers"])
        
        st.info("💡 **Next:** Feynman Learning Mode will provide simplified explanations to help you master this checkpoint.")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🧠 Start Feynman Learning", use_container_width=True):
                from src.nodes.feynman import feynman_teaching_node
                feynman_result = feynman_teaching_node(state)
                st.session_state.state.update(feynman_result)
                st.rerun()

elif is_feynman:
    # Feynman mode - triggered after failed assessment
    st.markdown("### 🧠 Feynman Learning Mode")
    st.error("⚠️ Score below 70% - Let's learn with simplified explanations!")
    
    explanation = raw_q.replace("FEYNMAN_PHASE|", "")
    st.markdown(explanation)
    
    st.markdown("---")
    if st.button("🚀 Retake Assessment", use_container_width=True):
        state["questions"] = []
        state["learner_answers"] = ""
        state["understanding_score"] = 0
        st.session_state.state = safe_invoke(state)
        st.rerun()

elif questions and not is_feynman and score == 0:
    # Assessment mode - only show after study material
    st.markdown("### 📝 Knowledge Assessment")
    st.info("Answer all 5 questions based on the study material above.")
    
    # Parse questions from the LLM response
    questions_text = questions[0]
    
    with st.form("quiz"):
        user_answers = []
        
        # Split questions by number pattern
        import re
        question_blocks = re.split(r'\n(?=\d+\.)', questions_text.strip())
        
        for i, block in enumerate(question_blocks[:5], 1):  # Ensure only 5 questions
            if block.strip():
                st.markdown(f"**Question {i}:**")
                
                # Extract question text and options
                lines = block.strip().split('\n')
                question_text = lines[0] if lines else ""
                
                # Display question
                st.write(question_text.replace(f"{i}.", "").strip())
                
                # Extract options (A, B, C, D)
                options = []
                for line in lines[1:]:
                    line = line.strip()
                    if line and any(line.startswith(opt) for opt in ['A)', 'B)', 'C)', 'D)']):
                        options.append(line)
                
                # Radio button for answer selection
                if options:
                    answer = st.radio(
                        f"Select your answer for Question {i}:",
                        options,
                        key=f"q{i}",
                        label_visibility="collapsed"
                    )
                    # Extract just the letter (A, B, C, or D)
                    selected_letter = answer[0] if answer else "A"
                    user_answers.append(f"{i}.{selected_letter}")
                
                st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submit = st.form_submit_button("✅ Submit Assessment", use_container_width=True)
        
        if submit:
            # Format answers as "1.A, 2.B, 3.C, 4.D, 5.E"
            formatted_answers = ", ".join(user_answers)
            state["learner_answers"] = formatted_answers
            st.session_state.state = safe_invoke(state)
            st.rerun()
