from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.itemPedido import ItemPedido
from app.models.pedido import Pedido
from app.models.produto import Produto
from app.schemas.itemPedidoSchema import (
    ItemPedidoCriar,
    ItemPedidoResponse
)

itemPedidoRouter = APIRouter(
    prefix="/itens-pedido",
    tags=["Itens do Pedido"]
)

#Criar item de pedido
@itemPedidoRouter.post("/", response_model=ItemPedidoResponse)
async def criarItemPedido(
    dados: ItemPedidoCriar,
    db: Session = Depends(get_db)
):
    # Verifica pedido
    pedido = db.query(Pedido).filter(Pedido.id == dados.pedidoId).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    # Verifica produto
    produto = db.query(Produto).filter(Produto.id == dados.produtoId).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    item = ItemPedido(
        pedidoId=dados.pedidoId,
        produtoId=dados.produtoId,
        quantidade=dados.quantidade,
        precoUnitario=dados.precoUnitario
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


# Listar itens de um pedido
@itemPedidoRouter.get("/pedido/{pedido_id}", response_model=list[ItemPedidoResponse])
async def listarPtensDoPedido(
    pedido_id: int,
    db: Session = Depends(get_db)
):
    itens = db.query(ItemPedido).filter(
        ItemPedido.pedidoId == pedido_id
    ).all()

    return itens


# Remover item
@itemPedidoRouter.delete("/{item_id}")
async def removerItem(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ItemPedido).filter(ItemPedido.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    # Devolve o estoque antes de deletar!
    produto = db.query(Produto).filter(Produto.id == item.produtoId).first()
    if produto:
        produto.estoque += item.quantidade
        
    # Ajusta o total do pedido
    pedido = db.query(Pedido).filter(Pedido.id == item.pedidoId).first()
    if pedido:
        pedido.total -= item.subtotal

    db.delete(item)
    db.commit()
    return {"msg": "Item removido e estoque devolvido"}
