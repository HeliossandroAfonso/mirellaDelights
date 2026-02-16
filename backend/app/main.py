from fastapi import FastAPI
# Removi as configurações de segurança daqui, pois combinamos de mover para o config.py

app = FastAPI()

# Isso registra as classes no SQLAlchemy para evitar o erro de 'Pedido' não encontrado
from app.models.usuario import Usuario
from app.models.produto import Produto
from app.models.pedido import Pedido
from app.models.itemPedido import ItemPedido
# ------------------------------------------------

from app.routers.authRouter import authRouter

app.include_router(authRouter)