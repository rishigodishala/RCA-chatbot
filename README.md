# RCA Chatbot: Problem-Solving with Root Cause Analysis

This chatbot helps users perform systematic root cause analysis (RCA) for technical problems using AI-guided methodologies like 8D, 5-Why, and A3.

## How It Works

1. **Select Methodology**: Choose from 8D (Eight Disciplines), 5-Why, or A3 problem-solving frameworks in the sidebar.

2. **Start Investigation**: Type "start" in the chat to begin the process.

3. **Provide Context**: Answer initial questions about the problem (description, timing, impact).

4. **Guided Questions**: The AI asks targeted questions based on the chosen methodology to dig deeper into root causes.

5. **Evidence Upload**: Upload images of defects, error messages, or other visual evidence to support the investigation.

6. **Progress Tracking**: Monitor investigation metrics and progress in the sidebar.

7. **Report Generation**: Generate detailed text or PDF reports summarizing findings, root causes, and recommendations.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/rishigodishala/RCA-chatbot.git
   cd RCA-chatbot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up OpenAI API key in `.env`:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Run the chatbot:
```bash
streamlit run app.py
```

Open the provided URL in your browser and start investigating problems!

## RCA Methodologies

- **8D**: Structured team-based approach for complex problems.
- **5-Why**: Iterative questioning to find root causes.
- **A3**: One-page visual problem-solving format.

## Technologies

- Python, Streamlit, LangChain, OpenAI API, RAG (Retrieval-Augmented Generation)
