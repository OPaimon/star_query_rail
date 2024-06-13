from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from star_query_rail.api.dep import CurrentAccount, SessionDep
from star_query_rail.core import security
from star_query_rail.dependence import crud
from star_query_rail.dependence.models import ConnectEU, EmailBase, EUCPublic, Token

router = APIRouter()


@router.post("/login/access-token")
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=30 * 24 * 60)
    return Token(
        access_token=security.create_access_token(
            user.email, expires_delta=access_token_expires
        )
    )


@router.post("/login/test-token", response_model=EmailBase)
def test_token(current_account: CurrentAccount) -> Any:
    """
    Test access token
    """
    return current_account
