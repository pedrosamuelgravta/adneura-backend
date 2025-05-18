import time
import random
from core.celery import celery_app


@celery_app.task(rate_limit="15/m")
def image_generation(usuario: str, prompt: str):
    print(f"[{usuario}] Simulando geração de imagem para o prompt: '{prompt}'")

    # Simula o tempo que a OpenAI demoraria para gerar a imagem
    delay = random.uniform(4, 6)  # Simula 4 a 6 segundos por geração
    time.sleep(delay)

    # Simula uma URL de imagem gerada
    fake_url = f"https://fake.cdn.openai.com/{usuario.replace(' ', '_')}_{int(time.time())}.png"

    print(f"[{usuario}] Imagem gerada em {delay:.2f}s: {fake_url}")
    return {"usuario": usuario, "prompt": prompt, "url": fake_url}
