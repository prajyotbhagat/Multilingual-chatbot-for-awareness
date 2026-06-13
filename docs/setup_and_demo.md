# Setup and Demo Guide

## Local Testing
1. Ensure dependencies are installed (`pip install -r requirements.txt`).
2. Populate the `.env` file with your `GOOGLE_API_KEY` and Twilio credentials.
3. Run the crawler to fetch the scheme data: `python src/crawler.py`
4. Build the vector store (it builds automatically on first run, but you can trigger it): `python src/rag_pipeline.py`
5. Start the FastAPI server: `uvicorn app.main:app --reload`

## Connecting to WhatsApp (Twilio Sandbox)
1. Sign up for Twilio and activate the WhatsApp Sandbox.
2. Expose your local port 8000 using ngrok: `ngrok http 8000`
3. Copy the ngrok forwarding URL (e.g., `https://xxxx.ngrok.io`).
4. In the Twilio Sandbox configuration, paste the URL appended with `/whatsapp` (e.g., `https://xxxx.ngrok.io/whatsapp`) into the "WHEN A MESSAGE COMES IN" webhook field.
5. Save the configuration.
6. Send the join code to the Twilio Sandbox number from your WhatsApp app.
7. Send a message like "I am a 35 year old farmer, what schemes am I eligible for?" to start interacting.

## Deployment to Render / Hugging Face Spaces
- Use the included `Dockerfile` to deploy directly to Render Web Services or as a Hugging Face Docker Space.
- Ensure all environment variables from `.env.example` are securely added in the platform's secret manager.
