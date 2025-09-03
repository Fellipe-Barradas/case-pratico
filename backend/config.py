from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from typing import Generator
from dotenv import load_dotenv
import os

load_dotenv()

database_name = os.getenv("DATABASE_NAME")
database_user = os.getenv("DATABASE_USER")
database_password = os.getenv("DATABASE_PASSWORD")
database_host = os.getenv("DATABASE_HOST")
database_port = os.getenv("DATABASE_PORT", "5432")  

database_url = f"postgresql+psycopg2://{database_user}:{database_password}@{database_host}:{database_port}/{database_name}"

# Criar engine síncronos
engine = create_engine(database_url, echo=True, pool_size=3, max_overflow=0)

# Funções síncronas para criar/deletar tabelas
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
        
def drop_db_and_tables():
    SQLModel.metadata.drop_all(engine)
    
# Função síncrona para obter sessão
def get_session() -> Generator[Session, None, None]:
    session = sessionmaker(
        engine, class_=Session, expire_on_commit=False
    )()
    try:
        yield session
    finally:
        session.close()