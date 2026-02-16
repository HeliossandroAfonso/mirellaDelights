from pydantic import BaseModel
from decimal import Decimal

class ItemPedidoBase(BaseModel):
    produtoId: int
    quantidade: int
    precoUnitario: Decimal
    subtotal: Decimal


class ItemPedidoCriar(ItemPedidoBase):
    pedidoId: int

#Retorno do banco de dados
class ItemPedidoResponse(ItemPedidoBase):
    id: int
    pedidoId: int

    class Config:
        from_attributes = True
