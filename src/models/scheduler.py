from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from base import Base
from task_list import TaskList


class Scheduler(Base):
    __tablename__ = 'scheduler'

    UniqueKey = Column(String(16), primary_key=True)
    TaskUniqueId = Column(String(32), ForeignKey('tasklist.UniqueId'))
    ScheduledTime =Column(String(250), nullable=False)
    Status= Column(Integer, nullable=False)
    tasklist = relationship(TaskList)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'UniqueKey': self.UniqueKey,
            'TaskUniqueId': self.TaskUniqueId,
            'ScheduledTime': self.ScheduledTime,
            'Status': self.Status,
        }