from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.core.database import Base

class ItemPedido(Base):
    __tablename__ = "itensPedido"

    id = Column(Integer, primary_key=True, index=True)
    pedidoId = Column("pedidoId", Integer, ForeignKey("pedidos.id"), nullable=False)
    produtoId = Column("produtoId", Integer,ForeignKey("produtos.id"),nullable=False)
    quantidade = Column("quantidade", Integer, nullable=False)
    precoUnitario = Column("precoUnitario", Numeric(10, 2), nullable=False)

    # Relacionamentos com a tabela pedido
    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto", back_populates="itensPedido")
