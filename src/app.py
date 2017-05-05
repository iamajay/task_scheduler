from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from apscheduler.scheduler import Scheduler as sch

app = Flask(__name__)
sched = sch()
sched.start()

# Connect to Database and create database session
engine = create_engine('mysql://localhost/test?charset=utf8&user=root&passwd=')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
