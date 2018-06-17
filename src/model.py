import os
import sys
import time
import uuid
import random
import string

from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.types import Numeric

from session_factory import Base

class User(Base):
  __tablename__ = 'user'
  id = Column(Integer, primary_key=True)
  email = Column(String(250), nullable=False)
  flags = Column(Integer, nullable=True)
  created_at_utc = Column(String(250), nullable=False)
  updated_at_utc = Column(String(250), nullable=False)

  def __init__(self, form):
    self.email = form.get('email')
    self.flags = form.get('flags', 0)
    self.created_at_utc = form.get('created_at_utc')
    self.created_at_utc = form.get('updated_at_utc')

  def to_string(self):
    d = dict(self.__dict__)
    del d['_sa_instance_state']
    return str(d)

# i.e, a logo design
class ReviewObject(Base):
  __tablename__ = 'review_object'
  id = Column(Integer, primary_key=True)
  uri = Column(String(250), nullable=False)
  uid = Column(Integer, ForeignKey("user.id"), nullable=True)
  flags = Column(Integer, nullable=False)
  filename = Column(String(250), nullable=False)
  description = Column(String(250), nullable=True)
  created_at_utc = Column(String(250), nullable=False)
  updated_at_utc = Column(String(250), nullable=False)

  reviews = relationship("Review", lazy='joined')
  thumbnails = relationship("Thumbnail", lazy='joined')

  def __init__(self):
    self.created_at_utc = time.time()
    self.flags = constants.CONST_FLAGS_ACTIVE

  def to_string(self):
    d = dict(self.__dict__)
    del d['_sa_instance_state']
    return str(d)

# ie, person, corporation, llc
class Notification(Base):
  __tablename__ = 'notification'
  id = Column(Integer, primary_key=True)
  type = Column(String(250), nullable=False)
  kv_json = Column(String(250), nullable=True)
  receivers = Column(String(250), nullable=True)
  sender = Column(String(250), nullable=True)
  flags = Column(Integer, nullable=True)
  created_at_utc = Column(String(250), nullable=True)
  updated_at_utc = Column(String(250), nullable=True)

  def __init__(self, form):
    self.type = form.get('type')
    self.kv_json = form.get('kv_json', None)
    self.sender = form.get('sender')
    self.receivers = form.get('receivers')
    self.flags = form.get('flags', 0)
    self.created_at_utc = form.get('created_at_utc')
    self.updated_at_utc = form.get('updated_at_utc')

  def to_string(self):
    d = dict(self.__dict__)
    del d['_sa_instance_state']
    return str(d)

class Review(Base):
  __tablename__ = 'review'
  id = Column(Integer, primary_key=True)
  flags = Column(Integer, nullable=True)
  created_at_utc = Column(String(250), nullable=False)
  body = Column(String(5000), nullable=False)
  uid = Column(Integer, nullable=True)
  review_object_uri = Column(String, ForeignKey("review_object.uri"), nullable=False)

  def __init__(self):
    self.created_at_utc = time.time()

  def to_string(self):
    d = dict(self.__dict__)
    del d['_sa_instance_state']
    return str(d)


class Thumbnail(Base):
  __tablename__ = 'thumbnail'
  id = Column(Integer, primary_key=True)
  flags = Column(Integer, nullable=True)
  filename = Column(String(250), nullable=False)
  size_code = Column(Integer, nullable=True)
  created_at_utc = Column(String(250), nullable=False)
  updated_at_utc = Column(String(250), nullable=True)
  review_object_uri = Column(String, ForeignKey("review_object.uri"), nullable=False)

  def __init__(self):
    self.created_at_utc = time.time()

  def to_string(self):
    d = dict(self.__dict__)
    del d['_sa_instance_state']
    return str(d)
