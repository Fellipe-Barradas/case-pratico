from sqlmodel import Session
from models import TipoEmail


class TipoEmailRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, tipo_email: TipoEmail):
        self.session.add(tipo_email)
        self.session.commit()
        self.session.refresh(tipo_email)
        return tipo_email

    def read(self, tipo_email_id: int):
        return self.session.get(TipoEmail, tipo_email_id)

    def update(self, tipo_email: TipoEmail):
        self.session.merge(tipo_email)
        self.session.commit()
        return tipo_email

    def delete(self, tipo_email: TipoEmail):
        self.session.delete(tipo_email)
        self.session.commit()