# src/ai_engine/ai_engine_hf_direct.py
# Direct API implementation for Hugging Face models

import requests
import json
import os
from typing import Dict, Any, List
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Hugging Face token
HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

class HuggingFaceDirect:
    """Direct API implementation for Hugging Face models"""
    
    def __init__(self, model_id: str = "google/flan-t5-base"):
        self.model_id = model_id
        self.api_url = f"https://api-inference.huggingface.co/models/{model_id}"
        self.headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}
    
    def invoke(self, input_data: Any) -> str:
        """Invoke the Hugging Face model directly via API"""
        try:
            # Handle different input formats
            if isinstance(input_data, dict) and 'query' in input_data:
                prompt_text = input_data['query']
            elif isinstance(input_data, str):
                prompt_text = input_data
            else:
                prompt_text = str(input_data)
            
            # Prepare the payload
            payload = {
                "inputs": prompt_text,
                "parameters": {
                    "temperature": 0.7,
                    "max_new_tokens": 500
                }
            }
            
            # Make the API request
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                # Extract the generated text
                if isinstance(result, list) and len(result) > 0:
                    if isinstance(result[0], dict) and 'generated_text' in result[0]:
                        return result[0]['generated_text']
                    else:
                        return str(result[0])
                else:
                    return str(result)
            elif response.status_code == 503:
                # Model is loading, get the estimated time
                error_data = response.json()
                if 'estimated_time' in error_data:
                    estimated_time = error_data['estimated_time']
                    return f"Model is currently loading. Estimated time: {estimated_time} seconds. Please try again in a moment."
                else:
                    return "Model is currently loading. Please try again in a moment."
            elif response.status_code == 404:
                # Model not found, try a different approach
                return f"Model {self.model_id} not found. This might be due to an API issue or the model being unavailable. Please try again later or switch to a different AI engine."
            else:
                raise Exception(f"Hugging Face API error: {response.status_code} - {response.text}")
                
        except Exception as e:
            raise Exception(f"Error invoking Hugging Face model: {str(e)}")

class MockLLM:
    def __init__(self):
        pass
        
    def invoke(self, input_data: Any) -> str:
        if isinstance(input_data, dict) and 'query' in input_data:
            query = input_data['query']
        elif isinstance(input_data, str):
            query = input_data
        else:
            query = str(input_data)
            
        return f"""This is a mock response for your query: "{query[:50]}..."

In a real implementation with Hugging Face:
1. You would get an AI-generated response
2. Make sure you have internet connection
3. Some models work without API tokens

For better results, you can:
1. Set HUGGINGFACEHUB_API_TOKEN in your .env file
2. Use models that don't require authentication
3. Install local models like Ollama (https://ollama.com/)"""

# Initialize the model - use a simple fallback approach
try:
    if HF_TOKEN:
        # Try a simple model first
        llm = HuggingFaceDirect("google/flan-t5-small")
        print("Using direct HuggingFace API: google/flan-t5-small")
    else:
        # Fallback to mock if no token
        llm = MockLLM()
        print("Using mock LLM - Hugging Face token not available")
        
except Exception as e:
    print(f"Error initializing HuggingFaceDirect: {e}")
    
    # Fallback to mock
    llm = MockLLM()
    print("Using mock LLM due to initialization error")

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
    
    # Format the prompt with the query
    formatted_prompt = prompt.format(query=query)
    
    # Invoke the model
    if llm is not None:
        print("Invoking direct HuggingFace API...")
        try:
            result = llm.invoke(formatted_prompt)
            print("API invoked successfully")
            return result
        except Exception as e:
            error_msg = f"Error invoking HuggingFace API: {str(e)}"
            print(error_msg)
            # Return a more user-friendly error message
            return f"Sorry, I couldn't generate a response at the moment. This could be due to:\n1. Internet connectivity issues\n2. Model availability\n3. Rate limits\n\nError details: {str(e)[:200]}...\n\nPlease try again later."
    else:
        return "Error: No LLM model available"

def generate_quiz(topic: str, difficulty: str, num_questions: int) -> list[dict]:
    """
    Generate quiz questions for the given topic and difficulty using Hugging Face models
    """
    print(f"Generating quiz for topic: {topic}, difficulty: {difficulty}, questions: {num_questions}")
    
    # Format the prompt
    formatted_prompt = QUIZ_PROMPT.format(
        topic=topic, 
        difficulty=difficulty, 
        num_questions=num_questions
    )
    
    # Invoke the model
    if llm is not None:
        print("Invoking direct HuggingFace API for quiz...")
        try:
            result = llm.invoke(formatted_prompt)
            print("Quiz API invoked successfully")
        except Exception as e:
            error_msg = f"Error invoking HuggingFace API for quiz: {str(e)}"
            print(error_msg)
            # Return a more user-friendly error message
            result = f"Sorry, I couldn't generate a quiz at the moment. This could be due to:\n1. Internet connectivity issues\n2. Model availability\n3. Rate limits\n\nError details: {str(e)[:200]}...\n\nPlease try again later."
    else:
        result = "Error: No LLM model available"
    
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