from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from decimal import Decimal

from app.core.database import get_db
from app.models.pedido import Pedido, StatusPedido
from app.models.itemPedido import ItemPedido
from app.models.usuario import Usuario
from app.models.produto import Produto
from app.dependencias.dependencias import verificarToken
from app.schemas.pedidoSchema import PedidoCreate, PedidoResponse

pedidoRouter = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)

@pedidoRouter.post("/", response_model=PedidoResponse)
async def criarPedido(
    dados: PedidoCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(verificarToken)
):
    if not dados.itens:
        raise HTTPException(status_code=400, detail="Pedido sem itens")

    # 1. Inicia o pedido com total 0
    pedido = Pedido(
        usuarioId=usuario.id,
        status=StatusPedido.PENDENTE,
        formaPagamento=dados.formaPagamento,
        total=Decimal("0.00")
    )

    db.add(pedido)
    db.flush()  # Gera o ID do pedido para usarmos nos itens

    acumulador_total = Decimal("0.00")

    for item in dados.itens:
        # 2. Busca o produto e valida estoque
        #produto = db.query(Produto).filter(Produto.id == item.produtoId).first()
        produto = db.query(Produto).filter(Produto.id == item.produtoId).first()
        
        if not produto:
            db.rollback()
            raise HTTPException(status_code=404, detail=f"Produto {item.produtoId} não encontrado")
        
        if produto.estoque < item.quantidade:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Estoque insuficiente para {produto.nome}")

        # 3. Baixa o estoque do produto
        produto.estoque -= item.quantidade

        # 4. Calcula subtotal (usando o preço atual do banco por segurança)
        subtotal_item = produto.preco * item.quantidade
        acumulador_total += subtotal_item

        # 5. Cria o item vinculado ao pedido
        item_pedido = ItemPedido(
            pedidoId=pedido.id,
            produtoId=produto.id,
            quantidade=item.quantidade,
            precoUnitario=produto.preco,
            subtotal=subtotal_item     
        )
        db.add(item_pedido)

    # 6. Atualiza o total final do pedido com o que foi somado no loop
    pedido.total = acumulador_total
    
    db.commit()
    db.refresh(pedido)

    return pedido

@pedidoRouter.get("/meus", response_model=list[PedidoResponse])
async def listarMeusPedidos(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(verificarToken)
):
    pedidos = (
        db.query(Pedido)
        .filter(Pedido.usuarioId == usuario.id)
        .all()
    )

    return pedidos

@pedidoRouter.get("/{pedidoId}", response_model=PedidoResponse)
async def buscarPedido(
    pedidoId: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(verificarToken)
):
    pedido = (
        db.query(Pedido)
        .filter(
            Pedido.id == pedidoId,
            Pedido.usuarioId == usuario.id
        )
        .first()
    )

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    return pedido

@pedidoRouter.patch("/{pedidoId}/status")
async def atualizarStatus(
    pedidoId: int,
    novoStatus: StatusPedido,
    db: Session = Depends(get_db)
):
    pedido = db.query(Pedido).filter(Pedido.id == pedidoId).first()

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    pedido.status = novoStatus
    db.commit()

    return {"msg": "Status atualizado com sucesso"}
