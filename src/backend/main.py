# src/backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from typing import Dict, Any
import os
import sys
import traceback

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, continue with system environment variables

# Add parent directory to sys.path to resolve ai_engine module import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    style: str  # "in_depth", "visual", "hands_on"

class QuizRequest(BaseModel):
    topic: str
    difficulty: str
    num_questions: int

class QueryResponse(BaseModel):
    response: str

class QuizResponse(BaseModel):
    questions: list[Dict[str, Any]]

# Determine which AI engine to use
USE_HUGGINGFACE = os.getenv("USE_HUGGINGFACE", "false").lower() == "true"
USE_OLLAMA = os.getenv("USE_OLLAMA", "false").lower() == "true"

# Try to import the appropriate AI engine
try:
    if USE_OLLAMA:
        print("Using Ollama models")
        from ai_engine.ai_engine_ollama import generate_ai_response as ai_generate_response, generate_quiz as ai_generate_quiz
    elif USE_HUGGINGFACE:
        print("Using HuggingFace models")
        # Try the direct implementation first
        try:
            from ai_engine.ai_engine_hf_direct import generate_ai_response as ai_generate_response, generate_quiz as ai_generate_quiz
            print("Using direct HuggingFace API implementation")
        except Exception as e:
            print(f"Failed to import direct HuggingFace engine: {e}")
            # Fall back to the LangChain implementation
            from ai_engine.ai_engine_hf import generate_ai_response as ai_generate_response, generate_quiz as ai_generate_quiz
    else:
        print("Using OpenAI models")
        from ai_engine.ai_engine import generate_ai_response as ai_generate_response, generate_quiz as ai_generate_quiz
except Exception as e:
    # If we're supposed to use Ollama, but it failed to import, try HuggingFace as fallback
    if USE_OLLAMA:
        print(f"Failed to import Ollama engine: {e}")
        print("Falling back to HuggingFace models")
        try:
            from ai_engine.ai_engine_hf_direct import generate_ai_response as ai_generate_response, generate_quiz as ai_generate_quiz
            print("Using direct HuggingFace API implementation")
        except Exception as e2:
            print(f"Failed to import direct HuggingFace engine: {e2}")
            # Fall back to the LangChain implementation
            from ai_engine.ai_engine_hf import generate_ai_response as ai_generate_response, generate_quiz as ai_generate_quiz
    # If we're supposed to use HuggingFace, but it failed to import, try to fall back gracefully
    elif USE_HUGGINGFACE:
        print(f"Failed to import HuggingFace engine: {e}")
        print("Falling back to HuggingFace engine with error handling")
        # Try the direct implementation first
        try:
            from ai_engine.ai_engine_hf_direct import generate_ai_response as ai_generate_response, generate_quiz as ai_generate_quiz
            print("Using direct HuggingFace API implementation")
        except Exception as e2:
            print(f"Failed to import direct HuggingFace engine: {e2}")
            # Fall back to the LangChain implementation
            from ai_engine.ai_engine_hf import generate_ai_response as ai_generate_response, generate_quiz as ai_generate_quiz
    else:
        # If we're supposed to use OpenAI but it failed, and we're not using HuggingFace, re-raise the error
        print(f"Failed to import OpenAI engine: {e}")
        raise e

@app.post("/generate_response", response_model=QueryResponse)
async def generate_response(request: QueryRequest):
    try:
        # Log the request for debugging
        print(f"Received request: {request.query} with style {request.style}")
        
        # This will be handled by the AI engine
        result = ai_generate_response(request.query, request.style)
        
        print("Response generated successfully")
        return {"response": result}
    except Exception as e:
        # Log the full error for debugging
        error_details = f"Error in generate_response: {str(e)}\n{traceback.format_exc()}"
        print(error_details)
        raise HTTPException(status_code=500, detail=error_details)

@app.post("/generate_quiz", response_model=QuizResponse)
async def generate_quiz_endpoint(request: QuizRequest):
    try:
        # Log the request for debugging
        print(f"Received quiz request: {request.topic} ({request.difficulty}, {request.num_questions} questions)")
        
        # This will be handled by the AI engine
        result = ai_generate_quiz(request.topic, request.difficulty, request.num_questions)
        
        print(f"Quiz generated successfully with {len(result)} questions")
        return {"questions": result}
    except Exception as e:
        # Log the full error for debugging
        error_details = f"Error in generate_quiz: {str(e)}\n{traceback.format_exc()}"
        print(error_details)
        raise HTTPException(status_code=500, detail=error_details)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
