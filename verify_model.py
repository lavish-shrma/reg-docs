import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

candidates = [
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-1.0-pro",
    "gemini-pro",
    "gemini-2.0-flash-exp",
    "gemini-2.0-flash"
]

print("--- START CHECK ---")
for model in candidates:
    print(f"Testing {model}...")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": "Hi"}]}]}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"SUCCESS: {model} worked!")
            break
        else:
            print(f"FAILED: {model} -> {response.status_code} ({response.reason})")
            if response.status_code == 429:
                print("  (Quota Limit)")
            elif response.status_code == 404:
                print("  (Not Found)")
    except Exception as e:
        print(f"ERROR: {model} -> {e}")
print("--- END CHECK ---")
