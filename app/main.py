from fastapi import FastAPI, Request, Response
import urllib.parse
from twilio.twiml.messaging_response import MessagingResponse
import sys
import os

# Ensure the root project directory is in the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.dialog_manager import process_message

app = FastAPI(title="Multilingual Welfare Chatbot")

@app.get("/")
def health_check():
    return {"status": "active", "message": "Welfare Chatbot is running"}

@app.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    """
    Webhook endpoint to handle incoming WhatsApp messages from Twilio.
    """
    # Twilio sends data as form-urlencoded
    body = await request.body()
    form_data = urllib.parse.parse_qs(body.decode('utf-8'))
    
    # Extract phone number and message body safely
    sender_number = form_data.get('From', [''])[0]
    incoming_msg = form_data.get('Body', [''])[0].strip()
    
    print(f"Received message from {sender_number}: {incoming_msg}")
    
    if not incoming_msg:
        response_text = "Please send a valid message."
    else:
        # Process through our Dialog Manager and LangChain
        try:
            response_text = process_message(sender_number, incoming_msg)
        except Exception as e:
            print(f"Error processing message: {e}")
            response_text = "Sorry, I am facing some technical difficulties right now. Please try again later."
    
    # Format response for Twilio
    twiml = MessagingResponse()
    twiml.message(response_text)
    
    return Response(content=str(twiml), media_type="application/xml")
