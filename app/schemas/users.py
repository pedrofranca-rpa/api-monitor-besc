from pydantic import BaseModel, EmailStr


# =====================================================================
# BASE: Campos comuns entre criação e resposta
# =====================================================================
class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserLogin(BaseModel):
    username: str
    password: str


# app/schemas/users.py
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    company: str  # novo campo


# =====================================================================
# RESPONSE: Retorno para o cliente (oculta senha)
# =====================================================================
class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True  # (Pydantic v2) substitui orm_mode=True
        # se estiver no Pydantic v1, use:
        # orm_mode = True
