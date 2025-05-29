import os
import time
import requests

from celery.utils.log import get_task_logger
from core.celery import celery_app
from core.config import get_settings
from sqlmodel import Session
from core.db import engine
from api.repositories import AudienceRepository, TriggerRepository

from openai import OpenAI

logger = get_task_logger(__name__)
settings = get_settings()


@celery_app.task()
def image_generation(image_prompt: str, file_name: str, table_name: setattr, id: str):
    openai = OpenAI(api_key=settings.OPENAI_API_KEY)
    retries = 5
    image_bytes = None

    for _ in range(retries):
        try:
            logger.info(f"Iniciando geração da img→ {file_name}")
            start_time = time.time()
            response = openai.images.generate(
                model="dall-e-3",
                prompt=f"Create a widescreen, 16:9, photorealistic, photographic image using this reference: {image_prompt}.",
                size="1792x1024",
                quality="hd",
                n=1,
            )
            end_time = time.time()

            duration = end_time - start_time
            logger.info(f"Geração levou {duration:.2f}s para img {file_name}")
            image_bytes = response.data[0].url
            print(f"Imagem gerada: {image_bytes}")
            break

        except Exception as e:
            error_message = str(e)
            headers = getattr(e, "headers", {})
            logger.info(headers)
            if "rate_limit_exceeded" in error_message or "429" in error_message:

                reset_time = headers.get("x-ratelimit-reset-requests", "60")

                time.sleep(int(reset_time))
            else:
                logger.info(f"Erro inesperado: {error_message}")
                raise e

    if not image_bytes:
        logger.info(
            f"Falha ao gerar a imagem para o {file_name} após várias tentativas."
        )
        return

    output_folder = "./images/"
    output_file = f"{file_name}"
    os.makedirs(output_folder, exist_ok=True)
    file_path = os.path.join(output_folder, output_file)
    with open(file_path, "wb") as file:
        file.write(requests.get(image_bytes).content)

    session = Session(engine)
    try:
        if table_name == "audience":
            AudienceRepository.update_audience_image_url(
                audience_id=id,
                image_url=file_name,
                session=session,
            )
        else:
            TriggerRepository.update_trigger_image_url(
                trigger_id=id,
                image_url=file_name,
                session=session,
            )

    except Exception as e:
        logger.info(f"Erro ao salvar a imagem {file_name}: {e}")

    finally:
        session.close()
