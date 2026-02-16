from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
from enum import Enum


class StatusPedidoEnum(str, Enum):
    PENDENTE = "PENDENTE"
    PAGO = "PAGO"
    ENTREGUE = "ENTREGUE"
    CANCELADO = "CANCELADO"


# Item dentro do pedido
class ItemPedidoCreate(BaseModel):
    produtoId: int
    quantidade: int
    precoUnitario: Decimal


class ItemPedidoResponse(ItemPedidoCreate):
    id: int

    class Config:
        from_attributes = True


# Criar pedido
class PedidoCreate(BaseModel):
    formaPagamento: str
    itens: List[ItemPedidoCreate]


# Retorno do pedido
class PedidoResponse(BaseModel):
    id: int
    status: StatusPedidoEnum
    total: Decimal
    formaPagamento: str
    usuarioId: int
    itens: List[ItemPedidoResponse]

    class Config:
        from_attributes = True
