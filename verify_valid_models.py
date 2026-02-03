import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Candidates from model_list.txt
candidates = [
    "gemini-2.0-flash-lite",
    "gemini-flash-latest",
    "gemini-2.5-flash",
    "gemini-2.0-flash-001"
]

print("--- START CHECK ---")
for model in candidates:
    print(f"Testing {model}...")
    # Note: verify_model.py previously established that we need 'models/' prefix in the URL path if the model name doesn't have it?
    # Actually, the list says 'Name: models/gemini-...'
    # So we should probably use the full name in the URL if we construct it manually, or just the ID if the SDK handles it.
    # REST URL pattern: https://generativelanguage.googleapis.com/v1beta/models/{MODEL_ID}:generateContent
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": "Hi"}]}]}
    try:
        response = requests.post(url, json=payload)
        status = response.status_code
        print(f"Status: {status}")
        if status == 200:
            print(f"SUCCESS: {model} worked!")
            print(f"Response: {response.text[:50]}...")
            break
        else:
            print(f"FAILED: {model} -> {status}")
            if status == 404:
                print("  (Not Found)")
            elif status == 429:
                print("  (Quota/Rate Limit)")
                # Check if it's "Limit 0" or just rate limit
                if "limit: 0" in response.text.lower():
                     print("  (Limit 0 - No Access)")
                else:
                     print("  (Rate Limit - Access Exists!)")
                     # If it's just rate limit, this IS a valid model, just busy.
                     print(f"SUCCESS (Likely): {model} is valid but rate limited.")
                     break
    except Exception as e:
        print(f"ERROR: {model} -> {e}")
print("--- END CHECK ---")
