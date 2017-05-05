from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from base import Base
from task_list import TaskList


class TrackingKey(Base):
    __tablename__ = 'trackingkey'

    UniqueId = Column(String(32), primary_key=True)
    TrackKey = Column(String(5), nullable= False)
    TaskUniqueId = Column(String(32), ForeignKey('tasklist.UniqueId'))
    Time = Column(String(250), nullable= False)
    Date = Column(String(250), nullable= False)
    tasklist = relationship(TaskList)



    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'UniqueId': self.UniqueId,
            'TrackingKey': self.TrackKey,
            'TaskUniqueId': self.TaskUniqueId,
            'CreatedTime': self.Time
        }
