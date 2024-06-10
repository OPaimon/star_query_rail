from sqlmodel import JSON, Column, Field, SQLModel


class EmailBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    is_superuser: bool = False


class EmailRegister(SQLModel):
    email: str
    psw: str


class EmailUpdate(SQLModel):
    psw: str


class Email(EmailBase, table=True):
    psw: str


class Userbase(SQLModel):
    userid: int = Field(primary_key=True)
    name: str = Field(default="xq")


class UserRegister(SQLModel):
    userid: int
    name: str


class UserUpdate(SQLModel):
    cookie: str


class Userinfo(Userbase, table=True):
    cookie: dict | None = Field(default=None, sa_column=Column(JSON))


class CharacterRegister(SQLModel):
    cid: int
    name: str


class Character(SQLModel, table=True):
    cid: int = Field(primary_key=True)
    name: str


class ConnectEURegister(SQLModel):
    email: str
    userid: int


class ConnectEU(SQLModel, table=True):
    email: str = Field(foreign_key="email.email", primary_key=True)
    userid: int = Field(foreign_key="userinfo.userid", primary_key=True)


class ConnectUCBase(SQLModel):
    userid: int = Field(foreign_key="userinfo.userid", primary_key=True)
    cid: int = Field(foreign_key="character.cid", primary_key=True)


class ConnectUCRegister(SQLModel):
    userid: int
    cid: int


class ConnectUCUpdate(SQLModel):
    data: dict = Field(sa_column=Column(JSON))


class ConnectUC(ConnectUCBase, Table=True):
    data: dict = Field(sa_column=Column(JSON))


'''
class ConnectUC(ConnectUCBase, table=True):
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
'''
