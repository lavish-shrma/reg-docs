import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

with open("model_list.txt", "w") as f:
    try:
        for m in genai.list_models():
            if "generateContent" in m.supported_generation_methods:
                f.write(f"Name: {m.name}\n")
                f.write(f"Display: {m.display_name}\n")
                f.write(f"Description: {m.description}\n")
                f.write("-" * 20 + "\n")
    except Exception as e:
        f.write(f"Error: {e}\n")
print("Model list written to model_list.txt")
