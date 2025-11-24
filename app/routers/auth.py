from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.users import UserCreate, UserResponse, UserLogin
from app.services.user_service import UserService


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/login")
async def login_user(user_in: UserLogin, db: AsyncSession = Depends(get_db)):
    return await UserService.authenticate(db, user_in.username, user_in.password)


@router.post("/register", response_model=UserResponse)
async def register_user(
    user_in: UserCreate, db: AsyncSession = Depends(get_db)
) -> UserResponse:
    return await UserService.create(db, user_in)


@router.get("/me")
async def get_user_data(request: Request):
    """Endpoint protegido que retorna dados do usuário autenticado."""
    return {"user": request.state.user}
