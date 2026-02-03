import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

headers = {
    "Content-Type": "application/json"
}

data = {
    "contents": [{
        "parts": [{"text": "Hello, work?"}]
    }]
}

try:
    print(f"Sending request to {URL[:50]}...")
    response = requests.post(URL, headers=headers, json=data, timeout=10)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Response Success!")
        print(response.json())
    else:
        print("Response Failed!")
        print(response.text)

except Exception as e:
    print(f"An error occurred: {e}")
