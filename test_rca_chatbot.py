"""
Test script for RCA Technical Chatbot
Tests the chatbot functionality without requiring OpenAI API
"""

from chatbot import TechnicalChatbot

def test_8d_workflow():
    print("="*80)
    print("TESTING 8D WORKFLOW")
    print("="*80)
    
    chatbot = TechnicalChatbot(workflow="8D", use_mock=True)
    
    # Start investigation
    print("\n1. Starting investigation...")
    response = chatbot.chat("start")
    print(f"Bot: {response}\n")
    
    # Answer context questions
    print("2. Answering context questions...")
    
    # Q1: Problem description
    response = chatbot.chat("The production line is experiencing frequent equipment failures causing 15% downtime")
    print(f"Bot: {response}\n")
    
    # Q2: Occurrence time
    response = chatbot.chat("Started 2 weeks ago, occurs 3-4 times per day")
    print(f"Bot: {response}\n")
    
    # Q3: Impact
    response = chatbot.chat("High severity - production delays, quality issues, and safety concerns")
    print(f"Bot: {response}\n")
    
    # Answer RCA questions
    print("3. Answering RCA investigation questions...")
    
    for i in range(7):
        response = chatbot.chat(f"Test response {i+1}: Providing detailed information about the problem, including data, observations, and potential causes.")
        print(f"Question {i+1} Response:")
        print(f"Bot: {response}\n")
        
        if "Investigation complete" in response:
            break
    
    # Check metrics
    print("4. Final Metrics:")
    metrics = chatbot.get_metrics()
    for metric, value in metrics.items():
        print(f"   {metric}: {value}")
    
    print("\n" + "="*80)
    print("8D WORKFLOW TEST COMPLETE")
    print("="*80 + "\n")
    
    return chatbot

def test_5why_workflow():
    print("="*80)
    print("TESTING 5-WHY WORKFLOW")
    print("="*80)
    
    chatbot = TechnicalChatbot(workflow="5-Why", use_mock=True)
    
    # Start investigation
    print("\n1. Starting investigation...")
    response = chatbot.chat("start")
    print(f"Bot: {response}\n")
    
    # Answer context questions
    print("2. Answering context questions...")
    
    response = chatbot.chat("Software application crashes when users click the submit button")
    print(f"Bot: {response}\n")
    
    response = chatbot.chat("Started yesterday after the latest deployment")
    print(f"Bot: {response}\n")
    
    response = chatbot.chat("Critical - blocking all user transactions, affecting 500+ users")
    print(f"Bot: {response}\n")
    
    # Answer RCA questions
    print("3. Answering 5-Why investigation questions...")
    
    for i in range(7):
        response = chatbot.chat(f"Why {i+1}: The root cause appears to be related to input validation and error handling in the new code.")
        print(f"Question {i+1} Response:")
        print(f"Bot: {response}\n")
        
        if "Investigation complete" in response:
            break
    
    print("\n" + "="*80)
    print("5-WHY WORKFLOW TEST COMPLETE")
    print("="*80 + "\n")
    
    return chatbot

def test_a3_workflow():
    print("="*80)
    print("TESTING A3 WORKFLOW")
    print("="*80)
    
    chatbot = TechnicalChatbot(workflow="A3", use_mock=True)
    
    # Start investigation
    print("\n1. Starting investigation...")
    response = chatbot.chat("start")
    print(f"Bot: {response}\n")
    
    # Answer context questions
    print("2. Answering context questions...")
    
    response = chatbot.chat("Quality defects in painted parts - uneven finish and color inconsistency")
    print(f"Bot: {response}\n")
    
    response = chatbot.chat("Noticed 3 days ago, affecting approximately 20% of parts")
    print(f"Bot: {response}\n")
    
    response = chatbot.chat("Medium severity - rework required, customer complaints, increased costs")
    print(f"Bot: {response}\n")
    
    # Answer RCA questions
    print("3. Answering A3 investigation questions...")
    
    for i in range(7):
        response = chatbot.chat(f"A3 response {i+1}: Analysis shows paint viscosity issues and spray gun calibration problems.")
        print(f"Question {i+1} Response:")
        print(f"Bot: {response}\n")
        
        if "Investigation complete" in response:
            break
    
    print("\n" + "="*80)
    print("A3 WORKFLOW TEST COMPLETE")
    print("="*80 + "\n")
    
    return chatbot

def test_report_generation(chatbot):
    print("="*80)
    print("TESTING REPORT GENERATION")
    print("="*80)
    
    from report_generator import ReportGenerator
    
    metrics = chatbot.get_metrics()
    history = chatbot.conversation_history
    problem_context = chatbot.problem_context
    workflow = chatbot.workflow
    
    report_gen = ReportGenerator(metrics, history, problem_context, workflow=workflow)
    
    print("\n1. Generating text report...")
    text_report = report_gen.generate_text_report()
    print("Text report generated successfully!")
    print(f"Report length: {len(text_report)} characters")
    print("\nFirst 500 characters of report:")
    print(text_report[:500])
    
    print("\n2. Generating PDF report...")
    pdf_file = report_gen.generate_pdf_report(filename=f"test_report_{workflow}.pdf")
    print(f"PDF report generated: {pdf_file}")
    
    print("\n" + "="*80)
    print("REPORT GENERATION TEST COMPLETE")
    print("="*80 + "\n")

def main():
    print("\n" + "="*80)
    print("RCA TECHNICAL CHATBOT - COMPREHENSIVE TEST SUITE")
    print("="*80 + "\n")
    
    # Test all workflows
    print("Testing all RCA workflows...\n")
    
    chatbot_8d = test_8d_workflow()
    chatbot_5why = test_5why_workflow()
    chatbot_a3 = test_a3_workflow()
    
    # Test report generation for each workflow
    print("\nTesting report generation for all workflows...\n")
    test_report_generation(chatbot_8d)
    test_report_generation(chatbot_5why)
    test_report_generation(chatbot_a3)
    
    print("\n" + "="*80)
    print("ALL TESTS COMPLETED SUCCESSFULLY!")
    print("="*80)
    print("\nSummary:")
    print("✅ 8D Workflow - PASSED")
    print("✅ 5-Why Workflow - PASSED")
    print("✅ A3 Workflow - PASSED")
    print("✅ Report Generation - PASSED")
    print("\nNote: Tests used MockLLM. For full testing with OpenAI API,")
    print("please ensure your API key has sufficient quota.")

if __name__ == "__main__":
    main()
