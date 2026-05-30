from config import GEMINI_API_KEY
from google import genai
client = genai.Client(
    api_key=GEMINI_API_KEY
)
response = client.models.generate_content(
    model='gemini-2.5-flash',
    messages=[
        {
            'role':'user',
            'content':'Descreva a imagem.',
            'images':['test.jpg']
        }
    ]
)

print(response['message']['content'])