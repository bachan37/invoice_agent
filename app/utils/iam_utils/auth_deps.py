from typing import List

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from app.utils.iam_utils.jwt_utils import JWT_utils, JWTError

security = HTTPBearer(auto_error=False)

class TokenPayload(BaseModel):
    """Decoded JWT payload with user ID and role identifiers."""

    user_id: int
    roles: List[str]

def get_current_user_payload(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> TokenPayload:
    """Extract and validate JWT from Authorization header.

    Args:
        credentials: Bearer token from Authorization header (injected by FastAPI).

    Returns:
        TokenPayload with user id (user_id) and role_ids.

    Raises:
        HTTPException: 401 if credentials are missing, invalid, or expired.
    """
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    try:
        payload = JWT_utils.decode_access_token(credentials.credentials)
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        ) from exc

    user_id = payload.get("user_id")
    roles = payload.get("roles") or []

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    return TokenPayload(user_id=user_id, roles=roles)