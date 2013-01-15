__author__ = 'estsauver'
from datetime import datetime
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, backref


uname = "senior_project"
databaseName = "bioreactor"

#this assumes that we have postgresql running on the local machine and that we're connecting to a user
#with no password and to a database equal to databaseName
_engine = create_engine('postgresql+psycopg2://{}@localhost/{}'.format(uname, databaseName))
_Base = declarative_base()
Session = sessionmaker(bind=_engine)


class Experiment(_Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True)
    startTime = Column(DateTime)


    def __init__(self):
        self.startTime = datetime.now()

    def __repr__(self):
        return "<Experiment('%s')>" % self.id


class Datapoint(_Base):
    __tablename__ = "datapoints"

    id = Column(Integer, primary_key=True)

    value = Column(Float)
    error = Column(Float)
    dataType = Column(String)
    time = Column(DateTime)
    group_int = Column(Integer)
    experiment_id = Column(Integer, ForeignKey('experiments.id'))
    experiment = relationship(Experiment, backref=backref("datapoints", order_by=time))

    def __init__(self, value, error, dataType, experiment, group_int):
        self.value = value
        self.error = error
        self.dataType = dataType
        self.time = datetime.now()
        self.group_int = group_int
        self.experiment_id = experiment.id
        self.experiment = experiment

    def __repr__(self):
        return "<Datapoint('%s','%s','%s','%s')>" % (self.value, self.error, self.dataType, self.experiment_id)




_Base.metadata.create_all(_engine)
