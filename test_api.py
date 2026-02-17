import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

def test_groq_api():
    """Test if Groq API key is working"""
    api_key = os.getenv("GROQ_API_KEY")
    
    print(f"API Key found: {'Yes' if api_key else 'No'}")
    if api_key:
        print(f"API Key format: {'Valid' if api_key.startswith('gsk_') else 'Invalid'}")
        print(f"API Key length: {len(api_key)}")
    
    try:
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0,
            groq_api_key=api_key
        )
        
        # Test with a simple prompt
        response = llm.invoke("Say 'Hello World'")
        print(f"✅ API Test Successful: {response.content}")
        return True
        
    except Exception as e:
        print(f"❌ API Test Failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_groq_api()