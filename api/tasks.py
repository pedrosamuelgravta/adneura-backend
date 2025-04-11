# api/tasks.py
import os
import requests
import time
from celery import shared_task  # type: ignore
from django.conf import settings
from openai import OpenAI
from api.models import Trigger, Audience


@shared_task(bind=True, max_retries=5)
def generate_trigger_image(self, text, brand_id, audience_id, trigger_id):
    client = OpenAI()
    client.api_key = settings.OPENAI_API_KEY

    retries = 5
    image_url = None

    for _ in range(retries):
        try:
            start_time = time.time()
            response = client.images.generate(
                model="dall-e-3",
                prompt=text,
                size="1792x1024",
                n=1,
            )
            end_time = time.time()

            duration = end_time - start_time
            print(f"A geração da imagem trigger levou {duration:.2f} segundos.")

            image_url = response.data[0].url
            break

        except Exception as e:
            error_message = str(e)
            if "rate_limit_exceeded" in error_message or "429" in error_message:
                print(
                    "Rate limit exceeded. Aguardando 60 segundos antes de tentar novamente..."
                )
                raise self.retry(exc=e, countdown=60)
            else:
                print(f"Erro inesperado: {error_message}")
                raise e

    if not image_url:
        print(
            f"Falha ao gerar a imagem para trigger {trigger_id} após várias tentativas."
        )
        return

    output_folder = "./images/"
    output_file = f"B{brand_id}A{audience_id}T{trigger_id}img.jpg"
    os.makedirs(output_folder, exist_ok=True)
    file_path = os.path.join(output_folder, output_file)

    try:
        with open(file_path, "wb") as file:
            file.write(requests.get(image_url).content)
        print(f"Imagem do trigger {trigger_id} salva com sucesso!")

        Trigger.objects.filter(id=trigger_id).update(trigger_img=output_file)
    except Exception as e:
        print(f"Erro ao salvar a imagem do trigger {trigger_id}: {e}")


@shared_task
def generate_audience_image(text, brand_id, audience_id):
    client = OpenAI()
    client.api_key = settings.OPENAI_API_KEY

    retries = 5

    for _ in range(retries):
        try:
            start_time = time.time()
            response = client.images.generate(
                model="dall-e-3",
                prompt=text,
                size="1792x1024",
                n=1,
            )
            end_time = time.time()

            duration = end_time - start_time
            print(f"A geração da imagem levou {duration:.2f} segundos.")

            image_url = response.data[0].url
            break

        except Exception as e:
            error_message = str(e)

            if "rate_limit_exceeded" in error_message or "429" in error_message:
                headers = getattr(e, "headers", {})

                # Obtém tempo de reset dos cabeçalhos da resposta
                reset_time = headers.get("x-ratelimit-reset-requests", "60")

                time.sleep(
                    int(reset_time)
                )  # Aguarda o tempo necessário antes da próxima tentativa
            else:
                print(f"Erro inesperado: {error_message}")
                raise e

    output_folder = "./images/"
    output_file = f"B{brand_id}A{audience_id}img.jpg"
    os.makedirs(output_folder, exist_ok=True)
    file_path = os.path.join(output_folder, output_file)

    try:
        with open(file_path, "wb") as file:
            file.write(requests.get(image_url).content)
            print("Image saved on DB")

            Audience.objects.filter(id=audience_id).update(audience_img=output_file)
    except Exception as e:
        print(f"Erro ao salvar a imagem da audiência {audience_id}: {e}")
