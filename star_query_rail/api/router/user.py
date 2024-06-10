from fastapi import APIRouter, HTTPException

from star_query_rail.dependence import crud
from star_query_rail.dependence.models import Email

from ..dep import SessionDep

router = APIRouter()


@router.post(
    "/signup",
    response_model=Email,
)
def register_account(session: SessionDep, email: str, psw: str):
    """
    Register new account.
    """
    account = crud.query_account_by_email(session=session, email=email)
    if account:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = crud.create_account(session=session, email=email, psw=psw)
    return user
