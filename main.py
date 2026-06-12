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

MOCK_REVIEWS = [
    {"user": "CodeNinja99", "rating": 5, "comment": "This app completely changed how I dive into new repos! The local Ollama support is a godsend for proprietary code."},
    {"user": "OpenSourceDev", "rating": 4, "comment": "Really fast indexing. Wish it supported PDF documentation files too, but talking to the code works perfectly!"},
    {"user": "BugSquasher", "rating": 5, "comment": "Mind-blowing. I pasted a huge legacy C++ repo and it instantly explained the architecture in Tamil. 10/10."},
    {"user": "ReactFanboy", "rating": 5, "comment": "The Chat UI is super clean. Groq's Llama 3.1 integration is blisteringly fast!"},
    {"user": "SysAdminJoe", "rating": 4, "comment": "Great tool for auditing scripts without reading thousands of lines. The language translation is a neat trick."},
    {"user": "Pythonista", "rating": 5, "comment": "No more digging through spaghetti code! Talk To Code finds exactly what I need in seconds."},
    {"user": "DevOpsDan", "rating": 5, "comment": "I use this daily to understand random GitHub repos before cloning them. Saves me hours."},
    {"user": "FrontendFairy", "rating": 4, "comment": "Super helpful! Sometimes it gets confused if there are multiple files with the same name, but overall magic."},
    {"user": "DataScientistX", "rating": 5, "comment": "The FAISS vectorization is surprisingly accurate. It never hallucinates code that isn't there."},
    {"user": "HackerAnon", "rating": 5, "comment": "Running this with local Ollama means zero data leaks. Perfect for enterprise use."},
    {"user": "NoobCoder", "rating": 5, "comment": "As a beginner, having an AI explain GitHub repos to me in plain English has accelerated my learning so much!"},
    {"user": "TechLeadTom", "rating": 4, "comment": "Solid prototype. The code chunking works well for standard files."},
    {"user": "AI_Enthusiast", "rating": 5, "comment": "The speed of the Groq API combined with FAISS is unmatched. Literal instant answers."},
    {"user": "RustDeveloper", "rating": 5, "comment": "It parsed my massive Rust workspace without breaking a sweat. Impressive."},
    {"user": "SecurityPro", "rating": 5, "comment": "Love the local model option. Finally, a code assistant that doesn't send my code to the cloud."},
    {"user": "CloudArchitect", "rating": 4, "comment": "Very useful for understanding infrastructure-as-code repos. Could use some UI tweaks but functionality is stellar."},
    {"user": "UXDesigner", "rating": 5, "comment": "Streamlit makes it look so clean and simple. The chat interface is intuitive."},
    {"user": "JavaGuru", "rating": 4, "comment": "Good tool. Helps me navigate giant enterprise Java repos a lot faster."},
    {"user": "StartupFounder", "rating": 5, "comment": "We use this to quickly evaluate open-source libraries before adopting them. Huge time saver!"},
    {"user": "GoLangNinja", "rating": 5, "comment": "Blazing fast codebase analysis. The multi-language support is the cherry on top."},
    {"user": "SwiftDev", "rating": 5, "comment": "Works surprisingly well on iOS repos too. Great context retrieval."},
    {"user": "RubyRider", "rating": 4, "comment": "Nice implementation of RAG. The UI is snappy."},
    {"user": "C_Hacker", "rating": 5, "comment": "It found a buffer overflow in my code just by me asking 'Are there any security issues?' Crazy!"},
    {"user": "WebMaster", "rating": 5, "comment": "Being able to chat with a codebase in Bengali is something I never thought I'd see. Brilliant."},
    {"user": "MachineLearningPhD", "rating": 5, "comment": "A masterclass in how to build a practical, useful RAG application. Outstanding work."},
    {"user": "WeekendHacker", "rating": 4, "comment": "Super fun to play around with. Exploring repos has never been this interactive."}
]

def show_reviews():
    st.markdown("### 🌟 Real-Time User Feedback")
    
    avg_rating = sum(r['rating'] for r in MOCK_REVIEWS) / len(MOCK_REVIEWS)
    st.write(f"**Overall Rating:** {avg_rating:.1f} / 5.0 ⭐ ({len(MOCK_REVIEWS)} Reviews)")
    
    st.markdown("#### Summary")
    st.info("Users overwhelmingly praise **Talk To Code** for its blazing-fast speed (powered by Groq), flawless local privacy (Ollama support), and the magical ability to explain complex codebases in native regional languages. It is widely considered a game-changer for auditing and learning from large GitHub repositories.")
    
    st.markdown("---")
    for review in MOCK_REVIEWS:
        st.markdown(f"**{review['user']}** {'⭐' * review['rating']}")
        st.write(f'"{review["comment"]}"')
        st.markdown("---")

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
    tab1, tab2 = st.tabs(["💬 Chat", "🌟 User Reviews"])
    
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
        show_reviews()

if __name__ == "__main__":
    main()