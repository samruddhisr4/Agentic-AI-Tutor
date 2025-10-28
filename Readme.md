# Agentic AI Tutor

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini-blue)](https://ai.google/discover/gemini/)

An intelligent tutoring system powered by Large Language Models (LLMs) that provides personalized learning experiences through interactive AI-driven content generation and quiz creation.

![Agentic AI Tutor Demo](https://via.placeholder.com/800x400.png?text=Agentic+AI+Tutor+Interface)

## 🌟 Features

- **Multi-Modal Learning**: Generate content in different styles - in-depth explanations, visual learning experiences, and hands-on exercises
- **Quiz Generation**: Create customized multiple-choice questions for any topic with detailed explanations
- **Google Gemini AI Engine**: Powered by Google's advanced Gemini models for high-quality responses
- **Web Interface**: User-friendly Streamlit frontend for easy interaction
- **API Backend**: FastAPI-powered backend for robust performance
- **Placement Preparation**: Specialized content for computer science students preparing for placements

## 🚀 Technology Stack

- **Frontend**: [Streamlit](https://streamlit.io/) - For creating interactive web applications
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) - High-performance API framework
- **AI Orchestration**: [LangChain](https://www.langchain.com/) - Framework for developing applications powered by LLMs
- **LLM Provider**: [Google Gemini API](https://ai.google/discover/gemini/) - For advanced AI capabilities
- **Environment Management**: Python virtual environments with `requirements.txt`

## 📋 Prerequisites

- Python 3.8 or higher
- A Google Gemini API key (required)
- Internet connection

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
   # Use Google Gemini models (required)
   USE_GEMINI=true

   # Google Gemini API Key (required)
   GOOGLE_API_KEY=your-google-gemini-api-key-here
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
    "style": "in_depth" // Options: "in_depth", "visual", "hands_on"
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
│   │   └── ai_engine_gemini.py    # Google Gemini implementation
│   ├── backend/
│   │   └── main.py                # FastAPI backend
│   └── frontend/
│       └── app.py                 # Streamlit frontend
├── .env                           # Environment variables
├── requirements.txt               # Python dependencies
└── run_app.py                     # Application runner
```

## 🚨 Troubleshooting

### If you're getting timeout errors:

1. **Check your internet connection** - Google Gemini API requires stable internet access
2. **Verify your API key** - Make sure your Google Gemini API key is valid and properly configured
3. **Check your Google Cloud billing** - Ensure your Google Cloud project has billing enabled
4. **Try a simpler query** - Complex queries may take longer to process

### If you're getting authentication errors:

1. **Verify your API key** - Make sure your Google Gemini API key is correct
2. **Check Google Cloud project settings** - Ensure the Generative Language API is enabled
3. **Verify billing status** - Check that your Google Cloud project has billing enabled

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

- Thanks to [Google](https://ai.google/) for providing powerful Gemini language models
- Thanks to the [LangChain](https://www.langchain.com/) team for their excellent framework
