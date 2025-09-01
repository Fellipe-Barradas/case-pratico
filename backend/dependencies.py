from repository import EmailRepository, TipoEmailRepository
from config import Session, get_session
from fastapi import Depends

def get_email_repository(session: Session = Depends(get_session)) -> EmailRepository:
    return EmailRepository(session)

def get_tipo_email_repository(session: Session = Depends(get_session)) -> TipoEmailRepository:
    return TipoEmailRepository(session)