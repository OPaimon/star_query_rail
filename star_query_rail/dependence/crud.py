from typing import Any

from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select, create_engine

from star_query_rail.core.security import get_password_hash, verify_password
from star_query_rail.dependence.models import (
    Email,
    EmailRegister,
    EmailUpdate,
    Userinfo,
    UserRegister,
    UserUpdate,
    ConnectEU,
    ConnectEURegister,
    ConnectUC,
    ConnectUCRegister,
    Character,
    CharacterRegister,
)


def create_account(*, session: Session, account_register: EmailRegister) -> Email:
    db_account = Email.model_validate(
        account_register, update={"email": account_register.email, "psw": account_register.psw}
    )
    session.add(db_account)
    session.commit()
    return db_account


def create_user(*, session: Session, user_create: UserRegister) -> Userinfo:
    db_user = Userinfo.model_validate(
        user_create, update={"userid": user_create.userid,"name":user_create.name}
    )
    session.add(db_user)
    session.commit()
    return db_user


def create_eu(*, session: Session, eu_connect: ConnectEURegister) -> ConnectEU:
    db_connect = ConnectEU.model_validate(
        eu_connect, update={"email": eu_connect.email, "userid": eu_connect.email}
    )
    session.add(db_connect)
    session.commit()
    return db_connect


def create_character(*, session: Session, character_create: CharacterRegister) -> Character:
    db_character = Character.model_validate(
        character_create,update={"cid":character_create.cid,"name":character_create.name}
    )
    session.add(db_character)
    session.commit()
    return db_character


def create_uc(*, session: Session,ucRegister: ConnectUCRegister) -> ConnectUC:
    db_uc = ConnectUC.model_validate(
        ucRegister, update={"userid": ucRegister.userid, "cid": ucRegister.cid}
    )
    session.add(db_uc)
    session.commit()
    return db_uc


def query_account_by_email(*, session: Session, email: str) -> Email | None:
    statement = select(Email).where(Email.email == email)
    session_account = session.exec(statement).first()
    return session_account


def query_users_by_email(*,session:Session, email: str):
    statement = (
        select(Userinfo).join(ConnectEU).join(Email).where(Email.email == email)
    )
    result = session.exec(statement).all()
    return result


def query_characters_by_userid(*, session: Session, userid: int):
    statement = (
        select(Character)
        .join(ConnectUC)
        .join(Userinfo)
        .where(Userinfo.userid == userid)
    )
    result = session.exec(statement).all()
    return result


def authenticate(*, session: Session, email: str, password: str) -> Email | None:
    db_account = query_account_by_email(session=session, email=email)
    if not db_account:
        return None
    if not verify_password(password, db_account.psw):
        return None
    return db_account


def update_password(*, session: Session, email: str, email_update: EmailUpdate) -> Email:
    statement = select(Email).where(Email.email == email)
    try:
        email_record = session.exec(statement).one()
    except NoResultFound:
        raise ValueError("Email not found")
    email_record.psw = get_password_hash(email_update.psw)
    session.add(email_record)
    session.commit()
    session.refresh(email_record)
    return email_record


def del_account(*, session: Session, email: str):
    statement = select(Email).where(Email.email == email)
    account = session.execute(statement)
    print(account.all())
    session.delete(account.all())


def del_eu(*, session: Session, email: str, userid: int):
    statement = select(ConnectEU).where(ConnectEU.email == email and ConnectEU.userid == userid)
    eu = session.execute(statement)
    print(eu.all())
    session.delete(eu.all())


def del_user(*, session: Session, userid: int):
    statement = select(Userinfo).where(Userinfo.userid == userid)
    user = session.execute(statement)
    print(user.all())
    session.delete(user.all())
