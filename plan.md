# Implementation Plan

## Architecture Overview
The application will be a monolithic Python script built with Streamlit. It will interact with the GitHub API for data retrieval and the OpenAI API (via LangChain) for analysis.

## Key Components

### 1. User Interface (`main.py`)
- Built with Streamlit.
- Sidebar containing:
  - Text input for the GitHub username.
  - Submit and Clear buttons.
  - Basic "About" information.
- Main panel to display:
  - List of fetched repositories.
  - The final AI-generated analysis.

### 2. GitHub Data Fetcher (`fetch_github_repos`, `get_user_repos`)
- Uses `requests` for initial pagination and basic repo listing.
- Uses `PyGithub` library for deep inspection (fetching issues, contents, labels).
- **Data Flow**:
  1. Fetch list of repo metadata.
  2. Map into a structured list of dictionaries.
  3. Export to a temporary `repo_data.csv` for LLM consumption.

### 3. AI Analysis Pipeline
- **Loader**: Use LangChain's `CSVLoader` to read `repo_data.csv`.
- **Embeddings**: `OpenAIEmbeddings` to vectorize the repository data.
- **Vector Store**: `FAISS` to store and retrieve vectors.
- **Chain**: A `RetrievalQA` chain configured with a custom `PromptTemplate` instructing the LLM to score and identify the most complex repository based on the dataset.

## Error Handling
- Validate that the input username is valid.
- If a URL is pasted, extract the username from the end of the URL.
- Implement rate-limit checks or fallback mechanisms if the GitHub API rejects the request (e.g. `response.status_code != 200`).
