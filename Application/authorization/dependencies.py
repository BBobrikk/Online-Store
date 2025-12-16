from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Request
from Application.authorization.config import security
from fastapi.security import HTTPBearer

bearer_scheme = HTTPBearer()


async def require_auth(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
):
    payload = await security.access_token_required(request)
    return int(payload.sub)


async def require_admin(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
):
    payload = await security.access_token_required(request)
    role = payload.role
    if role == "admin":
        return role
    raise HTTPException(detail="Недостаточно прав", status_code=403)
