# Changelog

All notable changes to the Agentic AI Tutor project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation including user guide, architecture diagram, and contributing guide
- Enhanced README with badges, better structure, and documentation links
- LICENSE file with MIT license
- .env.example file for easier configuration
- Improved error handling and fallback mechanisms

### Changed
- Updated run_app.py to handle Hugging Face models without requiring OpenAI API key
- Enhanced AI engine initialization with better error handling
- Improved backend engine selection logic
- Enhanced HuggingFace engine with better error messages and fallback mechanisms

### Fixed
- Issue where Hugging Face fallback wasn't working when OpenAI quota was exhausted
- Engine initialization errors that caused application crashes
- Backend import issues when switching between AI engines

## [1.0.0] - 2025-10-26

### Added
- Initial release of Agentic AI Tutor
- Dual AI engine support (OpenAI and Hugging Face)
- Streamlit frontend with two main features:
  - AI Tutor for generating explanations
  - Quiz Generator for creating practice questions
- FastAPI backend with RESTful API endpoints
- Automatic fallback mechanism when OpenAI quota is exhausted
- Engine switching utility script