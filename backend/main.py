
from fastapi import Depends, FastAPI, File, UploadFile, Form, HTTPException
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

from typing import Optional

@app.post("/analisar-email")
async def analisar_email(
    email: Optional[str] = Form(None),
    file: Optional[UploadFile] = None,
    email_repository: EmailRepository = Depends(get_email_repository),
    tipo_email_repository: TipoEmailRepository = Depends(get_tipo_email_repository)
):
    conteudo = email
    if file:
        if file.content_type == "application/pdf":
            import io
            from PyPDF2 import PdfReader
            pdf_bytes = await file.read()
            pdf_stream = io.BytesIO(pdf_bytes)
            reader = PdfReader(pdf_stream)
            conteudo = "\n".join(page.extract_text() or "" for page in reader.pages)
        elif file.content_type == "text/plain":
            conteudo = (await file.read()).decode("utf-8")
        else:
            raise HTTPException(status_code=400, detail="Tipo de arquivo não suportado")
    if not conteudo:
        raise HTTPException(status_code=400, detail="Nenhum conteúdo para analisar")
    resposta_agente = get_tipo_email(conteudo)
    tipo = tipo_email_repository.get_by_tipo(resposta_agente["tipo"])
    email_obj = Email(assunto=conteudo[:100], tipo_email_id=tipo.id, resposta=resposta_agente["resposta"], criado_em=datetime.now())
    email_repository.create(email_obj)
    return {"email": email_obj}

@app.get("/obter-emails")
def obter_emails(size: int = 10, step: int = 1, tipo_email_id: int | None = None, email_repository: EmailRepository = Depends(get_email_repository)):
    return {"data": email_repository.get_all(step=step, limit=size, tipo_email_id=tipo_email_id)}

@app.get("/tipos-email")
def obter_tipos_email(tipo_email_repository: TipoEmailRepository = Depends(get_tipo_email_repository)):
    return {"data": tipo_email_repository.get_all()}

@app.delete("/delete-email")
def delete_email(email_id: int, email_repository: EmailRepository = Depends(get_email_repository)):
    email_repository.delete(email_id)
    return {"message": "Email deletado com sucesso"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)