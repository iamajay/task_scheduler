from flask import Flask, request, redirect, jsonify, url_for
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database_setup import Base, TaskList, Scheduler, BasicCronInsight, TrackingKey
import random
import string
import json
from time import strftime
import uuid
from datetime import datetime, timedelta
from ukey import gen_random_range

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///taskinsight.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/cron/')
def cronTask():
    scheduler = session.query(Scheduler).filter_by(Status=0).all()
    for instance in scheduler:
        now = datetime.now()
        schedule_time = instance.ScheduledTime
        schedule_time = datetime.strptime(schedule_time, "%H:%M:%S")
        schedule_time = now.replace(hour=schedule_time.time().hour, minute=schedule_time.time().minute, second=schedule_time.time().second, microsecond=0)
        if (schedule_time < now):
            instance.Status=1
            session.add(instance)
            session.commit()



@app.route('/')
def home():
    return redirect('/scheduler')

@app.route('/scheduler/')
def schedule():
    try:
        total_task=session.query(TaskList).count()
    except Exception, e:
    	total_task=0

    for i in range (total_task+1,total_task+1500):
        title= "Task "+str(i)+" Task Scheduler Date "+str(strftime("%d-%B-%W"))+" And Time "+str(strftime("%X"))+""
        uid= uuid.uuid4()
        uid=uid.hex
        uid=str(uid)
        current_time= str(datetime.now().strftime('%H:%M:%S'))
        new_tasks = TaskList(Title=title,UniqueId=uid,CreatedTime=current_time)
        random_key= gen_random_range(16)
        seconds=300
        scheduled_time= datetime.now() + timedelta(seconds=seconds)
        scheduled_time= str(scheduled_time.strftime('%H:%M:%S'))
        new_scheduler = Scheduler(UniqueKey=random_key,TaskUniqueId=uid,ScheduledTime=scheduled_time, Status= 0)
        session.add(new_tasks)
        session.add(new_scheduler)
        session.commit()
    return ("Status :Task List Created")


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)