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

# Only use Google Gemini models
print("Using Google Gemini models")
from ai_engine.ai_engine_gemini import generate_ai_response as ai_generate_response, generate_quiz as ai_generate_quiz

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
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)