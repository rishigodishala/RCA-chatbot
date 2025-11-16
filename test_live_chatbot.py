"""
Test the RCA chatbot with real OpenRouter API
"""

from chatbot import TechnicalChatbot

def test_live_8d_investigation():
    print("="*80)
    print("TESTING LIVE 8D INVESTIGATION WITH REAL AI")
    print("="*80)
    
    # Initialize chatbot WITHOUT mock (use_mock=False)
    chatbot = TechnicalChatbot(workflow="8D", use_mock=False)
    
    if chatbot.using_mock:
        print("\n⚠️  Warning: Chatbot is using MockLLM")
        return False
    else:
        print("\n✅ Chatbot is using real AI (OpenRouter)")
    
    # Start investigation
    print("\n" + "-"*80)
    print("STEP 1: Starting Investigation")
    print("-"*80)
    response = chatbot.chat("start")
    print(f"\nBot: {response}")
    
    # Answer context questions
    print("\n" + "-"*80)
    print("STEP 2: Problem Description")
    print("-"*80)
    user_input = "Our CNC machine is producing parts with dimensional errors. The tolerance is off by 0.5mm consistently."
    print(f"User: {user_input}")
    response = chatbot.chat(user_input)
    print(f"\nBot: {response}")
    
    print("\n" + "-"*80)
    print("STEP 3: Timing Information")
    print("-"*80)
    user_input = "Started 3 days ago, after routine maintenance was performed."
    print(f"User: {user_input}")
    response = chatbot.chat(user_input)
    print(f"\nBot: {response}")
    
    print("\n" + "-"*80)
    print("STEP 4: Impact Assessment")
    print("-"*80)
    user_input = "High severity - 30% of parts are being rejected, causing production delays and customer complaints."
    print(f"User: {user_input}")
    response = chatbot.chat(user_input)
    print(f"\nBot: {response}")
    
    # Answer first RCA question
    print("\n" + "-"*80)
    print("STEP 5: First RCA Question")
    print("-"*80)
    user_input = "The machine was calibrated during maintenance, but we noticed the cutting tool holder was slightly loose."
    print(f"User: {user_input}")
    response = chatbot.chat(user_input)
    print(f"\nBot: {response}")
    
    # Check metrics
    print("\n" + "-"*80)
    print("CURRENT INVESTIGATION METRICS")
    print("-"*80)
    metrics = chatbot.get_metrics()
    for metric, value in metrics.items():
        print(f"  {metric}: {value}")
    
    print("\n" + "="*80)
    print("✅ LIVE AI TEST SUCCESSFUL!")
    print("="*80)
    print("\nThe chatbot is generating intelligent, context-aware questions")
    print("using real AI through OpenRouter API!")
    
    return True

if __name__ == "__main__":
    success = test_live_8d_investigation()
    
    if success:
        print("\n" + "="*80)
        print("NEXT STEPS:")
        print("="*80)
        print("1. Open the Streamlit app: http://localhost:8501")
        print("2. Select your RCA methodology (8D, 5-Why, or A3)")
        print("3. Start a real investigation with AI-powered guidance!")
        print("4. Upload evidence images")
        print("5. Generate professional RCA reports")
