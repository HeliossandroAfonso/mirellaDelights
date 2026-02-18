from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from app.core.database import get_db
from app.models.pedido import Pedido, StatusPedido

dashboardRouter = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@dashboardRouter.get("/resumo-hoje")
async def resumoVendasHoje(db: Session = Depends(get_db)):
    hoje = datetime.now().date()
    

    total_pedidos = db.query(Pedido).filter(func.date(Pedido.dataCriacao) == hoje).count()
    0
    faturamento = db.query(func.sum(Pedido.total)).filter(
        func.date(Pedido.dataCriacao) == hoje,
        Pedido.status != StatusPedido.CANCELADO
    ).scalar() or 0

    return {
        "data": hoje,
        "pedidos_realizados": total_pedidos,
        "faturamento_total": faturamento
    }