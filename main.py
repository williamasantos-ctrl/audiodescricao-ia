import os
from google import genai
import cv2
import time
import queue
import threading
import subprocess
import edge_tts
import asyncio
import pygame
import whisper
from PIL import Image

# Importando todas as variáveis do config.py (certifique-se que o config.py está corrigido)
from config import GEMINI_API_KEY, FRAME_INTERVAL, OUTPUT_AUDIO_DIR
from prompts import SYSTEM_PROMPT

client = genai.Client(
    api_key=str(GEMINI_API_KEY)
)

pygame.init()
pygame.mixer.init()

async def speak(text):

    try:

        print("[TTS]", text)

        outfile = f"audio/temp/{int(time.time()*1000)}.mp3"

        communicate = edge_tts.Communicate(
            text,
            voice="pt-BR-FranciscaNeural"
        )

        await communicate.save(outfile)

        pygame.mixer.music.load(outfile)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)

        pygame.mixer.music.unload()

        if os.path.exists(outfile):
            os.remove(outfile)

    except Exception as e:

        print("ERRO SPEAK:", e)

# Carregando o modelo Whisper (este processo é lento na primeira vez)
print("[INFO] Carregando modelo Whisper...")
#whisper_model = whisper.load_model("base")

# =========================================
# CRIA PASTAS
# =========================================
# Corrigido: Usando a variável do config.py
os.makedirs(OUTPUT_AUDIO_DIR, exist_ok=True)
os.makedirs("frames", exist_ok=True)

# =========================================
# FILAS
# =========================================
frame_queue = queue.Queue(maxsize=1)
speech_queue = queue.Queue()

def analyze_worker():

    while True:

        print("[WORKER] esperando frame")
        frame = frame_queue.get()
        print("[WORKER] frame recebido")
        if frame is None:
            break

        try:

            print("[DEBUG] worker recebeu frame")
            print("shape:", frame.shape)

            small = cv2.resize(frame,(320,180))

            frame_rgb = cv2.cvtColor(
                small,
                cv2.COLOR_BGR2RGB
            )

            image = Image.fromarray(
                frame_rgb
            )

            print("[DEBUG] enviando frame para Gemini")

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    SYSTEM_PROMPT,
                    image
                ]
            )

            print("[DEBUG] Gemini respondeu")

            text = response.text.strip()

            print("[IA]", text)

            speech_queue.put(text)

        except Exception as e:

            print("ERRO GEMINI:",e)

        finally:

            frame_queue.task_done()
# =========================================
# FUNÇÃO FALAR (Worker)
# =========================================
def speak_worker():

    last_text = ""

    while True:

        text = speech_queue.get()

        if text is None:
            speech_queue.task_done()
            break

        if text == last_text:
            speech_queue.task_done()
            continue

        last_text = text

        try:

            print("[VOICE]", text)

            asyncio.run(
                speak(text)
            )

        except Exception as e:

            print("ERRO TTS:", e)

        finally:

            speech_queue.task_done()
# =========================================
# ABRIR VIDEO E OBTER STREAM
# =========================================
def open_video(source):
    # YouTube ou TikTok
    if (
        "youtube.com" in source
        or "youtu.be" in source
        or "tiktok.com" in source
    ):
        print("[INFO] Obtendo stream de vídeo online...")
        # Certifique-se que yt-dlp está no PATH
        cmd = [
            "yt-dlp",
            "-g",
            source
        ]
        result = subprocess.check_output(
            cmd
        ).decode().strip()
        
        source = result.split("\n")[0] # Pega o primeiro link de stream

    cap = cv2.VideoCapture(
        source,
        cv2.CAP_FFMPEG
    )
    return cap

# =========================================
# LOOP PRINCIPAL DO VIDEO (Exibição e Captura)
# =========================================
def video_loop(source):

    cap = open_video(source)

    if not cap.isOpened():
        print("ERRO AO ABRIR VIDEO")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps <= 0:
        fps = 30

    frame_delay = 1/fps

    last_capture = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            print("[STREAM FINALIZADO]")
            break

        cv2.imshow("VIDEO", frame)

        now = time.time()

        if now-last_capture >= FRAME_INTERVAL:

            last_capture = now

            if not frame_queue.full():

                frame_queue.put(frame.copy())

                print("[FRAME → IA]")

        time.sleep(frame_delay)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    print("[INFO] esperando IA terminar...")

    frame_queue.join()

# =========================================
# TRANSCRIÇÃO DE ÁUDIO (Whisper)
# =========================================
def transcribe_audio(video_path):
    # Correção: O Whisper precisa de um arquivo local. Não funcionará com streams URL do YouTube.
    if (
        "youtube.com" in video_path
        or "youtu.be" in video_path
        or "tiktok.com" in video_path
    ):
        print("[AVISO] Transcrição de áudio não disponível para links online diretamente no momento (requer download).")
        return

    if not os.path.exists(video_path):
        print(f"[ERRO] Arquivo de vídeo para transcrição não encontrado: {video_path}")
        return

    print(f"[INFO] Iniciando transcrição do áudio de: {video_path}...")
    #result = whisper_model.transcribe(
    #     video_path,
    #     language="pt" # Forçar português ajuda a precisão
    # )
    
    # print("\n[TRANSCRIÇÃO COMPLETA]\n")
    # print(result["text"])
    # print("-" * 20 + "\n")
    
    # Opcional: Adicionar a transcrição à fila de fala antes de começar o vídeo
    # speech_queue.put("Transcrição do áudio original: " + result["text"])

# =========================================
# MAIN (Ponto de Entrada)
# =========================================
def main():

    source = input(
        "Cole link YouTube/TikTok ou caminho de arquivo MP4 local: "
    ).strip()

    if not source:
        print("Entrada vazia.")
        return

    ai_thread = threading.Thread(
        target=analyze_worker,
        daemon=True
    )
    ai_thread.start()

    voice_thread = threading.Thread(
        target=speak_worker,
        daemon=True
    )
    voice_thread.start()

    transcribe_audio(source)

    # INICIA VIDEO
    video_loop(source)

    print("[INFO] encerrando...")

    print("[INFO] esperando IA terminar...")
    frame_queue.join()

    print("[INFO] esperando TTS terminar...")
    speech_queue.join()

    print("[INFO] encerrando workers...")

    frame_queue.put(None)
    speech_queue.put(None)

    ai_thread.join(timeout=2)
    voice_thread.join(timeout=2)
    

# =========================================
if __name__ == "__main__":
    main()