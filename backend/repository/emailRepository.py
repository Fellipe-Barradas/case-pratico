from sqlmodel import Session
from models import Email


class EmailRepository:
    def __init__(self, session: Session):
        self.session = session

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