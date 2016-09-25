"""
Database models for the Guacamole application.
"""
from sqlalchemy import Column, Integer, Float, String

from .database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.name


class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    requester = Column(String(50), unique=False)
    environment = Column(String(120), unique=False)
    test = Column(String(50), unique=False)
    status = Column(String(10), unique=False)
    output = Column(String(10000), unique=False)
    duration = Column(Float(1000000), unique=False)

    def __init__(self, requester=None, environment=None, test=None):
        self.requester = requester
        self.environment = environment
        self.test = test

    def __repr__(self):
        return '<Job %r>' % self.id


class Environment(Base):
    __tablename__ = 'environments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hostname = Column(String(50), unique=False)
    operating_system = Column(String(50), unique=False)
    current_job = Column(String(50), unique=False)

    def __init__(self, hostname=None, operating_system=None, current_job=None):
        self.hostname = hostname
        self.operating_system = operating_system
        self.current_job = current_job

    def __repr__(self):
        return '<Environment %r>' % self.id
