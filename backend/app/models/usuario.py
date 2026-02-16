import enum
from sqlalchemy import Column, Integer, String, Enum, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


class PerfilUsuario(enum.Enum):
    ADMIN = "ADMIN"
    USUARIO = "USUARIO"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key=True, index=True)
    nome = Column("nome", String, nullable=False)
    telefone = Column("telefone", String, nullable=False)
    email = Column("email", String, unique=True, nullable=False)
    morada = Column("morada", String, nullable=False)
    password = Column("password", String, nullable=False)
    perfil = Column("perfil", Enum(PerfilUsuario),default=PerfilUsuario.USUARIO,nullable=False)
    activo = Column("activo", Boolean, default=True)

    # Relacionamento com a tabela pedido
    pedidos = relationship("Pedido", back_populates="usuario", cascade="all, delete")
