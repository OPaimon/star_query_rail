from sqlmodel import JSON, Column, Field, SQLModel, create_engine


class Email(SQLModel, table=True):
    email: str = Field(primary_key=True)
    psw: str


class Userinfo(SQLModel, table=True):
    userid: int = Field(primary_key=True)
    name: str
    cookie: dict | None = Field(default=None, sa_column=Column(JSON))


class Character(SQLModel, table=True):
    cid: int = Field(primary_key=True)
    name: str


class ConnectEU(SQLModel, table=True):
    email: str = Field(foreign_key="email.email", primary_key=True)
    userid: int = Field(foreign_key="userinfo.userid", primary_key=True)


class ConnectUC(SQLModel, table=True):
    userid: int = Field(foreign_key="userinfo.userid", primary_key=True)
    cid: int = Field(foreign_key="character.cid", primary_key=True)
    element: str
    rarity: int
    level: int
    rank: int
    equipment: dict | None = Field(default=None, sa_column=Column(JSON))
    relics: dict | None = Field(default=None, sa_column=Column(JSON))
    properties: dict = Field(sa_column=Column(JSON))
    skills: dict = Field(sa_column=Column(JSON))
    base_type: str
    figure_path: str
