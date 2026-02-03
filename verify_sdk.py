import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

models_to_test = [
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-pro",
    "models/gemini-1.5-flash", 
    "models/gemini-pro"
]

print("--- SDK TEST START ---")
for m in models_to_test:
    print(f"Testing {m}...")
    try:
        model = genai.GenerativeModel(m)
        response = model.generate_content("Hello")
        print(f"SUCCESS: {m}")
        print(f"Response: {response.text}")
        break 
    except Exception as e:
        print(f"FAILED: {m} -> {e}")
print("--- SDK TEST END ---")
