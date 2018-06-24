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

import constants


class Comment(Base):
  __tablename__ = 'comment'
  id = Column(Integer, primary_key=True)
  body = Column(String(1000), nullable=False)
  created_at_utc = Column(String(250), nullable=False)

  def __init__(self):
    self.created_at_utc = time.time()

  def to_string(self):
    d = dict(self.__dict__)
    del d['_sa_instance_state']
    return str(d)

class User(Base):
  __tablename__ = 'user'
  id = Column(Integer, primary_key=True)
  email = Column(String(250), nullable=False)
  flags = Column(Integer, nullable=True)
  created_at_utc = Column(String(250), nullable=False)
  updated_at_utc = Column(String(250), nullable=False)

  designs = relationship("ReviewObject", lazy='joined')

  def __init__(self):
    self.flags = constants.CONST_FLAGS_ACTIVE
    self.created_at_utc = time.time()

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
  name = Column(String(250), nullable=True)
  description = Column(String(250), nullable=True)
  created_at_utc = Column(String(250), nullable=False)
  updated_at_utc = Column(String(250), nullable=False)

  reviews = relationship("Review", lazy='joined')
  thumbnails = relationship("Thumbnail", lazy='joined')
  user = relationship("User", lazy='joined')

  def __init__(self):
    self.created_at_utc = time.time()
    self.flags = constants.CONST_FLAGS_ACTIVE

  def to_string(self):
    d = dict(self.__dict__)
    del d['_sa_instance_state']
    return str(d)

class Notification(Base):
  __tablename__ = 'notification'
  id = Column(Integer, primary_key=True)
  flags = Column(Integer, nullable=True)
  created_at_utc = Column(String(250), nullable=False)
  updated_at_utc = Column(String(250), nullable=True)

  def __init__(self):
    self.created_at_utc = time.time()

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
