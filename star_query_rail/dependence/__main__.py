from typing import Optional

from sqlmodel import JSON, Column, Field, SQLModel, create_engine
from models import Userinfo, Email, Character, ConnectEU, ConnectUC


def main():
    dbname = "starrail"
    url = f"postgresql://postgres:@localhost/{dbname}"
    print(url)
    engine = create_engine(url, echo=True)
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    main()
