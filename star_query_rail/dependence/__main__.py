from typing import Optional

from sqlmodel import JSON, Column, Field, SQLModel, create_engine


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


def main():
    dbname = "starrail"
    url = f"postgresql://postgres:@localhost/{dbname}"
    print(url)
    engine = create_engine(url, echo=True)
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    main()
