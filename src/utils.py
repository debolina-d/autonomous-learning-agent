import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

def get_llm():
    """Returns the Groq LLM instance with error handling."""
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")
    
    if not api_key.startswith("gsk_"):
        raise ValueError("Invalid GROQ_API_KEY format. Should start with 'gsk_'")
    
    try:
        return ChatGroq(
            model="llama-3.1-8b-instant",  # Updated to supported model
            temperature=0,
            groq_api_key=api_key
        )
    except Exception as e:
        raise ValueError(f"Failed to initialize Groq LLM: {str(e)}")