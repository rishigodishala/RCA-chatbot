import streamlit as st
from chatbot import TechnicalChatbot
from report_generator import ReportGenerator
from PIL import Image
import os

st.set_page_config(
    page_title="AI-Driven Technical Problem-Solving Chatbot",
    page_icon="🔧",
    layout="wide"
)

st.title("🔧 AI-Driven Technical Problem-Solving Chatbot")
st.markdown("*Root Cause Analysis using 8D, 5-Why, and A3 Methodologies*")

# Initialize session state
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = TechnicalChatbot(workflow="8D")
    
    # Display API status warning if using MockLLM
    if st.session_state.chatbot.using_mock:
        st.warning("⚠️ **Demo Mode Active** - OpenRouter API quota exceeded. Using simulated responses for demonstration. To use real AI, please add credits to your OpenRouter account.")

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'investigation_complete' not in st.session_state:
    st.session_state.investigation_complete = False

if 'problem_context' not in st.session_state:
    st.session_state.problem_context = {}

if 'uploaded_images' not in st.session_state:
    st.session_state.uploaded_images = []

# Sidebar - RCA Workflow Selection and Settings
with st.sidebar:
    st.header("⚙️ Investigation Settings")
    
    # Workflow selector
    workflow = st.selectbox(
        "Select RCA Methodology",
        ["8D", "5-Why", "A3"],
        help="Choose the Root Cause Analysis methodology to guide your investigation"
    )
    
    if workflow != st.session_state.chatbot.workflow:
        st.session_state.chatbot.set_workflow(workflow)
        st.success(f"Workflow changed to {workflow}")
    
    st.divider()
    
    # Display investigation metrics
    if st.session_state.messages and not st.session_state.investigation_complete:
        st.header("📊 Investigation Metrics")
        metrics = st.session_state.chatbot.get_metrics()
        
        for metric, value in metrics.items():
            if metric == "Investigation Progress":
                st.progress(value / 100, text=f"{metric}: {value:.0f}%")
            else:
                st.metric(metric, f"{value:.0f}")
    
    st.divider()
    
    # Image evidence section
    st.header("📸 Evidence Images")
    uploaded_files = st.file_uploader(
        "Upload evidence images",
        type=['png', 'jpg', 'jpeg'],
        accept_multiple_files=True,
        help="Upload photos of defects, error messages, or other visual evidence"
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            if uploaded_file not in st.session_state.uploaded_images:
                st.session_state.uploaded_images.append(uploaded_file)
                # Save image temporarily
                image = Image.open(uploaded_file)
                image_path = f"evidence_{uploaded_file.name}"
                st.session_state.chatbot.add_evidence_image(image_path)
        
        st.success(f"{len(st.session_state.uploaded_images)} image(s) uploaded")
        
        # Display thumbnails
        for img_file in st.session_state.uploaded_images:
            img = Image.open(img_file)
            st.image(img, caption=img_file.name, use_column_width=True)
    
    st.divider()
    
    # Methodology info
    with st.expander("ℹ️ About RCA Methodologies"):
        st.markdown("""
        **8D (Eight Disciplines):**
        - Structured team-based problem solving
        - 8 steps from problem definition to prevention
        - Best for complex, recurring problems
        
        **5-Why:**
        - Simple iterative questioning technique
        - Asks "why" 5 times to find root cause
        - Best for straightforward problems
        
        **A3:**
        - One-page problem-solving format
        - Visual, structured approach
        - Best for continuous improvement
        """)

# Main chat interface
st.markdown("### 💬 Investigation Chat")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type 'start' to begin the investigation"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = st.session_state.chatbot.chat(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

    if "Investigation complete" in response:
        st.session_state.investigation_complete = True
        st.session_state.problem_context = st.session_state.chatbot.problem_context

# Generate report section
if st.session_state.investigation_complete:
    st.divider()
    st.header("📄 Generate RCA Report")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 Generate Text Report", use_container_width=True):
            metrics = st.session_state.chatbot.get_metrics()
            history = st.session_state.chatbot.conversation_history
            problem_context = st.session_state.problem_context
            evidence_images = st.session_state.chatbot.evidence_images
            
            report_gen = ReportGenerator(
                metrics, 
                history, 
                problem_context,
                workflow=st.session_state.chatbot.workflow,
                evidence_images=evidence_images
            )
            text_report = report_gen.generate_text_report()
            st.text_area("RCA Report", text_report, height=400)
    
    with col2:
        if st.button("📊 Generate PDF Report", use_container_width=True):
            metrics = st.session_state.chatbot.get_metrics()
            history = st.session_state.chatbot.conversation_history
            problem_context = st.session_state.problem_context
            evidence_images = st.session_state.chatbot.evidence_images
            
            report_gen = ReportGenerator(
                metrics, 
                history, 
                problem_context,
                workflow=st.session_state.chatbot.workflow,
                evidence_images=evidence_images
            )
            pdf_file = report_gen.generate_pdf_report()
            
            with open(pdf_file, "rb") as f:
                st.download_button(
                    "⬇️ Download PDF Report",
                    f,
                    file_name=f"rca_report_{st.session_state.chatbot.workflow}.pdf",
                    mime="application/pdf"
                )
    
    with col3:
        if st.button("🔄 Start New Investigation", use_container_width=True):
            st.session_state.messages = []
            st.session_state.investigation_complete = False
            st.session_state.problem_context = {}
            st.session_state.uploaded_images = []
            st.session_state.chatbot = TechnicalChatbot(workflow=workflow)
            st.rerun()

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.8em;'>
    <p>AI-Driven Technical Problem-Solving Chatbot | Root Cause Analysis (RCA) | 8D • 5-Why • A3</p>
    <p>Powered by OpenAI GPT-4 and LangChain</p>
</div>
""", unsafe_allow_html=True)
