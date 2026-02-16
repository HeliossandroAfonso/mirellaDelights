from sqlalchemy import Column, Integer, String, Numeric, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


class Produto(Base):
    __tablename__ = "produtos"

    id = Column("id",Integer, primary_key=True, index=True)
    nome = Column("nome",String, nullable=False)
    descricao = Column("descricao",String)
    preco = Column("preco", Numeric(10, 2), nullable=False)
    estoque = Column("estoque", Integer, nullable=False, default=0)
    categoria = Column("categoria",String)
    ativo = Column("activo",Boolean, default=True)
   
    #  Relacionamento com a tabela item
    itensPedido = relationship("ItemPedido",back_populates="produto")
