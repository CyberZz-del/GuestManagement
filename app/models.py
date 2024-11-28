from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, Table, DateTime
from sqlalchemy.orm import relationship
from .database import Base
import enum

# 关联表：Event和Guest的多对多关系
event_guest = Table('event_guest', Base.metadata,
    Column('event_id', Integer, ForeignKey('events.id')),
    Column('guest_id', Integer, ForeignKey('guests.id'))
)

# 关联表：Event和CommitteeMember的多对多关系
event_committee = Table('event_committee', Base.metadata,
    Column('event_id', Integer, ForeignKey('events.id')),
    Column('committee_member_id', Integer, ForeignKey('committee_members.id'))
)

class Gender(enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    gender = Column(Enum(Gender))
    contact = Column(String(50))
    type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

class Staff(User):
    __tablename__ = "staff"

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    responsibility = Column(String(200))
    authority_level = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'staff',
    }

class Guest(User):
    __tablename__ = "guests"

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    location = Column(String(200))
    organization = Column(String(200))
    email = Column(String(100))
    passport = Column(String(50))
    nationality = Column(String(100))
    guest_level = Column(Integer)
    
    events = relationship("Event", secondary=event_guest, back_populates="guests")

    __mapper_args__ = {
        'polymorphic_identity': 'guest',
    }

class CommitteeMember(User):
    __tablename__ = "committee_members"

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    role = Column(String(100))
    permission_level = Column(Integer)
    team_type = Column(String(50))

    events = relationship("Event", secondary=event_committee, back_populates="managers")

    __mapper_args__ = {
        'polymorphic_identity': 'committee_member',
        'polymorphic_on': team_type
    }

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    location = Column(String(200))
    time = Column(DateTime)
    min_permission_level = Column(Integer)
    
    guests = relationship("Guest", secondary=event_guest, back_populates="events")
    managers = relationship("CommitteeMember", secondary=event_committee, back_populates="events")
