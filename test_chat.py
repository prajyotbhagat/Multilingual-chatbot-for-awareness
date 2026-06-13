import os
import sys
from dotenv import load_dotenv

# Ensure the project root is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

from src.dialog_manager import process_message

def run_tests():
    print("Initializing test session...")
    test_number = "whatsapp:+1234567890"
    
    print("\n--- TEST 1: Hindi query about farmers ---")
    query1 = "मुझे किसान योजना चाहिए, मेरा aadhaar card है"
    print(f"User: {query1}")
    response1 = process_message(test_number, query1)
    print(f"Bot:\n{response1}")
    
    print("\n--- TEST 2: Follow-up answering Yes ---")
    query2 = "हाँ, मेरी उम्र ३५ है।"
    print(f"User: {query2}")
    response2 = process_message(test_number, query2)
    print(f"Bot:\n{response2}")

    print("\n--- TEST 3: Tamil query about unorganized sector ---")
    test_number2 = "whatsapp:+0987654321"
    query3 = "நான் ஒரு தச்சுத் தொழிலாளி, எனக்கு எந்தத் திட்டம் உதவும்?"
    print(f"User: {query3}")
    response3 = process_message(test_number2, query3)
    print(f"Bot:\n{response3}")

if __name__ == "__main__":
    run_tests()
