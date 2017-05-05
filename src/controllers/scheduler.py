from flask import redirect
from models.task_list import TaskList
from models.scheduler import Scheduler
from time import strftime
import uuid
from datetime import timedelta
from util import gen_random_range
from datetime import datetime
from app import app, session


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
    return "Status :Task List Created", 200
