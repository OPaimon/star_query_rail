from fastapi import APIRouter, HTTPException

from star_query_rail.dependence import crud
from star_query_rail.dependence.models import (
    ConnectEU,
    Email,
    EmailRegister,
    EmailUpdate,
    Message,
)

from ..dep import CurrentAccount, SessionDep

router = APIRouter()


@router.post(
    "/signup",
    response_model=Email,
)
def register_account(session: SessionDep, email_register: EmailRegister):
    """
    Register new account.
    """
    account = crud.query_account_by_email(session=session, email=email_register.email)
    if account:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = crud.create_account(
        session=session,
        account_register=email_register,
    )
    return user


@router.delete("/me")
def delete_account(session: SessionDep, current_account: CurrentAccount):
    """
    Delete current account.
    """
    account = crud.query_account_by_email(session=session, email=current_account.email)
    if not account:
        raise HTTPException(
            status_code=400,
            detail="The user with this email does not exist in the system.",
        )
    session.query(ConnectEU).filter_by(email=current_account.email).delete()
    session.query(Email).filter_by(email=current_account.email).delete()
    session.commit()
    return Message(message="Account deleted")


@router.patch("/me/password", response_model=Message)
def update_password(
    session: SessionDep, current_account: CurrentAccount, email_update: EmailUpdate
):
    """
    Update current account password.
    """
    account = crud.query_account_by_email(session=session, email=current_account.email)
    if not account:
        raise HTTPException(
            status_code=400,
            detail="The user with this email does not exist in the system.",
        )
    account.psw = crud.get_password_hash(email_update.psw)
    session.commit()
    return Message(message="Password updated")


@router.get("/", response_model=list[Email])
def get_all_accounts(session: SessionDep, current_account: CurrentAccount):
    """
    Get all accounts.
    """
    if current_account.is_superuser:
        accounts = session.query(Email).all()
        return accounts


@router.delete("/{email}")
def delete_account_by_email(
    session: SessionDep, cnt_account: CurrentAccount, email: str
):
    """
    Delete account by email.
    """
    if not cnt_account.is_superuser:
        raise HTTPException(
            status_code=400,
            detail="The user does not have enough privileges.",
        )
    account = crud.query_account_by_email(session=session, email=email)
    if not account:
        raise HTTPException(
            status_code=400,
            detail="The user with this email does not exist in the system.",
        )
    session.query(ConnectEU).filter_by(email=email).delete()
    session.query(Email).filter_by(email=email).delete()
    session.commit()
    return Message(message="Account deleted")
