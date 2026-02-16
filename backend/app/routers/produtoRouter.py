from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.produto import Produto
from app.schemas.produtoSchema import (ProdutoCreate, ProdutoUpdate, ProdutoResponse)

produtoRouter = APIRouter(
    prefix="/produtos",
    tags=["Produtos"]
)

# Criar produto
@produtoRouter.post("/", response_model=ProdutoResponse)
async def criarProduto(
    dados: ProdutoCreate,
    db: Session = Depends(get_db)
):
    produto = Produto(**dados.model_dump())

    db.add(produto)
    db.commit()
    db.refresh(produto)

    return produto

# Listar produtos ativos
@produtoRouter.get("/", response_model=list[ProdutoResponse])
async def listarProdutos(db: Session = Depends(get_db)):
    produtos = db.query(Produto).filter(Produto.ativo == True).all()
    return produtos


# Buscar produto por ID
@produtoRouter.get("/{produto_id}", response_model=ProdutoResponse)
async def buscarProduto(
    produto_id: int,
    db: Session = Depends(get_db)
):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return produto


# Atualizar produto
@produtoRouter.put("/{produto_id}", response_model=ProdutoResponse)
async def atualizarProduto(
    produto_id: int,
    dados: ProdutoUpdate,
    db: Session = Depends(get_db)
):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(produto, campo, valor)

    db.commit()
    db.refresh(produto)

    return produto

# Desativar produto
@produtoRouter.delete("/{produto_id}")
async def desativarProduto(
    produto_id: int,
    db: Session = Depends(get_db)
):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    produto.ativo = False
    db.commit()

    return {"msg": "Produto desativado com sucesso"}
