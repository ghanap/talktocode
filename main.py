import streamlit as st
import os
import tempfile
import subprocess
from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOllama
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from github import Github
import pandas as pd
from io import StringIO
import datetime

load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY', '')
os.environ['GITHUB_TOKEN'] = os.getenv('GITHUB_TOKEN', '')

st.set_page_config(page_title="Talk To Code Chatbot", page_icon="💬", layout="wide")

def load_text_files(directory):
    docs = []
    valid_extensions = {'.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.css', '.md', '.cpp', '.c', '.h', '.hpp', '.java', '.go', '.rs', '.txt', '.json', '.yml', '.yaml', '.toml'}
    for root, _, files in os.walk(directory):
        if '.git' in root:
            continue
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in valid_extensions:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    rel_path = os.path.relpath(file_path, directory)
                    docs.append(Document(page_content=content, metadata={"source": rel_path}))
                except Exception:
                    pass
    return docs

@st.cache_resource(show_spinner=False)
def load_and_index_repo(repo_url):
    temp_dir = tempfile.mkdtemp()
    
    # Clone the repository
    try:
        subprocess.run(["git", "clone", "--depth", "1", repo_url, temp_dir], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        return None, f"Failed to clone repository: {e.stderr.decode()}"

    # Load documents
    docs = load_text_files(temp_dir)
    if not docs:
        return None, "No text or code files found in the repository."

    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # Embed and index
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(splits, embeddings)
    
    return vectorstore, "Success"

def save_review(rating, comment):
    try:
        g = Github(os.environ.get('GITHUB_TOKEN'))
        repo = g.get_repo("ghanap/talktocode")
        try:
            file = repo.get_contents("reviews.csv")
            content = file.decoded_content.decode("utf-8")
            df = pd.read_csv(StringIO(content))
        except Exception:
            df = pd.DataFrame(columns=["timestamp", "rating", "comment"])
            
        new_row = {"timestamp": datetime.datetime.now().isoformat(), "rating": rating, "comment": comment}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        
        csv_str = df.to_csv(index=False)
        if 'file' in locals():
            repo.update_file("reviews.csv", "Add new anonymous user review", csv_str, file.sha)
        else:
            repo.create_file("reviews.csv", "Create reviews.csv for feedback", csv_str)
        return True
    except Exception as e:
        return False

def show_feedback_form():
    st.markdown("### 📝 Leave Anonymous Feedback")
    st.write("Your feedback helps us improve! All submissions are completely anonymous.")
    
    with st.form("feedback_form", clear_on_submit=True):
        rating = st.slider("Rating (1-5 Stars)", min_value=1, max_value=5, value=5)
        comment = st.text_area("Your thoughts (optional)", placeholder="Works great! ...")
        submitted = st.form_submit_button("Submit Anonymous Feedback")
        
        if submitted:
            with st.spinner("Saving securely..."):
                if save_review(rating, comment):
                    st.success("Thank you! Your feedback has been saved securely.")
                else:
                    st.error("Failed to save feedback right now. Please try again later.")

def main():
    st.title("Talk To Code 💬💻")
    st.sidebar.title("Configuration")
    
    repo_url = st.sidebar.text_input("Enter GitHub Repository URL", placeholder="https://github.com/user/repo")
    language = st.sidebar.selectbox("Response Language", ["English", "Hindi", "Urdu", "Tamil", "Telugu", "Bengali", "Marathi", "Gujarati", "Kannada", "Malayalam"])
    
    st.sidebar.divider()
    provider = st.sidebar.radio("LLM Provider", ["Groq (Cloud)", "Ollama (Local)"])
    ollama_model = "llama3"
    ollama_base_url = "http://localhost:11434"
    if provider == "Ollama (Local)":
        ollama_model = st.sidebar.text_input("Ollama Model Name", value="llama3")
        ollama_base_url = st.sidebar.text_input("Ollama Base URL", value="http://localhost:11434")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None
        st.session_state.current_repo = ""
        st.session_state.qa_chain = None

    if repo_url and repo_url != st.session_state.current_repo:
        with st.spinner(f"Cloning and analyzing {repo_url}..."):
            vectorstore, msg = load_and_index_repo(repo_url)
            if vectorstore:
                st.session_state.vectorstore = vectorstore
                st.session_state.current_repo = repo_url
                st.session_state.messages = [{"role": "assistant", "content": f"Repository `{repo_url}` loaded successfully! What would you like to know about the code?"}]
                st.session_state.qa_chain = None # force rebuild
            else:
                st.sidebar.error(msg)
                
    if st.session_state.vectorstore:
        # Rebuild chain if provider config changed or if chain is None
        config_changed = (
            st.session_state.get("current_provider") != provider or 
            st.session_state.get("ollama_model") != ollama_model or 
            st.session_state.get("ollama_base_url") != ollama_base_url
        )
        if st.session_state.qa_chain is None or config_changed:
            memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
            if provider == "Groq (Cloud)":
                llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0)
            else:
                llm = ChatOllama(model=ollama_model, base_url=ollama_base_url, temperature=0)
                
            st.session_state.qa_chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=st.session_state.vectorstore.as_retriever(search_kwargs={"k": 5}),
                memory=memory
            )
            st.session_state.current_provider = provider
            st.session_state.ollama_model = ollama_model
            st.session_state.ollama_base_url = ollama_base_url
                
    # Layout tabs
    tab1, tab2 = st.tabs(["💬 Chat", "📝 Leave Feedback"])
    
    with tab1:
        # Display chat
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if st.session_state.vectorstore:
            if prompt := st.chat_input("Ask a question about the codebase..."):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        try:
                            lang_instruction = f"\n\n[System Requirement: You MUST provide your final response entirely in {language}.]" if language != "English" else ""
                            response = st.session_state.qa_chain({"question": prompt + lang_instruction})
                            answer = response["answer"]
                            st.markdown(answer)
                            st.session_state.messages.append({"role": "assistant", "content": answer})
                        except Exception as e:
                            st.error(f"Error querying the AI: {str(e)}")
        else:
            if not repo_url:
                st.info("👈 Please paste a GitHub Repository URL in the sidebar to load a codebase!")
                
    with tab2:
        show_feedback_form()

if __name__ == "__main__":
    main()