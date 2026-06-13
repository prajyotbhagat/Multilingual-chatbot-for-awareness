from typing import Dict, List
from langchain_core.messages import HumanMessage, AIMessage
from src.rag_pipeline import retrieve_context
from src.llm_engine import generate_response

# Simple in-memory session store for prototype
# Key: phone number, Value: list of LangChain Messages
SESSIONS: Dict[str, List] = {}

def get_session_history(phone_number: str) -> List:
    if phone_number not in SESSIONS:
        SESSIONS[phone_number] = []
    return SESSIONS[phone_number]

def process_message(phone_number: str, user_input: str) -> str:
    history = get_session_history(phone_number)
    
    # Add user message to history
    history.append(HumanMessage(content=user_input))
    
    # 1. Retrieve relevant context from FAISS using the raw Indic query
    context = retrieve_context(user_input)
    
    # 2. Generate response natively via LLM
    final_response = generate_response(user_input, history[:-1], context)
    
    # Add AI response to history
    history.append(AIMessage(content=final_response))
    
    # Enforce 4-6 turn memory to keep context lightweight
    if len(history) > 12: # 6 user turns + 6 AI turns
        # Keep the latest 10 messages to remember immediate context, but trim oldest
        SESSIONS[phone_number] = history[-10:]
        
    return final_response
