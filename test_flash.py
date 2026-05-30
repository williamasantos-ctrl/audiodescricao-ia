from config import GEMINI_API_KEY
from google import genai

client = genai.Client(
    api_key=GEMINI_API_KEY
)

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Olá"
    )

    print(response.text)

except Exception as e:
    print(type(e))
    print(e)