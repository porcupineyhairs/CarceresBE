from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, DateTime

from classes.ModelBase import ModelBase


class Subscription(ModelBase):
    __tablename__ = 'subscriptions'

    start = Column(DateTime(), nullable=False)
    end = Column(DateTime(), nullable=False)
    type = Column(Integer, nullable=False)

    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)
    car_id = Column(Integer, ForeignKey("cars.id"), nullable=False)
