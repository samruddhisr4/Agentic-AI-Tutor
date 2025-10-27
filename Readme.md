# Agentic AI Tutor

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-red)](https://platform.openai.com/)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Models-yellow)](https://huggingface.co/)

An intelligent tutoring system powered by Large Language Models (LLMs) that provides personalized learning experiences through interactive AI-driven content generation and quiz creation.

![Agentic AI Tutor Demo](https://via.placeholder.com/800x400.png?text=Agentic+AI+Tutor+Interface)

## 🌟 Features

- **Multi-Modal Learning**: Generate content in different styles - in-depth explanations, visual learning experiences, and hands-on exercises
- **Quiz Generation**: Create customized multiple-choice questions for any topic with detailed explanations
- **Dual AI Engine Support**: Seamlessly switch between OpenAI and Hugging Face models
- **Automatic Fallback**: Automatically switches to Hugging Face models when OpenAI quota is exhausted
- **Web Interface**: User-friendly Streamlit frontend for easy interaction
- **API Backend**: FastAPI-powered backend for robust performance
- **Placement Preparation**: Specialized content for computer science students preparing for placements

## 🚀 Technology Stack

- **Frontend**: [Streamlit](https://streamlit.io/) - For creating interactive web applications
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) - High-performance API framework
- **AI Orchestration**: [LangChain](https://www.langchain.com/) - Framework for developing applications powered by LLMs
- **LLM Providers**: 
  - [OpenAI API](https://platform.openai.com/) - For premium AI capabilities
  - [Hugging Face](https://huggingface.co/) - For free, open-source AI models
- **Environment Management**: Python virtual environments with `requirements.txt`

## 📋 Prerequisites

- Python 3.8 or higher
- An OpenAI API key (optional, for premium features)
- Internet connection (required for Hugging Face models)

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Agentic-AI-Tutor
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 📚 Documentation

- [User Guide](docs/user_guide.md) - Instructions for using the application
- [Architecture](docs/architecture.md) - System architecture diagram
- [Contributing Guide](docs/contributing.md) - Guidelines for contributing to the project
- [Troubleshooting Guide](docs/troubleshooting.md) - Common issues and solutions

## ⚙️ Configuration

1. **Set up environment variables**:
   Create a `.env` file in the project root with the following content:
   ```env
   # For OpenAI (optional but recommended for better quality)
   OPENAI_API_KEY=your-openai-api-key-here
   
   # To use Hugging Face models (free alternative)
   USE_HUGGINGFACE=true
   
   # Hugging Face API Token (optional but recommended for better access)
   # Get your token from: https://huggingface.co/settings/tokens
   # HUGGINGFACEHUB_API_TOKEN=your-huggingface-token-here
   ```
   
2. **Engine Selection**:
   - To use OpenAI (requires API key): Set `USE_HUGGINGFACE=false` or remove the line
   - To use Hugging Face (free): Set `USE_HUGGINGFACE=true`
   
   You can also use the provided switch script:
   ```bash
   python switch_engine.py
   ```

## 🎯 Usage

### Running the Full Application

```bash
python run_app.py
```

This will start both the backend API server and the Streamlit frontend.

### Running Components Separately

**Start the backend API server**:
```bash
cd src/backend
uvicorn main:app --reload --port 8000
```

**Start the frontend**:
```bash
cd src/frontend
streamlit run app.py
```

### API Endpoints

- **Generate Response**: `POST /generate_response`
  ```json
  {
    "query": "Explain quantum computing",
    "style": "in_depth"  // Options: "in_depth", "visual", "hands_on"
  }
  ```

- **Generate Quiz**: `POST /generate_quiz`
  ```json
  {
    "topic": "Machine Learning",
    "difficulty": "intermediate",
    "num_questions": 5
  }
  ```

## 📁 Project Structure

```
Agentic-AI-Tutor/
├── src/
│   ├── ai_engine/
│   │   ├── ai_engine.py       # OpenAI implementation
│   │   └── ai_engine_hf.py    # Hugging Face implementation
│   ├── backend/
│   │   └── main.py            # FastAPI backend
│   └── frontend/
│       └── app.py             # Streamlit frontend
├── .env                       # Environment variables
├── requirements.txt           # Python dependencies
├── run_app.py                # Application runner
└── switch_engine.py          # Engine switching utility
```

## 🔁 Fallback Mechanism

The system automatically handles API quota issues:
1. When OpenAI quota is exhausted, the system gracefully falls back to Hugging Face models
2. If Hugging Face models are unavailable, a mock response is provided
3. Users can manually switch engines using `switch_engine.py`

## 🚨 Troubleshooting

### If you're getting mock responses instead of real AI responses:

1. **Check your internet connection** - Hugging Face models require internet access
2. **Get a Hugging Face API token**:
   - Go to [Hugging Face Tokens](https://huggingface.co/settings/tokens)
   - Create a new token
   - Add it to your `.env` file: `HUGGINGFACEHUB_API_TOKEN=your-token-here`
3. **Try using OpenAI instead** (if you have quota available):
   - Set `USE_HUGGINGFACE=false` in your `.env` file
4. **Run the debug script** to diagnose issues:
   ```bash
   python debug_hf.py
   ```

### If you're getting OpenAI quota errors:

1. **Check your billing status** at [OpenAI Billing](https://platform.openai.com/account/billing)
2. **Verify your payment method** is properly set up
3. **Wait for account verification** - new accounts may take 24-48 hours to be fully activated
4. **Switch to Hugging Face models** by setting `USE_HUGGINGFACE=true` in your `.env` file

See our detailed [Troubleshooting Guide](docs/troubleshooting.md) for more help.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

See our [Contributing Guide](docs/contributing.md) for more details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## 🙏 Acknowledgements

- Thanks to [OpenAI](https://openai.com/) for providing powerful language models
- Thanks to [Hugging Face](https://huggingface.co/) for open-source AI models
- Thanks to the [LangChain](https://www.langchain.com/) team for their excellent framework