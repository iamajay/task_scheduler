from models.scheduler import Scheduler
from models.basic_cron_insight import BasicCronInsight
from models.tracking_key import TrackingKey
from util import gen_random_range, gen_random_alphanu_range
from datetime import datetime
import timeit
from app import app, sched, session


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
            today= str(datetime.now().strftime("%y-%m-%d"))
            tracking_info= TrackingKey(UniqueId=random_key,TrackKey=track_key,TaskUniqueId=task_unique_id,Time=time,Date=today)
            session.commit()
            session.add(tracking_info)
            session.commit()
    stop = timeit.default_timer()
    running_time= stop - start 
    random_key= gen_random_range(16)
    today= str(datetime.now().strftime("%y-%m-%d"))
    current_time= str(datetime.now().strftime('%H:%M:%S'))
    basic_cron = BasicCronInsight(UniqueId=random_key,Compleated=count,ExecutionTime=running_time,CronDate=today,CronTime=current_time)
    session.add(basic_cron)
    session.commit()
    return str(running_time), 200
