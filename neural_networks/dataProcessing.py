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


class Datapoint(_Base):
    __tablename__ = "datapoints"

    id = Column(Integer, primary_key=True)

    time_recorded = Column(DateTime)
    experiment_id = Column(Integer, ForeignKey('experiments.id'))
    experiment = relationship("Experiment", backref=backref("datapoints", order_by=time))

    def __init__(self, experiment):
        self.time_recorded = datetime.now()
        self.experiment_id = experiment.id
        self.experiment = experiment

    def __repr__(self):
        return "<Datapoint('%s', '%s')>" % (self.time_recorded, self.experiment)


class Datavalue(_Base):
    __tablename__ = "datavalues"

    id = Column(Integer, primary_key=True)
    value = Column(Float)
    error = Column(Float)
    dataType = Column(String)

    datapoint_id = Column(Integer, ForeignKey('datapoints.id'))
    datapoint = relationship("datapoint", backref=backref("datavalues", order_by=id))

    def __init__(self, value, error, datatype, datapoint):
        self.value = value
        self.error = error
        self.datatype = datatype
        self.datapoint_id = datapoint.id
        self.datapoint = datapoint

    def __repr__(self):
        return "<Datavalue('%s','%s','%s','%s')>" % (self.value, self.error, self.datatype, self.datapoint)


class Experiment(_Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True)
    startTime = Column(DateTime)


    def __init__(self):
        self.startTime = datetime.now()

    def __repr__(self):
        return "<Experiment('%s')>" % self.id


_Base.metadata.create_all(_engine)

