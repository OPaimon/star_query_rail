from sqlalchemy import create_engine, Column, Integer, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy
from sqlalchemy import Column, Integer, String


# 创建 SQLAlchemy 引擎
engine = create_engine('postgresql://postgres:@localhost/starrail', echo=True)

# 创建基类
Base = sqlalchemy.orm.declarative_base()


class User(Base):
    __tablename__ = 'User'
    userid = Column(Integer, primary_key=True)
    name = Column(String)
    cookie = Column(JSON)

class Character(Base):
    __tablename__ = 'Character'
    cid = Column(Integer, primary_key=True)
    name = Column(String)


class Connect(Base):
    __tablename__ = 'Connect'
    userid = Column(Integer, ForeignKey('userid'), primary_key=True)
    cid = Column(Integer, ForeignKey('cid'), primary_key=True)
    element = Column(String)
    rarity = Column(Integer)
    level = Column(Integer)
    rank = Column(Integer)
    equipment = Column(JSON, nullable=True)
    relics = Column(JSON)
    properties = Column(JSON)
    skills = Column(JSON)
    base_type = Column(String)
    figure_path = Column(String)


Base.metadata.create_all(engine)

if __name__ == "__main__":
    main()



