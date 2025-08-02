import streamlit as st
import os
from document_processor import extract_chunks
from vector_store import VectorStoreManager
from llm_handler import AnswerGenerator

# --- App Configuration (Must be the first Streamlit command) ---
st.set_page_config(
    page_title="DocuQuery AI",
    page_icon="🤖",
    layout="centered"
)

# --- Custom CSS for the final polished theme ---
st.markdown("""
<style>
    /* Main app background */
    body {
        color: #d1d5db; 
        background-color: #1e1e1e;
    }

    /* Main app container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #2a2a2e;
    }

    /* Chat message styling */
    [data-testid="stChatMessage"] {
        border-radius: 10px;
        padding: 1rem 1.25rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        width: 90%;
    }
    
    /* User message background */
    [data-testid="stChatMessage"]:has(div[data-testid="stAvatarIcon-user"]) {
        background-color: #2c3e50;
    }

    /* Assistant message background */
    [data-testid="stChatMessage"]:has(div[data-testid="stAvatarIcon-assistant"]) {
        background-color: #343541;
    }

    /* Increase the base font size for better readability */
    html, body, [class*="st-"] {
        font-size: 21px;
    }
    
    /* Title styling */
    h1 {
        font-size: 2.8rem !important;
        font-weight: 700;
        color: #d1d5db;
        text-align: center;
    }
    
    /* Input bar styling */
    [data-testid="stChatInput"] {
        background-color: #2a2a2e;
    }

</style>
""", unsafe_allow_html=True)

# --- App Title and Description ---
st.title("📄 DocuQuery AI")
st.markdown("<p style='text-align: center;'>Upload a PDF document on the left and ask questions about its content.</p>", unsafe_allow_html=True)

# --- Session State Initialization ---
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = None
if 'llm_handler' not in st.session_state:
    try:
        # Securely load the GOOGLE API key
        api_key = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))
    except:
        api_key = os.getenv("GOOGLE_API_KEY")
    
    st.session_state.llm_handler = AnswerGenerator(api_key=api_key)

# --- Sidebar for Document Upload ---
with st.sidebar:
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    if uploaded_file:
        if st.session_state.get("uploaded_file_name") != uploaded_file.name:
            st.session_state.uploaded_file_name = uploaded_file.name
            
            with st.spinner("Processing document..."):
                temp_dir = "temp_docs"
                os.makedirs(temp_dir, exist_ok=True)
                file_path = os.path.join(temp_dir, uploaded_file.name)
                
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                chunks = extract_chunks(file_path)
                vector_store = VectorStoreManager()
                vector_store.build_index(chunks)
                
                st.session_state.vector_store = vector_store
                st.session_state.messages = [{"role": "assistant", "content": "Document processed! How can I help you?"}]
                
            st.success("Document processed!")

# --- Main Chat Interface ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if st.session_state.vector_store is None:
        with st.chat_message("assistant"):
            st.warning("Please upload a document first.")
    else:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                vector_store = st.session_state.vector_store
                llm_handler = st.session_state.llm_handler

                context_chunks = vector_store.search(prompt, top_k=7)
                response = llm_handler.generate_answer(prompt, context_chunks)
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})