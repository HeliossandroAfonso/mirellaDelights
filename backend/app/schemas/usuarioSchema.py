#Forçar tipagem de dados
from pydantic import BaseModel
from typing import Optional, List

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
        
class LoginSchema(BaseModel):
    email: str
    password: str
    
    class Config:
        from_attributes: True
        
