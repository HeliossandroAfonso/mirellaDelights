import enum
from sqlalchemy import Column, Integer, ForeignKey, Numeric, Enum, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class StatusPedido(enum.Enum):
    PENDENTE = "PENDENTE"
    PAGO = "PAGO"
    ENTREGUE = "ENTREGUE"
    CANCELADO = "CANCELADO"


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column("id",Integer, primary_key=True, index=True)
    usuarioId = Column("usuarioId", Integer, ForeignKey("usuarios.id"),nullable=False)
    status = Column("status", Enum(StatusPedido),default=StatusPedido.PENDENTE,nullable=False)
    total = Column("total", Numeric(10, 2), nullable=False)
    formaPagamento = Column("formaPAgamento",String, nullable=False)

    # Relacionamentos com usuario
    usuario = relationship("Usuario", back_populates="pedidos")

    itens = relationship("ItemPedido", back_populates="pedido", cascade="all, delete")
