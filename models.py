from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select

# create engine and connect do DB
connect_engine = create_engine('sqlite:///panzer.db')
connection = connect_engine.connect()

Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    
    def __repr__(self):
        return "<User(id='d', username='%s', email='%s', first_name='%s', last_name='%s')>" \
               % (self.id, self.username, self.email, self.first_name, self.last_name)

Base.metadata.create_all(connect_engine)

