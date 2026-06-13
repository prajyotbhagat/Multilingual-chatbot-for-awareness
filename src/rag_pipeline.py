import json
import os
from dotenv import load_dotenv

load_dotenv()

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

FAISS_INDEX_PATH = "data/faiss_index"

def load_schemes_data():
    if not os.path.exists("data/schemes.json"):
        return []
    with open("data/schemes.json", "r", encoding="utf-8") as f:
        return json.load(f)

from typing import List
import torch
from transformers import AutoModel, AutoTokenizer
from langchain_core.embeddings import Embeddings

class IndicBertEmbeddings(Embeddings):
    def __init__(self, model_name="ai4bharat/indic-bert"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings = []
        for text in texts:
            inputs = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
            with torch.no_grad():
                outputs = self.model(**inputs)
                embedding = outputs.last_hidden_state.mean(dim=1).squeeze().tolist()
            embeddings.append(embedding)
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]

# Singleton instance
global_embeddings = None

def get_embeddings():
    global global_embeddings
    if global_embeddings is None:
        print("Loading IndicBERT Embeddings Model into memory...")
        global_embeddings = IndicBertEmbeddings()
    return global_embeddings

def build_vector_store():
    schemes = load_schemes_data()
    if not schemes:
        print("No scheme data found. Please run the crawler first.")
        return None

    documents = []
    for scheme in schemes:
        # Create a rich text document for embedding
        content = f"Scheme Name: {scheme['title']}\n"
        content += f"Details: {scheme.get('content', '')}\n"
        
        doc = Document(
            page_content=content,
            metadata={"url": scheme['url'], "title": scheme['title']}
        )
        documents.append(doc)

    embeddings = get_embeddings()
    
    print("Building FAISS index...")
    vector_store = FAISS.from_documents(documents, embeddings)
    
    os.makedirs("data", exist_ok=True)
    vector_store.save_local(FAISS_INDEX_PATH)
    print("FAISS index built and saved locally.")
    return vector_store

def get_retriever():
    embeddings = get_embeddings()
    if os.path.exists(FAISS_INDEX_PATH):
        vector_store = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
    else:
        print("FAISS index not found. Building it now...")
        vector_store = build_vector_store()
    
    if vector_store:
        return vector_store.as_retriever(search_kwargs={"k": 2})
    return None

def retrieve_context(query: str) -> str:
    retriever = get_retriever()
    if not retriever:
        return "No scheme information available."
        
    docs = retriever.invoke(query)
    context = "\n\n".join([f"--- {doc.metadata['title']} ---\n{doc.page_content}" for doc in docs])
    return context

if __name__ == "__main__":
    build_vector_store()
