import google.generativeai as genai
import os
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

class AnswerGenerator:
    """
    Handles prompt construction and interaction with the Google Gemini API.
    """
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        self.model_name = model_name
        try:
            if not api_key:
                raise ValueError("API key not provided to AnswerGenerator.")
            
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(model_name)

        except Exception as e:
            print(f"Failed to initialize Google client: {e}")
            self.model = None

    def generate_answer(self, question: str, context_chunks: List[Dict]) -> str:
        """Generates a well-summarized answer using the Gemini model with a timeout."""
        if not self.model:
            return "Could not generate an answer due to an API client initialization error."

        context = "\n---\n".join([f"Source: Page {chunk['metadata']['page']}\n{chunk['text']}" for chunk in context_chunks])
        
        prompt = f"""
        You are an expert AI assistant for insurance policy analysis. Your task is to answer the user's question based ONLY on the provided policy clauses.
        Follow these instructions carefully:
        1. Synthesize information from all relevant clauses into a single, cohesive answer.
        2. Write the answer in a complete, easy-to-understand paragraph.
        3. Do not just list facts. Summarize the key conditions and details.
        4. If the provided clauses do not contain the answer, explicitly state that the information is not available in the provided text.

        **Policy Clauses:**
        {context}

        **Question:**
        {question}
        """
        
        try:
            # Add a 60-second timeout to prevent the application from hanging
            response = self.model.generate_content(
                prompt,
                request_options={"timeout": 60}
            )
            return response.text.strip()
        except Exception as e:
            print(f"Detailed API Error for question '{question[:30]}...': {e}")
            return "Could not generate an answer due to an API error."