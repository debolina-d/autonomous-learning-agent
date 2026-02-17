# src/nodes/gatherer.py
from ddgs import DDGS
from src.state import LearningState
from src.rag import RAGManager
from src.utils import get_llm

def gather_context_node(state: LearningState):
    print(f"--- [GATHERING] {state['topic']} ---")
    
    # 1. Search the web
    query = f"{state['topic']} machine learning deep learning tutorial explanation"
    raw_results = []
    
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=8)]
            raw_results = [r['body'] for r in results]
    except Exception as e:
        print(f"Search error: {e}")
        return {"gathered_context": "Error gathering context."}

    # 2. Use RAG to get relevant content
    rag = RAGManager(collection_name=state['topic'])
    
    # Clear previous data for this topic to ensure freshness
    rag.clear_collection()
    
    rag.add_documents(raw_results)
    
    refined_context = rag.retrieve(query=state['objectives'], n_results=3)
    
    if not refined_context:
        refined_context = "\n".join(raw_results[:2])
    
    # Limit content length for faster processing
    refined_context = refined_context[:2500]
    
    # 3. Format the content using LLM
    llm = get_llm()
    
    format_prompt = f"""
    Create a well-structured study material for the topic: {state['topic']}
    
    Learning Objectives: {state['objectives']}
    Raw Content: {refined_context[:3000]}  # Limit content length
    
    Format the content as:
    ## {state['topic']} - Study Guide
    
    ### Key Concepts
    [List main concepts clearly]
    
    ### Detailed Explanation
    [Provide clear explanations for each objective]
    
    ### Important Points
    [Highlight critical information]
    
    Keep it concise, educational, and focused on the learning objectives.
    """
    
    try:
        formatted_content = llm.invoke(format_prompt).content
        return {"gathered_context": formatted_content}
    except Exception as e:
        print(f"Formatting error: {e}")
        return {"gathered_context": refined_context}