# src/frontend/app.py
import streamlit as st
import requests
import json
from typing import Dict, List
import os

# Set page configuration
st.set_page_config(page_title="Agentic AI Tutor", page_icon="🤖", layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
/* Modern color palette with dark mode support */
:root {
    --primary-color: #6366f1;
    --primary-hover: #4f46e5;
    --secondary-color: #8b5cf6;
    --background-dark: #0f172a;
    --card-bg: #1e293b;
    --text-primary: #f1f5f9;
    --text-secondary: #cbd5e1;
    --border-radius: 12px;
    --box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.25);
    --transition: all 0.3s ease;
}

/* Global styles */
body {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: var(--text-primary);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Main container */
.main {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

/* Header styling */
.header-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-bottom: 2.5rem;
    padding: 2rem;
    background: rgba(30, 41, 59, 0.7);
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    animation: fadeIn 0.8s ease-out;
    width: 100%;
    box-sizing: border-box;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}

.header {
    color: white;
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    background: linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.subheader {
    color: var(--text-secondary);
    font-size: 1.2rem;
    font-weight: 400;
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.6;
    text-align: center;
}

/* Sidebar styling */
.css-1d391kg {
    background: var(--card-bg);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
}

.css-1d391kg .css-1l02zno {
    padding-top: 1rem;
}

.stRadio > label {
    color: var(--text-primary);
    font-weight: 500;
    padding: 0.75rem 1rem;
    border-radius: var(--border-radius);
    margin-bottom: 0.5rem;
    transition: var(--transition);
    cursor: pointer;
}

.stRadio > label:hover {
    background: rgba(99, 102, 241, 0.15);
}

/* Remove the circular border around radio buttons */
.stRadio > div[role="radiogroup"] {
    background: transparent;
    border-radius: 0;
    padding: 0;
    border: none;
}

/* Section headers */
.section-header {
    color: white;
    font-size: 1.8rem;
    font-weight: 700;
   
}










/* Card styling */
.card {
    background: var(--card-bg);
    border-radius: var(--border-radius);
   
    box-shadow: var(--box-shadow);
    margin-bottom: 1.5rem;
    color: var(--text-primary);
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: var(--transition);
    animation: slideUp 0.5s ease-out;
}
/* Full width response styling */
.full-width-response {
    background: var(--card-bg);
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);
    margin-bottom: 1.5rem;
    color: var(--text-primary);
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: var(--transition);
    animation: slideUp 0.5s ease-out;
    width: 100%;
    box-sizing: border-box;
    padding: 1.5rem;
}
.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.35);
}

@keyframes slideUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.card h3 {
    color: white;
    margin-top: 0;
    font-size: 1.4rem;
    font-weight: 600;
}

.card p {
    color: var(--text-secondary);
    line-height: 1.7;
    font-size: 1.05rem;
}

/* Input styling */
.stTextArea textarea, .stSelectbox div, .stSlider div {
    background: rgba(15, 23, 42, 0.7);
    border: 0px solid rgba(99, 102, 241, 0.3);
    border-radius: var(--border-radius);
    color: var(--text-primary);
    transition: var(--transition);
}

.stTextArea textarea:focus, .stSelectbox div:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.3);
}

.stTextArea textarea {
    font-size: 1.1rem;
    padding: 1rem;
}

/* Remove circular border from select boxes */
.stSelectbox > div {
    
}


/* Slider styling */
.stSlider > div {
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: var(--border-radius);
    
}



/* Button styling */
.stButton button {
    background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
    color: white;
    border: none;
    border-radius: 50px;
    padding: 0.8rem 2rem;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    transition: var(--transition);
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    width: 100%;
    margin-top: 1rem;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5);
    background: linear-gradient(90deg, var(--primary-hover), #7c3aed);
}


/* Remove hover effect on slider */
.stSlider > div:hover {
    border: 1px solid rgba(99, 102, 241, 0.3) !important;
    transform: none !important;
    box-shadow: none !important;
    background: rgba(15, 23, 42, 0.7) !important;
}

/* Remove transition effect on slider */
.stSlider div {
    transition: none !important;
}

.stButton button:active {
    transform: translateY(0);
}

.stButton button:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.5);
}

/* Alert styling */
.warning, .error, .info {
    border-radius: var(--border-radius);
    padding: 1.25rem;
    margin: 1.5rem 0;
    border: none;
    font-size: 1rem;
    line-height: 1.6;
    animation: fadeIn 0.5s ease-out;
}

.warning {
    background: linear-gradient(90deg, rgba(251, 191, 36, 0.2), rgba(251, 191, 36, 0.1));
    border-left: 4px solid #fbbf24;
    color: #fde68a;
}

.error {
    background: linear-gradient(90deg, rgba(239, 68, 68, 0.2), rgba(239, 68, 68, 0.1));
    border-left: 4px solid #ef4444;
    color: #fecaca;
}

.info {
    background: linear-gradient(90deg, rgba(59, 130, 246, 0.2), rgba(59, 130, 246, 0.1));
    border-left: 4px solid #3b82f6;
    color: #bfdbfe;
}

/* Quiz question styling */
.question-card {
    background: rgba(30, 41, 59, 0.7);
    border-radius: var(--border-radius);
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    border: 1px solid rgba(99, 102, 241, 0.2);
    transition: var(--transition);
    position: relative;
    overflow: hidden;
}

.question-card:hover {
    border-color: rgba(99, 102, 241, 0.5);
    transform: translateX(5px);
}

.question-card:before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    height: 100%;
    width: 4px;
    background: linear-gradient(to bottom, var(--primary-color), var(--secondary-color));
}

.question-card h4 {
    color: white;
    margin-top: 0;
    font-size: 1.25rem;
    font-weight: 600;
    padding-left: 1rem;
}

/* Full width response styling */
.full-width-response {
    background: var(--card-bg);
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);
    margin-bottom: 1.5rem;
    color: var(--text-primary);
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: var(--transition);
    animation: slideUp 0.5s ease-out;
    width: 100%;
    box-sizing: border-box;
    padding: 1.5rem;
}

.options-list {
    margin: 1rem 0;
    padding-left: 1.5rem;
}

.options-list div {
    color: var(--text-secondary);
    margin-bottom: 0.5rem;
    padding: 0.5rem;
    border-radius: 8px;
    transition: var(--transition);
}

.options-list div:hover {
    background: rgba(99, 102, 241, 0.1);
    color: white;
}

.correct-answer {
    background: linear-gradient(90deg, rgba(16, 185, 129, 0.2), rgba(16, 185, 129, 0.1));
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #6ee7b7;
    padding: 1rem;
    border-radius: var(--border-radius);
    margin: 1rem 0;
}

.explanation {
    background: linear-gradient(90deg, rgba(59, 130, 246, 0.2), rgba(59, 130, 246, 0.1));
    border: 1px solid rgba(59, 130, 246, 0.3);
    color: #93c5fd;
    padding: 1rem;
    border-radius: var(--border-radius);
    margin: 1rem 0;
}

/* Footer styling */
.footer {
    text-align: center;
    margin-top: 3rem;
    padding: 1.5rem;
    color: var(--text-secondary);
    font-size: 0.9rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

/* Responsive design */
@media (max-width: 768px) {
    .main {
        padding: 1rem;
    }
    
    .header {
        font-size: 2rem;
    }
    
    .card {
        padding: 1rem;
    }
}

/* Spinner styling */
.stSpinner {
    text-align: center;
    color: var(--text-secondary);
}

/* Icons */
.icon {
    font-size: 1.5rem;
    margin-right: 0.5rem;
    vertical-align: middle;
}

/* Align items in columns */
.row {
    display: flex;
    flex-wrap: wrap;
    margin: 0 -1rem;
}

.column {
    flex: 1;
    padding: 0 1rem;
    min-width: 300px;
}

@media (max-width: 768px) {
    .row {
        flex-direction: column;
    }
    
    .column {
        min-width: 100%;
        margin-bottom: 1rem;
    }
}

</style>
""", unsafe_allow_html=True)

# Title and header
st.markdown("<div class='header-container'><h1 class='header'>🤖 Agentic AI Tutor </h1><p class='subheader'>Your personal AI tutor for technical concepts and placement preparation</p></div>", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown("<h2 style='color: white; margin-bottom: 1.5rem;'>🧭 Navigation</h2>", unsafe_allow_html=True)
    page = st.radio("Choose a feature:", ["AI Tutor", "Quiz Generator"], 
                    index=0, 
                    key="navigation")
    
   
       
    st.markdown("</div>", unsafe_allow_html=True)

# Backend URL - Make it configurable for different environments
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# AI Tutor Page
if page == "AI Tutor":
    st.markdown("<h2 class='section-header'>🧠 AI Tutor</h2>", unsafe_allow_html=True)
    
    # Input area
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        user_query = st.text_area("Enter your question or topic:", height=150, 
                                  placeholder="e.g., Explain the concept of polymorphism in OOP...")
        
        # Style selection
        col1, col2 = st.columns([3, 1])
        with col1:
            style = st.selectbox("Choose response style:", 
                                ["in_depth", "visual", "hands_on"],
                                format_func=lambda x: {
                                    "in_depth": "📚 In-Depth Explanation",
                                    "visual": "🎨 Visual Learning",
                                    "hands_on": "💻 Hands-On Practice"
                                }[x])
        with col2:
            st.markdown("<div style='margin-top: 1.8rem;'></div>", unsafe_allow_html=True)
            if st.button("🚀 Generate Response"):
                if not user_query.strip():
                    st.error("Please enter a question or topic.")
                else:
                    try:
                        # Show a loading message with more detailed information
                        with st.spinner("🧠 AI is thinking..."):
                            # Make API call to backend with increased timeout
                            response = requests.post(
                                f"{BACKEND_URL}/generate_response",
                                json={"query": user_query, "style": style},
                                timeout=120  # Increased timeout to 120 seconds
                            )
                        
                        if response.status_code == 200:
                            result = response.json()
                            # Store the response in session state
                            st.session_state.ai_response = result['response']
                        elif response.status_code == 429:
                            st.error("""
                            ⚠️ **Quota Limit Reached**: Your Google Gemini account has exceeded its current quota.
                            
                            **Solutions:**
                            1. Wait a few minutes and try again
                            2. Check your Google Cloud Console for quota usage
                            3. Consider upgrading your plan for higher quotas
                            """)
                        else:
                            st.error(f"❌ Backend Error ({response.status_code}): {response.text}")
                            
                    except requests.exceptions.Timeout:
                        st.error("""
                        ⏱️ **Request timed out (120 seconds exceeded)**
                        
                        This might be due to:
                        - High demand on the AI model
                        - Complex query requiring more processing time
                        - Network connectivity issues
                        
                        **Please try again with a simpler query or wait a few minutes before retrying.**
                        """)
                    except requests.exceptions.ConnectionError:
                        st.error("""
                        🔌 **Could not connect to the backend server**
                        
                        Please make sure the application is running.
                        Run 'python run_app.py' in your terminal to start the application.
                        """)
                        st.error(f"Expected backend URL: {BACKEND_URL}")
                    except Exception as e:
                        st.error(f"❌ An unexpected error occurred: {str(e)}")
                        st.info("💡 Tip: Try a shorter or simpler query for faster response times.")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Display AI response outside the container if available
    if 'ai_response' in st.session_state and st.session_state.ai_response:
        st.markdown(f"<div class='full-width-response'><h3>🤖 AI Response:</h3><p>{st.session_state.ai_response}</p></div>", unsafe_allow_html=True)
        # Clear the response after displaying it
        st.session_state.ai_response = None
        st.markdown("</div>", unsafe_allow_html=True)

# Quiz Generator Page
elif page == "Quiz Generator":
    st.markdown("<h2 class='section-header'>📝 Quiz Generator</h2>", unsafe_allow_html=True)
    
    # Topic selection
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        topics = ["DBMS", "OS", "CN", "AI", "ML", "DL", "System Design", "GenAI"]
        selected_topic = st.selectbox("Select a topic:", topics)
        
        # Difficulty level
        difficulties = ["Beginner", "Intermediate", "Advanced"]
        selected_difficulty = st.selectbox("Select difficulty:", difficulties)
        
        # Number of questions
        num_questions = st.slider("Number of questions:", min_value=1, max_value=10, value=5)
        
        # Generate button
        if st.button("🎯 Generate Quiz"):
            try:
                # Show a loading message with more detailed information
                with st.spinner("🧠 Generating quiz questions..."):
                    # Make API call to backend with increased timeout
                    response = requests.post(
                        f"{BACKEND_URL}/generate_quiz",
                        json={
                            "topic": selected_topic,
                            "difficulty": selected_difficulty,
                            "num_questions": num_questions
                        },
                        timeout=120  # Increased timeout to 120 seconds
                    )
                
                if response.status_code == 200:
                    questions = response.json()["questions"]
                    
                    # Display quiz
                    st.markdown(f"<div class='card'><h3>📋 Generated Quiz ({len(questions)} questions)</h3></div>", unsafe_allow_html=True)
                    
                    for i, question in enumerate(questions, 1):
                        st.markdown(f"""
                        <div class='question-card'>
                            <h4>❓ Question {i}: {question.get('question', '')}</h4>
                        """, unsafe_allow_html=True)
                        
                        if 'options' in question and question['options']:
                            st.markdown("<div class='options-list'>", unsafe_allow_html=True)
                            for j, option in enumerate(question['options'], ord('A')):
                                st.write(f"**{chr(j)}.** {option}")
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        if 'correct_answer' in question and question['correct_answer']:
                            st.markdown(f"<div class='correct-answer'><b>✅ Correct Answer:</b> {question['correct_answer']}</div>", unsafe_allow_html=True)
                        
                        if 'explanation' in question and question['explanation']:
                            st.markdown(f"<div class='explanation'><b>📘 Explanation:</b> {question['explanation']}</div>", unsafe_allow_html=True)
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                elif response.status_code == 429:
                    st.error("""
                    ⚠️ **Quota Limit Reached**: Your Google Gemini account has exceeded its current quota.
                    
                    **Solutions:**
                    1. Wait a few minutes and try again
                    2. Check your Google Cloud Console for quota usage
                    3. Consider upgrading your plan for higher quotas
                    """)
                else:
                    st.error(f"❌ Backend Error ({response.status_code}): {response.text}")
                    
            except requests.exceptions.Timeout:
                st.error("""
                ⏱️ **Request timed out (120 seconds exceeded)**
                
                This might be due to:
                - High demand on the AI model
                - Complex quiz generation requiring more processing time
                - Network connectivity issues
                
                **Please try again with fewer questions or wait a few minutes before retrying.**
                """)
            except requests.exceptions.ConnectionError:
                st.error("""
                🔌 **Could not connect to the backend server**
                
                Please make sure the application is running.
                Run 'python run_app.py' in your terminal to start the application.
                """)
                st.error(f"Expected backend URL: {BACKEND_URL}")
            except Exception as e:
                st.error(f"❌ An unexpected error occurred: {str(e)}")
                st.info("💡 Tip: Try generating fewer questions for faster response times.")
        st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<div class='footer'>🤖 Agentic AI Tutor | Powered by Google Gemini | v1.0</div>", unsafe_allow_html=True)