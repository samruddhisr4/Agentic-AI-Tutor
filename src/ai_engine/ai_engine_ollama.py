# src/ai_engine/ai_engine_ollama.py
# AI engine using Ollama models

from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
import os
import time

# Get model from environment variable or use default
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "tinyllama")

# Initialize Ollama LLM with optimized parameters for faster responses
try:
    llm = Ollama(
        model=OLLAMA_MODEL,
        temperature=0.7,
        base_url="http://localhost:11434",
        # Add parameters to improve response time
        num_predict=100,
        repeat_penalty=1.2,
        top_k=30,
        top_p=0.85,
        stop=["\n\n\n"],
        # Additional parameters for optimization
        num_ctx=2048,
        num_thread=4,
    )
    print(f"Using Ollama model: {OLLAMA_MODEL} with optimized parameters")
except Exception as e:
    print(f"Could not initialize Ollama: {e}")
    # Fallback to mock LLM
    from .ai_engine_hf import MockLLM
    llm = MockLLM()
    print("Using mock LLM - please configure Ollama properly")

# Define prompt templates for different styles (optimized for faster responses)
IN_DEPTH_PROMPT = PromptTemplate(
    input_variables=["query"],
    template="""
You are an expert AI tutor. Provide a clear explanation of: {query}
Include:
1. Key concepts
2. Practical examples
3. Common applications
Keep response under 200 words.
"""
)

VISUAL_PROMPT = PromptTemplate(
    input_variables=["query"],
    template="""
You are an expert AI tutor. Explain {query} using visual analogies.
Format:
- Visual metaphor
- Key points (bullet list)
- Simple diagram description
Keep response under 200 words.
"""
)

HANDS_ON_PROMPT = PromptTemplate(
    input_variables=["query"],
    template="""
You are an expert AI tutor. Provide hands-on learning for: {query}
Include:
- Quick exercise
- Key steps
- Common mistakes
Keep response under 200 words.
"""
)

QUIZ_PROMPT = PromptTemplate(
    input_variables=["topic", "difficulty", "num_questions"],
    template="""
Create {num_questions} multiple-choice questions about {topic} at {difficulty} level.
Each question must have:
- Clear question
- 4 options (A, B, C, D)
- Correct answer
- Brief explanation
"""
)

def generate_ai_response(query: str, style: str) -> str:
    """
    Generate AI response based on the query and preferred style using Ollama models
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
    
    # Create chain and run
    if llm is not None:
        chain = prompt | llm
        print("Invoking chain...")
        try:
            # Add timeout to prevent hanging
            import asyncio
            import concurrent.futures
            from functools import partial
            
            # Run with timeout (30 seconds)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Use run_in_executor for timeout handling
            with concurrent.futures.ThreadPoolExecutor() as executor:
                start_time = time.time()
                future = executor.submit(chain.invoke, {"query": query})
                try:
                    result = future.result(timeout=30)  # 30 second timeout
                    end_time = time.time()
                    print(f"Chain invoked successfully in {end_time - start_time:.2f} seconds")
                except concurrent.futures.TimeoutError:
                    print("Ollama request timed out after 30 seconds")
                    result = "Sorry, the request timed out. The model is taking too long to respond. Please try a simpler query or try again later."
        except Exception as e:
            print(f"Error invoking Ollama chain: {e}")
            # Return a more user-friendly error message
            result = f"Sorry, I couldn't generate a response at the moment. This could be due to:\n1. Ollama service not running\n2. Model not available\n3. Connection issues\n\nPlease make sure Ollama is running and the model is available."
    else:
        result = "Error: No LLM model available"
    
    return result

def generate_quiz(topic: str, difficulty: str, num_questions: int) -> list[dict]:
    """
    Generate quiz questions for the given topic and difficulty using Ollama models
    """
    print(f"Generating quiz for topic: {topic}, difficulty: {difficulty}, questions: {num_questions}")
    
    # Create chain with quiz prompt
    if llm is not None:
        chain = QUIZ_PROMPT | llm
        
        # Run the chain
        print("Invoking quiz chain...")
        try:
            # Add timeout to prevent hanging
            import asyncio
            import concurrent.futures
            from functools import partial
            
            # Run with timeout (45 seconds for quiz generation)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Use run_in_executor for timeout handling
            with concurrent.futures.ThreadPoolExecutor() as executor:
                start_time = time.time()
                future = executor.submit(chain.invoke, {"topic": topic, "difficulty": difficulty, "num_questions": min(num_questions, 5)})  # Limit to 5 questions max
                try:
                    result = future.result(timeout=45)  # 45 second timeout
                    end_time = time.time()
                    print(f"Quiz chain invoked successfully in {end_time - start_time:.2f} seconds")
                except concurrent.futures.TimeoutError:
                    print("Ollama quiz request timed out after 45 seconds")
                    result = "Sorry, the quiz generation timed out. The model is taking too long to respond. Please try again with fewer questions."
        except Exception as e:
            print(f"Error invoking Ollama quiz chain: {e}")
            # Return a more user-friendly error message
            result = f"Sorry, I couldn't generate a quiz at the moment. This could be due to:\n1. Ollama service not running\n2. Model not available\n3. Connection issues\n\nPlease make sure Ollama is running and the model is available."
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
