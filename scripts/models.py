from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Marketing(Base):
    __tablename__ = 'marketing'

    event_id = Column(String, primary_key=True)
    phone_id = Column(String)
    ad_id = Column(Integer)
    provider = Column(String)
    placement = Column(String)
    length = Column(Integer)
    event_ts = Column(DateTime)

    def __init__(self, event_id, phone_id, ad_id, provider, placement, length, event_ts):
        self.event_id = event_id
        self.phone_id = phone_id
        self.ad_id = ad_id
        self.provider = provider
        self.placement = placement
        self.length = length
        self.event_ts = event_ts


class Users(Base):
    __tablename__ = 'users'

    event_id = Column(String, primary_key=True)
    user_id = Column(String)
    phone_id = Column(String)
    property = Column(String)
    value = Column(String, nullable=True)
    event_ts = Column(DateTime)

    def __init__(self, event_id, user_id, phone_id, property, value, event_ts):
        self.event_id = event_id
        self.user_id = user_id
        self.phone_id = phone_id
        self.property = property
        self.value = value
        self.event_ts = event_ts
