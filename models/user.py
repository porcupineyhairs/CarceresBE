#!/usr/bin/env python

from base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(193), unique=True)
    user_type = Column(Integer)
    # TODO: add relation to client (nullable)

