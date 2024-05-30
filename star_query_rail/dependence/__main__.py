import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, JSON, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 创建 SQLAlchemy 引擎
engine = create_engine('postgresql://postgres:@localhost/starrail', echo=True)

# 创建基类
Base = sqlalchemy.orm.declarative_base()

class user(Base):
    __tablename__ = 'User'
    userid = Column(Integer, primary_key=True)
    name = Column(String)
    cookie = Column(JSON)

class character(Base):
    __tablename__ = 'Character'
    cid = Column(Integer, primary_key=True)
    name = Column(String)



class connect(Base):
    __tablename__ = 'Connect'
    userid = Column(Integer, ForeignKey('User.userid'), primary_key=True)
    cid = Column(Integer, ForeignKey('Character.cid'), primary_key=True)
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
