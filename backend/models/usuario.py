import enum
from sqlalchemy import create_engine, String, Integer, Column, Enum
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv

class PerfilUsuario(enum.Enum):
    ADMIN = "ADMIN"
    USUARIO = "USUARIO"

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo= True)

Base = declarative_base()


class Usuario(Base):
    __tablename__="usuario"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable=False)
    telefone = Column("telefone", String, nullable=False)
    email = Column("email", String, nullable=False)
    morada = Column("morada", String, nullable=False)
    perfil = Column("perfil", Enum(PerfilUsuario), nullable=False, default=PerfilUsuario.USUARIO)
    password = Column("password", String, nullable=False)
    
    def __init__(self, nome, telefone, email, morada, password, perfil=PerfilUsuario.USUARIO):
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.morada = morada
        self.password = password
        self.perfil = perfil
        