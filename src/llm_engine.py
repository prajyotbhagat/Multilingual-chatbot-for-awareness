import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

def get_llm():
    # Make sure GOOGLE_API_KEY is set in the environment
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

def generate_response(user_input: str, chat_history: list, retrieved_context: str) -> str:
    llm = get_llm()
    system_prompt = """
You are a government welfare scheme awareness assistant for rural India.
Your goal is to help users find schemes they are eligible for and understand the application process.

CRITICAL INSTRUCTIONS:
1. STRICTLY answer ONLY using the provided scheme context. Do not hallucinate schemes or eligibility rules. If the context does not contain the answer, say "I don't have information about that specific scheme right now."
2. You must respond natively in the same language that the user used to ask the question. Keep your grammar simple and clear.
3. Be concise and format your response using WhatsApp-friendly markdown (e.g., *bold*, - bullet points).
4. Keep messages short (under 100 words per message).

CONTEXT:
{context}
"""
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("placeholder", "{chat_history}"),
        ("human", "{input}")
    ])
    
    chain = prompt_template | llm
    
    response = chain.invoke({
        "context": retrieved_context,
        "chat_history": chat_history,
        "input": user_input
    })
    
    return response.content
