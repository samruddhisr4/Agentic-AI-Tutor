# src/frontend/app.py
import streamlit as st
import requests
import json
from typing import Dict, List

# Set page configuration
st.set_page_config(page_title="Agentic AI Tutor", page_icon="🤖", layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
.main {
    background-color: #f5f5f5;
    padding: 20px;
    color: #333333;
}
.header {
    text-align: center;
    margin-bottom: 30px;
    color: #2c3e50;
}
.card {
    background-color: white;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
    color: #333333;
}
.card h3, .card h4 {
    color: #2c3e50;
    margin-top: 0;
}
.card p {
    color: #333333;
    line-height: 1.6;
}
.input-area {
    margin-bottom: 20px;
}
.button-area {
    display: flex;
    gap: 10px;
    margin-top: 10px;
}
.warning {
    background-color: #fff3cd;
    border: 1px solid #ffeaa7;
    color: #856404;
    padding: 15px;
    border-radius: 5px;
    margin: 15px 0;
}
.question-card {
    background-color: #f8f9fa;
    border-left: 4px solid #007bff;
    padding: 15px;
    margin-bottom: 15px;
    border-radius: 0 5px 5px 0;
}
.question-card h4 {
    color: #2c3e50;
    margin-top: 0;
}
.options-list {
    margin: 10px 0;
    padding-left: 20px;
}
.correct-answer {
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    color: #155724;
    padding: 10px;
    border-radius: 5px;
    margin: 10px 0;
}
.explanation {
    background-color: #e2f0ff;
    border: 1px solid #b8daff;
    color: #004085;
    padding: 10px;
    border-radius: 5px;
    margin: 10px 0;
}
.section-header {
    color: #2c3e50;
    border-bottom: 2px solid #007bff;
    padding-bottom: 10px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# Title and header
st.markdown("<h1 class='header'>🧠 Agentic AI Tutor & Quiz Generator</h1>", unsafe_allow_html=True)
st.markdown("<p class='header'>Your personal AI tutor for technical concepts and placement preparation</p>", unsafe_allow_html=True)

# Warning about new accounts
st.markdown("""
<div class="warning">
<b>Notice for New OpenAI Accounts:</b> If you're using a newly created OpenAI account, 
it may take some time (up to 24-48 hours) for your account to be fully verified and 
granted API access. This is normal and happens for security reasons.
</div>
""", unsafe_allow_html=True)

# Sidebar navigation
page = st.sidebar.radio("Choose a feature:", ["AI Tutor", "Quiz Generator"])

# AI Tutor Page
if page == "AI Tutor":
    st.markdown("<h2 class='section-header'>AI Tutor</h2>", unsafe_allow_html=True)
    
    # Input area
    user_query = st.text_area("Enter your question or topic:", height=150)
    
    # Style selection
    style = st.selectbox("Choose response style:", ["in_depth", "visual", "hands_on"])
    
    # Generate button
    if st.button("Generate Response"):
        if not user_query.strip():
            st.error("Please enter a question or topic.")
        else:
            try:
                # Show a loading message
                with st.spinner("Generating response... This may take a moment."):
                    # Make API call to backend with increased timeout
                    response = requests.post(
                        "http://localhost:8000/generate_response",
                        json={"query": user_query, "style": style},
                        timeout=60  # Increased timeout to 60 seconds
                    )
                
                if response.status_code == 200:
                    result = response.json()
                    st.markdown(f"<div class='card'><h3>AI Response:</h3><p>{result['response']}</p></div>", unsafe_allow_html=True)
                elif response.status_code == 429:
                    st.error("""
                    **Quota Limit Reached**: Your OpenAI account has exceeded its current quota.
                    
                    If you're using a new account:
                    1. Wait for account verification (can take up to 24-48 hours)
                    2. Check your billing status at https://platform.openai.com/account/billing
                    3. Ensure your payment method is verified
                    
                    If you're using an existing account:
                    1. Check your usage limits
                    2. Consider upgrading your plan
                    """)
                else:
                    st.error(f"Backend Error ({response.status_code}): {response.text}")
                    
            except requests.exceptions.Timeout:
                st.error("The request timed out. This might be due to high demand or quota limits. Please try again later.")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the backend server. Please make sure the application is running.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Quiz Generator Page
elif page == "Quiz Generator":
    st.markdown("<h2 class='section-header'>Quiz Generator</h2>", unsafe_allow_html=True)
    
    # Topic selection
    topics = ["DBMS", "OS", "CN", "AI", "ML", "DL", "System Design", "GenAI"]
    selected_topic = st.selectbox("Select a topic:", topics)
    
    # Difficulty level
    difficulties = ["Beginner", "Intermediate", "Advanced"]
    selected_difficulty = st.selectbox("Select difficulty:", difficulties)
    
    # Number of questions
    num_questions = st.slider("Number of questions:", min_value=1, max_value=10, value=5)
    
    # Generate button
    if st.button("Generate Quiz"):
        try:
            # Show a loading message
            with st.spinner("Generating quiz... This may take a moment."):
                # Make API call to backend with increased timeout
                response = requests.post(
                    "http://localhost:8000/generate_quiz",
                    json={
                        "topic": selected_topic,
                        "difficulty": selected_difficulty,
                        "num_questions": num_questions
                    },
                    timeout=60  # Increased timeout to 60 seconds
                )
            
            if response.status_code == 200:
                questions = response.json()["questions"]
                
                # Display quiz
                st.markdown(f"<div class='card'><h3>Generated Quiz ({len(questions)} questions)</h3></div>", unsafe_allow_html=True)
                
                for i, question in enumerate(questions, 1):
                    st.markdown(f"""
                    <div class='question-card'>
                        <h4>Question {i}: {question.get('question', '')}</h4>
                    """, unsafe_allow_html=True)
                    
                    if 'options' in question and question['options']:
                        st.markdown("<div class='options-list'>", unsafe_allow_html=True)
                        for j, option in enumerate(question['options'], ord('A')):
                            st.write(f"{chr(j)}. {option}")
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    if 'correct_answer' in question and question['correct_answer']:
                        st.markdown(f"<div class='correct-answer'><b>Correct Answer:</b> {question['correct_answer']}</div>", unsafe_allow_html=True)
                    
                    if 'explanation' in question and question['explanation']:
                        st.markdown(f"<div class='explanation'><b>Explanation:</b> {question['explanation']}</div>", unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
            elif response.status_code == 429:
                st.error("""
                **Quota Limit Reached**: Your OpenAI account has exceeded its current quota.
                
                If you're using a new account:
                1. Wait for account verification (can take up to 24-48 hours)
                2. Check your billing status at https://platform.openai.com/account/billing
                3. Ensure your payment method is verified
                
                If you're using an existing account:
                1. Check your usage limits
                2. Consider upgrading your plan
                """)
            else:
                st.error(f"Backend Error ({response.status_code}): {response.text}")
                
        except requests.exceptions.Timeout:
            st.error("The request timed out. This might be due to high demand or quota limits. Please try again later.")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the backend server. Please make sure the application is running.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")