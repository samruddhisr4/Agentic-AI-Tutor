# run_app.py
import subprocess
import sys
import os
import time
from dotenv import load_dotenv

def run_backend():
    """Run the FastAPI backend server"""
    try:
        # Change to the src/backend directory
        backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "backend")
        
        # Copy current environment to ensure all variables are passed through
        env = os.environ.copy()
        
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "main:app", "--reload", "--port", "8000"
        ], cwd=backend_dir, env=env)
        return process
    except Exception as e:
        print(f"Error starting backend: {e}")
        return None

def run_frontend():
    """Run the Streamlit frontend"""
    try:
        # Change to the src/frontend directory
        frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "frontend")
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "app.py"
        ], cwd=frontend_dir)
        return process
    except Exception as e:
        print(f"Error starting frontend: {e}")
        return None

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    
    # Check if we're using Hugging Face models
    use_huggingface = os.getenv("USE_HUGGINGFACE", "false").lower() == "true"
    
    # Only require OPENAI_API_KEY if we're not using Hugging Face
    if not use_huggingface and "OPENAI_API_KEY" not in os.environ:
        print("=" * 60)
        print("OPENAI_API_KEY is not set in your environment variables")
        print("=" * 60)
        print("You have two options:")
        print("1. Set your OpenAI API key in a .env file:")
        print("   OPENAI_API_KEY=your-api-key-here")
        print("2. Use Hugging Face models (free) by setting in .env:")
        print("   USE_HUGGINGFACE=true")
        print("=" * 60)
        sys.exit(1)
    elif use_huggingface:
        print("Using Hugging Face models (free alternative)")
    else:
        print("OPENAI_API_KEY is set successfully")
    
    # Start backend server
    backend_process = run_backend()
    
    if backend_process is None:
        print("Failed to start backend server")
        sys.exit(1)
    
    # Wait a moment for backend to start
    time.sleep(2)
    
    # Start frontend
    frontend_process = run_frontend()
    
    if frontend_process is None:
        print("Failed to start frontend server")
        backend_process.wait()
        sys.exit(1)
    
    # Wait for both processes to complete
    backend_process.wait()
    frontend_process.wait()