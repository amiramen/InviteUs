from sqlalchemy import Column, Integer, String,DateTime,Date, Text
from database import Base
import datetime

class ScheduleRecord(Base):

	__tablename__ = 'schedule_records'

	STATUS_OCCUPIED = 1
	STATUS_FREE = 2

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer)
	date = Column(Date)
	status = Column(Integer)
	last_update_date = Column(DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now)
	
	
	def __init__(self,**kwargs):
		vars(self).update(kwargs) #initial args

	def __repr__(self):
		return '<ScheduleRecord #%r>' % (self.id)
"""
class Event(Base):
	__tablename__ = 'events'
	id = Column(Integer, primary_key=True)
	title = Column(Text)
	description = Column(Text)
	type = Column(Integer) # EventTypeClass 
	#invited_users
	
	def __init__(self,**kwargs):
		vars(self).update(kwargs) #initial args

	def __repr__(self):
		return '<ScheduleRecord #%r>' % (self.id)

class EventType(Base):
	__tablename__ = 'event_type'
	id = Column(Integer, primary_key=True)
	PUBLIC = 1
	PRIVATE = 2
"""
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
 
    def __init__(self, email, first_name=None, last_name=None):
        self.email = email.lower()
        self.first_name = first_name
        self.last_name = last_name
 
    # These four methods are for Flask-Login
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)