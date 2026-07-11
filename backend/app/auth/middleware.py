"""StadiumOS AI — Auth Middleware

FastAPI dependencies for JWT verification and role-based access control.
"""

from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .service import verify_token

security = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> dict | None:
    """Extract and validate the current user from the JWT.

    Returns None for unauthenticated requests (optional auth).
    """
    if credentials is None:
        return None
    payload = verify_token(credentials.credentials)
    return payload


def require_auth(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """Require a valid JWT. Returns 401 if missing or invalid."""
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload


def require_role(*roles: str):
    """Factory: returns a dependency that requires the user to have one of the given roles."""
    async def _role_checker(payload: dict = Depends(require_auth)) -> dict:
        user_role = payload.get("role", "")
        if user_role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{user_role}' not authorized. Required: {', '.join(roles)}",
            )
        return payload
    return _role_checker
