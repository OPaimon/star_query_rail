from typing import Any
from sqlmodel import Session, select, create_engine

from star_query_rail.core.security import get_password_hash, verify_password
from star_query_rail.dependence.models import (
    Userinfo,
    Email,
    ConnectEU,
    ConnectUC,
    Character,
)

dbname = "starrail"
url = f"postgresql://postgres:@localhost/{dbname}"
engine = create_engine(url, echo=True)


def create_account(*, email: str, psw: str) -> Email:
    db_account = Email(email=email, psw=get_password_hash(psw))
    with Session(engine) as session:
        session.add(db_account)
        session.commit()
    return db_account


def create_user(*, userid: int, name: str, cookie: dict) -> Userinfo:
    db_user = Userinfo(userid=userid, name=name, cookie=cookie)
    with Session(engine) as session:
        session.add(db_user)
        session.commit()
    return db_user


def create_eu(*, email: str, userid: int) -> ConnectEU:
    db_connect = ConnectEU(email=email, userid=userid)
    with Session(engine) as session:
        session.add(db_connect)
        session.commit()
    return db_connect


def create_character(*, cid: int, name: str) -> Character:
    db_character = Character(cid=cid, name=name)
    with Session(engine) as session:
        session.add(db_character)
        session.commit()
    return db_character


def create_uc(
    *,
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
    with Session(engine) as session:
        session.add(db_uc)
        session.commit()
    return db_uc


def query_account_by_email(*, email: str) -> Email | None:
    with Session(engine) as session:
        statement = select(Email).where(Email.email == email)
        session_account = session.exec(statement).first()
    return session_account


def query_users_by_email(*, email: str):
    with Session(engine) as session:
        statement = (
            select(Userinfo).join(ConnectEU).join(Email).where(Email.email == email)
        )
        result = session.exec(statement).all()
    return result


def query_characters_by_userid(*, userid: int):
    with Session(engine) as session:
        statement = (
            select(Character)
            .join(ConnectUC)
            .join(Userinfo)
            .where(Userinfo.userid == userid)
        )
        result = session.exec(statement).all()
    return result


def authenticate(*, email: str, password: str) -> Email | None:
    db_account = query_account_by_email(email=email)
    if not db_account:
        return None
    if not verify_password(password, db_account.psw):
        return None
    return db_account


"""

def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(us password = user_data["password"]er_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

"""
