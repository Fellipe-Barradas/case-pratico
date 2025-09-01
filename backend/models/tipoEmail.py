from sqlmodel import SQLModel, Field

class TipoEmail(SQLModel, table=True):
    __tablename__ = "tipos_email"

    id: int = Field(default=None, primary_key=True)
    nome: str = Field(nullable=False, max_length=100)
