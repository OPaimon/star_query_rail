from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine

dbname = "starrail"
url = f"postgresql://postgres:@localhost/{dbname}"
engine = create_engine(url, echo=True)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
