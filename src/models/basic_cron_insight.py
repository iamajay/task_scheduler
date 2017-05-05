from sqlalchemy import Column, Integer, String
from base import Base


class BasicCronInsight(Base):
    __tablename__ = 'basiccroninsight'

    UniqueId = Column(String(32), primary_key=True)
    Compleated= Column(Integer)
    ExecutionTime = Column(String(250),nullable=False)
    CronTime = Column(String(250),nullable=False)
    CronDate = Column (String(250),nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'UniqueId': self.UniqueId,
            'ExecutionTime': self.ExecutionTime,
            'Compleated': self.Compleated,
            'CronDate': self.CronDate,
        }
