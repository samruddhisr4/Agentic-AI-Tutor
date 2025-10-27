# src/ai_engine/ai_engine_hf.py
# Alternative AI engine using Hugging Face models (no API key required)

# Try to import from the newer package first
try:
    from langchain_huggingface import HuggingFaceEndpoint
    print("Using langchain_huggingface package")
except ImportError:
    # Fall back to the older package
    try:
        from langchain_community.llms import HuggingFaceEndpoint
        print("Using langchain_community package")
    except ImportError:
        # If neither is available, we'll use a mock
        HuggingFaceEndpoint = None
        print("Neither langchain_huggingface nor langchain_community available")

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable
from langchain_core.runnables.config import RunnableConfig
from typing import Any, Optional
import os
import traceback

# Custom Mock LLM that properly implements LangChain's Runnable interface
class MockLLM(Runnable):
    def __init__(self):
        super().__init__()
    
    def invoke(self, input: Any, config: Optional[RunnableConfig] = None, **kwargs) -> str:
        # Simple mock response
        if isinstance(input, dict) and 'query' in input:
            query = input['query']
        elif isinstance(input, str):
            query = input
        else:
            query = str(input)
            
        return f"""This is a mock response for your query: "{query[:50]}..."

In a real implementation with Hugging Face:
1. You would get an AI-generated response
2. Make sure you have internet connection
3. Some models work without API tokens

For better results, you can:
1. Set HUGGINGFACEHUB_API_TOKEN in your .env file
2. Use models that don't require authentication
3. Install local models like Ollama (https://ollama.com/)"""

# Initialize LLM - try different approaches
llm = None
initialization_error = None

# Try multiple fallback approaches only if HuggingFaceEndpoint is available
if HuggingFaceEndpoint is not None:
    try:
        # Try to use HuggingFaceEndpoint with explicit provider
        llm = HuggingFaceEndpoint(
            model="google/flan-t5-base",
            task="text2text-generation",
            temperature=0.7
        )
        print("Using HuggingFace model: google/flan-t5-base")
    except Exception as e:
        print(f"Could not initialize HuggingFaceEndpoint with google/flan-t5-base: {e}")
        try:
            # Try with a different model
            llm = HuggingFaceEndpoint(
                model="declare-lab/flan-alpaca-base",
                task="text2text-generation",
                temperature=0.7
            )
            print("Using HuggingFace model: declare-lab/flan-alpaca-base")
        except Exception as e2:
            print(f"Could not initialize alternative HuggingFace model: {e2}")
            initialization_error = f"Failed to initialize HuggingFace models: {e}; {e2}"
            # Fallback to mock LLM
            llm = MockLLM()
            print("Using mock LLM - please configure properly for real AI responses")
else:
    initialization_error = "HuggingFaceEndpoint not available"
    # Fallback to mock LLM
    llm = MockLLM()
    print("HuggingFaceEndpoint not available, using mock LLM")

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
    Generate AI response based on the query and preferred style using Hugging Face models
    """
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
    
    # Create chain and run - handle case where llm might be None
    if llm is not None:
        chain = prompt | llm
        print("Invoking chain...")
        try:
            result = chain.invoke({"query": query})
            print("Chain invoked successfully")
        except Exception as e:
            error_msg = f"Error invoking HuggingFace chain: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            # Return a more user-friendly error message
            result = f"Sorry, I couldn't generate a response at the moment. This could be due to:\n1. Internet connectivity issues\n2. Model availability\n3. Rate limits\n\nError details: {str(e)[:200]}...\n\nPlease try again later."
    else:
        result = f"Error: No LLM model available. Initialization error: {initialization_error}"
    
    return result

def generate_quiz(topic: str, difficulty: str, num_questions: int) -> list[dict]:
    """
    Generate quiz questions for the given topic and difficulty using Hugging Face models
    """
    print(f"Generating quiz for topic: {topic}, difficulty: {difficulty}, questions: {num_questions}")
    
    # Create chain with quiz prompt - handle case where llm might be None
    if llm is not None:
        chain = QUIZ_PROMPT | llm
        
        # Run the chain
        print("Invoking quiz chain...")
        try:
            result = chain.invoke({"topic": topic, "difficulty": difficulty, "num_questions": num_questions})
            print("Quiz chain invoked successfully")
        except Exception as e:
            error_msg = f"Error invoking HuggingFace quiz chain: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            # Return a more user-friendly error message
            result = f"Sorry, I couldn't generate a quiz at the moment. This could be due to:\n1. Internet connectivity issues\n2. Model availability\n3. Rate limits\n\nError details: {str(e)[:200]}...\n\nPlease try again later."
    else:
        result = f"Error: No LLM model available. Initialization error: {initialization_error}"
    
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