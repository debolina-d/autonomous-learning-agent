# 🎓 Autonomous AI Learning Agent

An intelligent, autonomous educational platform designed to generate personalized learning roadmaps on any topic. Powered by an advanced agentic workflow (LangGraph) and high-speed LLMs (Groq), the application mimics a real-world tutor. It dynamically searches the web for study materials, generates interactive assessments, grades the user, and—if the user struggles—employs the **Feynman Technique** to explain complex concepts through simple analogies.

## ✨ Core Functionalities

- **Dynamic Roadmap Generation**: Enter any topic and the AI breaks it down into 5 progressive learning checkpoints with specific learning objectives.
- **Autonomous Content Gathering (RAG)**: Dynamically searches the web, embeds text into ChromaDB, and retrieves semantically relevant paragraphs to build clean Markdown study guides.
- **Interactive Knowledge Assessment**: Dynamically generates 5 Multiple-Choice Questions (MCQs) rendered as interactive cards. The AI Teacher grades tests and calculates percentage scores.
- **Adaptive "Feynman" Learning Mode**: Enforces a 70% mastery threshold. If a user scores below 70%, the system routes to a Feynman Teacher Node that identifies wrong answers and generates simplified, analogy-driven explanations.
- **Persistent Progress Tracking**: Utilizes Local Storage to save user progress, historical scores, and active checkpoints so users can resume at any time.

## 🛠️ Technology Stack

### Backend (The Brain)
- **FastAPI**: High-performance asynchronous web server and REST API framework.
- **LangGraph & LangChain**: Orchestrates the autonomous agent workflow with conditional logic routing.
- **Groq API (`llama-3.1-8b-instant`)**: Ultra-low latency LLM inference.
- **ChromaDB & Sentence Transformers**: Vector database and embeddings (`all-MiniLM-L6-v2`) for local RAG functionality.
- **DuckDuckGo Search (DDGS)**: Real-time programmatic web searching.

### Frontend (The Interface)
- **Vanilla JavaScript (ES6)**: Handles client-side logic, API calls, and markdown parsing natively.
- **HTML5 & Custom CSS3**: Modern "Glassmorphism" design, dark-mode aesthetics, and responsive micro-animations.

## 🏗️ Architectural Workflow (The LangGraph Pipeline)

The backend operates on a state machine (`StateGraph`) that passes a `LearningState` object between specialized nodes:

1. `gather_context_node`: Searches the web, runs RAG, and writes the study guide.
2. `validate_context_node`: Scores the generated study guide out of 5. Forces retries if quality is poor.
3. `generate_questions_node`: Reads the valid study guide and writes 5 targeted MCQs.
4. `verify_understanding_node`: Grades user answers against the study guide and outputs a score and feedback.
5. `feynman_teaching_node`: Triggered conditionally if the score is < 70% to generate simplified analogies.

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
python app.py
```
The app will start on port 8002. Open your browser at `http://localhost:8002`.

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
├── static/                 # Frontend Assets
│   ├── index.html          # Main UI
│   ├── style.css           # Glassmorphism styling
│   └── app.js              # Vanilla JS logic & API integration
├── app.py                  # FastAPI Backend Server
├── requirements.txt        # Python dependencies
├── runtime.txt             # Python version specification
├── .env                    # Environment variables (not tracked)
└── .gitignore              # Git ignore rules
```

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License
This project is open source and available under the MIT License.
