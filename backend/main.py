from fastapi import Depends, FastAPI
from repository import EmailRepository
from dependencies import get_email_repository, get_tipo_email_repository
app = FastAPI()

@app.get("/analisar-email")
def analisar_email(email: str, email_repository: EmailRepository = Depends(get_email_repository)):
    # Aqui você pode adicionar a lógica para analisar o email
    return {"email": email}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)