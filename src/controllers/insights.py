from flask import jsonify
from models.task_list import TaskList
from models.scheduler import Scheduler
from models.basic_cron_insight import BasicCronInsight
from models.tracking_key import TrackingKey
from app import app, session
from datetime import datetime, timedelta
from time import strftime, time, clock

@app.route('/insight/')
def insight():
    try:
        total_cron=session.query(BasicCronInsight).count()
    except Exception, e:
        total_cron=0
    cron_date=session.query(BasicCronInsight.CronDate).all()
    count_today =0
    count_yesterday=0
    count_week= 0
    count_month=0
    today= datetime.now().date()
    yesterday = (datetime.now().date() - timedelta(1))
    week =  (datetime.now().date() - timedelta(7))
    month=  (datetime.now().date() - timedelta(30))    
    for instance in cron_date:
        cron_execution_date= str(instance[0])
        cron_execution_date= datetime.strptime(cron_execution_date, "%y-%m-%d")
        if cron_execution_date.date() == today:
            count_today += 1
        if cron_execution_date.date() == yesterday:
            count_yesterday += 1
        if cron_execution_date.date()>week:
            count_week += 1
        if cron_execution_date.date() > month:
            count_month += 1

    try:
        total_task=session.query(TaskList).count()
    except Exception, e:
        total_task=0
    task_date=session.query(TaskList.CreatedDate).all()
    task_today =0
    task_yesterday=0
    task_week= 0
    task_month=0
    for instance in task_date:
        task_execution_date= str(instance[0])
        task_execution_date= datetime.strptime(task_execution_date, "%y-%m-%d")
        if task_execution_date.date() == today:
            task_today += 1
        if task_execution_date.date() == yesterday:
            task_yesterday += 1
        if task_execution_date.date()>week:
            task_week += 1
        if task_execution_date.date() > month:
            task_month += 1


    try:
        total_tracking=session.query(TrackingKey).count()
    except Exception, e:
        total_tracking=0
    tracking=session.query(TrackingKey.Date).all()
    track_today =0
    track_yesterday=0
    track_week= 0
    track_month=0
    for instance in tracking:
        track_date= str(instance[0])
        track_date= datetime.strptime(track_date, "%y-%m-%d")
        if track_date.date() == today:
            track_today += 1
        if track_date.date() == yesterday:
            track_yesterday += 1
        if track_date.date()>week:
            track_week += 1
        if track_date.date() > month:
            track_month += 1    


    completed_task=session.query(Scheduler).filter_by(Status=1).count()
    incomplete_task=session.query(Scheduler).filter_by(Status=0).count()

    list = [
        {
          "Today Cron Ececuted": count_today,
          "yesterday Cron Executed": count_yesterday,
          "week cron Executed": count_week,
           "month Cron executed": count_month,
            "total cron executed": total_cron,
        },

         {
          "Today task Created": task_today,
          "yesterday task Created": task_yesterday,
          "week task Created": task_week,
           "month task Created": task_month,
            "total task Created": total_task,
        },
        {
          "Task Compleated": completed_task,
          "Task Incomplete": incomplete_task,
          
        },
        {
          "Today tracking key Created": track_today,
          "yesterday tracking key Created": track_yesterday,
          "week tracking key Created": track_week,
           "month tracking key Created": track_month,
            "total tracking Created": total_tracking,
        },

        
    ]
          
    return jsonify(Result = list)

@app.route('/insight/<querydate>')
def dateinsight(querydate):
    try:
        insight_date = datetime.strptime(querydate, "%y-%m-%d").date()
    except Exception, e:
        return "Invailid date format please enter YY-MM-DD"
    insight_date = str(insight_date)
    insight_date = insight_date[2:]
    print insight_date
    cron_hours= session.query(BasicCronInsight.CronTime).filter_by(CronDate=insight_date).all()
    for instance in cron_hours:
        time1= str(instance[0])
        time1 = time1[:5]
        timenow=datetime.now().strftime("%H-%M")
    

