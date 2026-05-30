from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

print("KEY OK")

for m in genai.list_models():
    print(m.name)