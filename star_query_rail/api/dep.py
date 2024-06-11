import secrets
from collections.abc import Generator
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session, create_engine

from star_query_rail.core import security
from star_query_rail.core.config import settings
from star_query_rail.dependence import crud
from star_query_rail.dependence.models import Email, TokenPayload

dbname = "starrail"
url = f"postgresql://postgres:@localhost/{dbname}"
engine = create_engine(url, echo=True)

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="login/access-token")


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_account(session: SessionDep, token: TokenDep) -> Email:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.query_account_by_email(session=session, email=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


CurrentAccount = Annotated[Email, Depends(get_current_account)]
