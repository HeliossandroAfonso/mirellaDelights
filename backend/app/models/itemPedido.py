from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.core.database import Base


class ItemPedido(Base):
    __tablename__ = "itensPedido"

    id = Column(Integer, primary_key=True, index=True)

    pedidoId = Column(
        Integer,
        ForeignKey("pedidos.id", ondelete="CASCADE"),
        nullable=False
    )

    produtoId = Column(
        Integer,
        ForeignKey("produtos.id"),
        nullable=False
    )

    quantidade = Column(Integer, nullable=False)
    precoUnitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)

    # 🔹 Relacionamentos
    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto", back_populates="itensPedido")
