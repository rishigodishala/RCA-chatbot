import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from rag_engine import RAGEngine
from mcp_module import MCPModule

# Load environment variables
load_dotenv()

class TechnicalChatbot:
    def __init__(self, workflow="8D", use_mock=False):
        # Initialize LLM (supports both OpenAI and OpenRouter)
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and not use_mock:
            try:
                # Check if it's an OpenRouter key (starts with sk-or-v1-)
                if api_key.startswith("sk-or-v1-"):
                    # Configure for OpenRouter
                    self.llm = ChatOpenAI(
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
                    # Standard OpenAI configuration
                    self.llm = ChatOpenAI(temperature=0.7, model="gpt-4o-mini", openai_api_key=api_key)
                self.using_mock = False
            except Exception as e:
                print(f"Warning: Failed to initialize LLM: {e}")
                self.llm = MockLLM()
                self.using_mock = True
        else:
            self.llm = MockLLM()  # Fallback to mock if no API key
            self.using_mock = True
        
        self.rag = RAGEngine()
        self.mcp = MCPModule()
        self.conversation_history = []
        self.problem_context = {}
        self.workflow = workflow  # "8D", "5-Why", or "A3"
        self.evidence_images = []
        
        # RCA metrics instead of personality scores
        self.metrics = {
            "Problem Severity": 0,
            "Root Cause Confidence": 0,
            "Solution Feasibility": 0,
            "Investigation Progress": 0
        }
        
        self.question_count = 0
        self.max_questions = 10
        
        # Initial problem context questions
        self.context_questions = [
            "What technical problem are you investigating?",
            "When did this problem first occur? (Date/Time)",
            "What is the impact or severity of this problem? (e.g., production downtime, quality issues, safety concerns)"
        ]

    def generate_question(self):
        if self.question_count >= self.max_questions:
            return None

        if self.question_count < 3:
            # Initial problem context questions
            question = self.context_questions[self.question_count]
        else:
            # Adaptive RCA questions using LLM based on selected workflow
            workflow_query = f"{self.workflow} methodology root cause analysis questions"
            context = self.rag.retrieve(workflow_query, k=3)
            context_str = "\n".join(context)

            history_str = "\n".join([f"Q: {q}\nA: {a}" for q, a in self.conversation_history[-3:]])
            problem_str = str(self.problem_context)

            prompt = PromptTemplate(
                input_variables=["context", "history", "problem", "workflow", "metrics"],
                template="""
                You are a technical problem-solving expert guiding a Root Cause Analysis (RCA) investigation using the {workflow} methodology.
                
                RCA Methodology Context:
                {context}

                Problem Context: {problem}

                Recent Investigation History:
                {history}

                Current Metrics: {metrics}

                Based on the {workflow} methodology, generate ONE specific, probing question to help identify the root cause of this technical problem.
                The question should:
                - Be open-ended and encourage detailed responses
                - Focus on facts, data, and evidence
                - Help narrow down potential root causes
                - Follow the {workflow} framework structure
                - Avoid yes/no questions
                - Build upon previous answers

                Generate only the question, nothing else.
                Question:
                """
            )

            formatted_prompt = prompt.format(
                context=context_str,
                history=history_str,
                problem=problem_str,
                workflow=self.workflow,
                metrics=str(self.metrics)
            )
            
            if isinstance(self.llm, MockLLM):
                question = self.llm(formatted_prompt)
            else:
                response = self.llm.invoke(formatted_prompt)
                question = response.content.strip()

        self.question_count += 1
        return question

    def analyze_response(self, response):
        if self.question_count <= 3:
            # Problem context collection
            if self.question_count == 1:
                self.problem_context['problem_description'] = response
            elif self.question_count == 2:
                self.problem_context['occurrence_time'] = response
            elif self.question_count == 3:
                self.problem_context['impact_severity'] = response
            return "Problem context recorded. Let's begin the root cause investigation."

        # RCA analysis using LLM
        context = self.rag.retrieve(f"{self.workflow} root cause analysis techniques", k=3)
        context_str = "\n".join(context)

        history_str = "\n".join([f"Q: {q}\nA: {a}" for q, a in self.conversation_history[-3:]])
        problem_str = str(self.problem_context)

        prompt = PromptTemplate(
            input_variables=["context", "response", "history", "problem", "workflow"],
            template="""
            You are analyzing a response in a {workflow} Root Cause Analysis investigation.

            RCA Context:
            {context}

            Problem Context: {problem}

            User's Response: {response}

            Investigation History: {history}

            Analyze this response and provide:
            1. Key insights about potential root causes
            2. What this reveals about the problem
            3. Suggested next investigation steps
            4. Update investigation progress (0-100%)

            Provide a brief, actionable analysis focusing on root cause identification.
            Analysis:
            """
        )

        formatted_prompt = prompt.format(
            context=context_str,
            response=response,
            history=history_str,
            problem=problem_str,
            workflow=self.workflow
        )
        
        if isinstance(self.llm, MockLLM):
            analysis = self.llm(formatted_prompt)
        else:
            response_obj = self.llm.invoke(formatted_prompt)
            analysis = response_obj.content.strip()

        # Update metrics based on progress
        self.metrics["Investigation Progress"] = min(100, (self.question_count / self.max_questions) * 100)
        
        return analysis

    def chat(self, user_input):
        if user_input.lower() in ['start', 'begin']:
            self.conversation_history = []
            self.problem_context = {}
            self.metrics = {k: 0 for k in self.metrics}
            self.question_count = 0
            self.evidence_images = []
            question = self.generate_question()
            self.conversation_history.append(("System", f"{self.workflow} Investigation started"))
            return f"Welcome to the AI-Driven Technical Problem-Solving Chatbot.\n\nI'll guide you through a {self.workflow} Root Cause Analysis investigation.\n\n{question}"

        # Store response
        prev_question = self.conversation_history[-1][0] if self.conversation_history and self.conversation_history[-1][0] != "System" else "Initial"
        self.conversation_history.append((prev_question, user_input))

        analysis = self.analyze_response(user_input)

        if self.question_count >= self.max_questions:
            return f"Investigation complete.\n\n{analysis}\n\nYou can now generate a detailed RCA report with your findings."

        next_question = self.generate_question()
        return f"{analysis}\n\n{next_question}"

    def get_metrics(self):
        return self.metrics
    
    def add_evidence_image(self, image_path):
        """Add evidence image to the investigation"""
        self.evidence_images.append(image_path)
        return f"Evidence image added: {image_path}"
    
    def set_workflow(self, workflow):
        """Change RCA workflow (8D, 5-Why, A3)"""
        if workflow in ["8D", "5-Why", "A3"]:
            self.workflow = workflow
            return f"Workflow changed to {workflow}"
        return "Invalid workflow. Choose: 8D, 5-Why, or A3"

class MockLLM:
    def __init__(self):
        self.mock_question_index = 0
        self.rca_questions = [
            "Can you describe the exact symptoms or manifestations of this problem? What specifically goes wrong?",
            "What data or measurements have you collected about this problem? Are there any patterns in when it occurs?",
            "What changes were made to the system, process, or environment before this problem started occurring?",
            "Have you identified any common factors or conditions present when the problem occurs?",
            "What have you already tried to fix this problem, and what were the results?",
            "Are there any similar systems or processes that are NOT experiencing this problem? What's different about them?",
            "What evidence do you have that points to potential root causes? Can you share any error logs, measurements, or observations?"
        ]
        self.mock_analyses = [
            "Analysis: Based on your response, this appears to be a systematic issue rather than a random occurrence. The pattern suggests we should investigate process controls and monitoring systems. Next, we need to examine what changed in the system before the problem started.",
            "Analysis: The data you've provided indicates a correlation with specific operating conditions. This narrows down our investigation to environmental or operational factors. Let's explore the process parameters in more detail.",
            "Analysis: Your description reveals multiple potential contributing factors. We should use a fishbone diagram to organize these causes by category (equipment, materials, methods, people, environment). The timing suggests a recent change may be the trigger.",
            "Analysis: This evidence points toward a root cause in the maintenance or calibration procedures. The inconsistency pattern is typical of degrading equipment or inadequate preventive maintenance. We need to verify this hypothesis.",
            "Analysis: The fact that similar systems don't have this issue is a strong clue. This suggests the root cause is specific to this installation or configuration. Let's compare the differences systematically.",
            "Analysis: Your troubleshooting attempts have helped eliminate several potential causes. The persistence of the problem despite these efforts suggests we need to look deeper into systemic issues rather than surface-level symptoms.",
            "Analysis: The evidence you've gathered is valuable for root cause verification. The data supports the hypothesis that this is a process control issue. We should now focus on developing and testing corrective actions."
        ]

    def __call__(self, prompt):
        if "Question:" in prompt or "generate" in prompt.lower():
            # RCA question generation
            q = self.rca_questions[self.mock_question_index % len(self.rca_questions)]
            self.mock_question_index += 1
            return q
        elif "Analyze" in prompt or "analysis" in prompt.lower():
            # RCA analysis
            analysis = self.mock_analyses[self.mock_question_index % len(self.mock_analyses)]
            return analysis
        return "Mock RCA response"
