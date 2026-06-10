# Project Constitution

## 1. Principles
- **Simplicity First**: Write readable, maintainable code over "clever" code.
- **Fail Gracefully**: If an API request fails, provide clear error messages to the user instead of crashing.
- **Componentization**: Keep UI logic (Streamlit) separated from core business logic (LangChain, API calls).

## 2. Tech Stack
- **Language**: Python 3
- **Frontend**: Streamlit
- **Data Manipulation**: Pandas
- **AI/Vector DB**: LangChain, OpenAI, FAISS
- **External APIs**: GitHub REST API

## 3. Formatting & Standards
- Follow standard PEP-8 style guidelines for Python.
- Document all core functions with clear docstrings explaining inputs and outputs.
- Keep environment variables organized in a `.env` file and never commit secrets.
