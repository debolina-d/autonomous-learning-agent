import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn

from src.graph import create_graph
from src.utils import get_llm

load_dotenv()

# Check for required API key
if not os.getenv("GROQ_API_KEY"):
    print("WARNING: GROQ_API_KEY not found in environment variables")

app = FastAPI(title="AI Learning Assistant API")

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Request Models
class TopicRequest(BaseModel):
    topic: str

# Helper: Generate checkpoints using LLM
def generate_checkpoints(topic: str):
    """Generate learning checkpoints using Groq LLM"""
    try:
        llm = get_llm()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM initialization failed: {str(e)}")
    
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
        print(f"Error generating checkpoints: {e}")
        # Return fallback on error
        return [
            {"topic": f"{topic} - Fundamentals", "obj": "Basic concepts, Core principles, Key terminology, Foundation, Overview"},
            {"topic": f"{topic} - Core Concepts", "obj": "Main ideas, Essential components, Key mechanisms, Structure, Function"},
            {"topic": f"{topic} - Advanced Topics", "obj": "Complex concepts, Advanced techniques, Optimization, Best practices, Edge cases"},
            {"topic": f"{topic} - Applications", "obj": "Real-world use, Practical examples, Implementation, Case studies, Problem solving"},
            {"topic": f"{topic} - Mastery", "obj": "Integration, Advanced applications, Troubleshooting, Performance, Expert level"}
        ]

# Endpoints
@app.get("/")
async def get_index():
    """Serves the main HTML5 dashboard"""
    return FileResponse("static/index.html")

@app.post("/api/checkpoints")
async def api_generate_checkpoints(request: TopicRequest):
    """Generates 5 progressive checkpoints for a topic"""
    if not request.topic:
        raise HTTPException(status_code=400, detail="Topic string cannot be empty")
    
    checkpoints = generate_checkpoints(request.topic)
    return checkpoints

@app.post("/api/invoke")
async def invoke_workflow(state: dict):
    """Invokes the compiled LangGraph workflow with state payload"""
    try:
        agent = create_graph()
        # invoke is a blocking call that runs synchronous graph execution
        result = agent.invoke(state)
        return result
    except Exception as e:
        print(f"Workflow execution error: {e}")
        raise HTTPException(status_code=500, detail=f"Workflow execution failed: {str(e)}")

# Render dynamic port binding
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8002))
    print(f"Server running on http://localhost:{port}")
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
