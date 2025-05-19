from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.models import Brand, User, Audience, StrategicGoal
from tasks.image import image_generation
from celery.result import AsyncResult
from core.celery import celery_app
from fastapi.middleware.cors import CORSMiddleware

from api.routers import *

from core.db import initialize_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting db...")
    initialize_db()
    yield
    print("Stopping db...")


app = FastAPI(lifespan=lifespan)

origins = ["http://localhost:5173", "https://homolog.gravta.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(brand_router)
app.include_router(audience_router)
app.include_router(strategic_goal_router)
app.include_router(trigger_router)
app.include_router(demographic_router)


@app.post("/mensagem/teste")
def simular_envio_em_lote():
    prompts = [
        "um gato astronauta",
        "um castelo em Marte",
        "uma xícara voadora",
        "um cachorro tocando violão",
        "um trem flutuando no espaço",
        "um sapo com capa de super-herói",
        "uma baleia voando sobre a cidade",
        "um dragão cozinhando",
        "um carro feito de chocolate",
        "um robô fazendo jardinagem",
        "um elefante surfando",
        "um pássaro cantando ópera",
        "um peixe pilotando um avião",
        "um urso dançando balé",
        "um leão jogando xadrez",
        "um coelho astronauta",
        "um gato de óculos",
        "um cachorro astronauta",
        "um gato de óculos com um livro na mão",
        "um gato de óculos com um livro na mão e uma xícara de café",
        "um gato de óculos com um livro na mão e uma xícara de café em uma mesa de café",
        "um gato de óculos com um livro na mão e uma xícara de café em uma mesa de café em um café",
        "um gato de óculos com um livro na mão e uma xícara de café em uma mesa de café em um café em Paris",
        "um gato de óculos com um livro na mão e uma xícara de café em uma mesa de café em um café em Paris com a Torre Eiffel ao fundo",
        "um gato de óculos com um livro na mão e uma xícara de café em uma mesa de café em um café em Paris com a Torre Eiffel ao fundo e um balão de ar quente",
        "um gato de óculos com um livro na mão e uma xícara de café em uma mesa de café em um café em Paris com a Torre Eiffel ao fundo e um balão de ar quente voando",
        "um gato de óculos com um livro na mão e uma xícara de café em uma mesa de café em um café em Paris com a Torre Eiffel ao fundo e um balão de ar quente voando sobre a cidade",
    ]

    tarefas = []
    for i, prompt in enumerate(prompts):
        task = image_generation.delay(f"User {i+1}", prompt)
        tarefas.append({"usuario": f"User {i+1}", "task_id": task.id})

    return {"mensagem": "Tasks enviadas", "tarefas": tarefas}


@app.get("/status/{task_id}")
def verificar_status(task_id: str):
    resultado = AsyncResult(task_id, app=celery_app)
    return {"status": resultado.status, "resultado": resultado.result}
