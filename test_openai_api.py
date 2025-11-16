"""
Test OpenAI API connection with the new API key
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

def test_openai_connection():
    print("="*80)
    print("TESTING OPENAI API CONNECTION")
    print("="*80)
    
    # Get API key
    api_key = os.getenv("OPENAI_API_KEY")
    print(f"\n1. API Key loaded: {api_key[:20]}...{api_key[-10:]}")
    
    try:
        # Initialize LLM
        print("\n2. Initializing ChatOpenAI with OpenRouter...")
        
        # Check if it's an OpenRouter key
        if api_key.startswith("sk-or-v1-"):
            print("   Detected OpenRouter API key")
            llm = ChatOpenAI(
                temperature=0.7,
                model="openai/gpt-4o-mini",  # OpenRouter model format
                openai_api_key=api_key,
                openai_api_base="https://openrouter.ai/api/v1",
                default_headers={
                    "HTTP-Referer": "https://github.com/yourusername/rca-chatbot",
                    "X-Title": "RCA Technical Chatbot"
                }
            )
        else:
            print("   Detected standard OpenAI API key")
            llm = ChatOpenAI(
                temperature=0.7,
                model="gpt-4o-mini",
                openai_api_key=api_key
            )
        print("   ✅ LLM initialized successfully")
        
        # Test simple prompt
        print("\n3. Testing with a simple prompt...")
        test_prompt = "Say 'Hello! The API is working correctly.' in one sentence."
        
        response = llm.invoke(test_prompt)
        print(f"   ✅ API Response: {response.content}")
        
        # Test RCA-related prompt
        print("\n4. Testing with RCA-related prompt...")
        rca_prompt = """You are a technical problem-solving expert. 
        Generate one specific question to help identify the root cause of a machine failure problem.
        The question should be open-ended and focus on gathering facts."""
        
        response = llm.invoke(rca_prompt)
        print(f"   ✅ RCA Question Generated:")
        print(f"   {response.content}")
        
        print("\n" + "="*80)
        print("✅ ALL API TESTS PASSED!")
        print("="*80)
        print("\nThe OpenAI API is working correctly with your new key.")
        print("You can now use the chatbot with real AI responses!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\n" + "="*80)
        print("API TEST FAILED")
        print("="*80)
        return False

if __name__ == "__main__":
    success = test_openai_connection()
    exit(0 if success else 1)
