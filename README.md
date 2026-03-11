# 🎓 AI Learning Assistant

An intelligent, autonomous learning system powered by LangGraph that provides personalized education through adaptive assessments and the Feynman teaching technique.

## 🌟 Features

- **Dynamic Topic Generation**: Enter any topic and AI generates 5 progressive learning checkpoints
- **Web-Powered Learning**: Gathers study materials from DuckDuckGo search with RAG-based semantic retrieval
- **Interactive MCQ Assessments**: 5 multiple-choice questions per checkpoint with radio button selection
- **Adaptive Learning Flow**: 70% mastery threshold determines progression
- **Feynman Teaching Mode**: Simplified explanations triggered for scores below threshold
- **Progress Tracking**: Visual sidebar showing completed, current, and locked checkpoints
- **Modern UI**: Clean Streamlit interface with intuitive navigation

## 🏗️ Architecture

### Core Components

- **LangGraph Workflow**: Orchestrates the learning pipeline with conditional routing
- **RAG System**: ChromaDB + sentence-transformers for semantic content retrieval
- **LLM Integration**: Groq API (llama-3.1-8b-instant) for content generation
- **State Management**: TypedDict-based state tracking across workflow nodes

### Workflow Nodes

1. **Gatherer**: Web search → RAG retrieval → LLM formatting
2. **Validator**: Context relevance scoring (1-5 scale)
3. **Question Generator**: Creates 5 MCQs with A/B/C/D options
4. **Verifier**: Grades answers and calculates percentage score
5. **Feynman Teacher**: Generates 5-step simplified explanations

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Groq API Key ([Get one here](https://console.groq.com/keys))

### Installation

1. Clone the repository:
```bash
git clone https://github.com/debolina-d/autonomous-learning-agent.git
cd autonomous-learning-agent
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
GROQ_API_KEY=your_groq_api_key_here
LANGCHAIN_TRACING_V2=false  # Set to true for LangSmith tracing
```

### Running the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 Usage

1. **Enter a Topic**: Type any subject you want to learn (e.g., "Machine Learning", "Python Programming")
2. **AI Generates Path**: System creates 5 progressive checkpoints with learning objectives
3. **Study Material**: Review AI-curated content from web sources
4. **Take Assessment**: Answer 5 MCQs using radio button selection
5. **Get Feedback**:
   - **Score ≥ 70%**: Proceed to next checkpoint
   - **Score < 70%**: Enter Feynman Learning Mode for simplified explanations
6. **Retake or Progress**: Retake assessment after Feynman learning or move to next checkpoint
7. **Complete Path**: Finish all 5 checkpoints to master the topic

## 🛠️ Technology Stack

- **Framework**: Streamlit
- **Orchestration**: LangGraph
- **LLM**: Groq (llama-3.1-8b-instant)
- **Vector DB**: ChromaDB
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **Search**: DuckDuckGo Search (DDGS)
- **State Management**: LangChain

## 📁 Project Structure

```
code/
├── src/
│   ├── nodes/              # LangGraph workflow nodes
│   │   ├── gatherer.py     # Context gathering with web search + RAG
│   │   ├── validator.py    # Context relevance validation
│   │   ├── question_generator.py  # MCQ generation
│   │   ├── verifier.py     # Answer grading
│   │   └── feynman.py      # Feynman teaching explanations
│   ├── graph.py            # LangGraph workflow definition
│   ├── rag.py              # RAG manager with ChromaDB
│   ├── state.py            # State schema definitions
│   └── utils.py            # LLM configuration
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── runtime.txt             # Python version specification
├── .env                    # Environment variables (not tracked)
└── .gitignore              # Git ignore rules
```

## 🔧 Configuration

### Environment Variables

- `GROQ_API_KEY`: Required - Your Groq API key
- `LANGCHAIN_TRACING_V2`: Optional - Enable LangSmith tracing (true/false)
- `LANGCHAIN_API_KEY`: Optional - LangSmith API key for tracing
- `LANGCHAIN_PROJECT`: Optional - LangSmith project name

### Customization

**Modify Mastery Threshold** (default: 70%):
```python
# In src/graph.py, update the routing condition
if state["understanding_score"] >= 70:  # Change this value
```

**Adjust Number of Questions** (default: 5):
```python
# In src/nodes/question_generator.py
# Update the prompt to generate different number of questions
```

**Change LLM Model**:
```python
# In src/utils.py
llm = ChatGroq(
    model="llama-3.1-8b-instant",  # Change model here
    temperature=0
)
```

## 🎯 Workflow Requirements

The system implements 10 core workflow requirements:

1. ✅ **Define Checkpoint**: User enters topic → AI generates 5 checkpoints
2. ✅ **Gather Context**: DuckDuckGo search (8 results) + RAG retrieval
3. ✅ **Validate Context**: Relevance scoring (1-5 scale, 4+ passes)
4. ✅ **Process Context**: LLM formats into structured study guide
5. ✅ **Generate Questions**: Creates exactly 5 MCQs with A/B/C/D options
6. ✅ **Assess Learner**: Radio button MCQ interface with submission
7. ✅ **Evaluate Score**: Calculates percentage (correct/5 * 100)
8. ✅ **Apply Feynman Teaching**: 5-step explanations for scores < 70%
9. ✅ **Mark Complete & Progress**: Tracks checkpoint completion
10. ✅ **Continue or End**: Loops until all 5 checkpoints completed

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **LangChain/LangGraph**: Workflow orchestration framework
- **Groq**: Fast LLM inference
- **ChromaDB**: Vector database for RAG
- **Streamlit**: Web application framework

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Built with ❤️ using LangGraph and Streamlit**
