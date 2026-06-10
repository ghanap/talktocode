# User Manual - GitHub Automated Analysis Tool

Welcome to the GitHub Automated Analysis Tool! This application helps you easily discover and analyze the most technically challenging repositories on a user's GitHub profile using AI.

## Prerequisites
- Python 3.9 or higher installed on your computer.
- A GitHub Personal Access Token.
- A Groq API Key.

## 1. Setup the Environment
First, you need to install all the required Python libraries.

1. Open a terminal or command prompt inside the project folder.
2. (Optional but recommended) Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
   * Activate it on Windows: `.venv\Scripts\activate`
   * Activate it on Mac/Linux: `source .venv/bin/activate`
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 2. Configure API Keys
The application requires API keys to communicate with GitHub and Groq.

1. In the root of your project folder, create a new file named exactly `.env`.
2. Open the `.env` file and add your keys in the following format:
   ```ini
   GROQ_API_KEY="your_actual_groq_key_here"
   GITHUB_TOKEN="your_actual_github_token_here"
   ACTIVELOOP_TOKEN="your_activeloop_token_here"
   ```
   *(Note: Without a valid GitHub token, the app will quickly hit rate limits and fail to load repositories).*

## 3. Deploy/Run Locally
Once your environment is set up and your keys are configured, you are ready to launch the app!

1. In your terminal, run the following command:
   ```bash
   streamlit run main.py
   ```
2. A local web server will start, and your default web browser should automatically open a new tab pointing to `http://localhost:8501`.
3. If it doesn't open automatically, simply copy and paste `http://localhost:8501` into your browser's address bar.

## 4. How to Use
1. In the sidebar on the left, type the **GitHub Username** (e.g., `torvalds`) of the developer you want to analyze. Do not paste full URLs.
2. Click the **Submit** button.
3. The app will fetch the repositories and start analyzing them using LangChain and Groq LLMs. Please be patient, as AI analysis can take a moment.
4. The result will display the most technically complex repository along with a detailed explanation of why it was chosen.
