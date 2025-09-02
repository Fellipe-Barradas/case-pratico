from fastapi import Depends, FastAPI
from models import Email
from contextlib import asynccontextmanager
from config import create_db_and_tables
from repository import EmailRepository, TipoEmailRepository
from fastapi.middleware.cors import CORSMiddleware
from dependencies import get_email_repository, get_tipo_email_repository
from script.ia import get_tipo_email
from datetime import datetime


@asynccontextmanager
async def lifespan(app: FastAPI):
    # drop_db_and_tables()  # Drop tables if they exist
    create_db_and_tables()
    yield

app = FastAPI(title="Classificador de Emails", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou ["*"] com cuidado
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/analisar-email")
def analisar_email(email: str, email_repository: EmailRepository = Depends(get_email_repository), tipo_email_repository: TipoEmailRepository = Depends(get_tipo_email_repository)):
    resposta_agente = get_tipo_email(email)
    tipo = tipo_email_repository.get_by_tipo(resposta_agente["tipo"])
    email = Email(assunto=email, tipo_email_id=tipo.id, resposta=resposta_agente["resposta"], criado_em=datetime.now())
    email_repository.create(email)
    return {email}

@app.get("/obter-emails")
def obter_emails(size: int = 10, step: int = 1, tipo_email_id: int | None = None, email_repository: EmailRepository = Depends(get_email_repository)):
    return {"data": email_repository.get_all(step=step, limit=size, tipo_email_id=tipo_email_id)}

@app.get("/tipos-email")
def obter_tipos_email(tipo_email_repository: TipoEmailRepository = Depends(get_tipo_email_repository)):
    return {"data": tipo_email_repository.get_all()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)