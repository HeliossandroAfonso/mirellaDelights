from fastapi import FastAPI

app = FastAPI()

# Isso registra as classes no SQLAlchemy para evitar o erro de 'Pedido' não encontrado
from app.models.usuario import Usuario
from app.models.produto import Produto
from app.models.pedido import Pedido
from app.models.itemPedido import ItemPedido
# ------------------------------------------------

from app.routers.authRouter import authRouter
from app.routers.pedidoRouter import pedidoRouter
from app.routers.itemPedidoRouter import itemPedidoRouter
from app.routers.produtoRouter import produtoRouter
from app.routers.dashboardRouter import dashboardRouter

app.include_router(authRouter)
app.include_router(pedidoRouter)
app.include_router(itemPedidoRouter)
app.include_router(produtoRouter)
app.include_router(dashboardRouter)