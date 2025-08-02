# vector_store.py
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import numpy as np
import pickle
import os

class VectorStoreManager:
    """Manages vector embeddings and the FAISS index with save/load capabilities."""
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.chunks = []

    def build_index(self, chunks: List[Dict]):
        """Builds a FAISS index from the provided text chunks."""
        self.chunks = chunks
        texts = [chunk['text'] for chunk in chunks]
        embeddings = self.model.encode(texts, convert_to_numpy=True).astype('float32')
        
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)

    def save_index(self, path: str):
        """Saves the FAISS index and chunks to a file."""
        if self.index is None:
            raise RuntimeError("Index has not been built. Cannot save.")
        
        # Create a dictionary to hold both the index and the chunks
        data_to_save = {
            'index': faiss.serialize_index(self.index),
            'chunks': self.chunks
        }
        
        with open(path, 'wb') as f:
            pickle.dump(data_to_save, f)

    def load_index(self, path: str):
        """Loads the FAISS index and chunks from a file."""
        with open(path, 'rb') as f:
            data_loaded = pickle.load(f)
        
        self.index = faiss.deserialize_index(data_loaded['index'])
        self.chunks = data_loaded['chunks']

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Searches the index for the most relevant chunks."""
        if self.index is None:
            raise RuntimeError("Index has not been built or loaded. Call build_index() or load_index() first.")
            
        query_embedding = self.model.encode([query], convert_to_numpy=True).astype('float32')
        _, indices = self.index.search(query_embedding, top_k)
        
        return [self.chunks[i] for i in indices[0]]