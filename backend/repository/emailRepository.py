from sqlmodel import Session, select
from models import Email, TipoEmail

class EmailRepository:
    def __init__(self, session: Session):
        self.session = session
    def get_all(self, step=1, limit=10, tipo_email_id=None):
        statement = select(Email, TipoEmail).where(Email.tipo_email_id == TipoEmail.id)
        if tipo_email_id is not None:
            statement = statement.where(Email.tipo_email_id == tipo_email_id)
        statement = statement.offset((step - 1) * limit).limit(limit)
        results = self.session.exec(statement).all()
        emails = []
        for email, tipo in results:
            emails.append({
                "id": email.id,
                "assunto": email.assunto,
                "resposta": email.resposta,
                "criado_em": email.criado_em,
                "tipo_email_id": email.tipo_email_id,
                "tipo_email": tipo.nome if hasattr(tipo, 'nome') else None
            })
        return emails

    def create(self, email: Email):
        self.session.add(email)
        self.session.commit()
        self.session.refresh(email)
        return email

    def read(self, email_id: int):
        return self.session.get(Email, email_id)

    def update(self, email: Email):
        self.session.merge(email)
        self.session.commit()
        return email

    def delete(self, email: Email):
        self.session.delete(email)
        self.session.commit()