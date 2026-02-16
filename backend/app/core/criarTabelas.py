''' from fastapi import FastAPI
from database import engine
from app.models import Usuario, Produto, Pedido, ItemPedido

Usuario.metadata.create_all(bind=engine)
Produto.metadata.create_all(bind=engine)
Pedido.metadata.create_all(bind=engine)
ItemPedido.metadata.create_all(bind=engine)

app = FastAPI()
 '''