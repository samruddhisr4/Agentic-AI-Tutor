# Deployment Guide

## Deploying to Streamlit Cloud

### 1. Prepare Your Repository

1. Create a new repository on GitHub
2. Push your Agentic AI Tutor code to the repository

### 2. Set Up Streamlit Cloud Account

1. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
2. Sign in with your GitHub account
3. Click "New app"

### 3. Configure Your App

When setting up your app on Streamlit Cloud:

1. **Repository**: Select your Agentic AI Tutor repository
2. **Branch**: Select the branch (usually main or master)
3. **Main file**: Set to `src/frontend/app.py` (just the frontend for Streamlit Cloud)
4. **App URL**: Choose a custom subdomain or use the default

### 4. Set Environment Variables

In the Streamlit Cloud dashboard, go to your app settings and add these environment variables:

```
USE_GEMINI=true
GOOGLE_API_KEY=your_actual_google_api_key_here
BACKEND_URL=https://your-backend-url.com
```

Note: For Streamlit Cloud, you'll need to deploy the backend separately (e.g., on Render, Heroku, or Google Cloud Run) since Streamlit Cloud only runs the frontend.

## Deploying the Backend Separately

### Option 1: Render (Recommended)

1. Create a free account at [render.com](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repository
4. Set the following build command:
   ```
   pip install -r requirements.txt
   ```
5. Set the start command:
   ```
   uvicorn src.backend.main:app --host 0.0.0.0 --port $PORT
   ```
6. Add environment variables:
   ```
   USE_GEMINI=true
   GOOGLE_API_KEY=your_actual_google_api_key_here
   ```

### Option 2: Google Cloud Run

1. Install Google Cloud SDK
2. Build and deploy:
   ```bash
   gcloud run deploy agentic-ai-tutor-backend \
     --source . \
     --platform managed \
     --allow-unauthenticated \
     --set-env-vars USE_GEMINI=true,GOOGLE_API_KEY=your_api_key
   ```

## Local Development

To run the application locally:

1. Set up environment variables in `.env`:

   ```
   USE_GEMINI=true
   GOOGLE_API_KEY=your_google_api_key_here
   ```

2. Run the application:
   ```bash
   python run_app.py
   ```

This will start both the backend (on port 8000) and frontend (on port 8501).

## Troubleshooting Common Issues

### Dependency Conflicts

If you see dependency conflicts like:

```
Because langchain-openai==0.2.10 depends on langchain-core>=0.3.21,<0.4.0 and you require langchain-core==0.3.15, we can conclude that your requirements and langchain-openai==0.2.10 are incompatible.
```

This means there are version mismatches between packages. Our requirements.txt has been updated with compatible versions:

- `langchain==0.3.7`
- `langchain-core==0.3.21` (updated to satisfy all dependencies)
- `langchain-google-genai==2.0.1`
- `langchain-community==0.3.2`
- `langchain-openai==0.2.10`
- `langchain-huggingface==0.1.2`

### ModuleNotFoundError: No module named 'langchain_core.pydantic_v1'

This error occurs due to version incompatibility between langchain packages. To fix:

1. Use the exact versions specified in requirements.txt
2. Redeploy your application

### Port Binding Issues

If you see "No open ports detected" error:

1. Make sure your start command includes `--host 0.0.0.0 --port $PORT`
2. Ensure your main.py file uses `os.environ.get("PORT", 8000)` for the port

### Environment Variables Not Loading

If your API key isn't being recognized:

1. Check that you've set the environment variables in your Render dashboard
2. Verify that you're using the correct variable names:
   - `USE_GEMINI=true`
   - `GOOGLE_API_KEY=your_actual_key`

### Checking Package Versions Locally

To verify your package versions locally:

```bash
pip list | grep langchain
```

This should show:

- langchain 0.3.7
- langchain-core 0.3.21
- langchain-google-genai 2.0.1
- langchain-community 0.3.2
- langchain-openai 0.2.10
- langchain-huggingface 0.1.2

### Forcing Clean Installation

If you continue to have issues:

```bash
pip uninstall langchain langchain-core langchain-google-genai langchain-community langchain-openai langchain-huggingface
pip install -r requirements.txt
```

This ensures all packages are installed with the exact compatible versions specified.
