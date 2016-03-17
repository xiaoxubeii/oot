__author__ = 'tardis'
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, PickleType, Text
from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()


class TextPickleType(PickleType):
    impl = Text


class BaseModel(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        super(BaseModel, self).__init__()


class ClusterModel(BaseModel, Base):
    __tablename__ = 'cluster'
    id = Column(String(200), primary_key=True)
    name = Column(String(200), nullable=False)
    conf = Column(TextPickleType(pickler=json) ,nullable=True)


class ServerModel(BaseModel, Base):
    __tablename__ = 'server'
    id = Column(String(200), primary_key=True)
    name = Column(String(200), nullable=False)
    host_name = Column(String(200), nullable=True)
    interfaces = Column(TextPickleType(pickler=json), nullable=True)
    disk = Column(TextPickleType(pickler=json), nullable=True)
    cpu = Column(TextPickleType(pickler=json), nullable=True)
    memory = Column(String(200), nullable=True)
    ipmi = Column(TextPickleType(pickler=json), nullable=True)

    cluster_id = Column(String(200), ForeignKey('cluster.id'))
    cluster = relationship(ClusterModel)

    conf = Column(TextPickleType(pickler=json), nullable=True)

    def __str__(self):
        return json.dumps(self.__dict__)

