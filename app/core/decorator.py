from functools import wraps
from fastapi import Request, HTTPException, status
from app.core.security import decode_token


def jwt_required(func):
    """
    Decorador que protege endpoints exigindo um token JWT válido.
    Exemplo:
        @router.get("/me")
        @jwt_required
        async def get_user(request: Request):
            ...
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get("request") or next(
            (a for a in args if isinstance(a, Request)), None
        )

        if not request:
            raise HTTPException(500, "Request object não encontrado")

        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token ausente ou mal formatado",
            )

        token = auth_header.split(" ")[1]
        payload = decode_token(token)

        # Injeta o payload do token como atributo da request
        request.state.user = payload

        return await func(*args, **kwargs)

    return wrapper
