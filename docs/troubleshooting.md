# Troubleshooting Guide

This guide helps you diagnose and resolve common issues with the Agentic AI Tutor.

## Common Issues and Solutions

### 1. Getting Mock Responses Instead of Real AI Responses

**Symptoms**: You see messages like "This is a mock response for your query..." instead of actual AI-generated content.

**Causes and Solutions**:

#### OpenAI Quota Exceeded
- **Error Message**: "You exceeded your current quota"
- **Solution**: 
  1. Check your billing status at [OpenAI Billing](https://platform.openai.com/account/billing)
  2. Verify your payment method is properly set up
  3. Wait for account verification (new accounts may take 24-48 hours)
  4. Switch to Hugging Face models by setting `USE_HUGGINGFACE=true` in your `.env` file

#### Hugging Face Provider Issues
- **Error Message**: "StopIteration" or "provider" related errors
- **Solution**:
  1. Get a Hugging Face API token from [Hugging Face Tokens](https://huggingface.co/settings/tokens)
  2. Add it to your `.env` file: `HUGGINGFACEHUB_API_TOKEN=your-token-here`
  3. Restart the application

#### Hugging Face API 404 Errors
- **Error Message**: "404 - Not Found" when calling Hugging Face API
- **Solution**:
  1. Verify your token is valid by running `python test_hf_token.py`
  2. Try using a different model by modifying the `ai_engine_hf_direct.py` file
  3. Check your network connectivity and firewall settings
  4. Consider using local models like Ollama as an alternative

### 2. Network Connectivity Issues

**Symptoms**: Slow responses, timeouts, or connection errors.

**Solutions**:
1. Check your internet connection
2. Ensure your firewall isn't blocking the application
3. Try using a different network connection

### 3. Dependency Installation Issues

**Symptoms**: Import errors or missing modules.

**Solutions**:
1. Make sure you've activated your virtual environment
2. Run `pip install -r requirements.txt` again
3. If you encounter compilation issues, try:
   ```bash
   pip install numpy==1.26.4 --only-binary=all
   ```

## Diagnostic Tools

### Run the Troubleshooting Script

```bash
python troubleshoot.py
```

This script will:
- Check your environment variables
- Test OpenAI integration
- Test Hugging Face integration
- Provide specific recommendations

### Check Environment Variables

Make sure your `.env` file contains the necessary configuration:

```env
# For OpenAI (optional but recommended for better quality)
OPENAI_API_KEY=your-openai-api-key-here

# To use Hugging Face models (free alternative)
USE_HUGGINGFACE=true

# Hugging Face API Token (optional but recommended for better access)
HUGGINGFACEHUB_API_TOKEN=your-huggingface-token-here
```

## Advanced Troubleshooting

### Enable Debug Logging

To get more detailed information about what's happening:

1. Set the environment variable:
   ```bash
   export LANGCHAIN_VERBOSE=true  # On Windows: set LANGCHAIN_VERBOSE=true
   ```

2. Run the application and check the console output for detailed logs

### Test Individual Components

You can test the AI engines directly:

```bash
python test_openai.py
python test_hf_api.py
python test_hf_direct.py
python test_hf_token.py
```

## Alternative Solutions

### Using Local Models with Ollama

If you continue to have issues with cloud-based models, consider using local models:

1. Install [Ollama](https://ollama.com/)
2. Pull a model:
   ```bash
   ollama pull llama2
   ```
3. The application would need to be modified to use Ollama instead of the current providers

### Using Different Hugging Face Models

If the default models aren't working, you can try different models by modifying the `ai_engine_hf_direct.py` file:

```python
# Try different models
llm = HuggingFaceDirect("mistralai/Mistral-7B-v0.1")
```

Note: You may need to adjust parameters based on the specific model requirements.

### Manual Model Testing

You can test Hugging Face models manually using curl:

```bash
curl -X POST "https://api-inference.huggingface.co/models/google/flan-t5-small" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE" \
     -H "Content-Type: application/json" \
     -d '{"inputs":"What is 2+2?"}'
```

## Getting Help

If you're still experiencing issues:

1. Run the troubleshooting script and save the output
2. Check the console logs for error messages
3. Open an issue on the GitHub repository with:
   - The error messages you're seeing
   - Your environment configuration (without sensitive information)
   - The output of the troubleshooting script