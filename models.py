import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func, String


Base = declarative_base()

#create database location
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "mydb2.db"))

engine = create_engine(database_file, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base.query = db_session.query_property()

class User(Base):
    __tablename__ = 'users'
    uuid = Column(Integer, primary_key=True)
    username = Column(String(256), index=True, unique=True)
    posts = relationship('Post', backref='author')


class Post(Base):
    __tablename__ = 'posts'
    uuid = Column(Integer, primary_key=True)
    title = Column(String(256), index=True)
    body = Column(Text)
    author_id = Column(Integer, ForeignKey('users.uuid'))

