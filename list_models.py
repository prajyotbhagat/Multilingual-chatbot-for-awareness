import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY")

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    models = [m['name'] for m in data.get('models', [])]
    print("SUCCESS! Available models:")
    for m in models:
        print(f" - {m}")
else:
    print(f"ERROR: {response.status_code}")
    print(response.text)
