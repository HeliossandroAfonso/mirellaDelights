from fastapi import APIRouter, Depends, HTTPException
from app.models.usuario import Usuario
from app.dependencias.dependencias import pegarPessoas, verificarToken
from app.core.config import bcryptContext, ALGORITHM, ACCESS_TOKEN_EXPIRE, SECRET_KEY
from app.schemas.usuarioSchema import UsuarioSchemas, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

authRouter = APIRouter(prefix="/auth",tags=["auth"])

def criarToken(idUsuario, duracaoTk =timedelta(minutes=ACCESS_TOKEN_EXPIRE)):
    #JWT
    data_expiracao = datetime.now(timezone.utc) + duracaoTk
    dic_info = {
        "sub": str(idUsuario),
        "exp": data_expiracao
    }
    jwtCodificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwtCodificado  

def autenticarUsuario(email, password, session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    elif not bcryptContext.verify(password, usuario.password):
        return False
    else:
        return usuario

#Criação de uma rota de requisição
@authRouter.get("/")
async def home():
    """
    rota padrão para autenticação.
    """
    return {"nada"}

@authRouter.post("/criarConta")
async def criarConta(
    usuarioSchemas: UsuarioSchemas,
    session: Session = Depends(pegarPessoas)
):
    usuario_existente = session.query(Usuario).filter(
        Usuario.email == usuarioSchemas.email
    ).first()

    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="Usuário com este email já existe"
        )

    password_crypt = bcryptContext.hash(usuarioSchemas.password[:72])

    novo_usuario = Usuario(
        nome=usuarioSchemas.nome,
        email=usuarioSchemas.email,
        password=password_crypt,
        activo=usuarioSchemas.activo,
        perfil=usuarioSchemas.perfil,
        telefone=usuarioSchemas.telefone,
        morada=usuarioSchemas.morada
    )

    session.add(novo_usuario)
    session.commit()
    session.refresh(novo_usuario)

    return {"msg": "Usuário criado com sucesso", "usuarioId": novo_usuario.id}

#login -> email e password -> token JWT (Json web Token) dsfkjsdfskjfsf

@authRouter.post("/login")
async def login(loginSchema: LoginSchema, session: Session = Depends(pegarPessoas)):
    usuario = autenticarUsuario(loginSchema.email, loginSchema.password, session) 
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario não encontrado ou password errada")
    else:
        access_token = criarToken(usuario.id)
        refresh_token = criarToken(usuario.id, duracaoTk=timedelta(days=7))
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer"
    }
    
#Login para usar o fastapi
@authRouter.post("/login-from")
async def login_form(dados_from: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegarPessoas)):
    usuario = autenticarUsuario(dados_from.username, dados_from.password, session) 
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario não encontrado ou password errada")
    else:
        access_token = criarToken(usuario.id)
        #refresh_token = criarToken(usuario.id, duracaoTk=timedelta(days=7))
    
    return {
        "access_token": access_token,
        #"refresh_token": refresh_token,
        "token_type": "Bearer"
    }

@authRouter.get("/refresh")
async def refresh(usuario: Usuario = Depends(verificarToken)):
    access_token = criarToken(usuario.id)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
        }