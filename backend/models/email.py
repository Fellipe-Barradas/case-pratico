from sqlmodel import SQLModel, Field
from datetime import datetime


class Email(SQLModel, table=True):
    __tablename__ = "emails"
    
    id: int = Field(default=None, primary_key=True)
    assunto: str = Field(nullable=False, max_length=255)
    resposta: str | None = Field(default=None, max_length=255)
    tipo_email_id: int | None = Field(foreign_key="tipos_email.id", nullable=True, default=None)
    criado_em: datetime | None = Field(default=None)