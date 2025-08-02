# main.py
import logging
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import os
import hashlib
import asyncio
from typing import List, Dict

from document_processor import extract_chunks
from vector_store import VectorStoreManager
from llm_handler import AnswerGenerator

# --- Application Setup ---
app = FastAPI(
    title="LLM-Powered Intelligent Query–Retrieval System (with Explainability)",
    description="API for the HackRX hackathon.",
    version="2.0.0"
)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
EXPECTED_TOKEN = "465488d927b070624076252e730f616f29634c9c97e10863aacb4c4b0e2e80e2"
CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)
LOCAL_PDF_PATH = "policy.pdf"

# --- Pydantic Models for Enhanced Output ---
class Source(BaseModel):
    page: int
    text: str

class Answer(BaseModel):
    answer: str
    sources: List[Source]

class QueryRequest(BaseModel):
    documents: str
    questions: list[str]

class AnswerResponse(BaseModel):
    answers: List[Answer]

# --- Global instances ---
vector_store = VectorStoreManager()
llm_handler = AnswerGenerator()

# --- Helper function returns both answer and sources ---
async def process_question(question: str, semaphore: asyncio.Semaphore) -> Dict:
    async with semaphore:
        logging.info(f"Processing question: '{question[:30]}...'")
        
        def run_blocking_tasks():
            context_chunks = vector_store.search(question, top_k=5) # Using 5 sources for a cleaner output
            logging.info(f"Context for '{question[:30]}...': Pages {[c['metadata']['page'] for c in context_chunks]}")
            answer_text = llm_handler.generate_answer(question, context_chunks)
            return {"answer": answer_text, "sources": context_chunks}
        
        result = await asyncio.to_thread(run_blocking_tasks)
        return result

# --- API Endpoint ---
@app.post("/api/v1/hackrx/run", response_model=AnswerResponse)
async def run_submission(request: QueryRequest, Authorization: str = Header(None)):
    if Authorization != f"Bearer {EXPECTED_TOKEN}":
        raise HTTPException(status_code=401, detail="Invalid authorization token")

    if not os.path.exists(LOCAL_PDF_PATH):
        raise HTTPException(status_code=404, detail=f"Local file not found: {LOCAL_PDF_PATH}.")

    cache_path = os.path.join(CACHE_DIR, "local_policy.pkl")
    if not os.path.exists(cache_path):
        logging.info(f"Processing local file: {LOCAL_PDF_PATH}")
        chunks = extract_chunks(LOCAL_PDF_PATH)
        vector_store.build_index(chunks)
        vector_store.save_index(cache_path)
        logging.info(f"Index built and saved to cache: {cache_path}")
    else:
        if vector_store.index is None:
            logging.info(f"Loading cached index from: {cache_path}")
            vector_store.load_index(cache_path)

    semaphore = asyncio.Semaphore(2)
    tasks = [process_question(q, semaphore) for q in request.questions]
    results = await asyncio.gather(*tasks)

    # Format the results into the new Pydantic models
    final_answers = []
    for res in results:
        sources_list = [Source(page=s['metadata']['page'], text=s['text']) for s in res['sources']]
        final_answers.append(Answer(answer=res['answer'], sources=sources_list))
        
    return AnswerResponse(answers=final_answers)