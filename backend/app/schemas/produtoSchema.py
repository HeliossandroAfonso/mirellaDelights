from pydantic import BaseModel
from decimal import Decimal
from typing import Optional


class ProdutoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: Decimal
    estoque: int
    categoria: Optional[str] = None
    ativo: bool = True


class ProdutoCreate(ProdutoBase):
    pass

class ProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[Decimal] = None
    estoque: Optional[int] = None
    categoria: Optional[str] = None
    ativo: Optional[bool] = None


# Resposta
class ProdutoResponse(ProdutoBase):
    id: int

    class Config:
        from_attributes = True
