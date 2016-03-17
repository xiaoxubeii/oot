__author__ = 'tardis'
from sqlalchemy import create_engine
from oot.db.sqlalchemy.model import Base

engine = create_engine('mysql+mysqlconnector://oot:oot@localhost:3306/oot')
Base.metadata.create_all(engine)
