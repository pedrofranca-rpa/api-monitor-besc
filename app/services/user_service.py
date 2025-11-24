from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.users import UserCreate
from app.core.security import hash_password, verify_password, create_access_token
from fastapi import HTTPException, status


class UserService:

    @staticmethod
    async def create(db: AsyncSession, data: UserCreate):

        result = await db.execute(select(User).filter(User.username == data.username))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Username já existe")

        result = await db.execute(select(User).filter(User.email == data.email))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email já cadastrado")

        user = User(
            username=data.username,
            email=data.email,
            hashed_password=hash_password(data.password),
            company=data.company,
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)

        return JSONResponse(
            status_code=201,
            content={
                "message": "Usuário criado com sucesso!",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "company": user.company,
                },
            },
        )

    @staticmethod
    async def authenticate(db: AsyncSession, username: str, password: str):
        result = await db.execute(select(User).filter(User.username == username))
        user = result.scalar_one_or_none()

        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas",
            )

        token = create_access_token(user.username)
        return {"access_token": token, "token_type": "bearer"}
