# src/ai_engine/ai_engine_gemini.py
# AI engine using Google's Gemini models

import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from pydantic import SecretStr
import os
import traceback

# Initialize Gemini LLM with error handling
api_key = os.getenv("GOOGLE_API_KEY")
llm = None
initialization_error = None

if api_key:
    try:
        # Configure the Google Generative AI library
        genai.configure(api_key=api_key)
        
        # Initialize the LLM with LangChain wrapper
        # Convert api_key to string to avoid validation errors
        llm = ChatGoogleGenerativeAI(
            model="gemini-pro-latest",
            google_api_key=str(api_key),
            temperature=0.7
        )
        print("Successfully initialized Gemini LLM")
        
        # Warm up the model with a simple request to reduce first-request latency
        try:
            warmup_result = llm.invoke("Hello, this is a warmup request.")
            print("Model warmed up successfully")
        except Exception as warmup_error:
            print(f"Warning: Model warmup failed: {warmup_error}")
            # Continue even if warmup fails
    except Exception as e:
        initialization_error = str(e)
        print(f"Warning: Failed to initialize Gemini LLM: {e}")
else:
    initialization_error = "GOOGLE_API_KEY environment variable is not set"
    print("GOOGLE_API_KEY environment variable is not set")

# Define prompt templates for different styles
IN_DEPTH_PROMPT = PromptTemplate(
    input_variables=["query"],
    template="""
You are an expert AI tutor. Provide a comprehensive, in-depth explanation of the following topic:
{query}

Please include:
- Detailed background information
- Key concepts and principles
- Real-world applications
- Step-by-step reasoning
- Common misconceptions and clarifications
- Relevant examples and case studies
"""
)

VISUAL_PROMPT = PromptTemplate(
    input_variables=["query"],
    template="""
You are an expert AI tutor. Create a visual learning experience for the following topic:
{query}

Please provide:
- A conceptual diagram or flowchart description
- Visual metaphors and analogies
- Color-coded explanations
- Step-by-step visual breakdowns
- Suggested diagrams to draw
- How to visualize the concept mentally
"""
)

HANDS_ON_PROMPT = PromptTemplate(
    input_variables=["query"],
    template="""
You are an expert AI tutor. Create a hands-on learning experience for the following topic:
{query}

Please provide:
- Practical exercises and coding examples
- Step-by-step implementation guides
- Real-world problem-solving scenarios
- Interactive learning activities
- Debugging tips and common errors
- Practice problems with solutions
"""
)

QUIZ_PROMPT = PromptTemplate(
    input_variables=["topic", "difficulty", "num_questions"],
    template="""
Create {num_questions} multiple-choice questions about {topic} at {difficulty} level for final year computer science students preparing for placements.

Format each question EXACTLY as follows:

1. What is the primary function of an operating system?
A. To compile code
B. To manage computer hardware and software resources
C. To design websites
D. To create databases
Answer: B
Explanation: The operating system manages hardware and software resources, which is its primary function. Compiling code is done by compilers, website design by web developers, and database creation by database designers.

Follow this EXACT format for all questions:
- Number each question (1., 2., 3., etc.)
- Question on the next line
- Options A, B, C, D on separate lines starting with the letter and a period
- "Answer:" followed by the correct letter
- "Explanation:" followed by a detailed explanation

Ensure the questions cover key concepts, practical applications, and real-world scenarios relevant to {topic}.
"""
)

def generate_ai_response(query: str, style: str) -> str:
    """
    Generate AI response based on the query and preferred style using Gemini models
    """
    # Check if we have a valid LLM
    if llm is None:
        raise Exception(f"Gemini LLM is not available: {initialization_error}")
    
    try:
        print(f"Generating AI response for query: {query[:50]}... with style: {style}")
        
        # Select appropriate prompt based on style
        if style == "in_depth":
            prompt = IN_DEPTH_PROMPT
        elif style == "visual":
            prompt = VISUAL_PROMPT
        elif style == "hands_on":
            prompt = HANDS_ON_PROMPT
        else:
            prompt = IN_DEPTH_PROMPT  # default
        
        # Create chain and run
        chain = prompt | llm
        print("Invoking chain...")
        
        result = chain.invoke({"query": query})
        print("Chain invoked successfully")
        return str(result.content) if hasattr(result, 'content') else str(result)
        
    except Exception as e:
        error_msg = f"Error in generate_ai_response: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        raise Exception(error_msg)

def generate_quiz(topic: str, difficulty: str, num_questions: int) -> list[dict]:
    """
    Generate quiz questions for the given topic and difficulty using Gemini models
    """
    # Check if we have a valid LLM
    if llm is None:
        raise Exception(f"Gemini LLM is not available: {initialization_error}")
    
    try:
        print(f"Generating quiz for topic: {topic}, difficulty: {difficulty}, questions: {num_questions}")
        
        # Create chain with quiz prompt
        chain = QUIZ_PROMPT | llm
        
        # Run the chain
        print("Invoking quiz chain...")
        result = chain.invoke({"topic": topic, "difficulty": difficulty, "num_questions": num_questions})
        print("Quiz chain invoked successfully")
        
        # Parse the AI response into structured quiz questions
        content = str(result.content if hasattr(result, 'content') else result)
        
        # Try to parse the content into structured questions
        questions = _parse_quiz_response(content)
        return questions
        
    except Exception as e:
        error_msg = f"Error in generate_quiz: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        raise Exception(error_msg)

def _parse_quiz_response(content: str) -> list[dict]:
    """
    Parse the AI-generated quiz content into structured questions.
    """
    try:
        # Split content into lines
        lines = content.strip().split('\n')
        questions = []
        current_question = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for question patterns
            if (line.startswith('Q') and ':' in line) or line.startswith('Question') or (line[0].isdigit() and ('.' in line[:3] or ':' in line[:3])):
                if current_question:
                    questions.append(current_question)
                # Extract just the question text, removing the prefix
                question_text = line
                if ':' in line:
                    question_text = line.split(':', 1)[1].strip()
                elif line[0].isdigit() and ('.' in line or ':' in line):
                    question_text = line.split('.', 1)[1].strip() if '.' in line else line.split(':', 1)[1].strip()
                
                current_question = {
                    'question': question_text,
                    'options': [],
                    'correct_answer': '',
                    'explanation': ''
                }
            elif current_question and (line.startswith('A.') or line.startswith('B.') or line.startswith('C.') or line.startswith('D.') or 
                  line.startswith('(A)') or line.startswith('(B)') or line.startswith('(C)') or line.startswith('(D)') or
                  (line[0].isalpha() and line[1:3] in [').', ': '])):
                # Handle different option formats
                option_text = line
                if ':' in line:
                    option_text = line.split(':', 1)[1].strip()
                elif '.' in line and line.index('.') < 3:
                    option_text = line.split('.', 1)[1].strip()
                elif ')' in line and line.index(')') < 3:
                    option_text = line.split(')', 1)[1].strip()
                current_question['options'].append(option_text)
            elif current_question and (line.startswith('Answer:') or line.startswith('Correct Answer:') or 
                  (line.startswith('Correct:') or (line.lower().startswith('answer') and ':' in line))):
                answer_text = line
                for prefix in ['Answer:', 'Correct Answer:', 'Correct:', 'Answer']:
                    if answer_text.startswith(prefix):
                        answer_text = answer_text[len(prefix):].strip()
                        break
                current_question['correct_answer'] = answer_text
            elif current_question and (line.startswith('Explanation:') or line.startswith('Explanation') and ':' in line):
                explanation_text = line
                if ':' in line:
                    explanation_text = line.split(':', 1)[1].strip()
                current_question['explanation'] = explanation_text
        
        # Add the last question
        if current_question:
            questions.append(current_question)
            
        # If no structured questions found, try a different approach
        if not questions:
            # Try to split by double newlines for separate questions
            question_blocks = content.split('\n\n')
            for block in question_blocks:
                if block.strip():
                    # Create a simple question structure
                    questions.append({
                        'question': block.strip(),
                        'options': [],
                        'correct_answer': '',
                        'explanation': ''
                    })
            
        # If still no questions, create a sample question structure
        if not questions:
            return [{'question': 'Sample Question', 
                    'options': ['Option A', 'Option B', 'Option C', 'Option D'], 
                    'correct_answer': 'A', 
                    'explanation': 'This is a sample explanation.'}]
            
        return questions
        
    except Exception as e:
        print(f"Error parsing quiz response: {e}")
        # Return the raw content as a fallback
        return [{'question': 'Quiz Question', 'content': content}]