from sqlmodel import JSON, Column, Field, SQLModel


class EmailBase(SQLModel):
    email: str = Field(unique=True, index=True, primary_key=True)
    is_active: bool = True
    is_superuser: bool = False


class EmailRegister(SQLModel):
    email: str
    psw: str


class UserTest(SQLModel):
    userid: int
    cookie: str


class EmailUpdate(SQLModel):
    psw: str


class Email(EmailBase, table=True):
    psw: str


class Userbase(SQLModel):
    userid: int = Field(primary_key=True)
    nickname: str


class UserCreate(SQLModel):
    cookie: str


class UserRegister(SQLModel):
    userid: int
    nickname: str
    cookies: dict


class Userinfo(Userbase, table=True):
    cookies: dict | None = Field(default=None, sa_column=Column(JSON))


class CharacterUpdate(SQLModel):
    cid: int
    data: dict


class CharacterRegister(SQLModel):
    cid: int
    name: str


class Character(SQLModel, table=True):
    cid: int = Field(primary_key=True)
    name: str
    data: dict | None = Field(default=None, sa_column=Column(JSON))


class ConnectEUPublic(SQLModel):
    email: str
    userid: int
    nickname: str


class ConnectEURegister(SQLModel):
    email: str
    userid: int


class ConnectEU(SQLModel, table=True):
    email: str = Field(foreign_key="email.email", primary_key=True)
    userid: int = Field(foreign_key="userinfo.userid", primary_key=True)


class ConnectUC(SQLModel, Table=True):
    userid: int = Field(foreign_key="userinfo.userid", primary_key=True)
    cid: int = Field(foreign_key="character.cid", primary_key=True)


class ConnectUCRegister(SQLModel):
    userid: int
    cid: int


class ConnectUCUpdate(SQLModel):
    data: dict = Field(sa_column=Column(JSON))


class EUCPublic(ConnectEUPublic):
    characters: list[int]


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: str | None = None
