from flask import Flask, render_template, redirect, jsonify
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database_setup import Base, TaskList, Scheduler, BasicCronInsight, TrackingKey
import random
import string
import json
from time import strftime, time, clock
import uuid
from datetime import datetime, timedelta
from ukey import gen_random_range, gen_random_alphanu_range
from datetime import datetime
from apscheduler.scheduler import Scheduler as sch
import timeit



app = Flask(__name__)
sched = sch()
sched.start()

# Connect to Database and create database session
engine = create_engine('sqlite:///taskinsight.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/cron/')
@sched.cron_schedule(second=5)
def cronTask():
    start = timeit.default_timer()
    scheduler = session.query(Scheduler).filter_by(Status=0).all()
    count = 0
    for instance in scheduler:
        now = datetime.now()
        schedule_time = instance.ScheduledTime
        schedule_time = datetime.strptime(schedule_time, "%H:%M:%S")
        schedule_time = now.replace(hour=schedule_time.time().hour, minute=schedule_time.time().minute, second=schedule_time.time().second, microsecond=0)
        if (schedule_time < now):
            count += 1
            instance.Status=1
            session.add(instance)
            random_key= gen_random_range(16)
            track_key= gen_random_alphanu_range(5)
            task_unique_id= instance.TaskUniqueId
            time= instance.ScheduledTime
            tracking_info= TrackingKey(UniqueId=random_key,TrackKey=track_key,TaskUniqueId=task_unique_id,Time=time)
            session.commit()
            session.add(tracking_info)
            session.commit()
    stop = timeit.default_timer()
    running_time= stop - start 
    random_key= gen_random_range(16)
    today= str(datetime.now().strftime("%y-%m-%d"))
    basic_cron = BasicCronInsight(UniqueId=random_key,Compleated=count,ExecutionTime=running_time,CronDate=today)
    session.add(basic_cron)
    session.commit()
    return str(running_time)



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
        today= str(datetime.now().strftime("%y-%m-%d"))
        new_tasks = TaskList(Title=title,UniqueId=uid,CreatedTime=current_time,CreatedDate=today)
        random_key= gen_random_range(16)
        seconds=50
        scheduled_time= datetime.now() + timedelta(seconds=seconds)
        scheduled_time= str(scheduled_time.strftime('%H:%M:%S'))
        new_scheduler = Scheduler(UniqueKey=random_key,TaskUniqueId=uid,ScheduledTime=scheduled_time, Status= 0)
        session.add(new_tasks)
        session.add(new_scheduler)
        session.commit()
    return ("Status :Task List Created")


@app.route('/insight/')
def insight():
    return render_template('t.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)