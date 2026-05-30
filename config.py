import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

FRAME_INTERVAL = 5

OUTPUT_AUDIO_DIR = "audio/temp"