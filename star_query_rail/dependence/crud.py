from sqlmodel import Session, select

from star_query_rail.core.security import get_password_hash, verify_password
from star_query_rail.dependence.models import (
    Character,
    ConnectEU,
    ConnectUC,
    Email,
    Userinfo,
)


def create_account(*, session: Session, email: str, psw: str) -> Email:
    db_account = Email(email=email, psw=get_password_hash(psw))
    session.add(db_account)
    session.commit()
    return db_account


def create_user(*, session: Session, userid: int, name: str, cookie: dict) -> Userinfo:
    db_user = Userinfo(userid=userid, name=name, cookie=cookie)
    session.add(db_user)
    session.commit()
    return db_user


def create_eu(*, session: Session, email: str, userid: int) -> ConnectEU:
    db_connect = ConnectEU(email=email, userid=userid)
    session.add(db_connect)
    session.commit()
    return db_connect


def create_character(*, session: Session, cid: int, name: str) -> Character:
    db_character = Character(cid=cid, name=name)
    session.add(db_character)
    session.commit()
    return db_character


def create_uc(
    *,
    session: Session,
    userid: int,
    cid: int,
    element: str,
    rarity: int,
    level: int,
    rank: int,
    equipment: dict,
    relics: dict,
    properties: dict,
    skills: dict,
    base_type: str,
    figure_path: str,
) -> ConnectUC:
    db_uc = ConnectUC(
        userid=userid,
        cid=cid,
        element=element,
        rarity=rarity,
        level=level,
        rank=rank,
        equipment=equipment,
        relics=relics,
        properties=properties,
        skills=skills,
        base_type=base_type,
        figure_path=figure_path,
    )
    session.add(db_uc)
    session.commit()
    return db_uc


def query_account_by_email(*, session: Session, email: str) -> Email | None:
    statement = select(Email).where(Email.email == email)
    session_account = session.exec(statement).first()
    return session_account


def query_users_by_email(*, session: Session, email: str):
    statement = select(Userinfo).join(ConnectEU).join(Email).where(Email.email == email)
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
