import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

base_url = "https://generativelanguage.googleapis.com/v1beta"
variations = [
    f"{base_url}/models/gemini-1.5-flash:generateContent",
    f"{base_url}/gemini-1.5-flash:generateContent",
    f"{base_url}/models/models/gemini-1.5-flash:generateContent"
]

print("--- URL VARIATION TEST ---")
for url in variations:
    full_url = f"{url}?key={api_key}"
    print(f"Testing URL: {url} ...")
    payload = {"contents": [{"parts": [{"text": "Hi"}]}]}
    try:
        response = requests.post(full_url, json=payload)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("SUCCESS!")
        else:
            print(f"Response: {response.text[:100]}")
    except Exception as e:
        print(f"Error: {e}")
print("--- END TEST ---")
