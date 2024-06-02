from sqlmodel import JSON, Column, Field, SQLModel


class User(SQLModel, table=True):
    userid: int = Field(primary_key=True)
    psw: str
    name: str
    cookie: dict | None = Field(default=None, sa_column=Column(JSON))


class Character(SQLModel, table=True):
    cid: int = Field(primary_key=True)
    name: str


class Connect(SQLModel, table=True):
    userid: int = Field(foreign_key="user.userid", primary_key=True)
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
