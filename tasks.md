# Tasks

- [x] Set up standard project structure and initialize `requirements.txt`.
- [x] Implement the Streamlit basic layout (sidebar, text input, buttons).
- [x] Write `fetch_github_repos(username)` to retrieve all public repos using `requests` and pagination.
- [x] Implement error handling for invalid usernames (extracting from URLs if necessary) and API limits.
- [x] Write `get_user_repos(username)` using `PyGithub` to pull detailed metrics (stars, forks, languages, contents).
- [x] Integrate Pandas to export the structured dictionary list into `repo_data.csv`.
- [x] Set up LangChain `CSVLoader` and `FAISS` vector store with OpenAI embeddings.
- [x] Draft the custom `PromptTemplate` telling the AI how to score complexity.
- [x] Feed the QA chain the prompt and display the resulting markdown output in Streamlit.
- [x] Final polish, code cleanup, and README generation.
