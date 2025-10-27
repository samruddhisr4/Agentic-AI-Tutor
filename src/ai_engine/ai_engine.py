# src/ai_engine/ai_engine.py
from langchain_openai.llms import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from pydantic import SecretStr
import os
import traceback
import time

# Initialize OpenAI LLM with error handling
api_key = os.getenv("OPENAI_API_KEY")
llm = None
initialization_error = None

if api_key:
    try:
        llm = OpenAI(
            api_key=SecretStr(api_key),
            temperature=0.7,
            model="gpt-3.5-turbo-instruct"
        )
    except Exception as e:
        initialization_error = str(e)
        print(f"Warning: Failed to initialize OpenAI LLM: {e}")
        print("Falling back to HuggingFace models if USE_HUGGINGFACE is set")
else:
    initialization_error = "OPENAI_API_KEY environment variable is not set"
    print("OPENAI_API_KEY environment variable is not set")

# Only raise an error if we're not using HuggingFace as fallback
USE_HUGGINGFACE = os.getenv("USE_HUGGINGFACE", "false").lower() == "true"
if not USE_HUGGINGFACE and llm is None:
    raise ValueError(
        f"Failed to initialize OpenAI LLM: {initialization_error}\n\n"
        "Please either:\n"
        "1. Set your OpenAI API key as an environment variable, or\n"
        "2. Enable HuggingFace models by setting USE_HUGGINGFACE=true in your .env file\n\n"
        "To set your OpenAI API key, you can create a .env file in the project root with:\n"
        "OPENAI_API_KEY=your-api-key-here\n\n"
        "Or set it using one of these methods:\n\n"
        "On Windows (PowerShell):\n"
        "  $env:OPENAI_API_KEY='your-api-key-here'\n\n"
        "On Windows (Command Prompt):\n"
        "  set OPENAI_API_KEY=your-api-key-here\n\n"
        "On Linux/Mac:\n"
        "  export OPENAI_API_KEY='your-api-key-here'\n\n"
        "Get your API key from: https://platform.openai.com/api-keys"
    )

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

Each question should have:
- A clear, concise question statement
- Four answer options (A, B, C, D)
- One correct answer indicated
- A detailed explanation of why the correct answer is right and why others are wrong
- Relevance to placement exam patterns

Ensure the questions cover key concepts, practical applications, and real-world scenarios relevant to {topic}.
"""
)

def generate_ai_response(query: str, style: str) -> str:
    """
    Generate AI response based on the query and preferred style
    """
    # Check if we have a valid LLM
    if llm is None:
        raise Exception("OpenAI LLM is not available and HuggingFace fallback is not properly configured")
    
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
        
        # Create chain and run with retry logic
        chain = prompt | llm
        print("Invoking chain...")
        
        # Add retry logic for quota issues
        max_retries = 3
        for attempt in range(max_retries):
            try:
                result = chain.invoke({"query": query})
                print("Chain invoked successfully")
                return result
            except Exception as e:
                error_str = str(e)
                if ("insufficient_quota" in error_str or "rate limit" in error_str.lower()) and attempt < max_retries - 1:
                    print(f"Quota/rate limit issue encountered, retrying in {2 ** attempt} seconds... (attempt {attempt + 1})")
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    # If we've exhausted retries or it's a different kind of error, raise it
                    raise e
        
    except Exception as e:
        error_msg = f"Error in generate_ai_response: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        raise Exception(error_msg)

def generate_quiz(topic: str, difficulty: str, num_questions: int) -> list[dict]:
    """
    Generate quiz questions for the given topic and difficulty
    """
    # Check if we have a valid LLM
    if llm is None:
        raise Exception("OpenAI LLM is not available and HuggingFace fallback is not properly configured")
    
    try:
        print(f"Generating quiz for topic: {topic}, difficulty: {difficulty}, questions: {num_questions}")
        
        # Create chain with quiz prompt
        chain = QUIZ_PROMPT | llm
        
        # Run the chain with retry logic
        print("Invoking quiz chain...")
        
        # Add retry logic for quota issues
        max_retries = 3
        for attempt in range(max_retries):
            try:
                result = chain.invoke({"topic": topic, "difficulty": difficulty, "num_questions": num_questions})
                print("Quiz chain invoked successfully")
                break
            except Exception as e:
                error_str = str(e)
                if ("insufficient_quota" in error_str or "rate limit" in error_str.lower()) and attempt < max_retries - 1:
                    print(f"Quota/rate limit issue encountered, retrying in {2 ** attempt} seconds... (attempt {attempt + 1})")
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    # If we've exhausted retries or it's a different kind of error, raise it
                    raise e
        
        # Parse the result into structured format
        questions = []
        
        # Simple parsing logic - this would need to be more robust in production
        lines = result.split('\n')
        current_question = None
        
        for line in lines:
            if line.strip().startswith('Q') or line.strip().startswith('1.') or line.strip().startswith('2.') or line.strip().startswith('3.') or line.strip().startswith('4.') or line.strip().startswith('5.') or line.strip().startswith('6.') or line.strip().startswith('7.') or line.strip().startswith('8.') or line.strip().startswith('9.') or line.strip().startswith('10.'):
                if current_question:
                    questions.append(current_question)
                current_question = {'question': line.strip(), 'options': []}
            elif current_question and (line.strip().startswith('A:') or line.strip().startswith('B:') or line.strip().startswith('C:') or line.strip().startswith('D:')):
                current_question['options'].append(line.strip())
            elif current_question and (line.strip().startswith('Answer:') or line.strip().startswith('Correct Answer:')):
                current_question['correct_answer'] = line.strip().replace('Answer:', '').replace('Correct Answer:', '').strip()
            elif current_question and line.strip().startswith('Explanation:'):
                current_question['explanation'] = line.strip().replace('Explanation:', '').strip()
            elif current_question and (line.strip().startswith('Question:') or line.strip().startswith('Q:')):
                current_question['question'] = line.strip()
        
        if current_question:
            questions.append(current_question)
        
        print(f"Quiz generation completed with {len(questions)} questions")
        return questions
    except Exception as e:
        error_msg = f"Error in generate_quiz: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        raise Exception(error_msg)