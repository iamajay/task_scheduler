from sqlalchemy import Column, String
from base import Base


class TaskList(Base):
    __tablename__ = 'tasklist'

    UniqueId = Column(String(32), primary_key=True)
    Title = Column(String(250), nullable=False)
    CreatedTime = Column(String(250), nullable=False)
    CreatedDate = Column(String(250), nullable=False)
   
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'Title': self.Title,
            'UniqueId': self.UniqueId,
            'CreatedTime': self.CreatedTime,
            'CreatedDate': self.CreatedDate,
        }