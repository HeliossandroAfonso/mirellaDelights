#Forçar tipagem de dados
from pydantic import BaseModel
from typing import Optional

class UsuarioSchemas(BaseModel):
    nome: str
    telefone: str
    email: str
    morada: str
    password: str
    perfil: str
    activo: Optional[bool] = True
        
    class Config:
        from_attributes: True
        
class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    morada: Optional[str] = None
    password: Optional[str] = None
    perfil: Optional[str] = None
    activo: Optional[bool] = None
        
class LoginSchema(BaseModel):
    email: str
    password: str
    
    class Config:
        from_attributes: True
        
class UsuarioResponse(UsuarioSchemas):
    id: int
    
    class Config:
        from_attributes: True
        
