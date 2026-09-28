from dataclasses import dataclass

import jwt
from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.database.connection import get_db
from app.database.models import User


@dataclass(frozen=True)
class CurrentUser:
    id: str
    external_auth_id: str


bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    x_user_id: str | None = Header(default=None, alias="X-User-ID"),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> CurrentUser:
    if settings.dev_auth_bypass:
        external_id = x_user_id or "local-demo-user"
    else:
        if not credentials or not settings.jwt_secret:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
        try:
            decode_options = {
                "verify_iss": bool(settings.jwt_issuer),
                "verify_aud": bool(settings.jwt_audience),
            }
            payload = jwt.decode(
                credentials.credentials,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm],
                issuer=settings.jwt_issuer,
                audience=settings.jwt_audience,
                options=decode_options,
            )
            external_id = str(payload["sub"])
        except (InvalidTokenError, KeyError) as exc:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    user = db.scalar(select(User).where(User.external_auth_id == external_id))
    if user is None:
        user = User(external_auth_id=external_id, display_name="Demo User")
        db.add(user)
        db.commit()
        db.refresh(user)
    return CurrentUser(id=user.id, external_auth_id=user.external_auth_id)
