📄 DocuQuery AI 🤖

DocuQuery AI is an intelligent, conversational document analysis tool. It leverages Large Language Models (LLMs) to allow users to "chat with their documents," transforming dense, unstructured PDFs into an interactive Q&A experience.

📖 Description

This project was designed to solve the challenge of extracting specific, contextual information from large documents like insurance policies, legal contracts, or HR manuals. Instead of manually searching through pages of text, users can simply upload a document and ask questions in plain English. The system uses a Retrieval-Augmented Generation (RAG) pipeline to find the most relevant information and generate accurate, easy-to-understand answers.

✨ Features

Interactive Chat Interface: A polished, modern dark-mode UI built with Streamlit that provides a user-friendly experience similar to ChatGPT or Gemini.

Dynamic Document Upload: Users can upload any PDF document directly through the web interface for analysis.

Accurate Q&A Backend: Utilizes a powerful LLM backend (configurable for providers like Google Gemini or Anthropic Claude) to understand and answer complex questions.

Semantic Search: Implements a FAISS vector database with sentence-transformers embeddings to find the most semantically relevant clauses, going beyond simple keyword matching.

Robust and Reliable: The application is built with production-ready practices, including handling for API rate limits and timeouts.

🛠️ Tech Stack

Application Framework: Python, Streamlit

LLM Backend: Google Gemini (gemini-1.5-flash) / Anthropic Claude (claude-3-haiku)

NLP & Search: sentence-transformers, faiss-cpu

Document Processing: PyMuPDF

🚀 Getting Started

Follow these instructions to set up and run the project locally.

1. Prerequisites
Python 3.9+

A valid API key from Google AI Studio or Anthropic.

2. Installation
Clone the repository to your local machine:

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

Create and activate a Python virtual environment:

# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

Install the required dependencies:

pip install -r requirements.txt

Create a .env file in the root directory and add your API key. For example, if using Google:

GOOGLE_API_KEY="YOUR_API_KEY_HERE"


3. Running the Application
Run the Streamlit application from your terminal:

streamlit run app.py

Your web browser will automatically open a new tab with the DocuQuery AI chat interface.


🔮 Future Scope
This project has a strong foundation that can be extended with several advanced features:

Integrate Local LLMs with Ollama: To enhance privacy and remove reliance on third-party APIs, the application can be modified to use a local LLM server like Ollama. This would allow the entire system to run offline in a secure environment, making it ideal for handling sensitive documents without any data leaving the user's machine.

Enhanced Explainability: Modify the UI to display the source page numbers and text snippets directly alongside each answer, providing full clause traceability.

Implement a Reranker: Add a cross-encoder model after the initial retrieval step to re-rank the search results for even higher accuracy on difficult or ambiguous questions.

Multi-Document Support: Allow users to upload multiple documents into a single session and ask questions that require synthesizing information from all of them.

Support for More File Types: Extend the document_processor to handle .docx and .txt files in addition to PDFs.
