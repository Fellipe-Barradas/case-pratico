from sqlmodel import Session, select
from models import TipoEmail


class TipoEmailRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, tipo_email: TipoEmail):
        self.session.add(tipo_email)
        self.session.commit()
        self.session.refresh(tipo_email)
        return tipo_email

    def get_by_tipo(self, tipo: str):
        statement = select(TipoEmail).where(TipoEmail.nome == tipo)
        return self.session.exec(statement).first()

    def get_all(self):
        statement = select(TipoEmail)
        return self.session.exec(statement).all()

    def update(self, tipo_email: TipoEmail):
        self.session.merge(tipo_email)
        self.session.commit()
        return tipo_email

    def delete(self, tipo_email: TipoEmail):
        self.session.delete(tipo_email)
        self.session.commit()