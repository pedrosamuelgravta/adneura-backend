from datetime import datetime, timedelta, UTC
from passlib.context import CryptContext
import jwt

from fastapi.security import OAuth2PasswordBearer

from core.config import get_settings
from core.types import TokenType

settings = get_settings()


__pwd_context__ = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return __pwd_context__.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return __pwd_context__.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC).replace(tzinfo=None) + expires_delta
    else:
        expire = datetime.now(UTC).replace(tzinfo=None) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTE
        )
    to_encode.update({"exp": expire, "token_type": TokenType.ACCESS})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(tz=UTC) + expires_delta
    else:
        expire = datetime.now(
            tz=UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAY)
    to_encode.update({"exp": expire, "token_type": TokenType.REFRESH})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str, token_type: TokenType):
    try:
        print(token_type)
        print(token)
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        print(payload)
        if payload["token_type"] != token_type:
            return False
        return payload
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
