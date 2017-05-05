from sqlalchemy import create_engine
from models.base import Base

engine = create_engine('mysql://localhost/test?charset=utf8&user=root&passwd=')


Base.metadata.create_all(engine)