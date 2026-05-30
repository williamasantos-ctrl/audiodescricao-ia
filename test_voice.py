import asyncio
import edge_tts
import pygame

async def main():

    communicate = edge_tts.Communicate(
        "Teste de áudio funcionando.",
        voice="pt-BR-FranciscaNeural"
    )

    await communicate.save(
        "teste.mp3"
    )

    pygame.init()
    pygame.mixer.init()

    pygame.mixer.music.load(
        "teste.mp3"
    )

    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        await asyncio.sleep(0.1)

asyncio.run(main())