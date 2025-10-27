# Agentic AI Tutor User Guide

## Getting Started

Welcome to the Agentic AI Tutor! This guide will help you get started with using the application for your learning needs.

### Prerequisites

Before you begin, ensure you have:
1. Python 3.8 or higher installed on your system
2. Internet connection (required for Hugging Face models)
3. An OpenAI API key (optional, but recommended for better quality responses)

### Installation

Follow these steps to set up the application:

1. Clone or download the repository
2. Navigate to the project directory
3. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

Create a `.env` file in the project root with your configuration:

```env
# For OpenAI (optional but recommended)
OPENAI_API_KEY=your-openai-api-key-here

# To use Hugging Face models (free alternative)
USE_HUGGINGFACE=true
```

## Using the AI Tutor

### Accessing the Interface

Run the application:
```bash
python run_app.py
```

This will start both the backend API server and the Streamlit frontend. Your default web browser should automatically open to the application interface.

### Navigating the Interface

The interface has two main sections accessible via the sidebar:

1. **AI Tutor**: For generating detailed explanations on any topic
2. **Quiz Generator**: For creating practice quizzes

### AI Tutor Features

In the AI Tutor section:
1. Enter your question or topic in the text area
2. Select a response style:
   - **In-Depth**: Comprehensive explanations with background information
   - **Visual**: Learning experiences with diagrams and visual metaphors
   - **Hands-On**: Practical exercises and coding examples
3. Click "Generate Response"

### Quiz Generator Features

In the Quiz Generator section:
1. Select a topic from the dropdown (DBMS, OS, CN, AI, ML, DL, System Design, GenAI)
2. Choose difficulty level (Beginner, Intermediate, Advanced)
3. Set the number of questions (1-10)
4. Click "Generate Quiz"

## Troubleshooting

### Common Issues

1. **Connection Errors**: Ensure the backend server is running before accessing the frontend
2. **Quota Limits**: If using OpenAI and encountering quota issues, switch to Hugging Face models
3. **Slow Responses**: Hugging Face models may take longer to respond than OpenAI

### Switching AI Engines

To switch between OpenAI and Hugging Face models:
1. Run the engine switcher script:
   ```bash
   python switch_engine.py
   ```
2. Follow the prompts to select your preferred engine
3. Restart the application

### Using Hugging Face Models

Hugging Face models are a free alternative that work without an API key:
1. Set `USE_HUGGINGFACE=true` in your `.env` file
2. Optionally, add a Hugging Face token for better model access:
   ```env
   HUGGINGFACEHUB_API_TOKEN=your-huggingface-token-here
   ```

## Best Practices

1. **For Better Results**:
   - Be specific with your questions
   - Provide context when needed
   - Use the appropriate response style for your learning needs

2. **For Quiz Generation**:
   - Start with fewer questions for quicker results
   - Adjust difficulty based on your current knowledge level
   - Review explanations to understand concepts better

3. **When Using OpenAI**:
   - Monitor your usage to avoid exceeding quotas
   - Keep your API key secure and never share it

## Getting Help

If you encounter issues:
1. Check the console output for error messages
2. Verify your environment variables are set correctly
3. Ensure all dependencies are installed
4. Open an issue on the GitHub repository if problems persist